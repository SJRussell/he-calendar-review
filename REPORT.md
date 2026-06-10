# WLU Health Sciences Academic Calendar — Review

**Source:** Undergraduate Academic Calendar, Faculty of Science → Health Sciences (academic-calendar.wlu.ca)
**Scope:** All HE / HN course listings + Honours BSc Health Sciences degree structure, plus the cross-listed/required codes those entries reference.
**Years compared:** 2025/2026 (current, 30 HE/HN courses) vs 2026/2027 (next, 34 courses).
**Method:** Raw HTML scraped and decoded as cp1252 so apostrophes/quotes are verbatim; structural checks run programmatically; prose read manually for spelling/grammar.

> **Headline:** Every spelling, grammar, and dangling-reference defect found in 2025/26 is reproduced unchanged in 2026/27 — nothing was corrected between the two calendars. The one substantive 2026/27 change (a new HE-prefixed anatomy/physiology sequence) was only half-wired into the program, creating a redundant parallel track.

---

## Phase 1 — Spelling & grammar

### Course descriptions
| Course | Issue |
|---|---|
| HE202 | A stray label **`Prerequisites :`** is typed into the end of the description body (an editing slip leaked into prose). |
| HE224 | Opens *"Anatomy and Physiology I, introduces…"* — comma after the title breaks subject/verb. Also *"the structure and function organization"* → intended *"structural and functional organization."* |
| HE225 | *"Anatomy and Physiology II, continues…"* — same misplaced comma; plus stray comma in *"focusing on regulation, and homeostasis."* |
| HE330 | *"functional foods, food labeling obesity and weight management"* — missing comma (*"labeling, obesity"*); *"covering topics including;"* uses a semicolon where a colon is needed; US spelling *labeling* vs Canadian *labelling*. |
| HE410 | *"perspectives including;"* and *"Topics may include;"* — semicolons where colons belong; *"interactive/hands on"* → *"hands-on."* |

### Program notes
- *"…pharmacy, etc.)in the future"* — missing space after `)`.
- *"PC141 (orPC131)"* — missing space (*"or PC131"*).
- Note 4 psychology list out of numeric order: PS285 before PS275/PS276.

### Consistency
- Title casing: **HE411** "Critical perspectives in Public Health" and **HE430** "Advanced nutrition and chronic disease" use sentence case; every other title uses Title Case.
- "Registration status" / "Registration Status" / "registration status" — capitalization varies across prerequisite fields.
- Cross-list note style: most read `( Cross-listed as KP435 .)`; **HE320/HE321** drop the parentheses, and **HE368** says "Cross-listed **with**" instead of "as".
- *Encoding (low):* pages declare `charset=ISO-8859-1` but serve Windows-1252 bytes (curly quotes). Browsers tolerate it; strict parsers show replacement characters.

---

## Phase 2 — Prerequisites

**Dangling internal references (a listed HE/HN course has no calendar entry):**
| Referenced | Where | Severity |
|---|---|---|
| **HE302** | Prerequisite for **HE410** and **HE411** | HIGH — students cannot satisfy a course that doesn't exist (likely renamed/dropped). |
| **HE434** | Exclusion on **HE303**, and an option in the program's Year-4 list | HIGH — referenced in 3 places, defined nowhere. |
| **HE211** | Alternative prerequisite for **HE330** and **HE431** | MED — defunct code; live alternatives (BI216/KP220) still listed. |
| **MA241** | Alternative prerequisite for **HE300** | LOW — not hyperlinked (all live codes are), suggesting it's defunct; ST231 is the live path. |

**Other:**
- HE321 prereq *"KP225 / HE225 / HS202 or HN204"* mixes a slash-list with an "or" — ambiguous precedence.
- Cross-listed courses redundantly name their own code as an exclusion (e.g., HE300/KP434 excludes both HE300 and KP434). This is partly the standard anti-double-credit mechanism, but listing a course's *own primary code* is noise.

---

## Phase 3 — Curriculum overlaps & gaps

**1. Incomplete anatomy/physiology migration (HIGH).** In 2026/27 the Year-2 core was changed from `HN204 + HN220/KP222` to the new `HE224 + HE225`. But `HN204`, `HN210/KP221`, `HN220/KP222`, and `HN320` all remain published, and `HE320`/`HE321` were created without being slotted into any required sequence. The result is two overlapping generations of A&P courses with a tangled mutual-exclusion web (HE224 ⟷ HN204/HN220/HS202; HE320 ⟷ HN320/HS340; HE321 ⟷ HN210/KP221). `HE320` (Integrative Human Physiology) effectively duplicates `HN320` (Human Physiology II).

**2. Stale Year-4 selection list (HIGH).** "Select 2.0 credits from" lists `HE410, HE411, HE430, HE431, HE432, HE434, HE435, HE440, HE450, HE490` — it cites the non-existent **HE434** and omits three existing 400-level courses: **HE436** (Health and Human Rights), **HE437** (Principles of Population Health), **HE438** (Cancer Biology). Students can't tell whether 436/437/438 count toward the requirement.

**3. Orphaned new courses (MED).** HE320 and HE321 appear only as electives; they're not referenced anywhere in the degree structure.

**4. Missing descriptions (MED/LOW gaps).** HE320, HE321, HE435 (a titled course, "Exercise is Medicine"), HE368, HN210, HN220 show only a cross-list pointer with no academic description in the HE calendar.

**5. Conceptual overlap (note, not error).** HE301 (Social Determinants), HE411 (Public Health), HE437 (Population Health) share territory; HE437's own description concedes it revisits material "briefly highlighted in previous methods courses."

**6. Inconsistent term data.** Only ~1/3 of courses specify a term offered; the field is blank for most. Not necessarily an error, but uneven for planning.

---

## Phase 4 — Dashboard

`index.html` — single self-contained file (open directly in a browser, no server needed). Year toggle (2025/26 ↔ 2026/27), search, level/issues-only/new-only filters, clickable course cards opening a detail panel (description, prereqs with dangling refs highlighted, exclusions, cross-list, per-course findings, and greyed placeholder slots for syllabus/instructor), an Issues tab grouped by severity, and a Program-structure tab.

### Files in `C:\Users\srussell\health-sci-calendar-review\`
- `index.html` — the dashboard.
- `dashboard_data.json` — merged data + issue annotations (dashboard source of truth).
- `courses_2025.json`, `courses_2026.json` — parsed course data.
- `findings.json` — programmatic structural findings.
- `program_text_2025_26.txt`, `program_text_2026_27.txt` — verbatim degree structure.
- `raw/` — original HTML.
- `parse_courses.py`, `extract_text.py`, `analyze.py`, `build_dashboard.py`, `gen_html.py` — the pipeline (re-runnable to refresh from source).
