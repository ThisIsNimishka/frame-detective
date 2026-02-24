"""app/views/index.py — Title screen."""
from app.templates.base import base
from app.templates.components import hud, briefing


def render_index() -> str:
    body = hud(quit_href="/") + """
<div class="title-screen">

  <!-- Radar rings with FRAME DETECTIVE logo -->
  <div class="radar-wrap">
    <div class="radar-ring r1"></div>
    <div class="radar-ring r2"></div>
    <div class="radar-ring r3"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;">
      <div class="title-name">FRAME<br>DETECTIVE</div>
      <div class="title-tagline">INTEL PRESENTMON</div>
    </div>
  </div>

  <!-- Briefing typewriter -->
  <div class="title-brief panel">
""" + briefing("DIRECTOR INTEL",
    "A lag spike hit. The gamer is blaming the GPU. The boss wants answers in 8 missions. "
    "Welcome to the Frame Detective Bureau. We see every frame.") + """
  </div>

  <!-- CTA -->
  <div class="title-btns">
    <button class="btn btn-cyan" onclick="startNewGame()">BEGIN MISSION</button>
    <button id="btn-continue" class="btn btn-yellow" onclick="continueGame()" style="display:none">▶ CONTINUE</button>
  </div>

  <div style="margin-top:22px;font-family:var(--font-h);font-size:9px;color:var(--dim);letter-spacing:3px;">
    PRESS ENTER OR CLICK TO START
  </div>

</div>"""

    extra_js = """
/* Show continue button if save exists */
(function() {
  var s = loadState();
  if (s && s.done && s.done.length > 0) {
    var btn = document.getElementById('btn-continue');
    if (btn) btn.style.display = 'inline-flex';
  }
})();

function startNewGame() {
  clearState();
  navigateTo('map.html');
}

function continueGame() {
  var s = loadState();
  if (!s) { navigateTo('map.html'); return; }
  var next = 0;
  while (s.done.indexOf(next) !== -1 && next < 8) next++;
  if (next >= 8) { navigateTo('win.html'); return; }
  navigateTo('mission-' + (next + 1) + '.html');
}

/* Enter key starts game */
document.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); startNewGame(); }
});

/* Logo glitch effect */
(function() {
  var logo = document.querySelector('.title-name');
  if (!logo) return;
  setInterval(function() {
    if (Math.random() > 0.82) {
      logo.style.textShadow = '3px 0 var(--red), -3px 0 var(--cyan)';
      logo.style.transform  = 'translate(' + (Math.random()*5-2.5).toFixed(1) + 'px, 0)';
      setTimeout(function() {
        logo.style.textShadow = '';
        logo.style.transform  = '';
      }, 80);
    }
  }, 1600);
})();
"""
    return base("Frame Detective", body, extra_js)
