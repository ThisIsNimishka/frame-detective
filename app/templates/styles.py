"""app/templates/styles.py — Complete clean CSS for Frame Detective."""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

/* ── VARIABLES ─────────────────────────────────────────────── */
:root {
  --bg:      #050b18;
  --bg2:     #0a1428;
  --panel:   rgba(8,16,32,0.94);
  --cyan:    #00e5ff;
  --cyan2:   #00b4cc;
  --green:   #39ff14;
  --yellow:  #ffe600;
  --orange:  #ff8c00;
  --red:     #ff2244;
  --purple:  #bf5fff;
  --white:   #e0f0ff;
  --muted:   #5a7a94;
  --dim:     #2e4460;
  --font-h:  'Orbitron', 'Arial Black', sans-serif;
  --font-b:  'Rajdhani', 'Arial', sans-serif;
  --cs: 16px;
}

/* ── RESET ─────────────────────────────────────────────────── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
a { color: inherit; text-decoration: none; }

/* ── BODY ──────────────────────────────────────────────────── */
body {
  font-family: var(--font-b);
  background: var(--bg);
  color: var(--white);
  min-height: 100vh;
  overflow-x: hidden;
  font-size: 15px;
  line-height: 1.6;
}

/* ── CANVAS ────────────────────────────────────────────────── */
#bgcanvas {
  position: fixed; inset: 0; z-index: 0;
  pointer-events: none; width: 100vw; height: 100vh;
}

/* ── CSS GRID OVERLAY ──────────────────────────────────────── */
body::before {
  content: '';
  position: fixed; inset: 0; z-index: 1; pointer-events: none;
  background-image:
    linear-gradient(rgba(0,229,255,.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,.018) 1px, transparent 1px);
  background-size: 56px 56px;
}

/* ── CRT SCANLINES ─────────────────────────────────────────── */
body::after {
  content:''; position:fixed; inset:0; z-index:9990; pointer-events:none;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(0,0,0,.045) 3px, rgba(0,0,0,.045) 4px);
}

/* ── PAGE TRANSITION VEIL ──────────────────────────────────── */
#page-veil {
  position:fixed; inset:0; z-index:9995; background:var(--bg);
  pointer-events:none;
  animation: veil-in .5s cubic-bezier(.65,0,.35,1) both;
}
@keyframes veil-in  { from{opacity:1} to{opacity:0} }
#page-veil.out {animation: veil-out .32s cubic-bezier(.65,0,.35,1) both;}
@keyframes veil-out { from{opacity:0} to{opacity:1} }

/* ── PAGE WRAP ─────────────────────────────────────────────── */
.page-wrap {
  position: relative; z-index: 10;
  max-width: 1020px; margin: 0 auto;
  padding: 88px 22px 60px;
  animation: slide-up .45s cubic-bezier(.16,1,.3,1) both;
}
@keyframes slide-up {
  from { opacity:0; transform: translateY(20px) scale(.985); }
  to   { opacity:1; transform: translateY(0)    scale(1); }
}

/* ══════════════════════════════════════════════════════════════
   HUD
══════════════════════════════════════════════════════════════ */
.hud {
  position: fixed; top:0; left:0; right:0; z-index:1000;
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  padding: 8px 20px;
  background: rgba(3,8,18,.97);
  border-bottom: 1px solid rgba(0,229,255,.14);
  box-shadow: 0 2px 40px rgba(0,0,0,.8);
  backdrop-filter: blur(20px);
  animation: hud-drop .4s cubic-bezier(.16,1,.3,1) both;
}
@keyframes hud-drop {
  from { transform:translateY(-100%); opacity:0; }
  to   { transform:translateY(0);     opacity:1; }
}

.hud-logo {
  font-family: var(--font-h); font-size: 11px;
  color: var(--cyan); letter-spacing: 4px; font-weight: 900;
  text-shadow: 0 0 18px rgba(0,229,255,.7);
  flex-shrink: 0;
}
.hud-sep { color: var(--dim); flex-shrink: 0; }
.hud-badge {
  font-family: var(--font-h); font-size: 10px; font-weight: 900;
  color: #05101e;
  background: linear-gradient(135deg, var(--yellow), var(--orange));
  padding: 4px 11px; border-radius: 2px;
  box-shadow: 0 0 14px rgba(255,200,0,.3);
  flex-shrink: 0;
  clip-path: polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
}

/* XP bar */
.xp-group {
  display: flex; align-items: center; gap: 8px;
  flex: 1; min-width: 160px;
}
.xp-label { font-size: 10px; color: var(--yellow); letter-spacing: 2px; flex-shrink:0; }
.xp-bar {
  flex: 1; height: 9px; min-width: 70px;
  background: rgba(0,229,255,.08);
  border: 1px solid rgba(0,229,255,.15);
  border-radius: 2px; overflow: hidden;
}
#xp-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--cyan2), var(--cyan), var(--yellow));
  border-radius: 2px;
  transition: width .8s cubic-bezier(.4,0,.2,1);
  box-shadow: 0 0 10px rgba(0,229,255,.5);
}
.xp-val { font-size: 10px; color: var(--cyan2); letter-spacing:.5px; flex-shrink:0; }

/* HP hearts */
.hp-group { display:flex; align-items:center; gap:6px; flex-shrink:0; }
.hp-label { font-size:10px; color:var(--red); letter-spacing:2px; }
.hearts { display:flex; gap:4px; }
.heart {
  font-size: 16px;
  transition: all .35s;
  filter: drop-shadow(0 0 5px rgba(255,34,68,.7));
}
.heart.dead { filter: grayscale(1) brightness(.2); transform: scale(.75); }

/* Streak */
.streak { display:flex; align-items:center; gap:5px; flex-shrink:0; }
.streak-label { font-size: 13px; }
#hud-streak {
  font-family: var(--font-h); font-size: 11px;
  color: var(--orange); font-weight: 900;
  min-width: 20px; text-align: center;
}

/* Badges */
.hud-badges { display:flex; gap:5px; flex-wrap:wrap; flex-shrink:0; }
.hud-badge-icon { font-size: 17px; transition: all .3s; cursor: help; }
.hud-badge-icon.locked { filter: grayscale(1) brightness(.15); }
.hud-badge-icon:not(.locked) { filter: drop-shadow(0 0 6px var(--yellow)); }

/* Quit */
.hud-quit {
  font-family: var(--font-h); font-size: 10px; letter-spacing: 2px;
  color: var(--muted);
  background: rgba(255,34,68,.04);
  border: 1px solid rgba(255,34,68,.22);
  padding: 5px 13px; border-radius: 2px; cursor: pointer;
  flex-shrink: 0; white-space: nowrap;
  display: inline-flex; align-items: center; gap: 5px;
  transition: all .15s;
  clip-path: polygon(4px 0,100% 0,calc(100% - 4px) 100%,0 100%);
}
.hud-quit:hover {
  color: var(--red); border-color: var(--red);
  background: rgba(255,34,68,.12);
  box-shadow: 0 0 14px rgba(255,34,68,.25);
}

/* ══════════════════════════════════════════════════════════════
   PANELS
══════════════════════════════════════════════════════════════ */
.panel {
  position: relative; overflow: visible;
  background: var(--panel);
  border: 1px solid rgba(0,229,255,.1);
  border-radius: 2px; margin-bottom: 18px;
  animation: panel-in .4s cubic-bezier(.16,1,.3,1) both;
}
.panel:nth-child(2) { animation-delay:  60ms; }
.panel:nth-child(3) { animation-delay: 120ms; }
.panel:nth-child(4) { animation-delay: 180ms; }
.panel:nth-child(5) { animation-delay: 240ms; }
@keyframes panel-in {
  from { opacity:0; transform: translateY(10px); }
  to   { opacity:1; transform: translateY(0); }
}

/* ── PRINT CERTIFICATE FIX ── */
@media print {
  body { background: white !important; color: black !important; }
  #bgcanvas, .hud, .win-actions, #page-veil, .radar-wrap, .radar-ring, .boss-arena::after {
    display: none !important;
  }
  .page-wrap, .win-wrap { 
    margin: 0 !important; 
    padding: 0 !important; 
    border: none !important; 
    background: transparent !important;
  }
  .win-wrap {
    display: block !important;
    text-align: center;
  }
  .cert-name {
    color: #000 !important;
    border-bottom: 2px solid #000 !important;
    text-shadow: none !important;
  }
  .stat-box {
    background: white !important;
    border: 1px solid #ccc !important;
    color: black !important;
  }
  .stat-box::before, .stat-box::after { display: none !important; }
  .win-title { color: #000 !important; }
  .badge-row span { filter: none !important; }
}

/* cyan corner brackets */
.panel::before {
  content: ''; position: absolute; inset: -1px;
  pointer-events: none; z-index: 2;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top left    /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) top left    /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) top right   /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) top right   /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) bottom left /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) bottom right/var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right/2px var(--cs);
  background-repeat: no-repeat;
  opacity: .55;
}

.panel-head {
  padding: 16px 24px;
  background: rgba(0, 229, 255, 0.04);
  border-bottom: 1px solid rgba(0, 229, 255, 0.15);
  display: flex;
  align-items: center;
  /* Z-PATTERN FOCUS: nudge headers slightly to the right */
  padding-left: 32px;
}
.panel-head::before {
  content: ''; width: 24px; height: 2px; flex-shrink: 0;
  background: linear-gradient(90deg, transparent, var(--cyan));
}
.panel-head::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(0,229,255,.3), transparent);
}
.panel-title {
  font-family: var(--font-h); font-size: 9px; letter-spacing: 3px;
  color: var(--cyan); white-space: nowrap; flex-shrink: 0;
}
.panel-body {
  padding: 30px 32px;
  font-size: 1.05rem;
  line-height: 1.7;
}
.panel-body p {
  color: rgba(224,240,255,.85); line-height: 1.78; margin-bottom: 12px;
  font-size: 15px;
}
.panel-body p:last-child { margin-bottom: 0; }
.panel-body strong { color: var(--white); font-weight: 700; }
.panel-body em { color: var(--cyan); font-style: normal; }
.panel-body u  { color: var(--yellow); }

/* ── BRIEFING ──────────────────────────────────────────────── */
.briefing {
  padding: 18px 22px;
  background: rgba(0,18,36,.5);
  border-left: 3px solid var(--cyan);
}
.briefing-speaker {
  display: block;
  font-family: var(--font-h); font-size: 9px; letter-spacing: 3px;
  color: var(--cyan); margin-bottom: 10px;
  text-shadow: 0 0 14px rgba(0,229,255,.6);
}
.briefing-text {
  color: rgba(224,240,255,.85); font-size: 15px; line-height: 1.78;
}
.tw-cursor {
  display: inline-block; width: 2px; height: 1.1em;
  background: var(--cyan); vertical-align: text-bottom;
  animation: blink .7s step-end infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* ══════════════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════════════ */
.btn {
  font-family: var(--font-h); font-weight: 900;
  letter-spacing: 3px; cursor: pointer; border: none;
  display: inline-flex; align-items: center; gap: 8px;
  text-decoration: none; white-space: nowrap;
  border-radius: 2px; transition: all .15s;
}
.btn:active { transform: translateY(1px) !important; }

.btn-cyan {
  color: #030810;
  background: linear-gradient(135deg, var(--cyan), var(--cyan2));
  padding: 16px 52px; font-size: 12px;
  box-shadow: 0 0 36px rgba(0,229,255,.5), 0 3px 0 rgba(0,80,100,.8);
  clip-path: polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
  position: relative; overflow: hidden;
}
.btn-cyan::after {
  content: ''; position:absolute; inset:0;
  background: linear-gradient(90deg,transparent,rgba(255,255,255,.22),transparent);
  transform: translateX(-100%); transition: transform .5s;
}
.btn-cyan:hover::after { transform: translateX(100%); }
.btn-cyan:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 55px rgba(0,229,255,.8), 0 5px 0 rgba(0,80,100,.8);
}

.btn-green {
  color: #030810;
  background: linear-gradient(135deg,#2dd10f,#39ff14);
  padding: 13px 38px; font-size: 11px;
  box-shadow: 0 0 28px rgba(57,255,20,.45), 0 3px 0 rgba(10,60,5,.8);
  clip-path: polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
}
.btn-green:hover { transform:translateY(-2px); box-shadow:0 0 45px rgba(57,255,20,.8); }

.btn-yellow {
  color: #030810;
  background: linear-gradient(135deg,#b89000,#ffe600);
  padding: 13px 38px; font-size: 11px;
  box-shadow: 0 0 28px rgba(255,230,0,.4), 0 3px 0 rgba(60,50,0,.8);
  clip-path: polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
}
.btn-yellow:hover { transform:translateY(-2px); box-shadow:0 0 45px rgba(255,230,0,.8); }

.btn-ghost {
  color: var(--muted); font-size: 10px; letter-spacing: 2px;
  border: 1px solid rgba(255,255,255,.1);
  background: rgba(0,0,0,.3); padding: 8px 18px;
  clip-path: polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
}
.btn-ghost:hover { color:var(--cyan); border-color:rgba(0,229,255,.4); }

.btn-red {
  color: var(--red); font-size: 10px; letter-spacing: 2px;
  border: 1px solid rgba(255,34,68,.25);
  background: rgba(255,34,68,.05); padding: 8px 18px;
  clip-path: polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
}
.btn-red:hover { background:rgba(255,34,68,.15); border-color:var(--red); }

/* ══════════════════════════════════════════════════════════════
   MISSION HEADER
══════════════════════════════════════════════════════════════ */
.mission-hdr { display:flex; align-items:center; gap:16px; margin-bottom:20px; }
.mission-id {
  font-family: var(--font-h); font-size: 9px;
  color: var(--cyan2); letter-spacing: 3px;
}
.mission-title {
  font-family: var(--font-h); font-size: clamp(16px, 3vw, 24px);
  color: var(--white); letter-spacing: 2px;
  text-shadow: 0 0 28px rgba(0,229,255,.35);
}

/* ══════════════════════════════════════════════════════════════
   BOSS / QUIZ SECTION
══════════════════════════════════════════════════════════════ */
.boss-arena {
  --cs: 20px;
  border-color: rgba(255,34,68,.18);
}
.boss-arena::before {
  background:
    linear-gradient(var(--red),var(--red)) top left    /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) top left    /2px var(--cs),
    linear-gradient(var(--red),var(--red)) top right   /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) top right   /2px var(--cs),
    linear-gradient(var(--red),var(--red)) bottom left /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) bottom left /2px var(--cs),
    linear-gradient(var(--red),var(--red)) bottom right/var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) bottom right/2px var(--cs);
  background-repeat: no-repeat; opacity: .5;
}

.boss-header { padding: 18px 22px; display:flex; align-items:center; gap:18px; }
.boss-emoji  { font-size: 52px; filter: drop-shadow(0 0 20px rgba(255,34,68,.6)); }
.boss-info   { flex: 1; }
.boss-name {
  font-family: var(--font-h); font-size: clamp(15px,2.8vw,22px);
  color: var(--red); letter-spacing: 2px;
  text-shadow: 0 0 22px rgba(255,34,68,.55);
}
.boss-sub    { font-size: 13px; color: var(--muted); margin-top: 4px; }
.boss-hp-row { margin-top: 10px; }
.boss-hp-lbl { font-family:var(--font-h); font-size:9px; color:var(--red); letter-spacing:2px; margin-bottom:5px; }
.boss-hp-bg  { height:7px; background:rgba(255,34,68,.1); border-radius:2px; overflow:hidden; border:1px solid rgba(255,34,68,.2); }
.boss-hp-bar { height:100%; width:100%; background:linear-gradient(90deg,#cc1030,var(--red)); transition:width 1s cubic-bezier(.4,0,.2,1); box-shadow:0 0 12px rgba(255,34,68,.5); }

/* Timer */
.quiz-timer {
  padding: 10px 22px;
  display: flex; align-items: center; gap: 10px;
}
.quiz-timer-label { font-family:var(--font-h); font-size:9px; color:var(--muted); letter-spacing:2px; flex-shrink:0; }
.quiz-timer-bar   { flex:1; height:5px; background:rgba(255,230,0,.1); border-radius:3px; overflow:hidden; }
#timer-fill       { height:100%; width:100%; background:linear-gradient(90deg,#2dd10f,var(--yellow),var(--orange)); transition:width 1s linear; box-shadow:0 0 8px rgba(255,230,0,.4); }
.quiz-timer-count { font-family:var(--font-h); font-size:13px; color:var(--yellow); min-width:26px; text-align:right; flex-shrink:0; }

/* Question */
.question-text {
  font-family: var(--font-h); font-size: clamp(13px,2vw,16px);
  line-height: 1.6; color: var(--white); letter-spacing:.5px;
  padding: 16px 22px;
  border-top: 1px solid rgba(255,34,68,.1);
}

/* Options */
.options { padding: 0 18px 18px; display:flex; flex-direction:column; gap:10px; }
.qbtn {
  font-family: var(--font-h); font-size: clamp(11px,1.6vw,13px);
  background: rgba(6,14,28,.85);
  border: 1px solid rgba(0,229,255,.15);
  color: rgba(224,240,255,.85); padding: 15px 20px;
  cursor: pointer; text-align: left; border-radius: 2px;
  transition: all .18s; letter-spacing: 1px;
  display: flex; align-items: center; gap: 12px;
  position: relative; overflow: hidden;
  clip-path: polygon(7px 0,100% 0,calc(100% - 7px) 100%,0 100%);
}
.qbtn .key-hint {
  font-size: 13px; color: var(--cyan); font-weight: 900;
  flex-shrink: 0; width: 22px; text-align: center;
}
.qbtn::before {
  content: ''; position:absolute; top:0; left:0; bottom:0; width:3px;
  background: linear-gradient(180deg,var(--cyan),var(--cyan2));
  opacity: 0; transition: opacity .18s;
}
.qbtn:hover:not([disabled]) {
  background: rgba(0,229,255,.08);
  border-color: rgba(0,229,255,.4);
  color: var(--white);
  box-shadow: 0 0 20px rgba(0,229,255,.12);
}
.qbtn:hover:not([disabled])::before { opacity: 1; }
.qbtn.correct {
  background: rgba(57,255,20,.1); border-color: var(--green);
  color: var(--green); box-shadow: 0 0 22px rgba(57,255,20,.3);
}
.qbtn.correct::before { background: var(--green); opacity: 1; }
.qbtn.wrong {
  background: rgba(255,34,68,.1); border-color: var(--red);
  color: var(--red); box-shadow: 0 0 22px rgba(255,34,68,.3);
}
.qbtn.wrong::before { background: var(--red); opacity: 1; }
.qbtn[disabled] { cursor: not-allowed; opacity: .65; }

/* Feedback */
.quiz-feedback {
  display: none; margin: 0 18px 18px;
  padding: 15px 18px; border-radius: 2px; border-left: 33px solid;
  line-height: 1.7; font-size: 14px;
  animation: feed-in .3s cubic-bezier(.16,1,.3,1) both;
}
@keyframes feed-in { from{opacity:0;transform:translateX(-10px)} to{opacity:1;transform:translateX(0)} }
.quiz-feedback.win  { background:rgba(57,255,20,.07);  border-color:var(--green); color:rgba(224,240,255,.9); }
.quiz-feedback.lose { background:rgba(255,34,68,.07);  border-color:var(--red);   color:rgba(224,240,255,.9); }

/* Hint */
.hint-panel {
  display: none; margin: 0 18px 10px;
  padding: 12px 16px; border-left: 2px solid var(--yellow);
  background: rgba(255,230,0,.05); border-radius: 2px;
}
.hint-panel.show { display: flex; gap: 10px; align-items: flex-start; }
.hint-label { font-family:var(--font-h); font-size:9px; color:var(--yellow); letter-spacing:2px; flex-shrink:0; }
.hint-body  { font-size: 14px; color: rgba(224,240,255,.8); line-height: 1.6; }

/* Next banner */
.next-bar {
  padding: 16px 20px;
  border-top: 1px solid rgba(0,229,255,.1);
  text-align: center;
  display: none;
}

/* ══════════════════════════════════════════════════════════════
   PIPELINE
══════════════════════════════════════════════════════════════ */
.pipe-row {
  display: flex; align-items: stretch; flex-wrap: wrap;
  padding: 16px 18px 18px;
}
.pipe-stage {
  flex: 1; min-width: 90px; padding: 16px 12px; text-align: center;
  border: 1px solid rgba(0,229,255,.08);
  background: rgba(4,10,22,.7); transition: all .3s;
  position: relative;
}
.pipe-stage + .pipe-stage { border-left: none; }
.pipe-stage.active {
  background: rgba(0,229,255,.07);
  border-color: rgba(0,229,255,.35);
  box-shadow: inset 0 0 22px rgba(0,229,255,.1);
}
.pipe-icon { font-size:24px; display:block; margin-bottom:8px; }
.pipe-name { font-family:var(--font-h); font-size:9px; color:var(--cyan2); letter-spacing:2px; }
.pipe-time { font-size:12px; color:var(--muted); margin-top:4px; }

/* ══════════════════════════════════════════════════════════════
   MAP PAGE
══════════════════════════════════════════════════════════════ */
.map-page { position:relative; z-index:10; }
.map-inner { max-width:1100px; margin:0 auto; padding:90px 22px 60px; }
.map-heading {
  font-family:var(--font-h); font-size:clamp(16px,3vw,26px);
  color:var(--white); letter-spacing:5px; margin-bottom:6px;
  text-shadow:0 0 28px rgba(0,229,255,.35);
}
.map-sub { font-size:13px; color:var(--muted); letter-spacing:2px; margin-bottom:20px; }

/* Progress */
.map-progress { margin-bottom:22px; }
#map-prog-lbl  {
  font-family:var(--font-h); font-size:9px; color:var(--cyan2);
  letter-spacing:3px; margin-bottom:6px;
}
.map-prog-track {
  height:6px; background:rgba(0,229,255,.08); border-radius:3px;
  overflow:hidden; border:1px solid rgba(0,229,255,.12);
}
#map-prog-fill {
  height:100%; background:linear-gradient(90deg,var(--cyan2),var(--cyan));
  border-radius:3px; transition:width .8s cubic-bezier(.4,0,.2,1);
  box-shadow:0 0 10px rgba(0,229,255,.5);
}

/* Grid */
.mission-grid {
  display: grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr));
  gap: 16px; margin-bottom: 24px;
}
.mcard {
  background: rgba(4, 10, 22, 0.7);
  border: 1px solid rgba(0, 229, 255, 0.1);
  border-radius: 2px;
  padding: 30px 20px;
  text-align: center;
  text-decoration: none;
  position: relative;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.mcard:hover:not(.locked) {
  background: rgba(0, 229, 255, 0.05);
  border-color: var(--cyan);
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
}
.mcard.locked { opacity: 0.3; cursor: not-allowed; filter: grayscale(1); }
.mcard.done { border-color: var(--green); }
  content: ''; position:absolute; inset:-1px; pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top left    /13px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top left    /2px 13px,
    linear-gradient(var(--cyan),var(--cyan)) top right   /13px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top right   /2px 13px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left /13px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left /2px 13px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right/13px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right/2px 13px;
  background-repeat:no-repeat; opacity:.42; transition:opacity .22s;
}
.mcard:hover:not(.locked)::before { opacity:.88; }
.mcard:hover:not(.locked) {
  border-color: rgba(0,229,255,.35); background: rgba(0,229,255,.06);
  transform: translateY(-4px) scale(1.025);
  box-shadow: 0 14px 40px rgba(0,0,0,.5), 0 0 26px rgba(0,229,255,.15);
}
.mcard.locked {
  pointer-events: none; opacity: .3; filter: grayscale(.9);
}
.mcard.done::before {
  background:
    linear-gradient(var(--green),var(--green)) top left    /13px 2px,
    linear-gradient(var(--green),var(--green)) top left    /2px 13px,
    linear-gradient(var(--green),var(--green)) top right   /13px 2px,
    linear-gradient(var(--green),var(--green)) top right   /2px 13px,
    linear-gradient(var(--green),var(--green)) bottom left /13px 2px,
    linear-gradient(var(--green),var(--green)) bottom left /2px 13px,
    linear-gradient(var(--green),var(--green)) bottom right/13px 2px,
    linear-gradient(var(--green),var(--green)) bottom right/2px 13px;
  background-repeat: no-repeat;
}
.mcard.done { border-color: rgba(57,255,20,.12); }

/* Mission card internals */
.mc-done  { display:none; position:absolute; top:8px; right:10px; font-family:var(--font-h); font-size:8px; color:var(--green); letter-spacing:1px; }
.mc-icon  { font-size:36px; display:block; margin-bottom:10px; filter:drop-shadow(0 0 12px rgba(0,229,255,.4)); }
.mc-num   { font-family:var(--font-h); font-size:9px; color:var(--cyan2); letter-spacing:3px; margin-bottom:5px; }
.mc-name  { font-family:var(--font-h); font-size:12px; color:var(--white); letter-spacing:1px; line-height:1.3; margin-bottom:6px; }
.mc-desc  { font-size:12px; color:var(--muted); line-height:1.5; margin-bottom:10px; min-height:30px; }
.mc-meta  { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
.mc-xp    { font-family:var(--font-h); font-size:10px; color:var(--yellow); }
.mc-stars { display:flex; gap:3px; }
.mc-star  { font-size:12px; color:var(--yellow); }
.mc-star.dim { color:var(--dim); }
.mc-flavor{ font-size:10px; color:var(--dim); font-style:italic; line-height:1.4; border-top:1px solid rgba(0,229,255,.06); padding-top:8px; }
.mc-boss  { position:absolute; bottom:8px; right:10px; font-size:13px; opacity:.45; }

/* Map footer */
.map-footer { display:flex; gap:12px; flex-wrap:wrap; padding-top:6px; }

/* ══════════════════════════════════════════════════════════════
   INDEX / TITLE
══════════════════════════════════════════════════════════════ */
.title-screen {
  position:relative; z-index:10; min-height:100vh;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  text-align:center; padding:40px 20px;
}
.radar-wrap { position:relative; width:260px; height:260px; margin:0 auto 40px; flex-shrink:0; }
.radar-ring { position:absolute; border-radius:50%; border:1px solid rgba(0,229,255,.1); }
.radar-ring.r1 { inset:0;  animation:spin 14s  linear infinite; }
.radar-ring.r2 { inset:30px; animation:spin 9s linear infinite reverse; }
.radar-ring.r3 { inset:60px; animation:spin 22s linear infinite; }
.radar-ring.r1::after {
  content:''; position:absolute; top:50%; left:50%;
  width:50%; height:1px;
  background:linear-gradient(90deg,rgba(0,229,255,.5),transparent);
  transform-origin:left center; animation:spin 4s linear infinite;
}
@keyframes spin { to{transform:rotate(360deg)} }

.title-name {
  font-family:var(--font-h); font-size:clamp(22px,6vw,40px);
  font-weight:900; letter-spacing:6px; line-height:1.1;
  color:var(--white); margin-bottom:4px;
  text-shadow:0 0 40px rgba(0,229,255,.7),0 0 80px rgba(0,229,255,.3);
}
.title-tagline {
  font-family:var(--font-h); font-size:clamp(8px,1.8vw,11px);
  color:var(--cyan2); letter-spacing:4px; margin-bottom:40px;
}
.title-brief {
  max-width:520px; margin:0 auto 36px; text-align:left;
}
.title-btns { display:flex; flex-direction:column; align-items:center; gap:14px; }

/* ══════════════════════════════════════════════════════════════
   WIN SCREEN
══════════════════════════════════════════════════════════════ */
.win-wrap {
  max-width:680px; margin:0 auto; padding:90px 22px 60px;
  text-align:center; position:relative; z-index:10;
}
.win-trophy      { font-size:64px; margin-bottom:12px; }
.win-title {
  font-family:var(--font-h); font-size:clamp(16px,3.5vw,28px);
  color:var(--yellow); letter-spacing:4px; margin-bottom:6px;
  text-shadow:0 0 36px rgba(255,230,0,.6);
  animation:glow-pulse 2.5s ease-in-out infinite alternate;
}
@keyframes glow-pulse {
  from{ text-shadow:0 0 26px rgba(255,230,0,.5); }
  to  { text-shadow:0 0 55px rgba(255,230,0,.9),0 0 90px rgba(255,230,0,.5); }
}
.win-sub { font-size:13px; color:var(--muted); letter-spacing:2px; margin-bottom:28px; }
.name-input {
  background:rgba(0,229,255,.05); border:1px solid rgba(0,229,255,.22);
  color:var(--white); padding:12px 20px; font-size:1.1rem;
  text-align:center; border-radius:2px;
  width:100%; max-width:300px; outline:none;
  font-family:var(--font-h); letter-spacing:2px;
}
.cert-name {
  font-family:var(--font-h); font-size:1.6rem; color:var(--cyan);
  margin-top:12px; letter-spacing:3px;
  text-shadow:0 0 18px rgba(0,229,255,.4);
}
.stats-row {
  display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr));
  gap:12px; margin:24px 0;
}
.stat-box {
  background:rgba(4,10,22,.85); border:1px solid rgba(0,229,255,.1);
  border-radius:2px; padding:16px; text-align:center;
  position:relative; overflow:visible;
}
.stat-box::before {
  content:''; position:absolute; inset:-1px; pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top left    /9px 1px,
    linear-gradient(var(--cyan),var(--cyan)) top left    /1px 9px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right/9px 1px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right/1px 9px;
  background-repeat:no-repeat; opacity:.3;
}
.stat-number { font-family:var(--font-h); font-size:22px; color:var(--cyan); font-weight:900; }
.stat-label  { font-size:10px; color:var(--muted); letter-spacing:2px; margin-top:4px; }
.badge-row   { display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin:20px 0; }
.win-actions { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin-top:22px; }

/* ══════════════════════════════════════════════════════════════
   EFFECTS
══════════════════════════════════════════════════════════════ */
.xp-popup {
  position:fixed; left:50%; transform:translateX(-50%); top:66px;
  z-index:9500; pointer-events:none;
  font-family:var(--font-h); font-size:16px; color:var(--yellow); font-weight:900;
  text-shadow:0 0 18px rgba(255,230,0,.8);
  animation:xp-float 2s cubic-bezier(.16,1,.3,1) both;
}
@keyframes xp-float {
  0%  {opacity:0;transform:translateX(-50%) translateY(0)}
  18% {opacity:1}
  80% {opacity:1}
  100%{opacity:0;transform:translateX(-50%) translateY(-58px)}
}
.dmg-flash {
  position:fixed; inset:0; z-index:9500; pointer-events:none;
  background:rgba(255,34,68,.22); animation:flash .4s ease;
}
@keyframes flash {0%,100%{opacity:0}30%{opacity:1}}
.screen-shake { animation:shake .4s cubic-bezier(.36,.07,.19,.97); }
@keyframes shake {0%,100%{transform:translate(0)}20%{transform:translate(-5px,2px)}40%{transform:translate(4px,-2px)}60%{transform:translate(-3px,1px)}80%{transform:translate(3px,-1px)}}
.particle { position:fixed; border-radius:50%; pointer-events:none; z-index:9480; animation:pt var(--pt,.9s) cubic-bezier(.2,0,.8,1) both; }
@keyframes pt {from{opacity:1;transform:translate(0,0) scale(1)}to{opacity:0;transform:translate(var(--px,0),var(--py,-80px)) scale(0)}}
.confetti-bit { position:fixed; width:8px; height:8px; pointer-events:none; z-index:9480; border-radius:2px; animation:conf var(--ct,1.4s) var(--cd,0s) cubic-bezier(.2,0,.8,1) both; }
@keyframes conf {from{opacity:1;transform:translate(0,0) rotate(0)}to{opacity:0;transform:translate(var(--cx,0),var(--cy,200px)) rotate(540deg)}}
.toast {
  position:fixed; bottom:22px; right:22px; z-index:9600;
  background:rgba(5,12,25,.96); border:1px solid rgba(0,229,255,.22);
  padding:14px 18px; border-radius:2px; min-width:210px;
  animation:toast-in .4s cubic-bezier(.16,1,.3,1);
  box-shadow:0 8px 30px rgba(0,0,0,.5);
}
.toast-head { font-family:var(--font-h); font-size:9px; color:var(--cyan); letter-spacing:3px; margin-bottom:5px; }
.toast-body { font-size:13px; color:rgba(224,240,255,.85); line-height:1.5; }
@keyframes toast-in { from{opacity:0;transform:translateX(28px)} to{opacity:1;transform:translateX(0)} }
"""
