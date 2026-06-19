# WLU Faculty of Science cognate courses for Health Sciences (MMS) students

Source: Wilfrid Laurier University 2026/2027 Undergraduate Academic Calendar
(`academic-calendar.wlu.ca`, `cal=1`, `s=1170`, `y=93`). Scraped by
`scrape_cognate.py`; structured data in `cognate_courses.json`. Pages decoded as
Windows-1252. `has_lab` is derived from the presence of "Lab" in the published
"Hours per week" string.

These are the Faculty of Science courses a Health Sciences (Molecular & Medical
Health Sciences stream) student would use to satisfy medical / dental /
allied-health prerequisites and to cover MCAT/DAT content.

---

## (a) Courses scraped per department

| Department | Calendar `d` | Course links found | Unique courses captured |
|---|---|---|---|
| Biology (BI) | 3247 | 67 | 64 BI (+2 CH cross-listed, +1 already counted) |
| Chemistry and Biochemistry (CH) | 3248 | 53 | 53 |
| Physics (PC) | 3245* | 39 | 39 |
| Mathematics (MA + ST) | 3251 | 80 | 62 MA + 18 ST |
| Psychology (PS) | 3246 | 68 | 68 |
| Kinesiology & Physical Education (KP) | 3250 | 62 | 62 |
| Medical Foundations | 3266 | 16 | 0 unique (all cross-listed from BI/CH/MA) |
| Paramedicine (PARA) | 3267 | 9 | 9 |

**Unique records in `cognate_courses.json` (deduped by course code): 375.**
By subject prefix: BI 64, CH 53, KP 62, MA 62, PS 68, PC 39, ST 18, PARA 9.
Courses with a lab component: **114**.

Notes on department resolution (discovered during scraping; the prompt's `d`
values needed two corrections):

- **Physics is `d=3245`, not `d=3253`.** The prompt's "Computer Science and
  Physics" page (`d=3253`) is a landing page that links only to sub-department
  pages, not courses. The actual physics (PC) courses live at `d=3245`
  ("Physics (PC/CP Dept)"). CP/computer-science courses were excluded as
  instructed; only PC codes were kept.
- **Medical Foundations (`d=3266`) owns no MF-prefixed courses.** It is a
  curated cross-listing whose 16 links point to BI/CH/MA courses owned by other
  departments. Each link carries the *owning* department's `d` in its href, so
  the scraper parses the full href (capturing the real `d`) rather than
  reconstructing the URL. The same mechanism correctly resolves other
  cross-listings (e.g. CH454 cross-listed into Biology carries `d=3248`).
- **There is no "BC" subject prefix at WLU.** Biochemistry is taught entirely
  under the **CH** prefix (CH250, CH350, CH354, CH459, etc.). The prompt's
  expectation of a BC prefix does not match the calendar.
- No download or parse failures after these corrections (0 problems reported).

\* Physics `d` corrected from the prompt's 3253 to 3245 (see above).

---

## (b) Health-professions prerequisite buckets to WLU course codes

"(with lab)" after a code means the published Hours per week includes a Lab
component. Mappings are based on course title **and** description; "(verify)"
flags a course worth confirming against the official prerequisite list before
relying on it. Cross-listed codes are shown as the calendar prints them
(e.g. `KP222/HN220`).

| Prerequisite / MCAT-DAT bucket | WLU course code(s) |
|---|---|
| **Intro biology (with lab)** | **BI110** *Unifying Life Processes*, **BI111** *Biological Diversity and Evolution*. Both are the standard first-year biology pair. NOTE: neither lists a "Lab" line (3h lecture + biweekly tutorial/seminar), so neither is flagged `has_lab`. Most med/dental schools accept this pair as intro biology; the **lab requirement is met later** via BI226/BI236/BI341 (verify whether a specific school requires lab in first-year bio). |
| **General / inorganic chemistry (with lab)** | **CH110 (with lab)** *Fundamentals of Chemistry I*, **CH111 (with lab)** *Fundamentals of Chemistry II* (standard first-year pair). For chemistry majors / heavier stream: **CH130 (with lab)** *General Chemistry I*, **CH131 (with lab)** *General Chemistry II*. Dedicated inorganic: **CH225** *Inorganic Chemistry I*, **CH226 (with lab)** *Inorganic Chemistry II*. |
| **Organic chemistry (with lab)** | **CH202 (with lab)** *Organic Chemistry I: Fundamentals*, **CH203 (with lab)** *Organic Chemistry II* (life-sci / general stream). Chemistry-major stream: **CH206 (with lab)** / **CH207 (with lab)** *Organic Chemistry I/II for Chemists*. **CH205** *Introductory Organic Chemistry II* (no lab). Upper-year: CH301 (with lab), CH302, CH303, CH306, CH404. |
| **Biochemistry** | **CH250 (with lab)** *Introductory Biochemistry* (the entry biochem course); **CH350** *Biochemistry I: Bioenergetics and Catabolic Pathways*, **CH354** *Biochemistry II: Structure & Analysis of Proteins and Nucleic Acids*, **CH459** *Biochemistry III*. Lab-specific: **CH357 (with lab)** *Laboratory Techniques in Biochemistry*, **CH358 (with lab)**, **CH452 (with lab)** *Capstone Biochemistry Laboratory*. Related: CH355 Bioanalytical, CH356 Biotechnology, CH419 Biochemical Toxicology. (No BC prefix exists; biochem = CH.) |
| **Human physiology** | **KP222/HN220 (with lab)** *Human Physiology*; **KP320/HE320** *Integrative Human Physiology*. Combined anatomy+physiology: **KP224/HE224/HS202 (with lab)** *Anatomy and Physiology I*, **KP225/HE225;HS204 (with lab)** *Anatomy and Physiology II*. Exercise stream: **KP322 (with lab)** *Exercise Physiology*, **KP422** *Advanced Exercise Physiology*. Pathophysiology: **BI416/HE431** *Pathophysiology*. (BI animal/plant physiology courses BI451/BI456/BI369 exist but are non-human; not for the human-physiology bucket.) |
| **Microbiology** | **BI374 (with lab)** *Physiological Applications of Microbiology*, **BI376** *Microbial Physiology*, **BI475 (with lab)** *Environmental Microbiology*. No single first-year "Microbiology" survey; these are the microbiology offerings (verify which satisfies a given school's microbiology requirement; BI374 is the lab-bearing option). |
| **Genetics** | **BI226** *Molecular Biology and Genetics* (core). Upper-year genetics-adjacent: BI336 *Molecular Cell Biology*, BI441 *Advanced Molecular Biotechnology* (with lab). (No standalone "BI Genetics" course beyond BI226; verify if a school wants a dedicated genetics course.) |
| **Cell / molecular biology** | **BI236** *Cell Biology*, **BI226** *Molecular Biology and Genetics*, **BI336** *Molecular Cell Biology*, **BI341 (with lab)** *Lab Methods: Cell and Molecular Biology* (also cross-listed **CH341 (with lab)**), **BI441 (with lab)** *Advanced Molecular Biotechnology*. |
| **Immunology** | **BI317/HE303** *Introduction to Immunology* (no lab). |
| **Physics (with lab)** | Life-sciences stream (recommended for health/MCAT): **PC141 (with lab)** *Mechanics for the Life Sciences*, **PC142 (with lab)** *Thermodynamics and Waves for the Life Sciences*. General stream: **PC131 (with lab)** *Mechanics*, **PC132 (with lab)** *Thermodynamics and Waves*. NOTE: **PC151/PC152** and **PC161/PC162** ("Introduction to...") are the **no-lab** lecture-only versions; pick PC131/132 or PC141/142 when a lab is required. |
| **Calculus** | **MA101 (with lab)** *Calculus I for the Natural Sciences*, **MA104 (with lab)** *Calculus II*. Entry/alternate: **MA100 (with lab)** *Introductory Calculus for the Natural Sciences*, **MA102 (with lab)**, **MA103 (with lab)** *Calculus I*. (MA "Lab" line is a computer/tutorial lab, not wet-lab.) MA129 is the business/social-science calculus (verify acceptability). |
| **Statistics** | **ST231 (with lab)** *Statistical Methods for Life and Health Sciences* (the natural fit for Health Sci), **ST230 (with lab)** *Introduction to Probability and Statistics for Science*, **ST260 (with lab)** *Introduction to Statistics*. ST259 *Probability I* (with lab) for theory. |
| **Introductory psychology** | **PS101** *Introduction to Psychology I*, **PS102** *Introduction to Psychology II* (the standard pair; covers MCAT psych foundations). |
| **Sociology / social-science (MCAT Psych/Soc)** | Within Science: **KP211/SY211** *Sociology of Physical Activity* (cross-listed with Sociology). Psychology social/behavioural courses that map to MCAT Psych/Soc content: **PS270** *Social Psychology*, **PS285** *Health Psychology*, **PS275/PS276** *Developmental Psychology*, **PS268** *Drugs and Behaviour*, **PS263** *Behavioural Neuroscience*. (A dedicated SY/Sociology department sits outside the Faculty of Science and was not in scope; SY211 is the only sociology course surfacing via these Science depts. Verify SY offerings in the Faculty of Arts for a full sociology prerequisite.) |
| **English / writing** | **None in the Faculty of Science scope.** No English/writing course appears in BI/CH/PC/MA/ST/PS/KP/PARA. WLU English (EN) and writing requirements live in the Faculty of Arts (out of scope here) and must be sourced there. |
| **Indigenous studies** | **None in the Faculty of Science scope.** No Indigenous-studies course appears in the scraped Science departments. WLU's Indigenous Studies (IN) program is in the Faculty of Arts (out of scope) and must be sourced there. |

---

## (c) Medical Foundations (MF) and Paramedicine (PM/PARA) courses found

### Medical Foundations (`d=3266`)
Medical Foundations has **no courses of its own**. The page is a curated
"foundations for medical/health study" reading list that **cross-lists 16
existing first/second-year science courses** from other departments. The exact
codes it points to:

- Biology: **BI110, BI111** (intro biology pair)
- Chemistry: **CH110, CH111** (fundamentals), **CH130, CH131** (general),
  **CH202, CH203** (organic), **CH206, CH207** (organic for chemists),
  **CH250** (introductory biochemistry)
- Mathematics: **MA100, MA101, MA102, MA103** (calculus stream)
- Physics: **PC131** (mechanics, with lab)

In other words, Medical Foundations is WLU's explicit signpost of the
pre-medical core: intro bio + general chem + organic chem + intro biochem +
calculus + a calculus-based physics course. These are exactly the courses a
pre-med Health Sci student should prioritise. (The MF-listed codes are recorded
in `cognate_scrape_manifest.json` under `medical_foundations_listed_codes`.)

### Paramedicine (PARA, `d=3267`)
Nine courses, all PARA-prefixed and **professional/contextual rather than
science-prerequisite** (no labs, no MCAT/DAT content). They cover the
sociology and professional practice of paramedicine, not biology/chemistry
prerequisites:

- **PARA200** Evolution of the Field of Paramedicine
- **PARA201** Paramedicine in Canada and Around the World
- **PARA300** Emerging Issues & Critical Topics in Paramedicine
- **PARA301** The Health & Wellbeing of Paramedics
- **PARA302** Understanding and Caring for Diverse Populations
- **PARA303** The Paramedic Identity: Who are we?
- **PARA400** Ethical and Legal Considerations in Paramedicine
- **PARA401** The Business of Paramedicine
- **PARA402** Paramedics as Leaders

These are relevant to allied-health career context and the social-determinants /
diverse-populations themes of the MCAT Psych/Soc section (esp. PARA302), but
they do **not** satisfy any hard science prerequisite.

---

## Files

- Structured data: `cognate_courses.json` (375 unique course records)
- Scrape manifest (per-dept counts, MF-listed codes, any problems):
  `cognate_scrape_manifest.json`
- Raw HTML: `raw/cognate/<dept>/c_<id>.html` + `_dept_index.html` per department
- Scraper: `scrape_cognate.py`
