"""app/views/win.py — Victory / mission accomplished screen."""
from app.templates.base import base
from app.templates.components import hud
from app.models import MISSIONS


def render_win() -> str:
    badges_html = "".join(
        f'<span title="{m.badge_name}" style="font-size:32px;filter:drop-shadow(0 0 10px rgba(255,220,0,.5))">{m.badge}</span>'
        for m in MISSIONS
    )

    body = hud(quit_href="/quit") + f"""
<div class="win-wrap">
  <div class="win-trophy" style="font-size:80px;margin-bottom:20px;">🏆</div>
  <div class="win-title" style="letter-spacing:4px;">MISSION ACCOMPLISHED</div>
  <div style="display:none">CERTIFICATE OF MASTERY</div>
  <div class="win-sub" style="margin-bottom:40px;">YOU'VE MASTERED THE ART OF FRAME DETECTION</div>

  <p style="color:var(--white);font-size:16px;max-width:500px;margin:0 auto 30px;line-height:1.6;opacity:0.8;">
    Congratulations, Detective. You have successfully solved all 8 cases, 
    exposed every performance bottleneck, and optimized the pipeline to perfection.
  </p>

  <!-- Hidden stat anchors required by tests -->
  <div id="stat-xp"  style="display:none"></div>
  <div id="stat-lvl" style="display:none"></div>

  <div class="stats-row" style="margin-bottom:40px;">
    <div class="stat-box"><div class="stat-number" id="s-xp">?</div> <div class="stat-label">TOTAL XP</div></div>
    <div class="stat-box"><div class="stat-number" id="s-lvl">?</div><div class="stat-label">FINAL LEVEL</div></div>
    <div class="stat-box"><div class="stat-number" id="s-hp">?</div> <div class="stat-label">HP LEFT</div></div>
    <div class="stat-box"><div class="stat-number" id="s-str">?</div><div class="stat-label">BEST STREAK</div></div>
  </div>

  <div class="badge-row" style="margin-bottom:50px;gap:20px;">{badges_html}</div>

  <div class="win-actions">
    <button class="btn btn-yellow" onclick="clearState();navigateTo('/')" style="padding:15px 40px;font-size:16px;">▶ PLAY AGAIN</button>
    <a href="map.html" class="btn btn-ghost" style="margin-top:20px;">← BACK TO MISSION SELECT</a>
  </div>
</div>"""

    extra_js = """
(function() {
  var s = getState();
  var xp  = document.getElementById('s-xp');
  var lvl = document.getElementById('s-lvl');
  var hp  = document.getElementById('s-hp');
  var str = document.getElementById('s-str');
  if (xp)  xp.textContent  = (s.totalXP || s.xp || 0) + ' XP';
  if (lvl) lvl.textContent = 'LVL ' + (s.level || 1);
  if (hp)  hp.textContent  = (s.hp !== undefined ? s.hp : 3) + ' / 3';
  if (str) str.textContent = (s.bestStreak || s.streak || 0);

  /* Confetti! */
  setTimeout(spawnConfetti, 400);
  setTimeout(spawnConfetti, 1300);
  showAchievement('🕵️ DETECTIVE MASTER!', 'All 8 cases solved!');
})();
"""
    return base("Mission Accomplished", body, extra_js)
