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
    {"name":"Anish Arora","role":"Faculty","note":"Recently appointed; absent from roster."},
  ],
}
FACULTY_ISSUES = [
  {"sev":"hi","cat":"faculty","msg":"The roster lists Robb Travers as Chair, but he is on leave. The current Chair, Kate Rossiter, does not appear at all - the public calendar names the wrong department head."},
  {"sev":"med","cat":"faculty","msg":"Full-Time Faculty roster omits Dr. Stewart J. Russell (Assistant Professor, appointed August 2025)."},
  {"sev":"med","cat":"faculty","msg":"Full-Time Faculty roster omits Dr. Anish Arora (recently appointed)."},
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

# ================= GRADUATE (MSc Health Sciences) =================
GRADP = {
  "2025/2026": {"d":3043,"s":1134,"y":91,"p":6903},
  "2026/2027": {"d":3329,"s":1186,"y":94,"p":7783},
}
def grad_course_url(file, yr):
    cid = re.search(r"c_(\d+)\.html", file).group(1)
    pp = GRADP[yr]
    return f"https://academic-calendar.wlu.ca/course.php?c={cid}&cal=3&d={pp['d']}&s={pp['s']}&y={pp['y']}"
def grad_program_url(yr):
    pp = GRADP[yr]
    return f"https://academic-calendar.wlu.ca/program.php?cal=3&d={pp['d']}&p={pp['p']}&s={pp['s']}&y={pp['y']}"

# curriculum role per grad course (drives the collapsed grouping + modal badges)
GRAD_GROUP = {
  "HE600":"Core","HE601":"Core","HE602":"Core","HE603":"Core","HE604A":"Core",
  "HE604B":"Core","HE605":"Core","HE606":"Core",
  "HE699":"Thesis & directed","HE650":"Thesis & directed",
  "HE631":"MMSC electives","HE632":"MMSC electives","HE638":"MMSC electives",
  "HE610":"CPPH electives","HE611":"CPPH electives","HE636":"CPPH electives",
  "HE637":"Shared electives","HE640":"Shared electives",
}
GRAD_ROLES = {
  "HE600":["Coursework core","Coursework option only"],
  "HE601":["Coursework core","Thesis Year 1 (MMSC & CPPH)"],
  "HE602":["Coursework core","Thesis Year 1 (MMSC & CPPH)"],
  "HE603":["Coursework core"], "HE605":["Coursework core"], "HE606":["Coursework core"],
  "HE604A":["Coursework core (choose 604A or 604B)"], "HE604B":["Coursework core (choose 604A or 604B)"],
  "HE699":["Master's thesis (Thesis option)"], "HE650":["Directed studies (CPPH thesis elective)"],
  "HE631":["MMSC elective","Coursework option only"], "HE632":["MMSC elective","Coursework option only"],
  "HE638":["MMSC elective","Coursework option only"],
  "HE610":["CPPH elective","Coursework option only"], "HE611":["CPPH elective","Coursework option only"],
  "HE636":["CPPH elective","Coursework option only"],
  "HE637":["MMSC + CPPH elective","Coursework option only"], "HE640":["MMSC + CPPH elective","Coursework option only"],
}
GRAD_GROUP_ORDER = ["Core","MMSC electives","CPPH electives","Shared electives","Thesis & directed"]

GRAD_ISSUES = {
  "HE600":[{"sev":"low","cat":"spelling","msg":"Description uses 'focussed'; the identical UG course HE400 uses 'focused'. Standardize one spelling."}],
  "HE640":[{"sev":"low","cat":"style","msg":"Description field contains only the placeholder text 'Irregular Course' instead of an actual course description."}],
}
GRAD_PROGRAM_ISSUES = [
  {"sev":"med","cat":"spelling","msg":"Program text reads 'The Coursework optio n is normally completed...' - 'optio n' is a broken word ('option')."},
  {"sev":"low","cat":"spelling","msg":"'earned Laurier BSC Health Sciences degree' - 'BSC' should be 'BSc'."},
  {"sev":"low","cat":"structure","msg":"The Thesis structure marks 'HE699 *' with an asterisk, but no footnote defining the asterisk appears anywhere on the page."},
  {"sev":"low","cat":"style","msg":"The specialization is named 'Molecular and Medical Sciences (MMSC)', yet course HE604B abbreviates it 'MMS' ('molecular medical sciences (MMS)'). Inconsistent acronym."},
  {"sev":"low","cat":"structure","msg":"HE637 (Principles of Population Health) and HE640 (Special Topics) appear under BOTH the MMSC and CPPH elective lists - confirm the dual-listing is intentional."},
  {"sev":"low","cat":"structure","msg":"Both the 'optio n' and 'BSC' typos, and the undefined HE699 asterisk, are present unchanged in 2025/26 and 2026/27. The only 2026/27 change was splitting admission requirements into separate thesis-stream and coursework-stream paragraphs."},
]

def merge_grad(dataset, yr):
    out=[]
    for c in dataset:
        rec=dict(c)
        p=primary(c["code"])
        rec["primary"]=p
        rec["level"]=level(c["code"])
        rec["group"]=GRAD_GROUP.get(p,"Other")
        rec["roles"]=GRAD_ROLES.get(p,[])
        rec["issues"]=GRAD_ISSUES.get(p, [])
        rec["url"]=grad_course_url(c["file"], yr)
        out.append(rec)
    return out

g25 = json.load(open(os.path.join(base,"grad_courses_2025.json"), encoding="utf-8"))
g26 = json.load(open(os.path.join(base,"grad_courses_2026.json"), encoding="utf-8"))

# ================= COGNATE COURSES + DESTINATION PATHWAYS =================
cognate = json.load(open(os.path.join(base,"cognate_courses.json"), encoding="utf-8"))

def has_lab_from_hours(h): return bool(h) and "lab" in h.lower()

# combined code -> {title, lab, url, level, dept} index (cognate + HE/HN, all aliases)
COURSE_INDEX = {}
for c in cognate:
    COURSE_INDEX[c["code"]] = {"title":c["title"], "lab":c.get("has_lab",False),
        "url":c.get("url",""), "level":level(c["code"]), "dept":c.get("dept","")}
# add HE/HN UG (2026/27) then grad HE6xx; index every alias of a cross-listed code
for c in merge(d26, "2026/2027"):
    rec = {"title":c["title"], "lab":has_lab_from_hours(c.get("hours","")),
           "url":c["url"], "level":c["level"], "dept":"HE"}
    for alias in c["code"].split("/"):
        COURSE_INDEX.setdefault(alias.strip(), rec)
for c in merge_grad(g26, "2026/2027"):
    rec = {"title":c["title"], "lab":has_lab_from_hours(c.get("hours","")),
           "url":c["url"], "level":c["level"], "dept":"HE-grad"}
    for alias in c["code"].split("/"):
        COURSE_INDEX.setdefault(alias.strip(), rec)

# Destination pathways. Each bucket: name, why, courses (WLU codes), note.
# arts=True flags a requirement met outside the Faculty of Science (no WLU-Science course to link).
PATHWAYS = [
 {"id":"med","label":"Medicine (MD)","group":"Medicine & dentistry","exam":"MCAT + CASPer/Casper",
  "summary":"Most Canadian medical schools require NO specific prerequisite courses (e.g. McMaster, Queen's, Western, Calgary, Alberta). The binding gates are MCAT content coverage, GPA, and CASPer/interview. A prescriptive minority and new Indigenous Studies requirements are the exceptions, below.",
  "buckets":[
    {"name":"Biology / life sciences","courses":["BI110","BI111","BI226","BI236"],"note":"Toronto requires 12 units life science; Ottawa requires 6 units biology."},
    {"name":"General chemistry","courses":["CH110","CH111"],"note":"McGill requires 2 intro chem WITH labs (100-level)."},
    {"name":"Organic chemistry","courses":["CH202","CH203"],"note":"McGill requires 1 organic chem with lab; core MCAT content."},
    {"name":"Biochemistry","courses":["CH250"],"note":"MCAT is biochem-heavy; recommended (not required) at McGill."},
    {"name":"Physics","courses":["PC141","PC142"],"note":"McGill requires 2 physics WITH labs; MCAT content. Use life-sci PC141/142 (lab) not the lecture-only versions."},
    {"name":"Statistics / quantitative","courses":["ST231"],"note":"MCAT quantitative reasoning; ST231 is the Health-Sci-aligned option."},
    {"name":"Psychology & sociology (MCAT Psych/Soc)","courses":["PS101","PS102"],"note":"MCAT Psych/Soc section. Add a sociology course (Faculty of Arts)."},
    {"name":"English","courses":[],"arts":True,"note":"Required at UBC and Ottawa. Faculty of Arts course, outside Science."},
    {"name":"Indigenous Studies","courses":[],"arts":True,"note":"Required at Calgary, Manitoba, Saskatchewan; UBC transitioning. Faculty of Arts."},
  ],
  "schoolNotes":["No-prereq schools: McMaster, Queen's, Western, Calgary, Alberta, Memorial, Dalhousie, Saskatchewan, TMU, Manitoba.","Prescriptive: McGill (bio/chem/ochem/physics with labs), Ottawa (bio + hum/soc-sci), Toronto (life sci + soc sci), UBC (English to English+Indigenous)."]},

 {"id":"dent","label":"Dentistry (DDS / DMD)","group":"Medicine & dentistry","exam":"DAT (paused at McGill)",
  "summary":"Unlike medicine, ALL 10 Canadian dental schools have prescriptive prerequisites, and many specify 'with labs'. Biology, general chemistry and organic chemistry are near-universal; biochemistry (7/10) and physiology (5/10) are common.",
  "buckets":[
    {"name":"Biology (with lab)","courses":["BI110","BI111","BI226"],"note":"Near-universal. NOTE BI110/111 have no lab line at WLU; confirm whether a target school requires first-year bio lab specifically."},
    {"name":"General chemistry (with lab)","courses":["CH110","CH111"],"note":"Near-universal; labs required at most schools."},
    {"name":"Organic chemistry (with lab)","courses":["CH202","CH203"],"note":"Near-universal; labs required."},
    {"name":"Biochemistry","courses":["CH250"],"note":"Required at 7/10 schools. CH250 carries a lab."},
    {"name":"Human physiology","courses":["HN220","HE224","HE225"],"note":"Required at ~5/10 (UofT, UAlberta, USask, Dal, Western)."},
    {"name":"Physics (with lab)","courses":["PC141","PC142"],"note":"Required at several (McGill, Manitoba, Dalhousie, Quebec schools); labs required."},
    {"name":"Microbiology","courses":["BI374"],"note":"Required at ~3/10 (UAlberta, USask, Dal). BI374 carries a lab."},
    {"name":"Statistics","courses":["ST231"],"note":"Required at UAlberta specifically."},
    {"name":"English / writing","courses":[],"arts":True,"note":"Required at several; Faculty of Arts."},
    {"name":"Humanities / social science","courses":[],"arts":True,"note":"Required at Dalhousie, Manitoba, Saskatchewan; Faculty of Arts."},
  ],
  "schoolNotes":["All 10 schools require the DAT (McGill paused 2024-25).","Heaviest lists: Manitoba, Saskatchewan, Dalhousie. Quebec schools (UdeM, Laval) add 1.5 yr physics + math."]},

 {"id":"labmed","label":"Medical Laboratory Science / Clinical Genetics","group":"Other regulated clinical","exam":"CSMLS certification (after accredited program)",
  "summary":"MLS and clinical-genetics paths value strong wet-lab technique, microbiology, biochemistry, genetics and cell/molecular biology. WLU is not an accredited MLT program, but these courses build the foundation and support bridging/graduate entry.",
  "buckets":[
    {"name":"Genetics & molecular biology","courses":["BI226","BI336"],"note":"Core to clinical genetics."},
    {"name":"Cell biology","courses":["BI236","BI341"],"note":"BI341 carries a lab."},
    {"name":"Microbiology (with lab)","courses":["BI374","BI376"],"note":"BI374 carries a lab."},
    {"name":"Biochemistry","courses":["CH250","CH350"],"note":"CH250 carries a lab."},
    {"name":"Immunology","courses":["HE303"],"note":"HE303/BI317."},
    {"name":"Pathophysiology","courses":["HE431"],"note":"HE431/BI416."},
    {"name":"Statistics","courses":["ST231"],"note":"Lab data interpretation."},
  ],"schoolNotes":["Confirm against the specific bridging/accredited program's admission list."]},

 {"id":"gc","label":"Genetic Counselling (MSc)","group":"Other regulated clinical","exam":"CAGC/ABGC certification (after MSc)",
  "summary":"Genetic counselling MSc programs look for genetics depth, psychology, statistics, and demonstrated counselling/advocacy exposure plus communication.",
  "buckets":[
    {"name":"Genetics","courses":["BI226","BI336"],"note":"Often a specific genetics course is required."},
    {"name":"Molecular & cell biology","courses":["BI236"],"note":""},
    {"name":"Biochemistry","courses":["CH250"],"note":""},
    {"name":"Psychology","courses":["PS101","PS102"],"note":"Developmental/abnormal psych often expected (Arts/PS)."},
    {"name":"Statistics","courses":["ST231"],"note":"Commonly required."},
    {"name":"Communication / KT","courses":["HE605"],"note":"MSc-level; counselling/advocacy exposure valued."},
  ],"schoolNotes":["Canadian programs (e.g. UofT, UBC, McGill) publish specific prereqs and prior-experience expectations: verify per program."]},

 {"id":"research","label":"Research / Graduate Study (thesis MSc, PhD)","group":"Research & graduate","exam":"GPA + research experience + supervisor match",
  "summary":"Research paths weight experimental design, lab/computational technique, quantitative and bioinformatics skills, primary-literature appraisal, and scientific communication. The thesis MSc (HE699) and HE490 directed research are the capstones.",
  "buckets":[
    {"name":"Cell & molecular biology","courses":["BI236","BI336","BI341"],"note":"BI341 carries a lab."},
    {"name":"Genetics","courses":["BI226"],"note":""},
    {"name":"Biochemistry","courses":["CH250","CH350"],"note":""},
    {"name":"Research methods & appraisal","courses":["HE201","HE603"],"note":"HE603 is the grad critical-appraisal course."},
    {"name":"Statistics & data","courses":["ST231"],"note":"Add upper-year stats / bioinformatics for omics."},
    {"name":"Directed research / thesis","courses":["HE490","HE699"],"note":"UG thesis (HE490) and MSc thesis (HE699)."},
    {"name":"Molecular electives","courses":["HE303","HE431","HE432","HE438"],"note":"Immunology, pathophysiology, virology, cancer biology."},
  ],"schoolNotes":["A documented authentic research experience matters more than any single course."]},

 {"id":"industry","label":"Biotech / Pharma / Regulatory","group":"Industry","exam":"Degree + technical skills (no single exam)",
  "summary":"Industry roles (QA/QC, clinical research associate, regulatory affairs, R&D technician) weight hands-on lab technique, GLP/regulatory literacy, data handling, and communication. This is where the experiential/lab gap bites hardest.",
  "buckets":[
    {"name":"Lab-bearing science","courses":["CH202","CH250","BI341","BI374"],"note":"Pick courses that actually carry labs (badged below)."},
    {"name":"Microbiology","courses":["BI374","BI376"],"note":"Relevant to QA/QC and biomanufacturing."},
    {"name":"Biochemistry","courses":["CH250","CH350"],"note":""},
    {"name":"Virology / disease biology","courses":["HE432","HE438"],"note":"Biomedical virology, cancer biology."},
    {"name":"Statistics & data","courses":["ST231"],"note":"Plus coding/bioinformatics for data roles."},
    {"name":"Communication / KT","courses":["HE605"],"note":"Regulatory and scientific writing."},
  ],"schoolNotes":["GLP/GMP and regulatory literacy are not currently covered by a dedicated course: candidate gap."]},
]
PATHWAY_GROUPS = ["Medicine & dentistry","Other regulated clinical","Research & graduate","Industry"]

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
  "grad": {
    "2025/2026": merge_grad(g25, "2025/2026"),
    "2026/2027": merge_grad(g26, "2026/2027"),
  },
  "gradGroupOrder": GRAD_GROUP_ORDER,
  "gradProgram": {
    "2025/2026": open(os.path.join(base,"grad_program_text_2025_26.txt"),encoding="utf-8").read(),
    "2026/2027": open(os.path.join(base,"grad_program_text_2026_27.txt"),encoding="utf-8").read(),
  },
  "gradProgramUrl": {
    "2025/2026": grad_program_url("2025/2026"),
    "2026/2027": grad_program_url("2026/2027"),
  },
  "gradProgramIssues": GRAD_PROGRAM_ISSUES,
  "gradCoordinator": "Ketan Shankardass (kshankardass@wlu.ca)",
  "courseIndex": COURSE_INDEX,
  "pathways": PATHWAYS,
  "pathwayGroups": PATHWAY_GROUPS,
}
json.dump(data, open(os.path.join(base,"dashboard_data.json"),"w",encoding="utf-8"), indent=2, ensure_ascii=False)
n_issues = sum(len(v) for v in ISSUES.values())+len(PROGRAM_ISSUES)+len(GLOBAL_ISSUES)+len(FACULTY_ISSUES)
n_grad = sum(len(v) for v in GRAD_ISSUES.values())+len(GRAD_PROGRAM_ISSUES)
print(f"data built: UG {len(d25)}/{len(d26)} courses, GR {len(g25)}/{len(g26)} courses; UG issues {n_issues}, GR issues {n_grad}")
