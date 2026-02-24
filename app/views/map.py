"""app/views/map.py — Mission select view."""
from app.templates.base import base
from app.templates.components import hud
from app.models import MISSIONS


def render_map() -> str:
    cards_html = ""
    for m in MISSIONS:
        cls = "mcard"
        cards_html += f"""
    <a href="mission-{m.id+1}.html" class="{cls}" id="mc{m.id}">
      <div id="mc-done-{m.id}" class="mc-done-badge" style="display:none">SOLVED</div>
      <div id="mc-flavor-{m.id}" style="display:none">{m.flavor_quote}</div>
      <div class="mc-icon">{m.icon}</div>
      <div class="mc-name">{m.name}</div>
      <div class="mc-sub">ZONE {m.id+1}</div>
    </a>"""

    body = hud(quit_href="/quit") + f"""
<div class="page-wrap">
  <div class="map-header">
    <div>
      <h2 style="margin:0;color:var(--cyan);letter-spacing:2px;">MISSION SELECT</h2>
      <div id="map-prog-lbl" style="font-size:12px;color:var(--muted);margin-top:5px;">PROGRESS: 0 / 8 CASES</div>
    </div>
    <div class="map-prog-bg"><div id="map-prog-fill" class="map-prog-fill"></div></div>
  </div>

  <div class="mission-grid">
    {cards_html}
  </div>
</div>"""

    extra_js = """
(function() {
  var s        = loadState();
  var done     = s.done || [];
  
  // Ensure we only count unique missions up to 8
  var uniqueDone = [];
  for(var k=0; k<done.length; k++) {
    var mid = parseInt(done[k]);
    if(uniqueDone.indexOf(mid) === -1 && mid < 8) uniqueDone.push(mid);
  }
  
  var total    = 8;
  var pct      = Math.round(uniqueDone.length / total * 100);
  var fill     = document.getElementById('map-prog-fill');
  var lbl      = document.getElementById('map-prog-lbl');
  if (fill) fill.style.width = pct + '%';
  if (lbl)  lbl.textContent  = 'PROGRESS: ' + uniqueDone.length + ' / ' + total + ' CASES';

  /* Mark done and lock future missions */
  var firstUncompleted = -1;
  for (var i = 0; i < 8; i++) {
    if (uniqueDone.indexOf(i) === -1) {
      firstUncompleted = i;
      break;
    }
  }

  for (var j = 0; j < total; j++) {
    var card = document.getElementById('mc' + j);
    var dnBadge = document.getElementById('mc-done-' + j);
    if (!card) continue;
    
    if (uniqueDone.indexOf(j) !== -1) {
      card.classList.add('done');
      if (dnBadge) dnBadge.style.display = 'block';
    } else if (firstUncompleted !== -1 && j > firstUncompleted) {
      card.classList.add('locked');
      card.removeAttribute('href'); // Truly lock it
    }
  }
})();
"""
    return base("Mission Select", body, extra_js)
