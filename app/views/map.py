"""app/views/map.py — Mission selection map."""
from app.templates.base import base
from app.templates.components import hud
from app.models import MISSIONS


def render_map() -> str:
    cards_html = ""
    for m in MISSIONS:
        stars_html = "".join(
            f'<span class="mc-star{"" if i < m.difficulty_stars else " dim"}">★</span>'
            for i in range(3)
        )
        cards_html += f"""
<a href="mission-{m.id + 1}.html" class="mcard" id="mc{m.id}"
   data-mid="{m.id}" data-xp="{m.xp}">
  <span class="mc-done" id="mc-done-{m.id}">✔ DONE</span>
  <span class="mc-icon">{m.icon}</span>
  <div class="mc-num">CASE {m.id + 1:02d}</div>
  <div class="mc-name">{m.name}</div>
  <div class="mc-desc">{m.desc}</div>
  <div class="mc-meta">
    <span class="mc-xp">+{m.xp} XP</span>
    <span class="mc-stars">{stars_html}</span>
  </div>
  <div class="mc-flavor">&ldquo;{m.flavor_quote}&rdquo;</div>
  <span class="mc-boss">{m.boss_emoji}</span>
</a>"""

    body = hud(quit_href="index.html") + f"""
<div class="map-page">
<div class="map-inner">

  <div class="map-heading">MISSION SELECT</div>
  <div class="map-sub">CHOOSE YOUR NEXT CASE, AGENT</div>

  <div class="map-progress">
    <div id="map-prog-lbl">PROGRESS: 0 / 8 CASES</div>
    <div class="map-prog-track">
      <div id="map-prog-fill" style="width:0%"></div>
    </div>
  </div>

  <div class="mission-grid">{cards_html}
  </div>

  <div class="map-footer">
    <a href="index.html" class="btn btn-ghost">← BACK</a>
  </div>

</div>
</div>"""

    extra_js = """
(function() {
  var s        = loadState();
  var done     = s.done || [];
  var total    = 8;
  var pct      = Math.round(done.length / total * 100);
  var fill     = document.getElementById('map-prog-fill');
  var lbl      = document.getElementById('map-prog-lbl');
  if (fill) fill.style.width = pct + '%';
  if (lbl)  lbl.textContent  = 'PROGRESS: ' + done.length + ' / ' + total + ' CASES';

  /* Mark done and lock future missions */
  for (var i = 0; i < total; i++) {
    var card = document.getElementById('mc' + i);
    var dnBadge = document.getElementById('mc-done-' + i);
    if (!card) continue;
    if (done.indexOf(i) !== -1) {
      card.classList.add('done');
      if (dnBadge) dnBadge.style.display = 'block';
    } else if (i > 0 && done.indexOf(i - 1) === -1) {
      card.classList.add('locked');
    }
  }
})();
"""
    return base("Mission Select", body, extra_js)
