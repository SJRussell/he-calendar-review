#!/usr/bin/env python
"""Structural analysis of HE/HN calendar data + merged data model for dashboard."""
import json, re, os

base = r"C:\Users\srussell\health-sci-calendar-review"
d25 = json.load(open(os.path.join(base,"courses_2025.json"), encoding="utf-8"))
d26 = json.load(open(os.path.join(base,"courses_2026.json"), encoding="utf-8"))

CODE_RE = re.compile(r"\b([A-Z]{2,3})\s?(\d{3}[A-Z]?)\b")

def aliases(code):
    # "HE300/KP434" -> ['HE300','KP434']
    return [c.strip() for c in code.split("/")]

def primary(code):
    return aliases(code)[0]

def all_codes(dataset):
    s = set()
    for c in dataset:
        for a in aliases(c["code"]):
            s.add(a)
    return s

def find_codes(text):
    if not text: return []
    return [f"{m.group(1)}{m.group(2)}" for m in CODE_RE.finditer(text)]

def analyze(dataset, label):
    present = all_codes(dataset)              # every code/alias that HAS a page this year
    he_hn_present = {c for c in present if c[:2] in ("HE","HN")}
    findings = {"label": label, "dangling_internal": [], "self_exclusion": [],
                "unlinked_text_codes": [], "missing_description": [], "missing_term": [],
                "crosslist_format": []}
    SPECIAL = re.compile(r"^HE440[A-Z]$")     # historical special-topics sub-codes
    for c in dataset:
        code = c["code"]; al = aliases(code)
        reqs = c["requirements"]
        # referenced codes in prereq/coreq (NOT exclusions, which legitimately name many)
        ref_text = " ".join(v for k,v in reqs.items() if "xclusion" not in k.lower())
        for rc in find_codes(ref_text):
            if rc[:2] in ("HE","HN") and rc not in he_hn_present and not SPECIAL.match(rc):
                findings["dangling_internal"].append({"course": code, "field": "prereq/coreq", "ref": rc})
        # self-referential exclusion: exclusion names the course's own alias
        excl = reqs.get("Exclusions","")
        for a in al:
            if re.search(rf"\b{a}\b", excl):
                findings["self_exclusion"].append({"course": code, "alias": a})
        # unlinked text codes in prereqs: codes present in text but not in prereq_links and not external-expected
        # (we only flag HE/HN unlinked, since those should be internal links)
        linked = set(c.get("prereq_links",[]))
        for rc in find_codes(reqs.get("Prerequisites","")):
            if rc[:2] in ("HE","HN") and rc not in linked and rc in he_hn_present:
                findings["unlinked_text_codes"].append({"course": code, "ref": rc})
        # missing description for non-special-topics, non-directed-studies titled courses
        title = c["title"].lower()
        is_container = any(k in title for k in ["special topics","directed studies","directed research"])
        if not c["description"].strip() and not is_container:
            findings["missing_description"].append(code)
        if not c["term"].strip():
            findings["missing_term"].append(code)
        # crosslist format consistency: description that is ONLY a crosslist note
        desc = c["description"].strip()
        if desc.lower().startswith("cross-listed") or desc.lower().startswith("( cross-listed"):
            has_parens = desc.startswith("(")
            findings["crosslist_format"].append({"course": code, "parenthesized": has_parens, "text": desc})
    return findings, present

f25, p25 = analyze(d25, "2025/2026")
f26, p26 = analyze(d26, "2026/2027")

# year-over-year
codes25 = {primary(c["code"]) for c in d25}
codes26 = {primary(c["code"]) for c in d26}
added = sorted(codes26 - codes25)
removed = sorted(codes25 - codes26)

report = {"f25": f25, "f26": f26, "added_2026": added, "removed_2026": removed}
json.dump(report, open(os.path.join(base,"findings.json"),"w",encoding="utf-8"), indent=2, ensure_ascii=False)

def show(f):
    print(f"\n===== {f['label']} =====")
    print("Dangling internal HE/HN prereq refs:", f["dangling_internal"])
    print("Self-referential exclusions:", [(x['course'],x['alias']) for x in f["self_exclusion"]])
    print("Missing description (titled courses):", f["missing_description"])
    print("Crosslist-only desc format:", [(x['course'],'parens' if x['parenthesized'] else 'NO-parens') for x in f["crosslist_format"]])
    print("Missing term:", f["missing_term"])
show(f25); show(f26)
print("\nAdded in 2026/27:", added)
print("Removed in 2026/27:", removed)
