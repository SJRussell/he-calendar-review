#!/usr/bin/env python
"""Dump clean readable text: program requirements + all course descriptions."""
import re, os, glob
from bs4 import BeautifulSoup

base = r"C:\Users\srussell\health-sci-calendar-review"

def clean(t):
    return re.sub(r"[ \t]+", " ", t.replace("\xa0", " ")).strip()

def program_text(path):
    soup = BeautifulSoup(open(path, encoding="cp1252", errors="replace").read(), "html.parser")
    # main content div
    main = soup.find("div", class_="content") or soup
    # remove script/style
    for s in main(["script", "style"]):
        s.decompose()
    # remove glossary tooltip definition spillover: drop attributes by taking get_text
    lines = []
    for el in main.find_all(["h1","h2","h3","h4","p","li","dt","dd","td","th"]):
        txt = clean(el.get_text(" ", strip=True))
        if txt and "showGlossaryDef" not in txt and len(txt) > 1:
            tag = el.name.upper()
            lines.append(f"[{tag}] {txt}")
    # dedupe consecutive
    out = []
    for l in lines:
        if not out or out[-1] != l:
            out.append(l)
    return "\n".join(out)

for yr, f in [("2025_26","prog_2025.html"),("2026_27","prog_2026.html")]:
    txt = program_text(os.path.join(base,"raw","program",f))
    open(os.path.join(base, f"program_text_{yr}.txt"), "w", encoding="utf-8").write(txt)
    print(f"wrote program_text_{yr}.txt ({len(txt)} chars)")

# graduate program pages (MSc: Thesis + Coursework options)
for yr, f in [("2025_26","prog_grad_2025.html"),("2026_27","prog_grad_2026.html")]:
    txt = program_text(os.path.join(base,"raw","grad",f))
    open(os.path.join(base, f"grad_program_text_{yr}.txt"), "w", encoding="utf-8").write(txt)
    print(f"wrote grad_program_text_{yr}.txt ({len(txt)} chars)")
