#!/usr/bin/env python
"""Parse WLU Health Sciences calendar course pages into structured JSON."""
import json, re, sys, glob, os
from bs4 import BeautifulSoup

def clean(txt):
    if txt is None:
        return ""
    txt = txt.replace("\xa0", " ")
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def parse_course(path, year_label):
    html = open(path, encoding="cp1252", errors="replace").read()
    soup = BeautifulSoup(html, "html.parser")
    # strip glossary tooltip noise: glossary <a> keep visible text only (handled by get_text)
    rec = {"file": os.path.basename(path), "year": year_label}
    h1 = None
    for cand in soup.find_all("h1"):
        if re.match(r"^[A-Z]{2,4}\s*\d{3}", cand.get_text(strip=True)):
            h1 = cand
            break
    if not h1:
        return None
    # h1 contains: CODE <br> title <br> credit <br/span> term
    # get_text with separator
    raw = h1.get_text("|", strip=True)
    parts = [p.strip() for p in raw.split("|") if p.strip()]
    rec["code"] = parts[0] if parts else ""
    rec["title"] = parts[1] if len(parts) > 1 else ""
    # find credit + term among remaining
    credit = term = ""
    for p in parts[2:]:
        if "Credit" in p:
            credit = p
        elif p.startswith("-"):
            term = p.lstrip("- ").strip()
        else:
            term = p
    # term sometimes attached like "0.5 Credit" then " - Fall"
    rec["credit"] = credit
    rec["term"] = term
    # Hours
    hours_div = soup.find("div", class_="hours")
    rec["hours"] = clean(hours_div.get_text(" ", strip=True)) if hours_div else ""
    # Description: the <p><div>...</div></p> right after hours, OR first <p> after h1
    # Find the reqs block; description is everything between h1 and div.reqs minus hours
    desc = ""
    reqs = soup.find("div", class_="reqs")
    # gather text nodes between h1 and reqs
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
    # remove the hours text from the front of description
    if rec["hours"]:
        hours_txt = clean(hours_div.get_text(" ", strip=True))
        if desc_full.startswith(hours_txt):
            desc_full = desc_full[len(hours_txt):].strip()
    rec["description"] = desc_full
    # Additional course info: prerequisites, exclusions, corequisites, etc.
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
            # capture course-code links across whole reqs block with their label
            for a in reqs.find_all("a", href=re.compile(r"course\.php")):
                rec["prereq_links"].append(clean(a.get_text()))
    return rec

def run(folder, year_label):
    out = []
    for f in sorted(glob.glob(os.path.join(folder, "c_*.html"))):
        r = parse_course(f, year_label)
        if r:
            out.append(r)
    return out

base = r"C:\Users\srussell\health-sci-calendar-review"
data2025 = run(os.path.join(base, "raw", "courses_2025"), "2025/2026")
data2026 = run(os.path.join(base, "raw", "courses_2026"), "2026/2027")
json.dump(data2025, open(os.path.join(base, "courses_2025.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
json.dump(data2026, open(os.path.join(base, "courses_2026.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"2025/26: {len(data2025)} courses")
print(f"2026/27: {len(data2026)} courses")
# quick print of codes
print("2025 codes:", ", ".join(sorted(c["code"] for c in data2025)))
print("2026 codes:", ", ".join(sorted(c["code"] for c in data2026)))
