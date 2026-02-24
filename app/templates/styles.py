"""app/templates/styles.py — premium CSS (fix pass: spacing, animations, quit button)."""

CSS = """
/* ── FONTS ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
:root {
  --bg:#030609; --bg2:#070c15; --panel:#0b1020;
  --panel2:#0e1528; --glass:rgba(11,16,32,0.88);
  --border:#162040; --border2:#1e2f5a; --border3:#2e4580;
  --cyan:#00f5ff; --cyan2:#00c8d4; --cyan3:#005a66;
  --green:#39ff14; --green2:#2dd10f; --green3:#1a7a0a;
  --yellow:#ffe600; --orange:#ff8c00; --orange2:#cc6f00;
  --red:#ff2244; --red2:#cc1133; --purple:#bf5fff; --purple2:#8833cc;
  --white:#e8f4ff; --dim:#3a5070; --mid:#6a8caa; --light:#9ab8d0;
  --gold:#ffd700; --gold2:#b8a000;
  --font-game:'Orbitron','Arial Black',Arial,sans-serif;
  --font-mono:'Share Tech Mono','Courier New',monospace;
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  font-family: var(--font-mono);
  background: #030609;
  color: var(--white);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── CANVAS BACKGROUND ───────────────────────────────────────── */
#bgcanvas {
  position: fixed; inset: 0; z-index: 0;
  pointer-events: none; width: 100vw; height: 100vh;
}

/* ── CRT SCANLINES ───────────────────────────────────────────── */
body::after {
  content:''; position:fixed; inset:0; z-index:9997; pointer-events:none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(0,0,0,.04) 3px, rgba(0,0,0,.04) 4px
  );
  animation: scanroll 12s linear infinite;
}
@keyframes scanroll {
  0% { background-position: 0 0; }
  100% { background-position: 0 400px; }
}

/* ── PAGE ENTER ANIMATION ────────────────────────────────────── */
.page-enter {
  animation: pageEnter 0.5s cubic-bezier(0.4, 0, 0.2, 1) both;
}
@keyframes pageEnter {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── HUD ─────────────────────────────────────────────────────── */
.hud {
  position:fixed; top:0; left:0; right:0; z-index:1000;
  background: rgba(3,6,9,.96);
  border-bottom: 1px solid var(--border2);
  box-shadow: 0 2px 20px rgba(0,0,0,.5), 0 1px 0 rgba(0,245,255,.1);
  padding: 10px 18px;
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.hud-logo {
  font-family: var(--font-game); font-size:11px; color:var(--cyan);
  letter-spacing:4px; flex-shrink:0; font-weight:900;
  text-shadow: 0 0 14px rgba(0,245,255,.6);
}
.hud-div { color:var(--border2); font-size:16px; flex-shrink:0; }
.hud-lvl {
  font-family: var(--font-game); font-size:10px;
  background: linear-gradient(135deg,var(--yellow),var(--orange));
  color: var(--bg); padding:5px 11px; border-radius:4px;
  font-weight:900; white-space:nowrap; flex-shrink:0;
  box-shadow: 0 0 12px rgba(255,200,0,.3);
}
.xp-wrap { display:flex; align-items:center; gap:8px; flex:1; min-width:180px; }
.xp-lbl  { font-size:10px; color:var(--yellow); white-space:nowrap; letter-spacing:1px; flex-shrink:0; }
.xp-bar  { flex:1; height:10px; background:var(--border); border-radius:5px; overflow:hidden; min-width:80px; position:relative; }
.xp-fill {
  height:100%; border-radius:5px; transition:width .7s cubic-bezier(.4,0,.2,1);
  background: linear-gradient(90deg,var(--yellow),var(--orange));
  box-shadow: 0 0 12px rgba(255,200,0,.5);
  position:relative; overflow:hidden;
}
.xp-fill::after {
  content:''; position:absolute; inset:0;
  background: linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);
  animation: shimmer 2s infinite;
}
@keyframes shimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }
.xp-num { font-size:10px; color:var(--yellow); white-space:nowrap; letter-spacing:.5px; flex-shrink:0; }
.hp-wrap  { display:flex; align-items:center; gap:5px; flex-shrink:0; }
.hp-lbl   { font-size:10px; color:var(--red); letter-spacing:1px; }
.hearts   { display:flex; gap:3px; }
.ht       { font-size:15px; transition:all .4s; filter:drop-shadow(0 0 5px rgba(255,50,80,.7)); }
.ht.dead  { filter:grayscale(1) brightness(.2); transform:scale(.8); }
.streak-wrap { display:flex; align-items:center; gap:4px; flex-shrink:0; }
.streak-lbl  { font-size:12px; }
.streak-num  {
  font-family:var(--font-game); font-size:11px; color:var(--orange);
  min-width:22px; text-align:center; font-weight:900;
  transition: all .2s;
}
.streak-num.bump { animation: streakbump .3s ease; }
@keyframes streakbump { 0%{transform:scale(1)} 50%{transform:scale(1.6)} 100%{transform:scale(1)} }
.badges  { display:flex; gap:4px; flex-wrap:wrap; flex-shrink:0; }
.bdg        { font-size:17px; transition:all .3s; cursor:help; }
.bdg.locked { filter:grayscale(1) brightness(.25); }
.bdg:not(.locked) { filter:drop-shadow(0 0 5px var(--yellow)); }
.hud-quit {
  font-family:var(--font-game); font-size:10px; color:var(--mid);
  background:rgba(255,34,68,.05); border:1px solid rgba(255,34,68,.2);
  padding:6px 14px; cursor:pointer; border-radius:3px; text-decoration:none;
  transition:all .15s; letter-spacing:1px;
  display:inline-flex; align-items:center; gap:5px;
  text-decoration:none; flex-shrink:0; white-space:nowrap;
}
.hud-quit:hover { background:rgba(255,34,68,.15); border-color:var(--red); color:var(--red); }

/* ── BUTTONS ─────────────────────────────────────────────────── */
.btn-primary {
  font-family: var(--font-game);
  font-size: clamp(9px,1.8vw,11px);
  color: var(--bg); background: var(--cyan);
  border: none; padding: 18px 50px; border-radius: 5px;
  cursor: pointer; letter-spacing: 3px; font-weight: 900;
  box-shadow: 0 0 32px rgba(0,245,255,.5), 0 4px 0 var(--cyan2);
  transition: transform .12s, box-shadow .12s;
  display: inline-block; text-decoration: none;
  animation: pulse-start 2.5s ease-in-out infinite;
  position: relative; overflow: hidden;
}
.btn-primary::before {
  content:''; position:absolute; top:-50%; left:-60%;
  width:40%; height:200%;
  background: linear-gradient(105deg,transparent,rgba(255,255,255,.3),transparent);
  animation: btnshine 3.5s ease-in-out infinite;
}
@keyframes btnshine { 0%,100%{left:-60%} 45%,55%{left:120%} }
.btn-primary:hover  { transform:translateY(-4px); box-shadow:0 0 60px rgba(0,245,255,.9),0 8px 0 var(--cyan2); }
.btn-primary:active { transform:translateY(2px);  box-shadow:0 0 18px rgba(0,245,255,.4),0 1px 0 var(--cyan2); }
@keyframes pulse-start {
  0%,100%{box-shadow:0 0 32px rgba(0,245,255,.5),0 4px 0 var(--cyan2);}
  50%    {box-shadow:0 0 70px rgba(0,245,255,.95),0 4px 0 var(--cyan2),0 0 120px rgba(0,245,255,.15);}
}
.btn-green {
  font-family: var(--font-game); font-size:10px; color:var(--bg);
  background: linear-gradient(135deg,var(--green),var(--green2));
  border: none; padding:15px 34px; border-radius:5px; cursor:pointer;
  letter-spacing:2px; font-weight:900;
  box-shadow: 0 4px 0 var(--green3), 0 0 26px rgba(57,255,20,.4);
  transition: all .12s; display:inline-block; text-decoration:none;
}
.btn-green:hover  { transform:translateY(-3px); box-shadow:0 7px 0 var(--green3),0 0 50px rgba(57,255,20,.7); }
.btn-green:active { transform:translateY(2px); box-shadow:0 2px 0 var(--green3); }
.btn-yellow {
  font-family: var(--font-game); font-size:9px; color:var(--bg);
  background: linear-gradient(135deg,var(--yellow),var(--orange));
  border:none; padding:14px 28px; border-radius:5px; cursor:pointer;
  letter-spacing:2px; font-weight:900;
  box-shadow:0 4px 0 var(--gold2); display:inline-block; text-decoration:none;
}
.btn-yellow:hover { transform:translateY(-2px); box-shadow:0 6px 0 var(--gold2),0 0 22px rgba(255,230,0,.4); }
.btn-back {
  font-family: var(--font-game); font-size:7px; color:var(--cyan);
  background:rgba(0,245,255,.05); border:1px solid rgba(0,245,255,.25);
  padding:8px 16px; cursor:pointer; border-radius:4px;
  transition:all .15s; letter-spacing:1px;
  display:inline-block; text-decoration:none;
}
.btn-back:hover { background:rgba(0,245,255,.12); border-color:var(--cyan); box-shadow:0 0 12px rgba(0,245,255,.2); }

/* ── PAGE WRAPPER ────────────────────────────────────────────── */
.page { position:relative; z-index:1; min-height:100vh; }

/* ── LAYOUT ──────────────────────────────────────────────────── */
.wrap { max-width:760px; margin:0 auto; padding:30px 22px 120px; position:relative; z-index:1; }
.blk  { margin-bottom:32px; }
.mission-hdr {
  display:flex; align-items:center; gap:14px; margin-bottom:40px;
  flex-wrap:wrap; padding-top:88px;
}
.mission-num {
  font-family:var(--font-game); font-size:7px; color:var(--dim);
  letter-spacing:3px;
}
.mission-name {
  font-family:var(--font-game); font-size:clamp(14px,2.5vw,22px); color:var(--cyan);
  letter-spacing:1px; text-shadow:0 0 20px rgba(0,245,255,.35);
}

/* ── CONTENT BLOCKS ──────────────────────────────────────────── */
.cutscene {
  background: linear-gradient(135deg,rgba(8,13,24,.95),rgba(12,18,36,.95));
  border: 1px solid var(--border2);
  border-left: 3px solid var(--cyan);
  border-radius: 0 12px 12px 0;
  padding: 24px 28px; font-size:14.5px; color:var(--mid);
  line-height: 2.1; position:relative; overflow:hidden;
  animation: slideInLeft .45s cubic-bezier(.4,0,.2,1) both;
}
@keyframes slideInLeft { from{opacity:0;transform:translateX(-30px)} to{opacity:1;transform:translateX(0)} }
.cutscene::before {
  content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg,var(--cyan),transparent);
  opacity:.6;
}
.spkr {
  font-family:var(--font-game); font-size:7px; color:var(--cyan);
  letter-spacing:3px; margin-bottom:14px; display:block;
  font-weight:900; text-shadow:0 0 8px rgba(0,245,255,.5);
}
.cutscene em { color:var(--cyan); font-style:normal; font-weight:bold; }
.cutscene u  { color:var(--yellow); text-decoration:none; }

/* ── TYPEWRITER CURSOR ───────────────────────────────────────── */
.tw-cursor {
  display:inline-block; width:2px; height:1em;
  background:var(--cyan); vertical-align:text-bottom;
  animation:blink .7s step-end infinite;
  margin-left:2px;
}
@keyframes blink { 50%{opacity:0} }

/* ── CARDS ───────────────────────────────────────────────────── */
.card {
  background: linear-gradient(135deg,var(--panel),var(--panel2));
  border: 1px solid var(--border2); border-radius: 12px;
  padding: 26px 28px;
  box-shadow: 0 4px 20px rgba(0,0,0,.3);
  transition: border-color .25s, box-shadow .25s, transform .25s;
  animation: cardIn .4s cubic-bezier(.4,0,.2,1) both;
}
@keyframes cardIn { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.card:hover { border-color:var(--border3); box-shadow:0 8px 32px rgba(0,245,255,.07); transform:translateY(-2px); }
.card-lbl {
  font-family:var(--font-game); font-size:7px; color:var(--purple);
  letter-spacing:3px; margin-bottom:14px; display:block; font-weight:900;
}
.card h3  { font-family:var(--font-game); font-size:1rem; color:var(--white); margin-bottom:16px; }
.card p   { font-size:14px; color:var(--mid); line-height:2; margin-bottom:14px; }
.card p:last-child { margin-bottom:0; }
.card strong { color:var(--light); }
.hl   { color:var(--cyan); }
.rule {
  background: rgba(0,245,255,.05); border: 1px solid rgba(0,245,255,.2);
  border-radius: 6px; padding: 12px 16px; color: var(--cyan) !important;
  margin-top:6px;
}
.section-hdr {
  font-family:var(--font-game); font-size:7px; color:var(--dim);
  letter-spacing:4px; margin-bottom:18px; font-weight:900;
}
.scroll-hint {
  font-size:8px; color:var(--dim); text-align:center;
  letter-spacing:2px; margin-top:28px;
  animation:blink 1.5s step-end infinite;
}

/* ── PIPELINE VISUAL ─────────────────────────────────────────── */
.pipe-visual {
  background: var(--bg2); border:1px solid var(--border);
  border-radius:12px; padding:26px; overflow-x:auto;
}
.pipe-label { font-family:var(--font-game); font-size:7px; color:var(--dim); letter-spacing:3px; margin-bottom:20px; font-weight:900; }
.pipe-row   { display:flex; align-items:center; min-width:560px; }
.pipe-stage {
  flex:1; padding:14px 8px; text-align:center; border-radius:8px;
  font-size:12px; font-weight:bold; line-height:1.5; transition:all .35s;
}
.pipe-stage.active { transform:translateY(-6px); box-shadow:0 10px 24px rgba(0,0,0,.5); }
.pipe-stage small { display:block; font-weight:normal; opacity:.6; font-size:10px; margin-top:5px; }
.ps-cpu  { background:rgba(0,245,255,.09); border:1px solid rgba(0,245,255,.25); color:var(--cyan); }
.ps-cpu.active  { background:rgba(0,245,255,.2); box-shadow:0 0 24px rgba(0,245,255,.35); }
.ps-wait { background:rgba(255,34,68,.06); border:1px dashed rgba(255,34,68,.25); color:var(--red); font-style:italic; }
.ps-gpu  { background:rgba(57,255,20,.07); border:1px solid rgba(57,255,20,.25); color:var(--green); }
.ps-gpu.active  { background:rgba(57,255,20,.18); box-shadow:0 0 24px rgba(57,255,20,.35); }
.ps-disp { background:rgba(255,140,0,.09); border:1px solid rgba(255,140,0,.25); color:var(--orange); }
.ps-disp.active { background:rgba(255,140,0,.2); box-shadow:0 0 24px rgba(255,140,0,.35); }
.pipe-arr { width:22px; text-align:center; color:var(--border2); font-size:14px; flex-shrink:0; }
.pipe-legend { margin-top:16px; font-size:12.5px; color:var(--dim); line-height:2.4; }

/* ── METRIC GRID ─────────────────────────────────────────────── */
.metric-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:12px; }
.mc {
  background: var(--bg2); border:1px solid var(--border);
  border-radius:10px; padding:18px; transition:all .25s; cursor:default;
}
.mc:hover { border-color:var(--cyan); transform:translateY(-3px); box-shadow:0 10px 24px rgba(0,245,255,.09); }
.mc.cpu  { border-top:3px solid var(--cyan); }
.mc.gpu  { border-top:3px solid var(--green); }
.mc.disp { border-top:3px solid var(--orange); }
.mc.lat  { border-top:3px solid var(--yellow); }
.mc-name  { font-family:var(--font-game); font-size:11px; color:var(--white); margin-bottom:6px; font-weight:700; }
.mc-plain { font-size:12px; color:var(--cyan); margin-bottom:10px; font-style:italic; }
.mc-desc  { font-size:12.5px; color:var(--mid); line-height:1.75; margin-bottom:10px; }
.mc-ranges{ display:flex; flex-wrap:wrap; gap:5px; }
.rt { font-size:7px; padding:3px 8px; border-radius:3px; font-weight:bold; letter-spacing:.5px; }
.rg { background:rgba(57,255,20,.10); color:var(--green); }
.rr { background:rgba(255,34,68,.10); color:var(--red); }
.ry { background:rgba(255,230,0,.08); color:var(--yellow); }

/* ── PRESENT MODE TABLE ──────────────────────────────────────── */
.mode-tbl { width:100%; border-collapse:collapse; font-size:12.5px; }
.mode-tbl th {
  font-family:var(--font-game); font-size:7px; color:var(--dim);
  letter-spacing:2px; padding:12px 14px; text-align:left;
  border-bottom:1px solid var(--border); text-transform:uppercase; font-weight:900;
}
.mode-tbl td { padding:12px 14px; border-bottom:1px solid rgba(26,42,80,.4); color:var(--mid); vertical-align:top; line-height:1.6; }
.mode-tbl tr:last-child td { border-bottom:none; }
.mode-tbl tr:hover td { background:rgba(0,245,255,.03); }
.mm { font-family:var(--font-mono); color:var(--cyan); font-size:11px; font-weight:bold; }
.pb { font-family:var(--font-game); font-size:7px; padding:3px 8px; border-radius:3px; font-weight:900; letter-spacing:.5px; }
.pb-best { background:rgba(57,255,20,.12); color:var(--green); }
.pb-good { background:rgba(0,245,255,.10); color:var(--cyan); }
.pb-ok   { background:rgba(255,230,0,.08); color:var(--yellow); }
.pb-bad  { background:rgba(255,34,68,.10); color:var(--red); }

/* ── SCENARIO BLOCKS ─────────────────────────────────────────── */
.scenario {
  background: linear-gradient(135deg,var(--panel),var(--panel2));
  border:1px solid var(--border2); border-radius:12px;
  padding:22px; transition:all .25s;
}
.scenario:hover { border-color:var(--border3); box-shadow:0 6px 24px rgba(0,0,0,.3); }
.sc-head   { display:flex; gap:14px; align-items:flex-start; margin-bottom:14px; }
.sc-em     { font-size:32px; flex-shrink:0; filter:drop-shadow(0 0 10px rgba(255,255,255,.2)); }
.sc-title  { font-family:var(--font-game); font-size:.9rem; color:var(--white); font-weight:700; }
.sc-sub    { font-size:12px; color:var(--dim); margin-top:4px; letter-spacing:.5px; }
.sc-signs  { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:13px; }
.sign      { font-size:12px; padding:4px 10px; border-radius:5px; border:1px solid; }
.sign.bad  { background:rgba(255,34,68,.08); color:#ff8899; border-color:rgba(255,34,68,.2); }
.sign.ok   { background:rgba(0,245,255,.06); color:var(--cyan); border-color:rgba(0,245,255,.2); }
.sign.good { background:rgba(57,255,20,.07); color:var(--green); border-color:rgba(57,255,20,.2); }
.sc-fix {
  background:var(--bg2); border-left:3px solid var(--cyan);
  border-radius:0 8px 8px 0; padding:14px 18px;
  font-size:13.5px; color:var(--mid); line-height:1.9;
}
.sc-fix strong { color:var(--cyan); }

/* ── CODE BLOCK ──────────────────────────────────────────────── */
.codeblock { background:#010304; border:1px solid var(--border); border-radius:10px; padding:20px 22px; overflow-x:auto; }
.codeblock pre { font-size:13px; color:var(--mid); line-height:2.2; }
.ck { color:var(--cyan); } .cv { color:var(--green); }
.cf { color:var(--orange); } .cm { color:var(--dim); }

/* ── PERCENTILE CARDS ────────────────────────────────────────── */
.pct-row  { display:flex; gap:12px; flex-wrap:wrap; }
.pct-card {
  flex:1; min-width:120px;
  background: linear-gradient(135deg,var(--panel),var(--panel2));
  border:1px solid var(--border); border-radius:14px;
  padding:20px 14px; text-align:center; transition:all .25s;
}
.pct-card:hover { transform:translateY(-4px); border-color:var(--border3); }
.pct-num  { font-family:var(--font-game); font-size:2rem; font-weight:900; line-height:1; margin-bottom:7px; }
.pct-name { font-family:var(--font-game); font-size:8px; color:var(--dim); margin-bottom:9px; font-weight:700; letter-spacing:1px; }
.pct-desc { font-size:12px; color:var(--mid); line-height:1.55; }

/* ── BOSS BATTLE ─────────────────────────────────────────────── */
.boss-arena {
  background: linear-gradient(135deg,rgba(15,5,5,.97),rgba(22,8,8,.97));
  border: 2px solid var(--yellow);
  border-radius: 14px; padding: 28px;
  position:relative;
  box-shadow: 0 0 60px rgba(255,180,0,.08), inset 0 0 80px rgba(255,50,20,.03);
  animation: bossaura 3.5s ease-in-out infinite;
}
@keyframes bossaura {
  0%,100%{box-shadow:0 0 40px rgba(255,200,0,.07),inset 0 0 80px rgba(255,50,20,.02);}
  50%    {box-shadow:0 0 80px rgba(255,200,0,.14),inset 0 0 80px rgba(255,50,20,.06);}
}
.boss-arena::before {
  content:'⚔ BOSS BATTLE';
  font-family:var(--font-game); font-size:8px; color:var(--yellow);
  position:absolute; top:-12px; left:18px;
  background:var(--bg); padding:0 12px;
  letter-spacing:3px; font-weight:900;
  text-shadow:0 0 12px rgba(255,200,0,.7);
}
.boss-hdr  { display:flex; align-items:center; gap:20px; margin-bottom:24px; }
.boss-em   {
  font-size:50px; flex-shrink:0;
  animation: bossFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 0 16px rgba(255,100,50,.5));
}
@keyframes bossFloat { 0%,100%{transform:translateY(0) rotate(-2deg)} 50%{transform:translateY(-10px) rotate(2deg)} }
.boss-name { font-family:var(--font-game); font-size:1.1rem; color:var(--yellow); font-weight:900; text-shadow:0 0 18px rgba(255,220,0,.5); }
.boss-sub  { font-size:12.5px; color:var(--dim); margin-top:5px; }
.boss-hp-wrap { margin-top:12px; }
.boss-hp-lbl { font-family:var(--font-game); font-size:7px; color:var(--red); letter-spacing:2px; margin-bottom:5px; }
.boss-hpbg   { height:12px; background:var(--border); border-radius:6px; overflow:hidden; }
.boss-hpfill {
  height:100%; border-radius:6px;
  background: linear-gradient(90deg,var(--red),var(--orange),var(--yellow));
  transition: width .6s cubic-bezier(.4,0,.2,1);
  box-shadow: 0 0 14px rgba(255,100,30,.6);
}

/* ── QUIZ ────────────────────────────────────────────────────── */
.quiz-timer-wrap { display:flex; align-items:center; gap:10px; margin-bottom:18px; }
.quiz-timer-lbl  { font-family:var(--font-game); font-size:7px; color:var(--dim); letter-spacing:2px; flex-shrink:0; }
.quiz-timer-bar  { flex:1; height:7px; background:var(--border); border-radius:4px; overflow:hidden; }
.quiz-timer-fill {
  height:100%; border-radius:4px;
  background:linear-gradient(90deg,var(--green),var(--yellow),var(--orange),var(--red));
  transition:width .9s linear;
  box-shadow:0 0 8px rgba(57,255,20,.4);
}
.quiz-timer-num  { font-family:var(--font-game); font-size:10px; color:var(--cyan); min-width:28px; text-align:right; flex-shrink:0; }
.q-txt {
  font-family:var(--font-game); font-size:14px; color:var(--white);
  margin-bottom:20px; line-height:1.7;
}
.q-opts { display:flex; flex-direction:column; gap:10px; }
.qbtn {
  background: rgba(8,14,26,.85); border:1px solid var(--border2);
  border-radius:10px; padding:15px 18px;
  font-size:13.5px; color:var(--mid); cursor:pointer;
  transition: all .18s cubic-bezier(.4,0,.2,1);
  text-align:left; display:flex; align-items:center; gap:14px;
  font-family:var(--font-mono); width:100%;
  animation: qslide .35s ease both;
}
.qbtn:nth-child(1){animation-delay:.06s}
.qbtn:nth-child(2){animation-delay:.12s}
.qbtn:nth-child(3){animation-delay:.18s}
.qbtn:nth-child(4){animation-delay:.24s}
@keyframes qslide { from{opacity:0;transform:translateX(-24px)} to{opacity:1;transform:translateX(0)} }
.qbtn:hover:not(.done) {
  border-color:var(--cyan); color:var(--white);
  background:rgba(0,245,255,.08);
  transform:translateX(6px);
  box-shadow:0 2px 16px rgba(0,245,255,.12);
}
.qbtn.done { cursor:not-allowed; }
.qbtn.ok   { border-color:var(--green)!important; background:rgba(57,255,20,.1)!important; color:var(--green)!important; box-shadow:0 0 20px rgba(57,255,20,.2)!important; }
.qbtn.bad  { border-color:var(--red)!important;   background:rgba(255,34,68,.08)!important; color:var(--red)!important; }
.qkey {
  font-family:var(--font-game); font-size:8px; width:24px; height:24px;
  border-radius:4px; display:flex; align-items:center; justify-content:center;
  border:1px solid var(--border); flex-shrink:0; color:var(--dim); font-weight:900;
  transition:all .15s;
}
.qbtn:hover:not(.done) .qkey { border-color:var(--cyan); color:var(--cyan); }
.qbtn.ok .qkey  { border-color:var(--green); color:var(--green); background:rgba(57,255,20,.1); }
.qbtn.bad .qkey { border-color:var(--red);   color:var(--red); }
.qfb      { margin-top:18px; padding:16px 20px; border-radius:10px; font-size:13.5px; line-height:1.9; display:none; }
.qfb.win  { display:block; background:rgba(57,255,20,.07); border:1px solid rgba(57,255,20,.25); color:var(--green); animation:fadeUp .4s ease; }
.qfb.lose { display:block; background:rgba(255,34,68,.07); border:1px solid rgba(255,34,68,.25); color:#ff8899; animation:fadeUp .4s ease; }
.qfb .fun-fact { margin-top:11px; padding-top:11px; border-top:1px solid rgba(255,255,255,.07); font-size:12.5px; color:var(--mid); font-style:italic; }
.hint-box {
  display:none; margin-top:12px; padding:12px 18px;
  background:rgba(255,140,0,.06); border:1px solid rgba(255,140,0,.2);
  border-radius:8px; font-size:13px; color:var(--orange); line-height:1.8;
  animation:fadeUp .4s ease;
}
.hint-box.show { display:block; }
.hint-lbl { font-family:var(--font-game); font-size:7px; letter-spacing:2px; margin-bottom:6px; display:block; }

/* ── NEXT MISSION BANNER ─────────────────────────────────────── */
.next-banner { display:none; margin-top:28px; text-align:center; }
.next-banner.show { display:block; animation:fadeUp .5s ease; }
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

/* ── MISSION MAP ─────────────────────────────────────────────── */
.map-wrap { max-width:980px; margin:0 auto; padding:96px 22px 90px; position:relative; z-index:1; }
.map-title {
  font-family:var(--font-game); font-size:clamp(13px,2.5vw,24px);
  color:var(--cyan); text-align:center; letter-spacing:5px;
  margin-bottom:8px;
  text-shadow:0 0 32px rgba(0,245,255,.4);
}
.map-sub  { font-size:14px; color:var(--dim); text-align:center; margin-bottom:12px; }
.map-progress { text-align:center; margin-bottom:34px; }
.map-progress-bar { width:300px; height:7px; background:var(--border); border-radius:4px; overflow:hidden; margin:10px auto 0; }
.map-progress-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,var(--cyan),var(--green)); transition:width .7s; box-shadow:0 0 10px rgba(0,245,255,.4); }
.map-progress-lbl  { font-family:var(--font-game); font-size:8px; color:var(--cyan); letter-spacing:2px; }
.mgrid  { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:16px; }
.mcard  {
  background: linear-gradient(135deg,var(--panel),var(--panel2));
  border:2px solid var(--border); border-radius:12px;
  padding:22px 20px; transition:all .25s;
  position:relative; overflow:hidden;
  display:block; text-decoration:none; color:inherit;
  animation: cardIn .4s cubic-bezier(.4,0,.2,1) both;
}
.mcard::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  opacity:0; transition:opacity .25s;
}
.mcard.available::before { background:linear-gradient(90deg,var(--cyan),transparent); opacity:1; }
.mcard.done::before { background:linear-gradient(90deg,var(--green),transparent); opacity:1; }
.mcard.clickable:hover {
  border-color:var(--cyan); transform:translateY(-5px);
  box-shadow:0 14px 44px rgba(0,245,255,.13);
}
.mcard.locked { opacity:.25; cursor:not-allowed; pointer-events:none; filter:grayscale(.9); }
.mcard.done   { border-color:var(--green); background:linear-gradient(135deg,var(--panel),rgba(57,255,20,.04)); }
.mcard.done:hover { box-shadow:0 14px 44px rgba(57,255,20,.13); }
.mcard-icon   { font-size:30px; margin-bottom:12px; display:block; }
.mcard-num    { font-family:var(--font-game); font-size:7px; color:var(--dim); letter-spacing:3px; margin-bottom:6px; }
.mcard-name   { font-family:var(--font-game); font-size:13px; color:var(--white); margin-bottom:10px; line-height:1.4; font-weight:700; }
.mcard-desc   { font-size:12.5px; color:var(--mid); line-height:1.75; margin-bottom:12px; }
.mcard-meta   { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:5px; }
.mcard-xp     { font-family:var(--font-game); font-size:7px; color:var(--yellow); font-weight:900; letter-spacing:1px; }
.mcard-stars  { display:flex; gap:3px; }
.mcard-star   { font-size:11px; }
.mcard-star.dim { filter:grayscale(1); opacity:.2; }
.mcard-flavor { font-size:11px; color:var(--dim); font-style:italic; margin-top:10px; line-height:1.6;
                border-top:1px solid var(--border); padding-top:10px; }
.mcard-done   {
  position:absolute; top:12px; right:12px;
  font-family:var(--font-game); font-size:7px; color:var(--green);
  font-weight:900; display:none; letter-spacing:1px;
  background:rgba(57,255,20,.1); padding:4px 9px; border-radius:4px;
  border:1px solid rgba(57,255,20,.3);
}
.boss-preview { font-size:18px; position:absolute; bottom:16px; right:16px; opacity:.25; }

/* ── MAP FOOTER NAV ──────────────────────────────────────────── */
.map-footer { text-align:center; margin-top:30px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap; }

/* ── FLOATING EFFECTS ────────────────────────────────────────── */
.xp-pop {
  position:fixed; top:78px; right:22px; pointer-events:none; z-index:9996;
  font-family:var(--font-game); font-size:14px; color:var(--yellow);
  text-shadow:0 0 14px var(--yellow); font-weight:900;
  animation:xpfloat 2s ease forwards;
}
@keyframes xpfloat {
  0%  {opacity:1; transform:translateY(0) scale(1);}
  20% {transform:translateY(-12px) scale(1.2);}
  100%{opacity:0; transform:translateY(-80px) scale(.7);}
}
.dmg-flash {
  position:fixed; inset:0;
  background:radial-gradient(ellipse at center,rgba(255,34,68,.28),rgba(255,34,68,.08));
  pointer-events:none; z-index:9997;
  animation:dflash .5s ease forwards;
}
@keyframes dflash { to{opacity:0} }
.screen-shake { animation:shake .38s cubic-bezier(.36,.07,.19,.97) both; }
@keyframes shake {
  10%,90%{transform:translateX(-2px)}
  20%,80%{transform:translateX(5px)}
  30%,50%,70%{transform:translateX(-7px)}
  40%,60%{transform:translateX(7px)}
}

/* ── ACHIEVEMENT TOAST ───────────────────────────────────────── */
.achievement-toast {
  position:fixed; bottom:26px; right:22px; z-index:9999;
  background:linear-gradient(135deg,rgba(14,21,40,.98),rgba(20,12,5,.98));
  border:1px solid var(--orange); border-radius:12px;
  padding:16px 20px; min-width:250px; max-width:320px;
  box-shadow:0 8px 32px rgba(255,140,0,.2);
  animation:toastIn .4s cubic-bezier(.4,0,.2,1), toastOut .4s .1s ease 2.8s forwards;
}
@keyframes toastIn  { from{opacity:0;transform:translateX(50px)} to{opacity:1;transform:translateX(0)} }
@keyframes toastOut { to{opacity:0;transform:translateX(50px)} }
.toast-title { font-family:var(--font-game); font-size:7px; color:var(--orange); letter-spacing:3px; margin-bottom:7px; }
.toast-body  { font-size:14px; color:var(--white); }

/* ── PARTICLES / CONFETTI ────────────────────────────────────── */
.particle {
  position:fixed; pointer-events:none; z-index:9995; border-radius:50%;
  animation:particleFly var(--pt,1.2s) ease-out forwards;
}
@keyframes particleFly {
  0%  {opacity:1; transform:translate(0,0) scale(1);}
  100%{opacity:0; transform:translate(var(--px,0),var(--py,-90px)) scale(0);}
}
.confetti-piece {
  position:fixed; pointer-events:none; z-index:9995; width:9px; height:9px;
  border-radius:2px;
  animation:confettifall var(--ct,2s) ease-out var(--cd,0s) forwards;
}
@keyframes confettifall {
  0%  {opacity:1; transform:translate(0,0) rotate(0deg) scale(1);}
  100%{opacity:0; transform:translate(var(--cx,0),var(--cy,220px)) rotate(720deg) scale(.4);}
}

/* ── WIN SCREEN ──────────────────────────────────────────────── */
.cert-wrap {
  background:linear-gradient(135deg,rgba(12,18,35,.97),rgba(18,10,5,.97));
  border:3px solid var(--yellow);
  border-radius:18px; padding:48px;
  max-width:620px; width:100%;
  box-shadow:0 0 100px rgba(255,220,0,.12), 0 0 200px rgba(255,140,0,.05);
  position:relative; overflow:hidden;
}
.cert-wrap::before {
  content:''; position:absolute; inset:8px;
  border:1px solid rgba(255,220,0,.12); border-radius:14px; pointer-events:none;
}
.cert-stamp { animation:stampIn .7s cubic-bezier(.175,.885,.32,1.275) .5s both; }
@keyframes stampIn { from{transform:scale(3) rotate(-15deg);opacity:0} to{transform:scale(1) rotate(0);opacity:1} }
.stats-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:22px; }
.stat-item {
  background:rgba(0,245,255,.04); border:1px solid var(--border2);
  border-radius:10px; padding:15px; text-align:center;
}
.stat-val { font-family:var(--font-game); font-size:1.3rem; color:var(--cyan); font-weight:900; }
.stat-lbl { font-size:10px; color:var(--dim); letter-spacing:1px; margin-top:4px; }

/* ── RESPONSIVE ──────────────────────────────────────────────── */
@media(max-width:600px) {
  .wrap        { padding:20px 14px 100px; }
  .mission-hdr { padding-top:82px; }
  .map-wrap    { padding-top:88px; }
  .cert-wrap   { padding:30px 22px; }
  .stats-grid  { grid-template-columns:1fr; }
  .hud         { gap:8px; padding:8px 12px; }
  .hud-logo    { display:none; }
}

/* ── TITLE SCREEN ────────────────────────────────────────────── */
.title-logo {
  font-family:var(--font-game); font-size:clamp(18px,4vw,30px);
  color:var(--cyan); letter-spacing:4px; line-height:1.3; font-weight:900;
  text-shadow:0 0 40px rgba(0,245,255,.6), 0 0 100px rgba(0,245,255,.2);
  text-align:center;
  animation: logopulse 3s ease-in-out infinite;
}
@keyframes logopulse {
  0%,100%{text-shadow:0 0 40px rgba(0,245,255,.6),0 0 100px rgba(0,245,255,.2);}
  50%    {text-shadow:0 0 60px rgba(0,245,255,.9),0 0 140px rgba(0,245,255,.35);}
}
.radar-ring {
  position:absolute; border-radius:50%;
  border:1px solid rgba(0,245,255,.15);
  animation:radarPulse 3s ease-out infinite;
}
.r1 { width:100%; height:100%; top:0; left:0;  animation-delay:0s; }
.r2 { width:78%;  height:78%;  top:11%; left:11%; animation-delay:.7s; }
.r3 { width:56%;  height:56%;  top:22%; left:22%; animation-delay:1.4s; }
@keyframes radarPulse {
  0%   {opacity:.4; transform:scale(.92);}
  50%  {opacity:.7; transform:scale(1.04); border-color:rgba(0,245,255,.35);}
  100% {opacity:.4; transform:scale(.92);}
}


/* ── PRINT CSS ───────────────────────────────────────────────── */
@media print {
  .hud, .btn-primary, .btn-green, .btn-yellow, .btn-back, #bgcanvas,
  body::after, .scroll-hint { display:none!important; }
  body { background:#fff; color:#000; }
  .cert-wrap { border:3px solid #333; box-shadow:none; background:#fff; }
  .cert-wrap * { color:#000!important; text-shadow:none!important; }
}
"""
