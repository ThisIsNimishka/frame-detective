"""app/views/win.py — Win / certificate screen."""
from app.templates.base import base
from app.templates.components import hud
from app.models import MISSIONS


def render_win() -> str:
    badges_html = "".join(
        f'<span title="{m.badge_name}" style="font-size:30px;filter:drop-shadow(0 0 8px rgba(255,220,0,.6))">{m.badge}</span>'
        for m in MISSIONS
    )

    body = hud() + f"""
<div class="page">
<div class="wrap" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding-top:88px;padding-bottom:60px;">
<div class="cert-wrap cert-stamp page-enter">

  <div style="text-align:center;margin-bottom:30px;">
    <div style="font-size:62px;margin-bottom:8px;">🏆</div>
    <div style="font-family:var(--font-game);font-size:clamp(16px,3vw,28px);color:var(--yellow);letter-spacing:3px;margin-bottom:6px;text-shadow:0 0 24px rgba(255,220,0,.5)">
      CERTIFICATE OF MASTERY
    </div>
    <div style="font-size:13px;color:var(--dim);letter-spacing:2px;">FRAME DETECTIVE — INTEL PRESENTMON</div>
  </div>

  <div style="text-align:center;margin-bottom:28px;">
    <p style="font-size:14px;color:var(--mid);margin-bottom:12px;line-height:1.8">
      This certifies that Agent
    </p>
    <input id="agent-name" type="text" placeholder="Enter your name..."
      style="background:rgba(0,245,255,.05);border:1px solid var(--border2);color:var(--white);
             padding:12px 20px;font-size:1.1rem;text-align:center;border-radius:8px;
             width:100%;max-width:320px;outline:none;font-family:var(--font-game);letter-spacing:2px;"
      oninput="document.getElementById('cert-name').textContent=this.value||'AGENT'"
    />
    <div id="cert-name" style="font-family:var(--font-game);font-size:1.5rem;color:var(--cyan);margin-top:12px;letter-spacing:3px;text-shadow:0 0 20px rgba(0,245,255,.4)">AGENT</div>
    <p style="font-size:14px;color:var(--mid);margin-top:10px;line-height:1.8">
      has completed all 8 cases and mastered Intel PresentMon frame analysis.
    </p>
  </div>

  <div id="stat-xp" style="display:none"></div>
  <div id="stat-lvl" style="display:none"></div>
  <div class="stats-grid" id="stats-grid">
    <div class="stat-item"><div class="stat-val" id="s-xp">?</div><div class="stat-lbl">TOTAL XP</div></div>
    <div class="stat-item"><div class="stat-val" id="s-lvl">?</div><div class="stat-lbl">FINAL LEVEL</div></div>
    <div class="stat-item"><div class="stat-val" id="s-hp">?</div><div class="stat-lbl">HP LEFT</div></div>
    <div class="stat-item"><div class="stat-val" id="s-str">?</div><div class="stat-lbl">BEST STREAK</div></div>
  </div>

  <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:28px;">
    {badges_html}
  </div>

  <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin-top:32px;">
    <button class="btn-green" onclick="window.print();playSound('click')">🖨 PRINT CERT</button>
    <button class="btn-yellow" onclick="clearState();window.location.href='index.html';playSound('click')">▶ PLAY AGAIN</button>
    <a href="map.html" class="btn-back" onclick="playSound('click')">← BACK TO MAP</a>
  </div>

</div>
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

  /* confetti burst */
  setTimeout(function() { spawnConfetti(); }, 400);
  setTimeout(function() { spawnConfetti(); }, 1200);

  showAchievement('🕵️ DETECTIVE MASTER!', 'All 8 cases solved!');
})();
"""
    return base("Case Closed", body, extra_js)
