#!/usr/bin/env python
"""Build single-file dashboard (index.html) from parsed course data + issues catalog."""
import json, re, os

base = r"C:\Users\srussell\health-sci-calendar-review"
d25 = json.load(open(os.path.join(base,"courses_2025.json"), encoding="utf-8"))
d26 = json.load(open(os.path.join(base,"courses_2026.json"), encoding="utf-8"))

def primary(code): return code.split("/")[0].strip()
def level(code):
    m = re.search(r"(\d)\d\d", primary(code))
    return int(m.group(1))*100 if m else 0

# ---- Issues catalog: keyed by primary course code (or "PROGRAM"/"GLOBAL") ----
# severity: high | med | low ; cat: spelling | grammar | style | prereq | structure | gap | encoding
ISSUES = {
  "HE410": [
    {"sev":"hi","cat":"prereq","msg":"Prereq lists HE302, which has no course entry in either calendar year. Students cannot satisfy a non-existent prerequisite (likely a renamed/dropped course)."},
  ],
  "HE411": [
    {"sev":"hi","cat":"prereq","msg":"Prereq lists HE302, which does not exist (same dangling reference as HE410)."},
    {"sev":"low","cat":"style","msg":"Title 'Critical perspectives in Public Health' uses sentence case; all other course titles use Title Case ('Critical Perspectives in Public Health')."},
  ],
  "HE303/BI317": [
    {"sev":"hi","cat":"prereq","msg":"Exclusion list names HE434, which has no course entry (also cited in the program's Year-4 list). Dangling reference."},
  ],
  "HE330": [
    {"sev":"med","cat":"prereq","msg":"Prereq alternative 'HE211' has no course entry (defunct code); the live alternatives are BI216/KP220."},
    {"sev":"low","cat":"grammar","msg":"'food labeling obesity' is missing a comma: should read 'food labeling, obesity'."},
    {"sev":"low","cat":"grammar","msg":"'covering topics including;' uses a semicolon where a colon is required ('including:')."},
    {"sev":"low","cat":"spelling","msg":"'food labeling' uses US spelling; Canadian-English house style is 'labelling' (also check 'behaviour' usage elsewhere for consistency)."},
  ],
  "HE431/BI416": [
    {"sev":"med","cat":"prereq","msg":"Prereq alternative 'HE211' has no course entry (defunct code)."},
  ],
  "HE202": [
    {"sev":"med","cat":"grammar","msg":"Description body ends with a stray, dangling label 'Prerequisites :' that was accidentally typed into the description field."},
    {"sev":"low","cat":"style","msg":"Prereq reads 'Registration Status' (title case) while most HE courses use 'Registration status'."},
  ],
  "HE430": [
    {"sev":"low","cat":"style","msg":"Title 'Advanced nutrition and chronic disease' uses sentence case; house style is Title Case."},
  ],
  "HE410 ": [],
  "HE224/KP224/HS202": [
    {"sev":"med","cat":"spelling","msg":"Exclusion list contains 'KP2222' (four digits) - a typo for KP222."},
    {"sev":"low","cat":"grammar","msg":"Description opens 'Anatomy and Physiology I, introduces...' - the comma after the title creates a subject/verb error. Remove the comma or rephrase."},
    {"sev":"low","cat":"grammar","msg":"'the structure and function organization of the human body' is awkward; intended sense is 'the structural and functional organization'."},
  ],
  "HE225/KP225/HS204": [
    {"sev":"low","cat":"grammar","msg":"Description opens 'Anatomy and Physiology II, continues...' - same misplaced comma after the title as HE224."},
    {"sev":"low","cat":"grammar","msg":"'focusing on regulation, and homeostasis' has a stray comma before 'and'."},
  ],
  "HE320/KP320": [
    {"sev":"med","cat":"gap","msg":"No academic description - the entry is only a cross-list pointer ('Cross-listed as KP320'). Students see no course content."},
    {"sev":"low","cat":"style","msg":"Cross-list note 'Cross-listed as KP320' is not parenthesized; house style elsewhere is '( Cross-listed as KP435 .)'."},
    {"sev":"med","cat":"structure","msg":"New 2026/27 course not slotted into any required sequence in the Honours BSc program structure (orphaned; available only as a free elective)."},
  ],
  "HE321/KP321": [
    {"sev":"med","cat":"gap","msg":"No academic description - only a cross-list pointer ('Cross-listed as KP321')."},
    {"sev":"low","cat":"style","msg":"Cross-list note is not parenthesized, unlike house style."},
    {"sev":"low","cat":"prereq","msg":"Prereq 'KP225 / HE225 / HS202 or HN204' mixes a slash-list and an 'or' with ambiguous precedence."},
    {"sev":"med","cat":"structure","msg":"New 2026/27 course not referenced anywhere in the program structure (orphaned)."},
  ],
  "HE435/KP435": [
    {"sev":"med","cat":"gap","msg":"Titled course ('Exercise is Medicine') with no academic description - only a cross-list pointer."},
  ],
  "HE368/PS368": [
    {"sev":"med","cat":"gap","msg":"No academic description - only a cross-list pointer ('Cross-listed with PS368'). Note 'with' here vs 'as' used by other cross-lists."},
  ],
  "HN210/KP221": [
    {"sev":"low","cat":"gap","msg":"No academic description in the HE calendar - only a cross-list pointer to KP221."},
  ],
  "HN220/KP222": [
    {"sev":"low","cat":"gap","msg":"No academic description - only a cross-list pointer to KP222."},
  ],
  "HE410__age": [],
  "HE410_dup": [],
  "HE410x": [],
  "HE410y": [],
  "HE437": [
    {"sev":"low","cat":"style","msg":"Prereq 'Year 3 or Year 4 Health Sciences' omits 'Honours BSc' that other courses include."},
  ],
  "HE304": [
    {"sev":"low","cat":"style","msg":"Prereq 'Year 3 or 4 of Honours Program' is a wording variant of the standard 'Year 3 or 4 Honours BSc Health Sciences'."},
  ],
  "HE300/KP434": [
    {"sev":"low","cat":"prereq","msg":"Prereq alternative 'MA241' is not hyperlinked (every live course code in the calendar is linked), suggesting MA241 is defunct; the linked alternative is ST231."},
    {"sev":"low","cat":"structure","msg":"Exclusion list redundantly names the course's own codes (HE300 and KP434) in addition to the cross-list mechanism."},
  ],
  "HE410_aging": [],
}
# Aging course HE410 grammar additions handled above; add HE410 semicolon items
ISSUES.setdefault("HE410", []).extend([
    {"sev":"low","cat":"grammar","msg":"'perspectives including;' and 'Topics may include;' use semicolons where colons are required."},
    {"sev":"low","cat":"grammar","msg":"'interactive/hands on components' should be hyphenated: 'hands-on'."},
])

PROGRAM_ISSUES = [
  {"sev":"hi","cat":"structure","msg":"Year-4 'select 2.0 credits from' list includes HE434, which has no course entry - a dangling requirement reference (present in BOTH calendar years)."},
  {"sev":"hi","cat":"gap","msg":"Year-4 selection list OMITS three existing 400-level courses: HE436 (Health and Human Rights), HE437 (Principles of Population Health), HE438 (Cancer Biology). The list appears stale - students may be unsure whether these count toward the 2.0-credit Year-4 requirement."},
  {"sev":"hi","cat":"structure","msg":"Anatomy/Physiology migration is incomplete in 2026/27: the program core swapped HN204 + HN220/KP222 for the new HE224 + HE225, but HN204, HN210/KP221, HN220/KP222 and HN320 remain published as courses, creating a redundant parallel A&P track with overlapping exclusion webs."},
  {"sev":"low","cat":"spelling","msg":"Note 1: 'pharmacy, etc.)in the future' is missing a space after the closing parenthesis."},
  {"sev":"low","cat":"spelling","msg":"Note 1: 'PC141 (orPC131)' is missing a space ('or PC131')."},
  {"sev":"low","cat":"style","msg":"Note 4 psychology list is out of numeric order: PS285 appears before PS275 and PS276."},
  {"sev":"low","cat":"style","msg":"Year-4 references '(see Note 5)' for electives while Years 2-3 reference Notes 2/3; the English/Philosophy elective rules (Note 2) are not cross-referenced in Year 4."},
]
GLOBAL_ISSUES = [
  {"sev":"med","cat":"structure","msg":"NONE of the spelling, grammar, or dangling-reference errors found in 2025/26 were corrected in the 2026/27 calendar - every issue persists across both years."},
  {"sev":"low","cat":"encoding","msg":"Course pages declare charset=ISO-8859-1 but serve Windows-1252 bytes (curly quotes 0x91/0x92). Most browsers tolerate this, but it is non-conformant and can render apostrophes as replacement characters in strict parsers."},
  {"sev":"low","cat":"style","msg":"'Registration status' vs 'Registration Status' vs 'registration status' capitalization is inconsistent across course prerequisite fields."},
]

# ---- Faculty roster (identical in both calendar years) + corrections ----
FACULTY = {
  "note": "Full-Time Faculty roster as published. Identical in 2025/2026 and 2026/2027.",
  "listed": [
    {"name":"Todd Coleman","cred":"PhD"},
    {"name":"Stephanie DeWitte-Orr","cred":"PhD"},
    {"name":"Diane Gregory","cred":"PhD"},
    {"name":"Renee MacPhee","cred":"PhD"},
    {"name":"Melody Morton Ninomiya","cred":"PhD"},
    {"name":"Nirosha Murugan","cred":"PhD"},
    {"name":"Sarah Poynter","cred":"PhD"},
    {"name":"Nicolas Rouleau","cred":"PhD","role":"Undergraduate Advisor"},
    {"name":"Ketan Shankardass","cred":"PhD"},
    {"name":"Robb Travers","cred":"PhD","role":"Chair (listed)","flag":"on leave"},
  ],
  "missing": [
    {"name":"Kate Rossiter","role":"Chair (current)","note":"Current Chair while Robb Travers is on leave; absent from roster."},
    {"name":"Stewart J. Russell","role":"Assistant Professor","note":"Appointed August 2025; absent from roster in both years."},
    {"name":"Anish","role":"Faculty","note":"Recently appointed; absent from roster. (Surname to confirm.)"},
  ],
}
FACULTY_ISSUES = [
  {"sev":"hi","cat":"faculty","msg":"The roster lists Robb Travers as Chair, but he is on leave. The current Chair, Kate Rossiter, does not appear at all - the public calendar names the wrong department head."},
  {"sev":"med","cat":"faculty","msg":"Full-Time Faculty roster omits Dr. Stewart J. Russell (Assistant Professor, appointed August 2025)."},
  {"sev":"med","cat":"faculty","msg":"Full-Time Faculty roster omits Anish (recently appointed; surname to confirm)."},
  {"sev":"med","cat":"faculty","msg":"The faculty roster is byte-identical between 2025/26 and 2026/27, so none of the missing appointments (Russell, Anish) or the Chair change (Rossiter) were added in the new calendar."},
]

# clean stray placeholder keys
ISSUES = {k:v for k,v in ISSUES.items() if v and not k.endswith(("_age","_dup","x","y","_aging")) and k.strip()==k}

# calendar URL params per year (d=department, s=section, y=year, p=program)
YEARP = {
  "2025/2026": {"d":3127,"s":1152,"y":92,"p":7164},
  "2026/2027": {"d":3258,"s":1170,"y":93,"p":7604},
}
def course_url(file, yr):
    cid = re.search(r"c_(\d+)\.html", file).group(1)
    pp = YEARP[yr]
    return f"https://academic-calendar.wlu.ca/course.php?c={cid}&cal=1&d={pp['d']}&s={pp['s']}&y={pp['y']}"
def program_url(yr):
    pp = YEARP[yr]
    return f"https://academic-calendar.wlu.ca/program.php?cal=1&d={pp['d']}&p={pp['p']}&s={pp['s']}&y={pp['y']}"

def merge(dataset, yr):
    out=[]
    for c in dataset:
        rec=dict(c)
        rec["primary"]=primary(c["code"])
        rec["level"]=level(c["code"])
        rec["issues"]=ISSUES.get(c["code"], [])
        rec["url"]=course_url(c["file"], yr)
        out.append(rec)
    return out

data = {
  "2025/2026": merge(d25, "2025/2026"),
  "2026/2027": merge(d26, "2026/2027"),
  "program": {
     "2025/2026": open(os.path.join(base,"program_text_2025_26.txt"),encoding="utf-8").read(),
     "2026/2027": open(os.path.join(base,"program_text_2026_27.txt"),encoding="utf-8").read(),
  },
  "programUrl": {
     "2025/2026": program_url("2025/2026"),
     "2026/2027": program_url("2026/2027"),
  },
  "programIssues": PROGRAM_ISSUES,
  "globalIssues": GLOBAL_ISSUES,
  "faculty": FACULTY,
  "facultyIssues": FACULTY_ISSUES,
}
json.dump(data, open(os.path.join(base,"dashboard_data.json"),"w",encoding="utf-8"), indent=2, ensure_ascii=False)
n_issues = sum(len(v) for v in ISSUES.values())+len(PROGRAM_ISSUES)+len(GLOBAL_ISSUES)+len(FACULTY_ISSUES)
print(f"data built: {len(d25)} (25/26), {len(d26)} (26/27) courses; {n_issues} catalogued issues across {len(ISSUES)} courses + program + global")
