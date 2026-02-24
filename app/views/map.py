"""app/views/map.py — Mission select map with quit/menu option."""
from app.templates.base import base
from app.templates.components import hud
from app.models import MISSIONS


def render_map() -> str:
    cards = []
    for m in MISSIONS:
        stars_html = "".join(
            f'<span class="mcard-star{"" if i < m.difficulty_stars else " dim"}">★</span>'
            for i in range(3)
        )
        cards.append(
            f'<a id="mc{m.id}" href="mission-{m.id + 1}.html" class="mcard locked" '
            f'onclick="playSound(\'click\')">'
            f'<span class="mcard-done" id="mcd{m.id}">✓ DONE</span>'
            f'<span class="mcard-icon">{m.icon}</span>'
            f'<div class="mcard-num">MISSION {str(m.id + 1).zfill(2)}</div>'
            f'<div class="mcard-name">{m.name}</div>'
            f'<div class="mcard-desc">{m.desc}</div>'
            f'<div class="mcard-meta">'
            f'  <span class="mcard-xp">+{m.xp} XP</span>'
            f'  <div class="mcard-stars">{stars_html}</div>'
            f'</div>'
            f'<div class="mcard-flavor">"{m.flavor_quote}"</div>'
            f'<span class="boss-preview">{m.boss_emoji}</span>'
            f'</a>'
        )

    body = hud() + f"""
<div class="page">
<div class="map-wrap">
  <div class="map-title">SELECT MISSION</div>
  <div class="map-sub">Navigate through 8 cases. Master every frame.</div>

  <div class="map-progress">
    <div class="map-progress-lbl" id="map-prog-lbl">0 / 8 COMPLETE</div>
    <div class="map-progress-bar">
      <div class="map-progress-fill" id="map-prog-fill" style="width:0%"></div>
    </div>
  </div>

  <div class="mgrid">
    {"".join(cards)}
  </div>

  <div class="map-footer">
    <a href="index.html" class="btn-back" onclick="playSound('click')">⬅ MAIN MENU</a>
    <button class="btn-back" style="background:rgba(255,34,68,.05);border-color:rgba(255,34,68,.2);color:var(--dim)"
      onclick="if(confirm('Reset all progress?')){{clearState();location.reload();}}">
      🔄 RESET
    </button>
  </div>
</div>
</div>"""

    extra_js = """
(function() {
  var s = getState();
  var done = s.done || [];

  /* unlock first undone mission and all done ones */
  var firstUndone = null;
  for (var i = 0; i < 8; i++) {
    var card = document.getElementById('mc' + i);
    var doneLabel = document.getElementById('mcd' + i);
    if (!card) continue;
    var isDone = done.indexOf(i) !== -1;
    var isNext = (firstUndone === null && !isDone);

    if (isDone) {
      card.classList.remove('locked');
      card.classList.add('done', 'clickable');
      if (doneLabel) doneLabel.style.display = 'block';
    } else if (isNext) {
      firstUndone = i;
      card.classList.remove('locked');
      card.classList.add('available', 'clickable');
    }
    /* all others stay locked */
  }
  /* First mission always unlocked */
  var mc0 = document.getElementById('mc0');
  if (mc0 && mc0.classList.contains('locked')) {
    mc0.classList.remove('locked');
    mc0.classList.add('available', 'clickable');
  }

  /* Progress bar */
  var pct = Math.round((done.length / 8) * 100);
  var fill = document.getElementById('map-prog-fill');
  var lbl  = document.getElementById('map-prog-lbl');
  if (fill) fill.style.width = pct + '%';
  if (lbl)  lbl.textContent  = done.length + ' / 8 COMPLETE';
})();
"""
    return base("Mission Map", body, extra_js)
