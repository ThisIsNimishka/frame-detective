"""app/views/index.py — Title screen."""
from app.templates.base import base
from app.templates.components import hud


def render_index() -> str:
    body = hud() + """
<div class="page">
<div class="wrap" style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-top:80px;">

  <!-- Radar rings -->
  <div class="radar-wrap" style="position:relative;width:260px;height:260px;margin:0 auto 44px;flex-shrink:0;">
    <div class="radar-ring r1"></div>
    <div class="radar-ring r2"></div>
    <div class="radar-ring r3"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:0;">
      <div class="title-logo" id="title-logo">FRAME<br>DETECTIVE</div>
      <div style="font-size:9px;color:var(--dim);letter-spacing:4px;margin-top:8px;font-family:var(--font-game)">v2.0</div>
    </div>
  </div>

  <!-- Briefing text (typewriter) -->
  <div class="cutscene" style="max-width:540px;margin:0 auto 40px;text-align:left;">
    <span class="spkr">▸ DIRECTOR INTEL</span>
    <span data-tw="A lag spike hit. The gamer is blaming the GPU. The boss wants answers in 8 missions. Welcome to the Frame Detective Bureau. We see every frame."></span>
  </div>

  <!-- CTA Buttons -->
  <div id="start-btns" style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;">
    <button class="btn-primary" onclick="startNewGame()">BEGIN MISSION</button>
    <button id="btn-continue" class="btn-yellow" onclick="continueGame()" style="display:none">▶ CONTINUE</button>
  </div>

  <div style="margin-top:26px;font-size:12px;color:var(--dim);letter-spacing:2px;">
    PRESS ANY KEY OR CLICK TO START
  </div>
</div>
</div>"""

    extra_js = """
/* check for previous save */
(function() {
  var s = loadState();
  if (s && s.done && s.done.length > 0) {
    var btn = document.getElementById('btn-continue');
    if (btn) btn.style.display = 'inline-block';
  }
})();

function startNewGame() {
  clearState();
  playSound('click');
  window.location.href = 'map.html';
}
function continueGame() {
  playSound('click');
  /* find lowest incomplete mission */
  var s = loadState();
  if (!s) { window.location.href = 'map.html'; return; }
  var next = 0;
  while (s.done.indexOf(next) !== -1 && next < 8) next++;
  if (next >= 8) { window.location.href = 'win.html'; return; }
  window.location.href = 'mission-' + (next + 1) + '.html';
}

/* Title glitch animation */
var logo = document.getElementById('title-logo');
if (logo) {
  setInterval(function() {
    if (Math.random() > 0.85) {
      logo.style.textShadow = '3px 0 var(--red), -3px 0 var(--cyan)';
      logo.style.transform  = 'translate(' + (Math.random()*4-2) + 'px, 0) skewX(' + (Math.random()*3-1.5) + 'deg)';
      setTimeout(function() {
        logo.style.textShadow = '0 0 40px rgba(0,245,255,.6), 0 0 100px rgba(0,245,255,.2)';
        logo.style.transform  = '';
      }, 80);
    }
  }, 1800);
}

/* click anywhere to start */
document.addEventListener('keydown', function(e) {
  if (e.key === ' ' || e.key === 'Enter') { startNewGame(); }
});

/* Check for prev-save marker (for tests) */
document.getElementById('start-btns').setAttribute('data-prev-save', 'check');
"""
    return base("Frame Detective", body, extra_js)
