#!/usr/bin/env python
import json, os
base = r"C:\Users\srussell\health-sci-calendar-review"
data = json.load(open(os.path.join(base,"dashboard_data.json"), encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WLU Health Sciences Calendar Review</title>
<style>
:root{
  --bg:#0f1115; --panel:#181b22; --panel2:#1f242d; --line:#2c333f;
  --ink:#e6e9ef; --mut:#9aa4b2; --accent:#5b8def; --accent2:#7c5cff;
  --hi:#ff5d6c; --med:#ffb454; --low:#62d0a4; --new:#7c5cff;
  --l100:#3a7bd5; --l200:#2bb3a3; --l300:#c98a2b; --l400:#c0556a;
}
*{box-sizing:border-box}
body{margin:0;font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--ink)}
header{position:sticky;top:0;z-index:20;background:linear-gradient(180deg,#12151c,#12151cf2);
  border-bottom:1px solid var(--line);padding:14px 22px;backdrop-filter:blur(6px)}
h1{font-size:18px;margin:0 0 2px;font-weight:650}
.sub{color:var(--mut);font-size:12.5px}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.spacer{flex:1}
.tabs{display:flex;gap:4px;margin-top:10px}
.tab{padding:7px 14px;border-radius:8px 8px 0 0;background:transparent;color:var(--mut);
  border:1px solid transparent;cursor:pointer;font-size:13.5px}
.tab.active{background:var(--panel);color:var(--ink);border-color:var(--line);border-bottom-color:var(--panel)}
.seg{display:inline-flex;background:var(--panel2);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.seg button{background:transparent;border:0;color:var(--mut);padding:7px 13px;cursor:pointer;font-size:13px}
.seg button.on{background:var(--accent);color:#fff}
input.search{background:var(--panel2);border:1px solid var(--line);color:var(--ink);
  padding:8px 12px;border-radius:9px;min-width:230px;font-size:13.5px}
.chip{padding:5px 11px;border-radius:20px;border:1px solid var(--line);background:var(--panel2);
  color:var(--mut);cursor:pointer;font-size:12.5px;user-select:none}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.stats{display:flex;gap:18px;margin-top:9px;font-size:12.5px;color:var(--mut)}
.stats b{color:var(--ink);font-size:15px}
main{padding:20px 22px 60px;max-width:1280px;margin:0 auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:14px;
  cursor:pointer;position:relative;transition:.12s;overflow:hidden}
.card:hover{transform:translateY(-2px);border-color:var(--accent)}
.card .lvl{position:absolute;left:0;top:0;bottom:0;width:4px}
.card h3{margin:0 0 3px;font-size:15px;font-weight:650;letter-spacing:.2px}
.card .ttl{color:var(--mut);font-size:13px;min-height:34px}
.card .meta{display:flex;gap:8px;margin-top:9px;font-size:11.5px;color:var(--mut);flex-wrap:wrap}
.pill{background:var(--panel2);border:1px solid var(--line);border-radius:6px;padding:2px 7px}
.badges{position:absolute;top:10px;right:10px;display:flex;gap:5px}
.dot{font-size:10.5px;font-weight:700;border-radius:20px;padding:2px 8px;color:#0c0e12}
.dot.hi{background:var(--hi)} .dot.med{background:var(--med)} .dot.low{background:var(--low)}
.dot.new{background:var(--new);color:#fff}
.xlist{font-size:11px;color:var(--accent2);margin-top:6px}
/* modal */
.scrim{position:fixed;inset:0;background:#000a;backdrop-filter:blur(3px);display:none;z-index:40}
.scrim.open{display:block}
.modal{position:fixed;right:0;top:0;bottom:0;width:min(560px,94vw);background:var(--panel);
  border-left:1px solid var(--line);z-index:50;transform:translateX(100%);transition:.2s;
  overflow-y:auto;padding:22px 24px 60px}
.modal.open{transform:none}
.modal .x{position:absolute;top:14px;right:16px;background:var(--panel2);border:1px solid var(--line);
  color:var(--ink);border-radius:8px;padding:5px 11px;cursor:pointer}
.modal h2{margin:4px 0 2px;font-size:22px}
.modal .mttl{color:var(--mut);font-size:15px;margin-bottom:12px}
.kv{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.kv .pill{font-size:12px}
.sec{margin:16px 0}
.sec h4{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.7px;color:var(--mut)}
.sec p{margin:0;color:var(--ink)}
.req code,.refcode{background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:12.5px}
.dangling{background:#3a1620;border-color:var(--hi);color:#ff9aa6}
.placeholder{color:#6b7280;font-style:italic}
.issue{border:1px solid var(--line);border-left-width:4px;border-radius:8px;padding:9px 11px;margin:8px 0;
  background:var(--panel2);font-size:13.5px}
.issue.hi{border-left-color:var(--hi)} .issue.med{border-left-color:var(--med)} .issue.low{border-left-color:var(--low)}
.issue .tag{font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);margin-bottom:3px}
.issue .tag b{color:var(--ink)}
.sevtag{display:inline-block;font-size:10px;font-weight:700;border-radius:4px;padding:1px 6px;margin-right:6px;color:#0c0e12}
.sevtag.hi{background:var(--hi)} .sevtag.med{background:var(--med)} .sevtag.low{background:var(--low)}
.issuesWrap h3{margin:22px 0 6px;font-size:14px}
.progtext{white-space:pre-wrap;background:var(--panel);border:1px solid var(--line);border-radius:11px;
  padding:16px;font-size:13.5px;line-height:1.7}
.note{color:var(--mut);font-size:12.5px;margin:6px 0 16px}
.hidden{display:none}
a.codelink{color:var(--accent);text-decoration:none}
.callink{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;
  text-decoration:none;padding:8px 14px;border-radius:9px;font-size:13px;font-weight:600;margin:4px 0 14px}
.callink:hover{filter:brightness(1.1)}
.cardlink{position:absolute;bottom:10px;right:12px;color:var(--mut);text-decoration:none;font-size:11px}
.cardlink:hover{color:var(--accent)}
.proglink{display:inline-flex;gap:6px;background:var(--panel2);border:1px solid var(--line);
  color:var(--accent);text-decoration:none;padding:7px 13px;border-radius:9px;font-size:13px;margin-bottom:6px}
.proglink:hover{border-color:var(--accent)}
.grid-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:14px}
/* collapsed columns-by-level view */
.cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;align-items:start}
.col{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:12px 12px 14px}
.col-h{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut);
  margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.col-h .swatch{width:10px;height:10px;border-radius:3px}
.col-h b{color:var(--ink);font-size:13.5px}
.col-h .ct{margin-left:auto;font-size:11px}
.boxes{display:flex;flex-wrap:wrap;gap:7px}
.minibox{position:relative;display:inline-flex;align-items:center;justify-content:center;
  min-width:62px;padding:8px 9px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);
  color:var(--ink);font-size:12.5px;font-weight:650;letter-spacing:.2px;cursor:pointer;transition:.1s}
.minibox:hover{border-color:var(--accent);transform:translateY(-1px)}
.minibox.flag-hi{border-color:var(--hi)}
.minibox.flag-med{border-color:var(--med)}
.minibox .ni{position:absolute;top:-5px;right:-5px;width:8px;height:8px;border-radius:50%;background:var(--new);border:1px solid var(--bg)}
.col.empty{opacity:.45}
@media(max-width:780px){.cols{grid-template-columns:repeat(2,1fr)}}
/* faculty tab */
.facgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}
@media(max-width:780px){.facgrid{grid-template-columns:1fr}}
.fach{font-size:13px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut);margin:0 0 10px}
.faclist{display:flex;flex-direction:column;gap:8px}
.facrow{display:flex;align-items:center;gap:10px;background:var(--panel);border:1px solid var(--line);
  border-radius:10px;padding:10px 12px}
.facrow.miss{border-left:4px solid var(--med)}
.facrow.miss.chair{border-left-color:var(--hi)}
.facrow .nm{font-weight:600}
.facrow .rl{font-size:11.5px;color:var(--accent2);background:var(--panel2);border:1px solid var(--line);
  border-radius:6px;padding:1px 7px}
.facrow .lv{font-size:11px;color:var(--med);margin-left:auto}
.facrow .nt{font-size:12px;color:var(--mut);width:100%;margin-top:4px}
.facrow.col{flex-wrap:wrap}
/* edit mode + instructor + status + diff + map */
.editbtn{padding:7px 13px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);
  color:var(--mut);cursor:pointer;font-size:13px}
.editbtn.on{background:var(--accent2);border-color:var(--accent2);color:#fff}
.exportbtn{padding:7px 13px;border-radius:9px;border:1px solid var(--accent);background:transparent;
  color:var(--accent);cursor:pointer;font-size:13px}
.instr{display:inline-flex;align-items:center;gap:6px}
.instr input{background:var(--panel2);border:1px solid var(--line);color:var(--ink);border-radius:7px;
  padding:6px 9px;font-size:13px;min-width:200px}
.statusSel{background:var(--panel2);border:1px solid var(--line);color:var(--ink);border-radius:6px;
  padding:3px 6px;font-size:11.5px;margin-left:8px}
.stbadge{font-size:10px;font-weight:700;border-radius:4px;padding:1px 6px;margin-left:8px;text-transform:uppercase}
.stbadge.ack{background:#3b4252;color:#cdd6e6}
.stbadge.fixed{background:var(--low);color:#08120d}
.stbadge.wontfix{background:#4a3340;color:#ffb9c6}
.issue.done{opacity:.55}
/* diff */
.difftbl{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}
.difftbl th,.difftbl td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
.difftbl th{background:var(--panel2);color:var(--mut);font-weight:600}
.diff-add{color:var(--low)} .diff-del{color:var(--hi)} .diff-chg{color:var(--med)}
.diffsec h3{margin:20px 0 4px;font-size:14px}
/* prereq map */
#mapWrap{overflow:auto;border:1px solid var(--line);border-radius:12px;background:var(--panel);margin-top:12px}
.mapnode rect{fill:var(--panel2);stroke:var(--line)}
.mapnode:hover rect{stroke:var(--accent)}
.mapnode text{fill:var(--ink);font:600 11px sans-serif}
.mapnode.dangling rect{fill:#3a1620;stroke:var(--hi);stroke-dasharray:3 2}
.mapnode.dangling text{fill:#ff9aa6}
.mapedge{stroke:#46506180;stroke-width:1.3;fill:none}
.mapedge.dang{stroke:var(--hi);stroke-dasharray:4 3}
.maplbl{fill:var(--mut);font:600 12px sans-serif}
body.gradmode .lvl-chip, body.gradmode #newOnly{display:none}
#progSeg button.on{background:var(--accent2)}
</style>
</head>
<body>
<header>
  <div class="row">
    <div>
      <h1>WLU Health Sciences &mdash; Academic Calendar Review</h1>
      <div class="sub">Faculty of Science &middot; HE / HN course listings &amp; Honours BSc structure</div>
    </div>
    <div class="spacer"></div>
    <button class="editbtn" id="editBtn" title="Toggle editing of instructors and issue status">&#9998; Edit</button>
    <button class="exportbtn" id="exportBtn" title="Download overrides.json to commit">&#8681; Export overrides</button>
    <div class="seg" id="progSeg" title="Undergraduate BSc vs Graduate MSc calendar">
      <button data-p="ug" class="on">Undergrad BSc</button>
      <button data-p="grad">Graduate MSc</button>
    </div>
    <div class="seg" id="yearSeg">
      <button data-y="2025/2026">2025/2026</button>
      <button data-y="2026/2027" class="on">2026/2027</button>
    </div>
  </div>
  <div class="tabs" id="tabs">
    <div class="tab active" data-t="courses">Courses</div>
    <div class="tab" data-t="issues">Issues</div>
    <div class="tab" data-t="map">Prereq map</div>
    <div class="tab" data-t="diff">Year diff</div>
    <div class="tab" data-t="program">Program structure</div>
    <div class="tab" data-t="faculty">Faculty</div>
  </div>
</header>
<main>
  <!-- COURSES TAB -->
  <section id="tab-courses">
    <div class="row" style="margin-bottom:6px">
      <div class="seg" id="viewSeg">
        <button data-v="collapsed">Collapsed</button>
        <button data-v="expanded" class="on">Expanded</button>
      </div>
      <input class="search" id="search" placeholder="Search code, title, description...">
      <span class="chip lvl-chip on" data-lvl="all">All levels</span>
      <span class="chip lvl-chip" data-lvl="100">100</span>
      <span class="chip lvl-chip" data-lvl="200">200</span>
      <span class="chip lvl-chip" data-lvl="300">300</span>
      <span class="chip lvl-chip" data-lvl="400">400</span>
      <span class="chip" id="issuesOnly">Issues only</span>
      <span class="chip" id="newOnly">New in 2026/27</span>
    </div>
    <div class="stats" id="stats"></div>
    <div id="grid" style="margin-top:14px"></div>
  </section>
  <!-- ISSUES TAB -->
  <section id="tab-issues" class="hidden issuesWrap">
    <div class="note">Findings for the selected calendar year. Severity: <span class="sevtag hi">HIGH</span> blocks correct enrolment or degree audit &middot; <span class="sevtag med">MED</span> content/clarity defect &middot; <span class="sevtag low">LOW</span> style/consistency.</div>
    <div id="issuesList"></div>
  </section>
  <!-- PROGRAM TAB -->
  <section id="tab-program" class="hidden">
    <div class="note">Honours BSc Health Sciences degree structure, verbatim from the calendar, plus program-level findings.</div>
    <div id="programIssues"></div>
    <h3 style="margin-top:22px">Degree structure (verbatim)</h3>
    <a class="proglink" id="progLink" href="#" target="_blank" rel="noopener">Open Honours BSc page on WLU calendar &#8599;</a>
    <div class="progtext" id="progText"></div>
  </section>
  <!-- PREREQ MAP TAB -->
  <section id="tab-map" class="hidden">
    <div class="note">Internal HE/HN prerequisite flow (left = lower level). Dashed red nodes are referenced prerequisites with no course entry. Click a node to open the course.</div>
    <div id="mapWrap"></div>
  </section>
  <!-- YEAR DIFF TAB -->
  <section id="tab-diff" class="hidden">
    <div class="note">What changed from 2025/2026 to 2026/2027.</div>
    <div id="diffBody"></div>
  </section>
  <!-- FACULTY TAB -->
  <section id="tab-faculty" class="hidden">
    <div class="note" id="facNote"></div>
    <div id="facultyIssues"></div>
    <div class="facgrid">
      <div><h3 class="fach">Listed in calendar</h3><div id="facListed" class="faclist"></div></div>
      <div><h3 class="fach">Missing / needs correction</h3><div id="facMissing" class="faclist"></div></div>
    </div>
  </section>
</main>

<div class="scrim" id="scrim"></div>
<aside class="modal" id="modal"></aside>

<script>
const DATA = __PAYLOAD__;
// ---- editable overrides: 3 layers (committed file -> localStorage) ----
const BASE_OVERRIDES = __OVERRIDES__;        // inlined fallback (offline / file://)
const LS_KEY = "wlu-he-overrides-v1";
let OV = {instructors:{}, status:{}};        // effective overrides (merged)
function loadLocal(){ try{return JSON.parse(localStorage.getItem(LS_KEY))||{};}catch(e){return {};} }
function saveLocal(){ localStorage.setItem(LS_KEY, JSON.stringify({instructors:OV.instructors,status:OV.status})); }
function mergeOverrides(remote){
  const local = loadLocal();
  OV = {
    instructors: Object.assign({}, BASE_OVERRIDES.instructors||{}, (remote&&remote.instructors)||{}, local.instructors||{}),
    status:      Object.assign({}, BASE_OVERRIDES.status||{},      (remote&&remote.status)||{},      local.status||{}),
  };
}
const state = {year:"2026/2027", program:"ug", tab:"courses", view:"expanded", lvl:"all", q:"", issuesOnly:false, newOnly:false, edit:false};
const $ = s=>document.querySelector(s);
const lvlColor = l=>({100:"var(--l100)",200:"var(--l200)",300:"var(--l300)",400:"var(--l400)"}[l]||"#555");
const gradColors={"Core":"#3a7bd5","MMSC electives":"#c0556a","CPPH electives":"#2bb3a3","Shared electives":"#c98a2b","Thesis & directed":"#7c5cff","Other":"#555"};
const gradColor = g=>gradColors[g]||"#555";
const sevRank = {hi:0,med:1,low:2};
const isGrad = ()=>state.program==="grad";

function setFor(yr){ return isGrad()? DATA.grad[yr] : DATA[yr]; }
function newCodes(){ // primaries present in 26/27 but not 25/26 (within current program)
  const a=new Set(setFor("2025/2026").map(c=>c.primary));
  return new Set(setFor("2026/2027").filter(c=>!a.has(c.primary)).map(c=>c.primary));
}
let NEW = newCodes();

function courses(){return setFor(state.year);}
function topSev(c){ if(!c.issues.length) return null;
  return c.issues.slice().sort((x,y)=>sevRank[x.sev]-sevRank[y.sev])[0].sev; }

function renderStats(list){
  const withIssues=list.filter(c=>c.issues.length).length;
  const hi=list.reduce((n,c)=>n+c.issues.filter(i=>i.sev=="hi").length,0);
  const tot=list.reduce((n,c)=>n+c.issues.length,0);
  $("#stats").innerHTML=
    `<span><b>${list.length}</b> courses</span>`+
    `<span><b>${withIssues}</b> with flags</span>`+
    `<span><b>${tot}</b> course-level findings</span>`+
    `<span style="color:var(--hi)"><b>${hi}</b> high-severity</span>`;
}

// ---- instructor + status helpers (persisted via OV) ----
function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&quot;").replace(/"/g,"&quot;");}
function getInstr(code){return OV.instructors[code]||"";}
function setInstr(code,val){ if(val&&val.trim())OV.instructors[code]=val.trim(); else delete OV.instructors[code]; saveLocal(); }
function instructorHTML(code){
  const v=getInstr(code);
  if(state.edit){
    return `<div class="instr"><input type="text" placeholder="Type instructor name" value="${esc(v)}"
      oninput="setInstr('${code}',this.value)"></div>`;
  }
  return v? `<p>${esc(v)}</p>` : `<p class="placeholder">Not yet assigned &mdash; turn on Edit to add.</p>`;
}
const issueKey=(code,idx)=>code+"|"+idx;
function getStatus(k){return OV.status[k]||"";}
function setStatus(k,val){ if(val)OV.status[k]=val; else delete OV.status[k]; saveLocal(); rerender(); }
function statusControl(k){
  const cur=getStatus(k);
  if(state.edit){
    return `<select class="statusSel" onchange="setStatus('${k}',this.value)">
      <option value="" ${cur==""?"selected":""}>open</option>
      <option value="ack" ${cur=="ack"?"selected":""}>acknowledged</option>
      <option value="fixed" ${cur=="fixed"?"selected":""}>fixed</option>
      <option value="wontfix" ${cur=="wontfix"?"selected":""}>won't fix</option>
    </select>`;
  }
  return cur? `<span class="stbadge ${cur}">${cur=="wontfix"?"won't fix":cur}</span>` : "";
}

function cardHTML(c){
  const sev=topSev(c);
  const badges=[];
  if(NEW.has(c.primary)) badges.push(`<span class="dot new">NEW</span>`);
  if(sev) badges.push(`<span class="dot ${sev}">${c.issues.length}&nbsp;flag${c.issues.length>1?"s":""}</span>`);
  const xl = c.code.includes("/")?`<div class="xlist">cross-listed: ${c.code}</div>`:"";
  const instr=getInstr(c.primary);
  const instrLine = instr?`<div class="xlist" style="color:var(--mut)">&#128100; ${esc(instr)}</div>`:"";
  const stripe = isGrad()? gradColor(c.group) : lvlColor(c.level);
  const tag = isGrad()? c.group : (c.level+" level");
  return `<div class="card" data-code="${c.code}">
    <div class="lvl" style="background:${stripe}"></div>
    <div class="badges">${badges.join("")}</div>
    <h3>${c.primary}</h3>
    <div class="ttl">${c.title||"<span class='placeholder'>(untitled)</span>"}</div>
    <div class="meta"><span class="pill">${(c.credit||"?").replace(' Credit','&nbsp;cr')}</span>
      <span class="pill">${c.term||"term n/s"}</span>
      <span class="pill">${tag}</span></div>
    ${xl}${instrLine}
    <a class="cardlink" href="${c.url}" target="_blank" rel="noopener" onclick="event.stopPropagation()">calendar &#8599;</a>
  </div>`;
}

function miniHTML(c){
  const sev=topSev(c);
  const flag = sev=="hi"?" flag-hi":(sev=="med"?" flag-med":"");
  const ni = NEW.has(c.primary)?`<span class="ni" title="New in 2026/27"></span>`:"";
  return `<div class="minibox${flag}" data-code="${c.code}" title="${(c.title||'').replace(/"/g,'&quot;')}">${c.primary}${ni}</div>`;
}
function colHTML(label,color,items){
  const empty = items.length?"":" empty";
  return `<div class="col${empty}">
    <div class="col-h"><span class="swatch" style="background:${color}"></span>
      <b>${label}</b><span class="ct">${items.length}</span></div>
    <div class="boxes">${items.map(miniHTML).join("")||'<span class="placeholder" style="font-size:12px">none</span>'}</div>
  </div>`;
}
// grouping abstraction for the collapsed view (level for UG, curriculum role for grad)
function grouping(){
  if(isGrad()) return {order:DATA.gradGroupOrder, of:c=>c.group, label:g=>g, color:gradColor};
  const levels = state.lvl!=="all" ? [+state.lvl] : [100,200,300,400];
  return {order:levels, of:c=>c.level, label:L=>L+" level", color:lvlColor};
}
function renderGrid(){
  let list=courses().slice();
  if(!isGrad() && state.lvl!=="all") list=list.filter(c=>c.level==+state.lvl);
  if(state.issuesOnly) list=list.filter(c=>c.issues.length);
  if(state.newOnly) list=list.filter(c=>NEW.has(c.primary));
  if(state.q){const q=state.q.toLowerCase();
    list=list.filter(c=>(c.code+" "+c.title+" "+c.description).toLowerCase().includes(q));}
  list.sort((a,b)=>a.level-b.level || a.primary.localeCompare(b.primary));
  renderStats(courses());
  if(state.view==="collapsed"){
    const g=grouping();
    const cols = g.order.map(k=>colHTML(g.label(k), g.color(k), list.filter(c=>g.of(c)===k)));
    $("#grid").innerHTML=`<div class="cols">${cols.join("")}</div>`;
  } else {
    $("#grid").innerHTML=`<div class="grid-cards">${list.map(cardHTML).join("")}</div>`
      || `<div class="note">No courses match.</div>`;
  }
  document.querySelectorAll("[data-code]").forEach(el=>el.onclick=()=>openModal(el.dataset.code));
}

function reqLine(label,val){
  if(!val) return "";
  // highlight known dangling internal refs
  const danglers=["HE302","HE434","HE211","KP2222"];
  let html=val;
  danglers.forEach(d=>{html=html.replace(new RegExp("\\b"+d+"\\b","g"),
    `<span class="refcode dangling" title="No course entry / typo">${d}</span>`);});
  return `<div class="sec req"><h4>${label}</h4><p>${html}</p></div>`;
}

function openModal(code){
  const c=courses().find(x=>x.code===code); if(!c)return;
  const r=c.requirements||{};
  const issues=c.issues.map((i,idx)=>({...i,__k:issueKey(c.primary,idx)})).sort((a,b)=>sevRank[a.sev]-sevRank[b.sev]);
  const issuesHTML=issues.length? issues.map(i=>{
    const st=getStatus(i.__k);
    return `<div class="issue ${i.sev}${st&&st!='ack'?' done':''}"><div class="tag"><b>${i.sev.toUpperCase()}</b> &middot; ${i.cat}${statusControl(i.__k)}</div>${i.msg}</div>`;
  }).join("")
    : `<p class="placeholder">No issues flagged for this course.</p>`;
  $("#modal").innerHTML=`
    <button class="x" onclick="closeModal()">Close &times;</button>
    <h2>${c.primary} ${NEW.has(c.primary)?'<span class="dot new" style="vertical-align:middle">NEW 26/27</span>':''}</h2>
    <div class="mttl">${c.title||"(untitled)"}</div>
    <a class="callink" href="${c.url}" target="_blank" rel="noopener">View on WLU calendar &#8599;</a>
    <div class="kv">
      <span class="pill">${c.credit||"credit n/s"}</span>
      <span class="pill">${c.term||"term not specified"}</span>
      <span class="pill">${isGrad()?c.group:(c.level+" level")}</span>
      ${c.code.includes("/")?`<span class="pill">cross-listed: ${c.code}</span>`:""}
    </div>
    ${isGrad()&&c.roles&&c.roles.length?`<div class="sec"><h4>Counts toward</h4><div style="display:flex;gap:6px;flex-wrap:wrap">${c.roles.map(r=>`<span class="rl">${r}</span>`).join("")}</div></div>`:""}
    <div class="sec"><h4>Description</h4>
      <p>${c.description? c.description : '<span class="placeholder">No description in the calendar.</span>'}</p></div>
    ${c.hours?`<div class="sec"><h4>Hours</h4><p>${c.hours}</p></div>`:""}
    ${reqLine("Prerequisites",r["Prerequisites"])}
    ${reqLine("Co-requisites",r["Co-requisites"])}
    ${reqLine("Exclusions",r["Exclusions"])}
    ${r["Notes"]?`<div class="sec"><h4>Notes</h4><p>${r["Notes"]}</p></div>`:""}
    <div class="sec"><h4>Instructor</h4>${instructorHTML(c.primary)}</div>
    <div class="sec"><h4>Syllabus</h4><p class="placeholder">Not yet linked (placeholder).</p></div>
    <div class="sec"><h4>Review findings (${issues.length})</h4>${issuesHTML}</div>
  `;
  $("#modal").classList.add("open"); $("#scrim").classList.add("open");
}
function closeModal(){$("#modal").classList.remove("open");$("#scrim").classList.remove("open");}
$("#scrim").onclick=closeModal;

function allIssueRows(){
  const rows=[];
  courses().forEach(c=>c.issues.forEach((i,idx)=>rows.push({code:c.primary,title:c.title,k:issueKey(c.primary,idx),...i})));
  if(isGrad()){
    DATA.gradProgramIssues.forEach((i,idx)=>rows.push({code:"MSc PROGRAM",title:"MSc structure",k:issueKey("GPROGRAM",idx),...i}));
  } else {
    DATA.programIssues.forEach((i,idx)=>rows.push({code:"PROGRAM",title:"Degree structure",k:issueKey("PROGRAM",idx),...i}));
    DATA.globalIssues.forEach((i,idx)=>rows.push({code:"GLOBAL",title:"Both years / site-wide",k:issueKey("GLOBAL",idx),...i}));
  }
  (DATA.facultyIssues||[]).forEach((i,idx)=>rows.push({code:"FACULTY",title:"Faculty roster",k:issueKey("FACULTY",idx),...i}));
  return rows;
}
function renderIssues(){
  const all=allIssueRows().sort((a,b)=>sevRank[a.sev]-sevRank[b.sev]);
  const open=all.filter(r=>{const s=getStatus(r.k);return s!=="fixed"&&s!=="wontfix";});
  const done=all.length-open.length;
  const groups={hi:[],med:[],low:[]}; all.forEach(r=>groups[r.sev].push(r));
  const names={hi:"High severity",med:"Medium severity",low:"Low severity / style"};
  let html=`<div class="note" style="margin-bottom:10px">${all.length} findings &middot; ${done} marked fixed/won't-fix &middot; ${all.length-done} open</div>`;
  ["hi","med","low"].forEach(s=>{
    if(!groups[s].length)return;
    html+=`<h3><span class="sevtag ${s}">${s.toUpperCase()}</span> ${names[s]} (${groups[s].length})</h3>`;
    groups[s].forEach(r=>{
      const st=getStatus(r.k);
      html+=`<div class="issue ${s}${st&&st!='ack'?' done':''}"><div class="tag"><b>${r.code}</b> &middot; ${r.cat}${r.title&&r.code.length<8?" &middot; "+r.title:""}${statusControl(r.k)}</div>${r.msg}</div>`;
    });
  });
  $("#issuesList").innerHTML=html;
}

function renderProgram(){
  const pIssues = isGrad()? DATA.gradProgramIssues : DATA.programIssues;
  const pText   = isGrad()? DATA.gradProgram[state.year] : DATA.program[state.year];
  const pUrl    = isGrad()? DATA.gradProgramUrl[state.year] : DATA.programUrl[state.year];
  const pi=pIssues.slice().sort((a,b)=>sevRank[a.sev]-sevRank[b.sev]);
  const coord = isGrad()? `<div class="note">Graduate Program Coordinator: ${DATA.gradCoordinator}. The MSc has two options (Thesis, Coursework) across two specializations (MMSC, CPPH).</div>` : "";
  $("#programIssues").innerHTML=coord+pi.map(i=>
    `<div class="issue ${i.sev}"><div class="tag"><b>${i.sev.toUpperCase()}</b> &middot; ${i.cat}</div>${i.msg}</div>`).join("");
  $("#progText").textContent=pText;
  $("#progLink").href=pUrl;
  $("#progLink").firstChild&&($("#progLink").innerHTML=(isGrad()?"Open MSc Health Sciences page on WLU calendar":"Open Honours BSc page on WLU calendar")+" &#8599;");
}

function renderFaculty(){
  const F=DATA.faculty||{listed:[],missing:[]};
  $("#facNote").textContent=F.note||"";
  const fi=(DATA.facultyIssues||[]).slice().sort((a,b)=>sevRank[a.sev]-sevRank[b.sev]);
  $("#facultyIssues").innerHTML=fi.map(i=>
    `<div class="issue ${i.sev}"><div class="tag"><b>${i.sev.toUpperCase()}</b> &middot; ${i.cat}</div>${i.msg}</div>`).join("");
  $("#facListed").innerHTML=F.listed.map(p=>
    `<div class="facrow col"><span class="nm">${p.name}</span>`+
    (p.cred?`<span class="rl">${p.cred}</span>`:"")+
    (p.role?`<span class="rl">${p.role}</span>`:"")+
    (p.flag?`<span class="lv">${p.flag}</span>`:"")+`</div>`).join("");
  $("#facMissing").innerHTML=F.missing.map(p=>{
    const chair=/chair/i.test(p.role||"");
    return `<div class="facrow miss col${chair?" chair":""}"><span class="nm">${p.name}</span>`+
    (p.role?`<span class="rl">${p.role}</span>`:"")+
    (p.note?`<div class="nt">${p.note}</div>`:"")+`</div>`;
  }).join("");
}

// ---- Prereq dependency map (SVG) ----
const INTERNAL=new Set(); // set of HE/HN primaries present this year
function buildMap(){
  const cs=courses();
  INTERNAL.clear(); cs.forEach(c=>INTERNAL.add(c.primary));
  const danglers={HE302:1,HE434:1,HE211:1};
  // nodes: internal courses + referenced danglers; edges: prereq internal code -> course
  const codeRe=/\b(HE|HN)\s?(\d{3})\b/g;
  const nodes={}; const edges=[];
  cs.forEach(c=>{ nodes[c.primary]={code:c.primary,level:c.level,title:c.title,real:true,full:c.code}; });
  cs.forEach(c=>{
    const pre=(c.requirements&&c.requirements["Prerequisites"])||"";
    let m; const seen=new Set();
    while((m=codeRe.exec(pre))){
      const ref=m[1]+m[2]; if(seen.has(ref))continue; seen.add(ref);
      if(ref===c.primary)continue;
      if(!nodes[ref]){
        if(danglers[ref]) nodes[ref]={code:ref,level:(+ref.match(/\d/) )*100,title:"(no course entry)",real:false};
        else continue; // skip external/non-mapped
      }
      edges.push({from:ref,to:c.primary,dang:!nodes[ref].real});
    }
  });
  return {nodes,edges};
}
function renderMap(){
  if(isGrad()){
    $("#mapWrap").innerHTML=`<div style="padding:22px" class="note">Graduate (MSc) courses do not list prerequisites - eligibility is governed by program option and specialization rather than a prerequisite chain. See the <b>Program structure</b> tab for the Thesis and Coursework pathways, and each course card's "Counts toward" badges.</div>`;
    return;
  }
  const {nodes,edges}=buildMap();
  const cols={100:[],200:[],300:[],400:[]};
  Object.values(nodes).forEach(n=>{const L=[100,200,300,400].includes(n.level)?n.level:100;cols[L].push(n);});
  const colX={100:40,200:260,300:480,400:700}, W=900, NW=150, NH=30, vgap=14, top=54;
  const pos={};
  [100,200,300,400].forEach(L=>{
    cols[L].sort((a,b)=>(a.real-b.real)||a.code.localeCompare(b.code));
    cols[L].forEach((n,i)=>{pos[n.code]={x:colX[L],y:top+i*(NH+vgap)};});
  });
  const maxRows=Math.max(...[100,200,300,400].map(L=>cols[L].length));
  const H=top+maxRows*(NH+vgap)+20;
  let svg=`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">`;
  [100,200,300,400].forEach(L=>{ svg+=`<text class="maplbl" x="${colX[L]}" y="30">${L} level</text>`; });
  edges.forEach(e=>{
    const a=pos[e.from],b=pos[e.to]; if(!a||!b)return;
    const x1=a.x+NW,y1=a.y+NH/2,x2=b.x,y2=b.y+NH/2,mx=(x1+x2)/2;
    svg+=`<path class="mapedge${e.dang?' dang':''}" d="M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}"/>`;
  });
  Object.values(nodes).forEach(n=>{
    const p=pos[n.code]; if(!p)return;
    svg+=`<g class="mapnode${n.real?'':' dangling'}" ${n.real?`data-code="${n.full}" style="cursor:pointer"`:''} transform="translate(${p.x},${p.y})">
      <rect width="${NW}" height="${NH}" rx="6"/><text x="9" y="${NH/2+4}">${n.code}${n.real?'':' &#9888;'}</text></g>`;
  });
  svg+=`</svg>`;
  $("#mapWrap").innerHTML=svg;
  document.querySelectorAll("#mapWrap .mapnode[data-code]").forEach(el=>el.onclick=()=>openModal(el.dataset.code));
}

// ---- Year diff 2025/26 -> 2026/27 ----
function renderDiff(){
  const A=setFor("2025/2026"), B=setFor("2026/2027");
  const byA={},byB={}; A.forEach(c=>byA[c.primary]=c); B.forEach(c=>byB[c.primary]=c);
  const added=B.filter(c=>!byA[c.primary]);
  const removed=A.filter(c=>!byB[c.primary]);
  const fld=c=>({title:c.title,pre:(c.requirements&&c.requirements["Prerequisites"])||"",exc:(c.requirements&&c.requirements["Exclusions"])||""});
  const changed=[];
  B.forEach(c=>{ const a=byA[c.primary]; if(!a)return; const x=fld(a),y=fld(c); const ch=[];
    if(x.title!==y.title)ch.push(["Title",x.title,y.title]);
    if(x.pre!==y.pre)ch.push(["Prerequisites",x.pre||"—",y.pre||"—"]);
    if(x.exc!==y.exc)ch.push(["Exclusions",x.exc||"—",y.exc||"—"]);
    if(ch.length)changed.push({code:c.primary,ch});
  });
  let h="";
  h+=`<div class="diffsec"><h3 class="diff-add">Added in 2026/27 (${added.length})</h3>`;
  h+= added.length? `<table class="difftbl"><tr><th>Code</th><th>Title</th></tr>`+
      added.map(c=>`<tr><td>${c.code}</td><td>${c.title||"&mdash;"}</td></tr>`).join("")+`</table>` : `<div class="note">None.</div>`;
  h+=`</div>`;
  h+=`<div class="diffsec"><h3 class="diff-del">Removed in 2026/27 (${removed.length})</h3>`;
  h+= removed.length? `<table class="difftbl"><tr><th>Code</th><th>Title</th></tr>`+
      removed.map(c=>`<tr><td>${c.code}</td><td>${c.title||"&mdash;"}</td></tr>`).join("")+`</table>` : `<div class="note">None.</div>`;
  h+=`</div>`;
  h+=`<div class="diffsec"><h3 class="diff-chg">Field changes (${changed.length} courses)</h3>`;
  h+= changed.length? `<table class="difftbl"><tr><th>Course</th><th>Field</th><th>2025/26</th><th>2026/27</th></tr>`+
      changed.map(d=>d.ch.map((row,i)=>`<tr>${i===0?`<td rowspan="${d.ch.length}"><b>${d.code}</b></td>`:""}<td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td></tr>`).join("")).join("")+`</table>`
      : `<div class="note">No title/prereq/exclusion changes among shared courses.</div>`;
  h+=`</div>`;
  const notFixed = isGrad()
    ? `The 2026/27 change was splitting admission requirements into separate thesis-stream and coursework-stream paragraphs. The 'optio n' and 'BSC' typos and the undefined HE699 asterisk persist unchanged in both years.`
    : `Every spelling, grammar, and dangling-reference issue from 2025/26 (HE302, HE434, HE211, the Year-4 list, the program-note typos) is reproduced unchanged in 2026/27.`;
  h+=`<div class="diffsec"><h3>Notable change / not fixed</h3><div class="issue med"><div class="tag"><b>${isGrad()?"MSc":"BSc"}</b></div>${notFixed}</div></div>`;
  $("#diffBody").innerHTML=h;
}

function setTab(t){
  state.tab=t;
  document.querySelectorAll(".tab").forEach(el=>el.classList.toggle("active",el.dataset.t===t));
  ["courses","issues","map","diff","program","faculty"].forEach(n=>
    $("#tab-"+n).classList.toggle("hidden",t!==n));
  if(t==="issues")renderIssues(); else if(t==="program")renderProgram();
  else if(t==="faculty")renderFaculty(); else if(t==="map")renderMap(); else if(t==="diff")renderDiff();
}
function rerender(){
  const t=state.tab;
  if(t==="courses")renderGrid(); else if(t==="issues")renderIssues();
  else if(t==="faculty")renderFaculty(); else if(t==="map")renderMap();
  else if(t==="diff")renderDiff(); else renderProgram();
}

// wire up
$("#tabs").onclick=e=>{if(e.target.dataset.t)setTab(e.target.dataset.t);};
$("#yearSeg").onclick=e=>{if(e.target.dataset.y){
  state.year=e.target.dataset.y;
  document.querySelectorAll("#yearSeg button").forEach(b=>b.classList.toggle("on",b.dataset.y===state.year));
  rerender();}};
$("#progSeg").onclick=e=>{if(e.target.dataset.p){
  state.program=e.target.dataset.p;
  document.querySelectorAll("#progSeg button").forEach(b=>b.classList.toggle("on",b.dataset.p===state.program));
  document.body.classList.toggle("gradmode", isGrad());
  state.lvl="all"; document.querySelectorAll(".lvl-chip").forEach(x=>x.classList.toggle("on",x.dataset.lvl==="all"));
  NEW=newCodes();
  rerender();}};
function setView(v){
  state.view=v;
  document.querySelectorAll("#viewSeg button").forEach(b=>b.classList.toggle("on",b.dataset.v===v));
  renderGrid();
}
$("#viewSeg").onclick=e=>{if(e.target.dataset.v){clearTimeout(autoCollapse);setView(e.target.dataset.v);}};
document.querySelectorAll(".lvl-chip").forEach(ch=>ch.onclick=()=>{
  state.lvl=ch.dataset.lvl;
  document.querySelectorAll(".lvl-chip").forEach(x=>x.classList.toggle("on",x===ch));
  renderGrid();});
$("#issuesOnly").onclick=function(){state.issuesOnly=!state.issuesOnly;this.classList.toggle("on",state.issuesOnly);renderGrid();};
$("#newOnly").onclick=function(){state.newOnly=!state.newOnly;this.classList.toggle("on",state.newOnly);renderGrid();};
$("#search").oninput=e=>{state.q=e.target.value;renderGrid();};
$("#editBtn").onclick=function(){
  state.edit=!state.edit; this.classList.toggle("on",state.edit);
  this.innerHTML = state.edit? "&#9998; Editing… (click to finish)" : "&#9998; Edit";
  // if a modal is open, re-render it so instructor field switches mode
  if($("#modal").classList.contains("open")){const code=$("#modal h2")?.textContent.trim().split(" ")[0];
    const c=courses().find(x=>x.primary===code); if(c)openModal(c.code);}
  rerender();
};
$("#exportBtn").onclick=function(){
  const out={_comment:"Committable overrides layer. Replace overrides.json in the repo with this file.",
    instructors:OV.instructors, status:OV.status};
  const blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download="overrides.json"; a.click();
};
document.onkeydown=e=>{if(e.key==="Escape")closeModal();};

// ---- init: merge committed overrides (runtime fetch) over inlined fallback, then render ----
let autoCollapse=null;
function boot(){
  renderGrid();
  autoCollapse=setTimeout(()=>{ if(state.view==="expanded" && state.tab==="courses") setView("collapsed"); },2000);
}
mergeOverrides(null); // inlined + localStorage first (works offline / file://)
boot();                // paint immediately
fetch("overrides.json",{cache:"no-store"}).then(r=>r.ok?r.json():null).then(remote=>{
  if(remote){ mergeOverrides(remote); rerender(); }   // upgrade to committed layer when served over http
}).catch(()=>{});
</script>
</body>
</html>"""

ov_raw = json.load(open(os.path.join(base,"overrides.json"), encoding="utf-8"))
ov = {"instructors": ov_raw.get("instructors",{}), "status": ov_raw.get("status",{})}
out = HTML.replace("__PAYLOAD__", payload).replace("__OVERRIDES__", json.dumps(ov, ensure_ascii=False))
open(os.path.join(base,"index.html"),"w",encoding="utf-8").write(out)
print("wrote index.html", len(out), "bytes")
