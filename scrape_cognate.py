#!/usr/bin/env python
"""Scrape WLU Faculty of Science cognate courses (for Health Sci MMS-stream
med/dental/allied-health prerequisites and MCAT/DAT content) from the
2026/2027 Undergraduate Academic Calendar.

Parsing logic is copied from parse_courses.py (NOT imported, because that
module's body re-runs the HE scrape). Pages declare ISO-8859-1 but serve
Windows-1252 bytes, so we decode as cp1252 (errors="replace").
"""
import json, re, os, glob, subprocess, sys
from bs4 import BeautifulSoup

BASE = r"C:\Users\srussell\health-sci-calendar-review"
RAW = os.path.join(BASE, "raw", "cognate")

DEPT_URL = "https://academic-calendar.wlu.ca/department.php?cal=1&d={d}&s=1170&y=93"
BASE_HOST = "https://academic-calendar.wlu.ca/"

# (dept-folder-name, D, filter-fn on code) -- filter returns True to KEEP.
#
# NOTE on D values (discovered while scraping):
#   - The prompt's "Computer Science and Physics" D=3253 is a LANDING page that
#     links only to sub-department pages, not courses. The physics (PC) courses
#     actually live at D=3245 ("Physics (PC/CP Dept)"). We use 3245 + a PC filter.
#   - "Medical Foundations" D=3266 owns NO MF-prefixed courses; it is a curated
#     cross-listing whose links point to BI/CH/BC/MA courses owned by other
#     departments. Each <a href> carries the OWNING department's d value, so we
#     parse the full href (capturing its real d) instead of reconstructing the
#     URL. This makes MF resolve correctly and tags each course by its true
#     subject prefix; the MF membership is recorded separately.
#   - The same full-href approach fixes spurious 404s elsewhere: e.g. CH454 is
#     cross-listed into Biology (D=3247) but its href carries d=3248.
DEPARTMENTS = [
    ("biology", "3247", lambda code: True),
    ("chem_biochem", "3248", lambda code: True),
    ("physics", "3245", lambda code: code.startswith("PC")),
    ("mathematics", "3251", lambda code: True),
    ("psychology", "3246", lambda code: True),
    ("kinesiology", "3250", lambda code: True),
    ("medical_foundations", "3266", lambda code: True),
    ("paramedicine", "3267", lambda code: True),
]

# ----------------------------------------------------------------------------
# Parsing helpers (copied from parse_courses.py)
# ----------------------------------------------------------------------------
def clean(txt):
    if txt is None:
        return ""
    txt = txt.replace("\xa0", " ")
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def parse_course(path, year_label):
    html = open(path, encoding="cp1252", errors="replace").read()
    soup = BeautifulSoup(html, "html.parser")
    rec = {"file": os.path.basename(path), "year": year_label}
    h1 = None
    for cand in soup.find_all("h1"):
        if re.match(r"^[A-Z]{2,4}\s*\d{3}", cand.get_text(strip=True)):
            h1 = cand
            break
    if not h1:
        return None
    raw = h1.get_text("|", strip=True)
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    rec["code"] = parts[0] if parts else ""
    rec["title"] = parts[1] if len(parts) > 1 else ""
    credit = term = ""
    for p in parts[2:]:
        if "Credit" in p:
            credit = p
        elif p.startswith("-"):
            term = p.lstrip("- ").strip()
        else:
            term = p
    rec["credit"] = credit
    rec["term"] = term
    hours_div = soup.find("div", class_="hours")
    rec["hours"] = clean(hours_div.get_text(" ", strip=True)) if hours_div else ""
    desc = ""
    reqs = soup.find("div", class_="reqs")
    node = h1.next_sibling
    collected = []
    while node and node is not reqs:
        if getattr(node, "get_text", None):
            t = node.get_text(" ", strip=True)
            collected.append(t)
        elif isinstance(node, str):
            collected.append(node)
        node = node.next_sibling
    desc_full = clean(" ".join(collected))
    if rec["hours"]:
        hours_txt = clean(hours_div.get_text(" ", strip=True))
        if desc_full.startswith(hours_txt):
            desc_full = desc_full[len(hours_txt):].strip()
    rec["description"] = desc_full
    rec["requirements"] = {}
    rec["prereq_links"] = []
    if reqs:
        dl = reqs.find("dl")
        if dl:
            dts = dl.find_all("dt")
            dds = dl.find_all("dd")
            for dt, dd in zip(dts, dds):
                key = clean(dt.get_text(" ", strip=True))
                val = clean(dd.get_text(" ", strip=True))
                rec["requirements"][key] = val
            for a in reqs.find_all("a", href=re.compile(r"course\.php")):
                rec["prereq_links"].append(clean(a.get_text()))
    return rec

# ----------------------------------------------------------------------------
# Scrape
# ----------------------------------------------------------------------------
def fetch(url, dest):
    """Download url to dest via curl. Returns True on success."""
    r = subprocess.run(["curl", "-s", "-S", url, "-o", dest],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False
    return os.path.exists(dest) and os.path.getsize(dest) > 0

def extract_course_links(dept_html_path):
    """Return list of (course_id, absolute_url) preserving order, deduped by id.

    Parses the FULL href so the owning department's d value is preserved
    (course pages 404 if fetched with the wrong d). HTML entities (&amp;)
    are decoded.
    """
    html = open(dept_html_path, encoding="cp1252", errors="replace").read()
    # match course.php?...c=<id>... capturing the whole querystring
    hrefs = re.findall(r'href="(course\.php\?[^"]*\bc=\d+[^"]*)"', html)
    seen = {}
    order = []
    for h in hrefs:
        h = h.replace("&amp;", "&")
        m = re.search(r"\bc=(\d+)", h)
        if not m:
            continue
        cid = m.group(1)
        if cid in seen:
            continue
        seen[cid] = BASE_HOST + h
        order.append(cid)
    return [(cid, seen[cid]) for cid in order]

def derive_dept(code):
    m = re.match(r"^([A-Z]{2,4})\s*\d", code)
    return m.group(1) if m else ""

def main():
    os.makedirs(RAW, exist_ok=True)
    problems = []
    per_dept_counts = {}
    # dedupe across departments by course code; remember MF membership.
    by_code = {}        # code -> record
    mf_codes = set()    # codes that appear in the Medical Foundations index

    for folder, D, keep in DEPARTMENTS:
        dept_dir = os.path.join(RAW, folder)
        os.makedirs(dept_dir, exist_ok=True)
        dept_html = os.path.join(dept_dir, "_dept_index.html")
        url = DEPT_URL.format(d=D)
        if not fetch(url, dept_html):
            problems.append(f"FAILED to fetch dept index {folder} (D={D}): {url}")
            per_dept_counts[folder] = 0
            continue
        links = extract_course_links(dept_html)
        print(f"[{folder}] D={D}: {len(links)} course links found", file=sys.stderr)

        # download each course page using its REAL url (owning dept's d)
        for cid, curl_url in links:
            dest = os.path.join(dept_dir, f"c_{cid}.html")
            if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
                if not fetch(curl_url, dest):
                    problems.append(f"FAILED to fetch course c={cid} ({folder}): {curl_url}")

        # parse, applying the dept keep-filter
        kept = 0
        for cid, curl_url in links:
            dest = os.path.join(dept_dir, f"c_{cid}.html")
            if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
                continue
            rec = parse_course(dest, "2026/2027")
            if rec is None:
                problems.append(f"PARSE returned None (404 / no course h1): {folder}/c_{cid}.html")
                continue
            code = rec["code"]
            if not keep(code):
                continue
            if folder == "medical_foundations":
                mf_codes.add(code)
            if code in by_code:
                # already captured under owning dept; just note MF membership
                kept += 1
                continue
            dept = derive_dept(code)
            reqs = rec.get("requirements", {})
            out = {
                "dept": dept,
                "code": code,
                "title": rec["title"],
                "credit": rec["credit"],
                "term": rec["term"],
                "hours": rec["hours"],
                "has_lab": "lab" in rec["hours"].lower(),
                "description": rec["description"],
                "prerequisites": reqs.get("Prerequisites", ""),
                "exclusions": reqs.get("Exclusions", ""),
                "prereq_links": rec["prereq_links"],
                "url": curl_url,
            }
            by_code[code] = out
            kept += 1
        per_dept_counts[folder] = kept
        print(f"[{folder}] kept {kept} courses after filter", file=sys.stderr)

    all_records = list(by_code.values())

    # sort for stable output: by dept then code
    def code_sort_key(r):
        m = re.match(r"^([A-Z]+)\s*(\d+)", r["code"])
        if m:
            return (r["dept"], m.group(1), int(m.group(2)))
        return (r["dept"], r["code"], 0)
    all_records.sort(key=code_sort_key)

    out_path = os.path.join(BASE, "cognate_courses.json")
    json.dump(all_records, open(out_path, "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print("\n=== SUMMARY ===", file=sys.stderr)
    for folder, D, _ in DEPARTMENTS:
        print(f"  {folder} (D={D}): {per_dept_counts.get(folder, 0)}", file=sys.stderr)
    print(f"  TOTAL: {len(all_records)}", file=sys.stderr)
    if problems:
        print("\n=== PROBLEMS ===", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
    else:
        print("\nNo download/parse problems.", file=sys.stderr)

    # also emit a manifest for downstream report generation (keeps the
    # cognate_courses.json elements to exactly the required keys)
    json.dump({"per_dept_counts": per_dept_counts,
               "problems": problems,
               "total": len(all_records),
               "medical_foundations_listed_codes": sorted(mf_codes)},
              open(os.path.join(BASE, "cognate_scrape_manifest.json"), "w",
                   encoding="utf-8"), indent=2)

if __name__ == "__main__":
    main()
