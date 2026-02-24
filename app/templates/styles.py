"""app/templates/styles.py — sci-fi cyberpunk premium theme."""

CSS = """
/* ── FONTS ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

/* ── ROOT ──────────────────────────────────────────────────── */
:root {
  --bg:#030810; --bg2:#060d1c; --bg3:#0a1428;
  --panel:rgba(5,12,25,.93); --panel2:rgba(8,18,35,.95);
  --glass:rgba(5,12,25,.88);
  --border:#0e2040; --border2:#1a3060; --border3:#2a4888;
  --cyan:#00e8ff; --cyan2:#00b8d0; --cyan3:#004d5c;
  --green:#39ff14; --green2:#2dd10f; --green3:#1a6a06;
  --yellow:#ffe600; --orange:#ff8c00; --orange2:#cc6e00;
  --red:#ff2040; --red2:#cc1030;
  --purple:#bf5fff; --purple2:#8830cc;
  --white:#d8f0ff; --dim:#2e4060; --mid:#607890; --light:#90b8d0;
  --gold:#ffd700; --gold2:#b89000;
  --font-game:'Orbitron','Arial Black',Arial,sans-serif;
  --font-mono:'Share Tech Mono','Courier New',monospace;
  --cs:18px; /* corner size */
}

/* ── RESET ─────────────────────────────────────────────────── */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}

/* ── BODY ──────────────────────────────────────────────────── */
body{
  font-family:var(--font-mono);
  background:var(--bg); color:var(--white);
  min-height:100vh; overflow-x:hidden;
}

/* ── BG CANVAS ─────────────────────────────────────────────── */
#bgcanvas{position:fixed;inset:0;z-index:0;pointer-events:none;width:100vw;height:100vh;}

/* ── GRID OVERLAY ──────────────────────────────────────────── */
body::before{
  content:''; position:fixed; inset:0; z-index:1; pointer-events:none;
  background-image:
    linear-gradient(rgba(0,232,255,.022) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,232,255,.022) 1px, transparent 1px);
  background-size:60px 60px;
}

/* ── CRT SCANLINES ─────────────────────────────────────────── */
body::after{
  content:''; position:fixed; inset:0; z-index:9997; pointer-events:none;
  background:repeating-linear-gradient(
    0deg,transparent,transparent 3px,rgba(0,0,0,.04) 3px,rgba(0,0,0,.04) 4px);
  animation:scanroll 12s linear infinite;
}
@keyframes scanroll{0%{background-position:0 0}100%{background-position:0 400px}}

/* ── PAGE VEIL (transition layer) ──────────────────────────── */
#page-veil{
  position:fixed; inset:0; z-index:9998;
  background:var(--bg); pointer-events:none;
  animation:veilReveal .5s cubic-bezier(.65,0,.35,1) both;
}
@keyframes veilReveal{from{opacity:1}to{opacity:0}}
#page-veil.closing{animation:veilClose .32s cubic-bezier(.65,0,.35,1) both;}
@keyframes veilClose{from{opacity:0}to{opacity:1}}

/* ── SCAN SWEEP (page-load effect) ─────────────────────────── */
#scan-sweep{
  position:fixed; inset:0; z-index:9996; pointer-events:none;
  background:linear-gradient(180deg,
    transparent 0%,rgba(0,232,255,.08) 48%,
    rgba(0,232,255,.16) 50%,rgba(0,232,255,.08) 52%,transparent 100%);
  animation:scanSweep .85s cubic-bezier(.4,0,.2,1) .08s both;
}
@keyframes scanSweep{from{transform:translateY(-100%);opacity:1}to{transform:translateY(100vh);opacity:0}}

/* ── WRAP ──────────────────────────────────────────────────── */
.wrap{
  position:relative; z-index:10;
  max-width:1020px; margin:0 auto; padding:90px 22px 60px;
  animation:pageEnter .5s cubic-bezier(.16,1,.3,1) both;
}
@keyframes pageEnter{from{opacity:0;transform:translateY(18px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}

/* ════════════════════════════════════════════════════════════
   HUD
═════════════════════════════════════════════════════════════*/
.hud{
  position:fixed; top:0; left:0; right:0; z-index:1000;
  background:rgba(3,8,16,.97);
  border-bottom:1px solid rgba(0,232,255,.14);
  box-shadow:0 0 40px rgba(0,0,0,.7),0 1px 0 rgba(0,232,255,.1);
  padding:9px 22px;
  display:flex; align-items:center; gap:14px; flex-wrap:wrap;
  backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px);
  animation:hudSlide .45s cubic-bezier(.16,1,.3,1) both;
}
@keyframes hudSlide{from{transform:translateY(-110%);opacity:0}to{transform:translateY(0);opacity:1}}
/* accent corners on HUD bottom edge */
.hud::before,.hud::after{
  content:''; position:absolute; bottom:-1px;
  width:80px; height:2px;
  background:linear-gradient(90deg,var(--cyan),transparent);
  box-shadow:0 0 14px var(--cyan);
}
.hud::before{left:0;}
.hud::after{right:0; background:linear-gradient(90deg,transparent,var(--cyan));}

.hud-logo{
  font-family:var(--font-game); font-size:11px; color:var(--cyan);
  letter-spacing:4px; flex-shrink:0; font-weight:900;
  text-shadow:0 0 22px rgba(0,232,255,.8),0 0 44px rgba(0,232,255,.4);
}
.hud-div{color:var(--border3);font-size:16px;flex-shrink:0;}
.hud-lvl{
  font-family:var(--font-game); font-size:10px;
  background:linear-gradient(135deg,var(--yellow),var(--orange));
  color:#030810; padding:5px 13px; border-radius:2px;
  font-weight:900; white-space:nowrap; flex-shrink:0;
  box-shadow:0 0 20px rgba(255,200,0,.35);
  clip-path:polygon(6px 0,100% 0,calc(100% - 6px) 100%,0 100%);
}
.xp-wrap{display:flex;align-items:center;gap:8px;flex:1;min-width:180px;}
.xp-lbl{font-size:10px;color:var(--yellow);white-space:nowrap;letter-spacing:2px;flex-shrink:0;}
.xp-bar{
  flex:1;height:10px;
  background:rgba(14,32,64,.8);
  border:1px solid rgba(0,232,255,.1);
  border-radius:2px;overflow:hidden;min-width:80px;
}
.xp-fill{
  height:100%;border-radius:2px;
  transition:width .8s cubic-bezier(.4,0,.2,1);
  background:linear-gradient(90deg,var(--cyan2),var(--cyan),var(--yellow));
  box-shadow:0 0 16px rgba(0,232,255,.6);
  position:relative;overflow:hidden;
}
.xp-fill::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);
  animation:shimmer 2s infinite;
}
@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.xp-num{font-size:10px;color:var(--cyan2);white-space:nowrap;letter-spacing:.5px;flex-shrink:0;}
.hp-wrap{display:flex;align-items:center;gap:6px;flex-shrink:0;}
.hp-lbl{font-size:10px;color:var(--red);letter-spacing:2px;}
.hearts{display:flex;gap:4px;}
.ht{font-size:16px;transition:all .4s;filter:drop-shadow(0 0 6px rgba(255,50,80,.8));}
.ht.dead{filter:grayscale(1) brightness(.15);transform:scale(.76);}
.streak-wrap{display:flex;align-items:center;gap:4px;flex-shrink:0;}
.streak-lbl{font-size:12px;}
.streak-num{
  font-family:var(--font-game);font-size:11px;color:var(--orange);
  min-width:24px;text-align:center;font-weight:900;transition:all .2s;
}
.streak-num.bump{animation:streakbump .3s ease;}
@keyframes streakbump{0%,100%{transform:scale(1)}50%{transform:scale(1.7)}}
.badges{display:flex;gap:5px;flex-wrap:wrap;flex-shrink:0;}
.bdg{font-size:18px;transition:all .4s;cursor:help;}
.bdg.locked{filter:grayscale(1) brightness(.15);}
.bdg:not(.locked){filter:drop-shadow(0 0 7px var(--yellow));}
.hud-quit{
  font-family:var(--font-game);font-size:10px;color:var(--mid);
  background:rgba(255,32,64,.05);border:1px solid rgba(255,32,64,.22);
  padding:6px 15px;cursor:pointer;border-radius:2px;
  transition:all .15s;letter-spacing:2px;
  display:inline-flex;align-items:center;gap:5px;
  text-decoration:none;flex-shrink:0;white-space:nowrap;
  clip-path:polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
}
.hud-quit:hover{
  background:rgba(255,32,64,.16);border-color:var(--red);color:var(--red);
  box-shadow:0 0 18px rgba(255,32,64,.3);
}

/* ════════════════════════════════════════════════════════════
   PANELS  (.blk)
═════════════════════════════════════════════════════════════*/
.blk{
  position:relative;
  background:var(--panel);
  border:1px solid rgba(0,232,255,.09);
  border-radius:2px;
  margin-bottom:20px;
  overflow:visible;
  animation:panelReveal .45s cubic-bezier(.16,1,.3,1) both;
}
/* stagger children */
.blk:nth-child(2){animation-delay:70ms;}
.blk:nth-child(3){animation-delay:140ms;}
.blk:nth-child(4){animation-delay:210ms;}
.blk:nth-child(5){animation-delay:280ms;}
.blk:nth-child(6){animation-delay:350ms;}
@keyframes panelReveal{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:translateY(0)}}

/* corner bracket decoration — all 4 corners via multi-stop background */
.blk::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;z-index:2;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) top    right /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    right /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /2px var(--cs),
    linear-gradient(var(--cyan),var(--cyan)) bottom right /var(--cs) 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /2px var(--cs);
  background-repeat:no-repeat;
  opacity:.65;
}

/* ── CARD (padded .blk subtype) ────────────────────────────── */
.card{padding:22px 26px;}
.card-lbl{
  font-family:var(--font-game);font-size:9px;letter-spacing:3px;
  color:var(--cyan);margin-bottom:6px;
  display:flex;align-items:center;gap:10px;white-space:nowrap;
}
.card-lbl::before,.card-lbl::after{
  content:'';flex:1;height:1px;min-width:8px;
  background:linear-gradient(90deg,transparent,rgba(0,232,255,.4));
}
.card-lbl::after{background:linear-gradient(90deg,rgba(0,232,255,.4),transparent);}
.card-ttl{
  font-family:var(--font-game);font-size:clamp(12px,2vw,16px);
  color:var(--white);margin-bottom:16px;letter-spacing:1px;
  text-shadow:0 0 22px rgba(0,232,255,.3);
}
.card p{line-height:1.75;color:var(--light);font-size:clamp(12px,1.6vw,14px);margin-bottom:12px;}
.card p:last-child{margin-bottom:0;}
.card strong{color:var(--white);}
.card em{color:var(--cyan);font-style:normal;}
.card u{color:var(--yellow);text-decoration:underline;text-decoration-color:rgba(255,230,0,.4);}
.card p.rule{border-top:1px solid rgba(0,232,255,.1);padding-top:12px;margin-top:8px;color:var(--mid);font-size:12px;}

/* ── SECTION HEADER ────────────────────────────────────────── */
.section-hdr{
  font-family:var(--font-game);font-size:10px;letter-spacing:4px;color:var(--cyan);
  padding:16px 26px 8px;
  display:flex;align-items:center;gap:12px;
}
.section-hdr::before{
  content:'';width:28px;height:2px;flex-shrink:0;
  background:linear-gradient(90deg,transparent,var(--cyan));
}
.section-hdr::after{
  content:'';flex:1;height:1px;
  background:linear-gradient(90deg,rgba(0,232,255,.4),transparent);
}

/* ── CUTSCENE / BRIEFING ───────────────────────────────────── */
.cutscene{
  padding:20px 26px;
  background:rgba(0,20,44,.45);
  border-left:2px solid var(--cyan);
}
.spkr{
  display:block;font-family:var(--font-game);font-size:9px;
  color:var(--cyan);letter-spacing:3px;margin-bottom:10px;
  text-shadow:0 0 18px rgba(0,232,255,.6);
}
.cutscene>span:not(.spkr){line-height:1.8;color:var(--light);font-size:clamp(12px,1.6vw,14px);}
.tw-cursor{
  display:inline-block;width:2px;height:1.1em;
  background:var(--cyan);animation:blink .7s step-end infinite;
  vertical-align:text-bottom;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

/* ════════════════════════════════════════════════════════════
   BUTTONS
═════════════════════════════════════════════════════════════*/
.btn-primary{
  font-family:var(--font-game);font-size:clamp(10px,1.8vw,12px);
  color:#030810;
  background:linear-gradient(135deg,var(--cyan),var(--cyan2));
  border:none;padding:18px 58px;border-radius:2px;
  cursor:pointer;letter-spacing:4px;font-weight:900;
  box-shadow:0 0 44px rgba(0,232,255,.55),0 4px 0 var(--cyan3);
  transition:transform .12s,box-shadow .2s;
  display:inline-block;text-decoration:none;
  clip-path:polygon(12px 0,100% 0,calc(100% - 12px) 100%,0 100%);
  position:relative;overflow:hidden;
}
.btn-primary::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.28),transparent);
  transform:translateX(-100%);transition:transform .5s;
}
.btn-primary:hover::after{transform:translateX(100%);}
.btn-primary:hover{
  transform:translateY(-3px) scale(1.02);
  box-shadow:0 0 65px rgba(0,232,255,.85),0 6px 0 var(--cyan3);
}
.btn-primary:active{transform:translateY(1px);box-shadow:0 0 22px rgba(0,232,255,.4),0 2px 0 var(--cyan3);}

.btn-back{
  font-family:var(--font-game);font-size:10px;color:var(--mid);
  border:1px solid rgba(255,255,255,.1);background:rgba(0,0,0,.3);
  padding:8px 18px;border-radius:2px;text-decoration:none;
  display:inline-flex;align-items:center;gap:6px;
  transition:all .15s;letter-spacing:2px;
  clip-path:polygon(6px 0,100% 0,calc(100% - 6px) 100%,0 100%);
}
.btn-back:hover{color:var(--cyan);border-color:rgba(0,232,255,.4);box-shadow:0 0 16px rgba(0,232,255,.2);}

/* ════════════════════════════════════════════════════════════
   MISSION HEADER
═════════════════════════════════════════════════════════════*/
.mission-hdr{display:flex;align-items:center;gap:20px;margin-bottom:24px;}
.mission-num{font-family:var(--font-game);font-size:9px;color:var(--cyan2);letter-spacing:3px;}
.mission-name{
  font-family:var(--font-game);font-size:clamp(14px,2.4vw,20px);
  color:var(--white);letter-spacing:2px;
  text-shadow:0 0 32px rgba(0,232,255,.4);
}

/* ════════════════════════════════════════════════════════════
   BOSS ARENA
═════════════════════════════════════════════════════════════*/
.boss-arena{--cs:22px;border-color:rgba(255,32,64,.18);}
.boss-arena::before{
  background:
    linear-gradient(var(--red),var(--red)) top    left  /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) top    left  /2px var(--cs),
    linear-gradient(var(--red),var(--red)) top    right /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) top    right /2px var(--cs),
    linear-gradient(var(--red),var(--red)) bottom left  /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) bottom left  /2px var(--cs),
    linear-gradient(var(--red),var(--red)) bottom right /var(--cs) 2px,
    linear-gradient(var(--red),var(--red)) bottom right /2px var(--cs);
  background-repeat:no-repeat;opacity:.55;
}
.boss-hdr{padding:20px 26px;display:flex;align-items:center;gap:20px;}
.boss-em{font-size:52px;filter:drop-shadow(0 0 22px rgba(255,32,64,.65));}
.boss-name{
  font-family:var(--font-game);font-size:clamp(14px,2.4vw,18px);
  color:var(--red);letter-spacing:2px;
  text-shadow:0 0 26px rgba(255,32,64,.6);
}
.boss-sub{font-size:12px;color:var(--mid);margin-top:4px;letter-spacing:1px;}
.boss-hp-wrap{margin-top:12px;}
.boss-hp-lbl{font-family:var(--font-game);font-size:9px;color:var(--red);letter-spacing:2px;margin-bottom:6px;}
.boss-hpbg{height:8px;background:rgba(255,32,64,.1);border-radius:2px;overflow:hidden;border:1px solid rgba(255,32,64,.2);}
.boss-hpfill{
  height:100%;width:100%;
  background:linear-gradient(90deg,var(--red2),var(--red));
  transition:width 1s cubic-bezier(.4,0,.2,1);
  box-shadow:0 0 14px rgba(255,32,64,.5);
  position:relative;overflow:hidden;
}
.boss-hpfill::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.2),transparent);
  animation:shimmer 1.5s infinite;
}
.q-text{
  font-family:var(--font-game);font-size:clamp(12px,1.9vw,15px);
  line-height:1.65;color:var(--white);
  padding:16px 26px;letter-spacing:.5px;
  border-top:1px solid rgba(255,32,64,.1);
}

/* ── QUIZ OPTION BUTTONS ───────────────────────────────────── */
#q-opts{padding:0 20px 20px;display:flex;flex-direction:column;gap:10px;}
.qbtn{
  font-family:var(--font-game);font-size:clamp(10px,1.4vw,12px);
  background:rgba(5,12,25,.85);
  border:1px solid rgba(0,232,255,.14);
  color:var(--light);padding:14px 20px;
  cursor:pointer;text-align:left;border-radius:2px;
  transition:all .18s;letter-spacing:1px;
  display:flex;align-items:center;gap:12px;
  position:relative;overflow:hidden;
  clip-path:polygon(8px 0,100% 0,calc(100% - 8px) 100%,0 100%);
}
.q-lbl{font-size:13px;color:var(--cyan);font-weight:900;flex-shrink:0;width:22px;text-align:center;}
.qbtn::before{
  content:'';position:absolute;top:0;left:0;bottom:0;width:3px;
  background:linear-gradient(180deg,var(--cyan),var(--cyan2));
  opacity:0;transition:opacity .18s;
}
.qbtn:hover:not(.done){
  background:rgba(0,232,255,.08);border-color:rgba(0,232,255,.4);color:var(--white);
  box-shadow:0 0 22px rgba(0,232,255,.15),inset 0 0 22px rgba(0,232,255,.05);
}
.qbtn:hover:not(.done)::before{opacity:1;}
.qbtn.ok{background:rgba(57,255,20,.1);border-color:var(--green);color:var(--green);box-shadow:0 0 26px rgba(57,255,20,.3);}
.qbtn.ok::before{background:var(--green);opacity:1;}
.qbtn.bad{background:rgba(255,32,64,.1);border-color:var(--red);color:var(--red);box-shadow:0 0 26px rgba(255,32,64,.3);}
.qbtn.bad::before{background:var(--red);opacity:1;}
.qbtn.done{cursor:not-allowed;opacity:.72;}

/* ── FEEDBACK ──────────────────────────────────────────────── */
.qfb{
  display:none;margin:0 20px 20px;
  padding:16px 20px;border-radius:2px;border-left:3px solid;
  line-height:1.7;font-size:13px;
  animation:feedIn .3s cubic-bezier(.16,1,.3,1);
}
@keyframes feedIn{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:translateX(0)}}
.qfb.win{background:rgba(57,255,20,.07);border-color:var(--green);color:var(--light);}
.qfb.lose{background:rgba(255,32,64,.07);border-color:var(--red);color:var(--light);}

/* ── TIMER ─────────────────────────────────────────────────── */
.timer-wrap{padding:0 20px 6px;display:flex;align-items:center;gap:10px;}
.timer-bar{flex:1;height:5px;background:rgba(255,230,0,.1);border-radius:2px;overflow:hidden;}
.timer-fill{
  height:100%;width:100%;
  background:linear-gradient(90deg,var(--green2),var(--yellow),var(--orange));
  transition:width 1s linear;
  box-shadow:0 0 10px rgba(255,230,0,.4);
}
.timer-num{font-family:var(--font-game);font-size:12px;color:var(--yellow);min-width:28px;text-align:right;}

/* ── NEXT BANNER ───────────────────────────────────────────── */
#next-banner{
  display:none;padding:16px 20px;border-top:1px solid rgba(0,232,255,.1);
  text-align:center;animation:feedIn .4s .1s cubic-bezier(.16,1,.3,1) both;
}
#next-banner.show{display:block;}
.next-btn{
  font-family:var(--font-game);font-size:11px;color:#030810;
  background:linear-gradient(90deg,var(--cyan2),var(--cyan));
  border:none;padding:14px 42px;border-radius:2px;
  cursor:pointer;letter-spacing:3px;font-weight:900;
  box-shadow:0 0 34px rgba(0,232,255,.5);
  clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
  transition:all .15s;text-decoration:none;display:inline-block;
}
.next-btn:hover{transform:translateY(-2px);box-shadow:0 0 55px rgba(0,232,255,.85);}

/* ── HINT BOX ──────────────────────────────────────────────── */
.hint-box{
  display:none;margin:0 20px 10px;
  padding:12px 18px;border-left:2px solid var(--yellow);
  background:rgba(255,230,0,.05);border-radius:2px;
  animation:feedIn .3s ease;
}
.hint-box.show{display:flex;gap:10px;align-items:flex-start;}
.hint-lbl{flex-shrink:0;font-family:var(--font-game);font-size:9px;color:var(--yellow);letter-spacing:2px;}
.fun-fact{color:var(--mid);font-size:12px;line-height:1.6;}

/* ════════════════════════════════════════════════════════════
   METRICS GRID
═════════════════════════════════════════════════════════════*/
.metric-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;padding:16px 20px 20px;}
.metric-card{
  position:relative;overflow:visible;
  background:rgba(4,10,22,.85);border:1px solid rgba(0,232,255,.08);
  border-radius:2px;padding:16px;transition:all .22s;
}
.metric-card::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /1px 10px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /1px 10px;
  background-repeat:no-repeat;opacity:.35;
}
.metric-card:hover{border-color:rgba(0,232,255,.25);transform:translateY(-3px);box-shadow:0 10px 32px rgba(0,0,0,.45),0 0 22px rgba(0,232,255,.1);}
.metric-icon{font-size:24px;margin-bottom:8px;}
.metric-name{font-family:var(--font-game);font-size:10px;color:var(--cyan);letter-spacing:2px;margin-bottom:4px;}
.metric-sub{font-size:10px;color:var(--mid);margin-bottom:8px;}
.metric-desc{font-size:11px;color:var(--light);line-height:1.6;margin-bottom:10px;}
.metric-ranges{display:flex;gap:4px;flex-wrap:wrap;}
.rg{background:rgba(57,255,20,.12);color:var(--green);border:1px solid rgba(57,255,20,.25);}
.ry{background:rgba(255,230,0,.1);color:var(--yellow);border:1px solid rgba(255,230,0,.25);}
.rr{background:rgba(255,32,64,.1);color:var(--red);border:1px solid rgba(255,32,64,.25);}
.rg,.ry,.rr{font-size:9px;padding:3px 7px;border-radius:2px;white-space:nowrap;}

/* ════════════════════════════════════════════════════════════
   PIPELINE
═════════════════════════════════════════════════════════════*/
.pipeline{display:flex;align-items:stretch;gap:0;padding:16px 20px 20px;flex-wrap:wrap;}
.ps{
  flex:1;min-width:100px;padding:16px 14px;text-align:center;
  border:1px solid rgba(0,232,255,.08);background:rgba(4,10,22,.7);
  transition:all .3s;position:relative;
}
.ps+.ps{border-left:none;}
.ps.active{background:rgba(0,232,255,.07);border-color:rgba(0,232,255,.35);box-shadow:0 0 26px rgba(0,232,255,.12) inset;}
.ps-icon{font-size:24px;margin-bottom:8px;display:block;}
.ps-name{font-family:var(--font-game);font-size:9px;color:var(--cyan2);letter-spacing:2px;}
.ps-ms{font-size:11px;color:var(--mid);margin-top:4px;}

/* ════════════════════════════════════════════════════════════
   PRESENT MODE TABLE
═════════════════════════════════════════════════════════════*/
.mode-tbl{width:100%;border-collapse:collapse;font-size:12px;}
.mode-tbl th{
  font-family:var(--font-game);font-size:9px;letter-spacing:2px;
  color:var(--cyan2);padding:10px 12px;text-align:left;
  border-bottom:1px solid rgba(0,232,255,.15);
}
.mode-tbl td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.04);vertical-align:middle;color:var(--light);}
.mode-tbl tr:hover td{background:rgba(0,232,255,.04);}
.mm{font-family:var(--font-game);font-size:9px;color:var(--white);letter-spacing:1px;}
.pb{padding:3px 8px;border-radius:2px;font-family:var(--font-game);font-size:8px;letter-spacing:1px;}
.pb-best{background:rgba(57,255,20,.15);color:var(--green);border:1px solid rgba(57,255,20,.3);}
.pb-good{background:rgba(0,232,255,.12);color:var(--cyan);border:1px solid rgba(0,232,255,.3);}
.pb-ok{background:rgba(255,230,0,.1);color:var(--yellow);border:1px solid rgba(255,230,0,.3);}
.pb-bad{background:rgba(255,32,64,.1);color:var(--red);border:1px solid rgba(255,32,64,.3);}

/* ════════════════════════════════════════════════════════════
   SCENARIO CARDS
═════════════════════════════════════════════════════════════*/
.scenario{padding:18px 22px;border-bottom:1px solid rgba(0,232,255,.06);}
.scenario:last-child{border-bottom:none;}
.scenario-hdr{display:flex;align-items:center;gap:12px;margin-bottom:10px;}
.scenario-icon{font-size:28px;}
.scenario-name{font-family:var(--font-game);font-size:12px;color:var(--white);letter-spacing:1px;}
.scenario-data{font-size:11px;color:var(--mid);margin-top:2px;}
.signs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;}
.sign{padding:4px 10px;border-radius:2px;font-size:10px;}
.sign-ok{background:rgba(57,255,20,.1);color:var(--green);border:1px solid rgba(57,255,20,.25);}
.sign-bad{background:rgba(255,32,64,.1);color:var(--red);border:1px solid rgba(255,32,64,.25);}
.scenario-fix{font-size:12px;color:var(--light);line-height:1.65;padding-top:6px;border-top:1px solid rgba(255,255,255,.04);}

/* ════════════════════════════════════════════════════════════
   STATS / PERCENTILE CARDS
═════════════════════════════════════════════════════════════*/
.pct-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;padding:16px 20px 20px;}
.pct-card{
  background:rgba(4,10,22,.85);border:1px solid rgba(0,232,255,.08);
  border-radius:2px;padding:20px 16px;text-align:center;transition:all .22s;
  position:relative;overflow:visible;
}
.pct-card::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /1px 10px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /1px 10px;
  background-repeat:no-repeat;opacity:.3;
}
.pct-card:hover{border-color:rgba(0,232,255,.25);transform:translateY(-3px);box-shadow:0 8px 28px rgba(0,0,0,.4);}
.pct-num{font-family:var(--font-game);font-size:22px;font-weight:900;margin-bottom:6px;}
.pct-name{font-family:var(--font-game);font-size:10px;color:var(--white);letter-spacing:2px;margin-bottom:8px;}
.pct-desc{font-size:11px;color:var(--mid);line-height:1.6;}

/* ════════════════════════════════════════════════════════════
   CODE BLOCKS
═════════════════════════════════════════════════════════════*/
.codeblock{
  background:rgba(2,6,14,.9);border:1px solid rgba(0,232,255,.12);
  border-radius:2px;padding:16px 18px;margin:12px 0;overflow-x:auto;
  position:relative;
}
.codeblock::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--cyan),transparent);
}
.codeblock pre{font-family:var(--font-mono);font-size:12px;line-height:1.7;color:var(--light);white-space:pre;}
.ck{color:var(--cyan);}
.cf{color:var(--purple);}
.cv{color:var(--yellow);}
.cm{color:var(--mid);font-style:italic;}

/* ════════════════════════════════════════════════════════════
   MAP PAGE
═════════════════════════════════════════════════════════════*/
.map-wrap{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px;
  padding:16px 0;
}
.map-card{
  position:relative;
  background:rgba(5,12,25,.88);
  border:1px solid rgba(0,232,255,.1);
  border-radius:2px;padding:22px 18px;text-align:center;
  text-decoration:none;display:block;
  transition:all .22s;overflow:visible;cursor:pointer;
}
.map-card::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) top    right /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    right /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /2px 14px;
  background-repeat:no-repeat;opacity:.45;transition:opacity .22s;
}
.map-card:hover:not(.locked)::before{opacity:.9;}
.map-card:hover:not(.locked){
  border-color:rgba(0,232,255,.35);
  transform:translateY(-4px) scale(1.02);
  box-shadow:0 12px 40px rgba(0,0,0,.5),0 0 30px rgba(0,232,255,.18);
  background:rgba(0,232,255,.06);
}
.map-card.locked{pointer-events:none;opacity:.35;filter:grayscale(.8);}
.map-card.done::before{
  background:
    linear-gradient(var(--green),var(--green)) top    left  /14px 2px,
    linear-gradient(var(--green),var(--green)) top    left  /2px 14px,
    linear-gradient(var(--green),var(--green)) top    right /14px 2px,
    linear-gradient(var(--green),var(--green)) top    right /2px 14px,
    linear-gradient(var(--green),var(--green)) bottom left  /14px 2px,
    linear-gradient(var(--green),var(--green)) bottom left  /2px 14px,
    linear-gradient(var(--green),var(--green)) bottom right /14px 2px,
    linear-gradient(var(--green),var(--green)) bottom right /2px 14px;
  background-repeat:no-repeat;
}
.mc-icon{font-size:36px;display:block;margin-bottom:10px;filter:drop-shadow(0 0 14px rgba(0,232,255,.5));}
.mc-num{font-family:var(--font-game);font-size:9px;color:var(--cyan2);letter-spacing:3px;margin-bottom:4px;}
.mc-name{font-family:var(--font-game);font-size:11px;color:var(--white);letter-spacing:1px;line-height:1.3;}
.mc-xp{font-size:10px;color:var(--yellow);margin-top:8px;letter-spacing:1px;}
.mc-boss{font-size:11px;color:var(--mid);margin-top:4px;}
.mc-badge{font-size:14px;position:absolute;top:10px;right:12px;}
.map-hdr{font-family:var(--font-game);font-size:clamp(16px,3vw,24px);color:var(--white);letter-spacing:4px;margin-bottom:6px;text-shadow:0 0 30px rgba(0,232,255,.4);}
.map-sub{font-size:12px;color:var(--mid);letter-spacing:2px;margin-bottom:24px;}
.map-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px;}
.btn-danger{
  font-family:var(--font-game);font-size:10px;color:var(--red);
  border:1px solid rgba(255,32,64,.3);background:rgba(255,32,64,.05);
  padding:10px 22px;border-radius:2px;cursor:pointer;letter-spacing:2px;
  clip-path:polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
  transition:all .15s;
}
.btn-danger:hover{background:rgba(255,32,64,.15);border-color:var(--red);box-shadow:0 0 20px rgba(255,32,64,.3);}

/* ════════════════════════════════════════════════════════════
   WIN SCREEN
═════════════════════════════════════════════════════════════*/
.cert-wrap{text-align:center;padding:40px 30px;}
.cert-title{
  font-family:var(--font-game);font-size:clamp(16px,3vw,24px);
  color:var(--gold);letter-spacing:6px;
  text-shadow:0 0 40px rgba(255,215,0,.7),0 0 80px rgba(255,215,0,.3);
  animation:glow 2s ease-in-out infinite alternate;
}
@keyframes glow{from{text-shadow:0 0 30px rgba(255,215,0,.6)}to{text-shadow:0 0 60px rgba(255,215,0,.9),0 0 100px rgba(255,215,0,.5)}}
.cert-sub{font-family:var(--font-game);font-size:10px;color:var(--mid);letter-spacing:4px;margin-top:8px;}
.cert-badges{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:28px 0;}
.cert-badge{font-size:36px;filter:drop-shadow(0 0 12px var(--gold));animation:badgePop .5s ease;}
@keyframes badgePop{0%{transform:scale(0) rotate(-20deg)}80%{transform:scale(1.2) rotate(5deg)}100%{transform:scale(1) rotate(0)}}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;margin:20px 0;}
.stat-card{
  background:rgba(4,10,22,.85);border:1px solid rgba(0,232,255,.1);
  border-radius:2px;padding:16px;text-align:center;
}
.stat-val{font-family:var(--font-game);font-size:22px;color:var(--cyan);font-weight:900;}
.stat-lbl{font-size:10px;color:var(--mid);letter-spacing:2px;margin-top:4px;}

/* ════════════════════════════════════════════════════════════
   INDEX / TITLE SCREEN
═════════════════════════════════════════════════════════════*/
.title-wrap{
  min-height:100vh;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;
  position:relative;z-index:10;padding:40px 20px;
}
.title-logo{
  font-family:var(--font-game);
  font-size:clamp(28px,8vw,72px);
  font-weight:900;line-height:1;letter-spacing:8px;
  color:var(--white);margin-bottom:8px;
  text-shadow:0 0 50px rgba(0,232,255,.6),0 0 100px rgba(0,232,255,.3);
  animation:logoReveal 1s cubic-bezier(.16,1,.3,1) .3s both;
}
@keyframes logoReveal{from{opacity:0;transform:scale(.8) translateY(30px)}to{opacity:1;transform:scale(1) translateY(0)}}
.title-sub{
  font-family:var(--font-game);font-size:clamp(8px,2vw,12px);letter-spacing:6px;
  color:var(--cyan2);margin-bottom:50px;
  animation:logoReveal .8s cubic-bezier(.16,1,.3,1) .6s both;
}
.title-btns{
  display:flex;flex-direction:column;align-items:center;gap:14px;
  animation:logoReveal .8s cubic-bezier(.16,1,.3,1) .9s both;
}

/* ════════════════════════════════════════════════════════════
   RADAR RING (title screen decoration)
═════════════════════════════════════════════════════════════*/
.radar-ring{
  position:absolute;width:clamp(260px,50vw,500px);height:clamp(260px,50vw,500px);
  border-radius:50%;border:1px solid rgba(0,232,255,.08);
  pointer-events:none;animation:radarSpin 12s linear infinite;
}
.radar-ring::before{
  content:'';position:absolute;inset:20px;border-radius:50%;
  border:1px solid rgba(0,232,255,.05);
}
.radar-ring::after{
  content:'';position:absolute;top:50%;left:50%;
  width:50%;height:1px;background:linear-gradient(90deg,transparent,rgba(0,232,255,.4));
  transform-origin:left center;animation:radarSpin 3s linear infinite;
}
@keyframes radarSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}

/* ════════════════════════════════════════════════════════════
   EFFECTS
═════════════════════════════════════════════════════════════*/
.xp-pop{
  position:fixed;left:50%;transform:translateX(-50%);
  top:70px;z-index:9500;pointer-events:none;
  font-family:var(--font-game);font-size:16px;color:var(--yellow);font-weight:900;
  text-shadow:0 0 20px rgba(255,230,0,.8);
  animation:xpFloat 2.2s cubic-bezier(.16,1,.3,1) both;
}
@keyframes xpFloat{0%{opacity:0;transform:translateX(-50%) translateY(0)}20%{opacity:1}80%{opacity:1}100%{opacity:0;transform:translateX(-50%) translateY(-60px)}}
.dmg-flash{
  position:fixed;inset:0;z-index:9500;pointer-events:none;
  background:rgba(255,32,64,.25);animation:dmgFlash .44s ease;
}
@keyframes dmgFlash{0%,100%{opacity:0}30%{opacity:1}}
.screen-shake{animation:shake .44s cubic-bezier(.36,.07,.19,.97);}
@keyframes shake{0%,100%{transform:translate(0)}20%{transform:translate(-5px,2px)}40%{transform:translate(4px,-2px)}60%{transform:translate(-3px,1px)}80%{transform:translate(3px,-1px)}}

.particle{position:fixed;border-radius:50%;pointer-events:none;z-index:9490;animation:ptFly var(--pt,.9s) cubic-bezier(.2,0,.8,1) both;}
@keyframes ptFly{from{opacity:1;transform:translate(0,0) scale(1)}to{opacity:0;transform:translate(var(--px,0),var(--py,-80px)) scale(0)}}
.confetti-piece{position:fixed;width:8px;height:8px;pointer-events:none;z-index:9490;border-radius:2px;animation:confFly var(--ct,1.4s) var(--cd,0s) cubic-bezier(.2,0,.8,1) both;}
@keyframes confFly{from{opacity:1;transform:translate(0,0) rotate(0)}to{opacity:0;transform:translate(var(--cx,0),var(--cy,200px)) rotate(540deg)}}
.achievement-toast{
  position:fixed;bottom:24px;right:24px;z-index:9600;
  background:rgba(5,12,25,.95);border:1px solid rgba(0,232,255,.22);
  padding:14px 18px;border-radius:2px;min-width:220px;
  animation:toastIn .4s cubic-bezier(.16,1,.3,1);
  box-shadow:0 8px 32px rgba(0,0,0,.5);
}
.achievement-toast::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /10px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /2px 10px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /10px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /2px 10px;
  background-repeat:no-repeat;opacity:.7;
}
@keyframes toastIn{from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:translateX(0)}}
.toast-title{font-family:var(--font-game);font-size:9px;color:var(--cyan);letter-spacing:3px;margin-bottom:6px;}
.toast-body{font-size:12px;color:var(--light);line-height:1.5;}

/* ════════════════════════════════════════════════════════════
   UTILITY
═════════════════════════════════════════════════════════════*/
a{color:inherit;text-decoration:none;}
.page-enter{animation:pageEnter .5s cubic-bezier(.16,1,.3,1) both;}
.neon-cyan{color:var(--cyan);text-shadow:0 0 18px rgba(0,232,255,.6);}

/* ════════════════════════════════════════════════════════════
   MAP PAGE  (mcard / mgrid — matches map.py HTML)
═════════════════════════════════════════════════════════════*/
.page{position:relative;z-index:10;}
.map-wrap{
  max-width:1100px;margin:0 auto;padding:90px 22px 60px;
  animation:pageEnter .5s cubic-bezier(.16,1,.3,1) both;
}
.map-title{
  font-family:var(--font-game);font-size:clamp(16px,3vw,24px);
  color:var(--white);letter-spacing:4px;margin-bottom:6px;
  text-shadow:0 0 30px rgba(0,232,255,.4);
}
.map-sub{font-size:12px;color:var(--mid);letter-spacing:2px;margin-bottom:18px;}

/* Progress bar */
.map-progress{margin-bottom:22px;}
.map-progress-lbl{font-family:var(--font-game);font-size:9px;color:var(--cyan2);letter-spacing:3px;margin-bottom:6px;}
.map-progress-bar{height:6px;background:rgba(0,232,255,.08);border-radius:3px;overflow:hidden;border:1px solid rgba(0,232,255,.1);}
.map-progress-fill{
  height:100%;background:linear-gradient(90deg,var(--cyan2),var(--cyan));
  border-radius:3px;transition:width .8s cubic-bezier(.4,0,.2,1);
  box-shadow:0 0 12px rgba(0,232,255,.5);
}

/* Mission card grid */
.mgrid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
  gap:16px;margin-bottom:24px;
}

/* Individual mission card */
.mcard{
  position:relative;overflow:visible;
  background:rgba(5,12,25,.9);
  border:1px solid rgba(0,232,255,.1);
  border-radius:2px;padding:20px 16px 18px;
  text-align:center;text-decoration:none;display:block;
  transition:all .22s;cursor:pointer;
}
/* corner brackets */
.mcard::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) top    right /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) top    right /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom left  /2px 14px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /14px 2px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /2px 14px;
  background-repeat:no-repeat;opacity:.45;transition:opacity .22s;
}
.mcard:hover:not(.locked)::before{opacity:.9;}
.mcard:hover:not(.locked){
  border-color:rgba(0,232,255,.35);
  transform:translateY(-4px) scale(1.02);
  box-shadow:0 12px 40px rgba(0,0,0,.5),0 0 28px rgba(0,232,255,.18);
  background:rgba(0,232,255,.06);
}
/* locked */
.mcard.locked{
  pointer-events:none;opacity:.32;filter:grayscale(.9);
}
/* done */
.mcard.done::before{
  background:
    linear-gradient(var(--green),var(--green)) top    left  /14px 2px,
    linear-gradient(var(--green),var(--green)) top    left  /2px 14px,
    linear-gradient(var(--green),var(--green)) top    right /14px 2px,
    linear-gradient(var(--green),var(--green)) top    right /2px 14px,
    linear-gradient(var(--green),var(--green)) bottom left  /14px 2px,
    linear-gradient(var(--green),var(--green)) bottom left  /2px 14px,
    linear-gradient(var(--green),var(--green)) bottom right /14px 2px,
    linear-gradient(var(--green),var(--green)) bottom right /2px 14px;
  background-repeat:no-repeat;
}
.mcard.available{border-color:rgba(0,232,255,.22);}

/* Done check */
.mcard-done{
  display:none;position:absolute;top:8px;right:10px;
  font-family:var(--font-game);font-size:8px;
  color:var(--green);letter-spacing:1px;
}
/* Card content */
.mcard-icon{font-size:36px;display:block;margin-bottom:10px;filter:drop-shadow(0 0 12px rgba(0,232,255,.45));}
.mcard-num{font-family:var(--font-game);font-size:9px;color:var(--cyan2);letter-spacing:3px;margin-bottom:5px;}
.mcard-name{font-family:var(--font-game);font-size:11px;color:var(--white);letter-spacing:1px;line-height:1.35;margin-bottom:6px;}
.mcard-desc{font-size:11px;color:var(--mid);line-height:1.5;margin-bottom:10px;min-height:32px;}
.mcard-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.mcard-xp{font-family:var(--font-game);font-size:10px;color:var(--yellow);letter-spacing:1px;}
.mcard-stars{display:flex;gap:3px;}
.mcard-star{font-size:12px;color:var(--yellow);}
.mcard-star.dim{color:var(--border3);}
.mcard-flavor{font-size:10px;color:var(--dim);font-style:italic;line-height:1.4;border-top:1px solid rgba(0,232,255,.06);padding-top:8px;margin-top:2px;}
.boss-preview{position:absolute;bottom:8px;right:10px;font-size:14px;opacity:.5;}

/* Map footer */
.map-footer{display:flex;gap:12px;flex-wrap:wrap;padding-top:8px;}

/* ════════════════════════════════════════════════════════════
   MISC FIXES
═════════════════════════════════════════════════════════════*/
/* Duplicate text-decoration fix for hud-quit */
.hud-quit{text-decoration:none;}
/* btn-danger (reset button on map) */
.btn-danger{
  font-family:var(--font-game);font-size:10px;color:var(--red);
  border:1px solid rgba(255,32,64,.28);background:rgba(255,32,64,.05);
  padding:9px 20px;border-radius:2px;cursor:pointer;letter-spacing:2px;
  clip-path:polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%);
  transition:all .15s;
}
.btn-danger:hover{background:rgba(255,32,64,.15);border-color:var(--red);box-shadow:0 0 20px rgba(255,32,64,.3);}

/* ════════════════════════════════════════════════════════════
   MISSING BUTTON VARIANTS  (used in win.py, index.py, missions)
═════════════════════════════════════════════════════════════*/
.btn-green{
  font-family:var(--font-game);font-size:11px;color:#030810;
  background:linear-gradient(135deg,var(--green2),var(--green));
  border:none;padding:14px 36px;border-radius:2px;
  cursor:pointer;letter-spacing:3px;font-weight:900;
  box-shadow:0 0 30px rgba(57,255,20,.5),0 3px 0 var(--green3);
  clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
  transition:all .15s;display:inline-block;text-decoration:none;
}
.btn-green:hover{transform:translateY(-2px);box-shadow:0 0 50px rgba(57,255,20,.8);}

.btn-yellow{
  font-family:var(--font-game);font-size:11px;color:#030810;
  background:linear-gradient(135deg,var(--gold2),var(--yellow));
  border:none;padding:14px 36px;border-radius:2px;
  cursor:pointer;letter-spacing:3px;font-weight:900;
  box-shadow:0 0 30px rgba(255,230,0,.5),0 3px 0 rgba(100,80,0,.8);
  clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);
  transition:all .15s;display:inline-block;text-decoration:none;
}
.btn-yellow:hover{transform:translateY(-2px);box-shadow:0 0 50px rgba(255,230,0,.8);}

/* ════════════════════════════════════════════════════════════
   WIN SCREEN — stat items
═════════════════════════════════════════════════════════════*/
.stat-item{
  background:rgba(4,10,22,.85);border:1px solid rgba(0,232,255,.1);
  border-radius:2px;padding:16px;text-align:center;
  position:relative;overflow:visible;
}
.stat-item::before{
  content:'';position:absolute;inset:-1px;pointer-events:none;
  background:
    linear-gradient(var(--cyan),var(--cyan)) top    left  /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) top    left  /1px 10px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /10px 1px,
    linear-gradient(var(--cyan),var(--cyan)) bottom right /1px 10px;
  background-repeat:no-repeat;opacity:.35;
}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:12px;margin:20px 0;}
.stat-val{font-family:var(--font-game);font-size:22px;color:var(--cyan);font-weight:900;}
.stat-lbl{font-size:10px;color:var(--mid);letter-spacing:2px;margin-top:4px;}

/* cert wrap */
.cert-wrap{text-align:center;padding:30px;width:100%;max-width:640px;}
.cert-stamp{animation:pageEnter .6s cubic-bezier(.16,1,.3,1) both;}

/* ════════════════════════════════════════════════════════════
   TIMER LABEL  (used inside timer-wrap)
═════════════════════════════════════════════════════════════*/
.timer-lbl{font-family:var(--font-game);font-size:9px;color:var(--mid);letter-spacing:2px;flex-shrink:0;}

/* ════════════════════════════════════════════════════════════
   RADAR RINGS (r1 / r2 / r3 used in index.py)
═════════════════════════════════════════════════════════════*/
.radar-ring{
  position:absolute;border-radius:50%;
  border:1px solid rgba(0,232,255,.12);
}
.radar-ring.r1{inset:0;animation:radarSpin 14s linear infinite;}
.radar-ring.r2{inset:30px;animation:radarSpin 9s linear infinite reverse;}
.radar-ring.r3{inset:60px;animation:radarSpin 20s linear infinite;}
/* The sweep arm — on r1 only */
.radar-ring.r1::after{
  content:'';position:absolute;top:50%;left:50%;
  width:50%;height:1px;
  background:linear-gradient(90deg,rgba(0,232,255,.5),transparent);
  transform-origin:left center;
  animation:radarSpin 4s linear infinite;
}
@keyframes radarSpin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

/* ════════════════════════════════════════════════════════════
   TITLE LOGO  (bigger, more impactful game font)
═════════════════════════════════════════════════════════════*/
.title-logo{
  font-family:var(--font-game);
  font-size:clamp(22px,6vw,38px);
  font-weight:900;line-height:1.1;letter-spacing:6px;
  color:var(--white);
  text-shadow:0 0 40px rgba(0,232,255,.7),0 0 80px rgba(0,232,255,.3);
  text-align:center;
}

/* ════════════════════════════════════════════════════════════
   IMPROVED FONT SIZES  — game-quality readability
═════════════════════════════════════════════════════════════*/
/* Bigger boss name */
.boss-name{font-size:clamp(16px,3vw,22px) !important;}
/* Bigger question text */
.q-text{font-size:clamp(13px,2vw,16px) !important;padding:20px 28px !important;}
/* Bigger quiz options */
.qbtn{font-size:clamp(11px,1.6vw,13px) !important;padding:16px 22px !important;}
/* Bigger card title */
.card-ttl{font-size:clamp(14px,2.2vw,18px) !important;}
/* Bigger card text */
.card p{font-size:clamp(13px,1.8vw,15px) !important;line-height:1.8 !important;}
/* Bigger mission name */
.mission-name{font-size:clamp(16px,3vw,22px) !important;}
"""
