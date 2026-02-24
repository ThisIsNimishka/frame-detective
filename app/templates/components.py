"""app/templates/components.py — HTML components for Frame Detective."""

import json
from app.models import MISSIONS


# ── HUD ───────────────────────────────────────────────────────
def hud(quit_href: str = "/quit") -> str:
    badges_html = "".join(
        f'<span id="bdg{m.id}" class="hud-badge-icon locked" title="{m.badge_name}">{m.badge}</span>'
        for m in MISSIONS
    )
    return f"""
<nav class="hud" id="main-hud">
  <div class="hud-logo">FRAME<br>DETECTIVE</div>
  <div class="hud-sep">|</div>
  <div id="hud-lvl" class="hud-badge">LVL 1</div>
  <div class="hud-sep">|</div>
  <div class="xp-group">
    <span class="xp-label">XP</span>
    <div class="xp-bar"><div id="xp-fill" style="width:0%"></div></div>
    <span class="xp-val" id="xp-num">0 XP</span>
  </div>
  <div class="hud-sep">|</div>
  <div class="hp-group">
    <span class="hp-label">HP</span>
    <div class="hearts">
      <span id="ht0" class="heart">♥</span>
      <span id="ht1" class="heart">♥</span>
      <span id="ht2" class="heart">♥</span>
    </div>
  </div>
  <div class="hud-sep">|</div>
  <div class="streak">
    <span class="streak-label">🔥</span>
    <span id="hud-streak">0</span>
  </div>
  <div class="hud-sep">|</div>
  <div class="hud-badges">{badges_html}</div>
  <div class="hud-sep">|</div>
  <a href="{quit_href}" class="hud-quit">✕ QUIT</a>
</nav>"""


# ── BRIEFING ──────────────────────────────────────────────────
def briefing(speaker: str, text: str) -> str:
    return f"""
<div class="briefing">
  <span class="briefing-speaker">▸ {speaker}</span>
  <span class="briefing-text" data-tw="{text}"></span>
</div>"""


# ── CARD ──────────────────────────────────────────────────────
def card(label: str, title: str, body_html: str) -> str:
    return f"""
<div class="panel">
  <div class="panel-head"><span class="panel-title">{label}</span></div>
  <div class="panel-head" style="padding-top:10px;padding-bottom:10px;border-bottom:none;">
    <span style="font-family:var(--font-h);font-size:clamp(13px,2vw,16px);color:var(--white);letter-spacing:1px;">{title}</span>
  </div>
  <div class="panel-body">{body_html}</div>
</div>"""


# ── PIPELINE ──────────────────────────────────────────────────
def pipeline() -> str:
    stages = [
        ("🎮", "GAME RUNS",    "0 ms"),
        ("📊", "PRESENTMON",   "1 ms"),
        ("🔬", "FRAME DATA",   "16 ms"),
        ("📈", "ANALYSIS",     "33 ms"),
        ("🕵️", "DETECTIVE",   "50 ms"),
    ]
    stages_html = ""
    for i, (icon, name, time) in enumerate(stages):
        active = "active" if i == 2 else ""
        stages_html += f"""
    <div class="pipe-stage {active}">
      <span class="pipe-icon">{icon}</span>
      <div class="pipe-name">{name}</div>
      <div class="pipe-time">{time}</div>
    </div>"""
    return f"""
<div class="panel">
  <div class="panel-head"><span class="panel-title">▸ DATA PIPELINE</span></div>
  <div class="pipe-row">{stages_html}
  </div>
</div>"""


# ── BOSS / QUIZ SECTION ───────────────────────────────────────
def boss_section(mission_id: int, boss_emoji: str, boss_name: str,
                 question: str, options: list, next_page: str,
                 mission_xp: int,
                 hint: str = "", fun_fact: str = "") -> str:

    labels    = ["A", "B", "C", "D"]
    opts_html = ""
    # options is list of (text, correct)
    for i, (text, correct) in enumerate(options):
        label = labels[i] if i < len(labels) else str(i + 1)
        dc    = "1" if correct else "0"
        opts_html += (
            f'<button class="qbtn" data-correct="{dc}">'
            f'<span class="key-hint">{label}</span>'
            f'<span>{text}</span>'
            f'</button>'
        )

    hint_panel = ""
    if hint:
        hint_panel = (
            f'<div id="hint-panel" class="hint-panel">'
            f'<span class="hint-label">💡 HINT</span>'
            f'<span class="hint-body">{hint}</span>'
            f'</div>'
        )

    fact_content = ""
    if fun_fact:
        fact_content = f'<div style="margin-top:10px;padding:10px;border-left:2px solid var(--purple);font-size:13px;color:rgba(224,240,255,.75)">🔬 <strong>FUN FACT:</strong> {fun_fact}</div>'

    # Convert options to simplified JSON for the engine
    quiz_data = [{"correct": c} for t, c in options]
    
    return f"""
<div class="panel boss-arena" id="boss-arena">
  <div class="boss-header">
    <div class="boss-emoji">{boss_emoji}</div>
    <div class="boss-info">
      <div class="boss-name">{boss_name}</div>
      <div class="boss-sub">Defeat the boss to complete this mission.</div>
      <div class="boss-hp-row">
        <div class="boss-hp-lbl">BOSS HP</div>
        <div class="boss-hp-bg"><div class="boss-hp-bar" id="boss-hp-bar"></div></div>
      </div>
    </div>
  </div>

  <div class="quiz-timer">
    <span class="quiz-timer-label">TIME</span>
    <div class="quiz-timer-bar"><div id="timer-fill" style="width:100%"></div></div>
    <span class="quiz-timer-count" id="timer-num">60</span>
  </div>

  <div class="question-text">{question}</div>
  <div class="options">{opts_html}</div>
  {hint_panel}
  <div id="quiz-feedback" class="quiz-feedback"></div>
  <div id="next-bar" class="next-bar">
    <a href="{next_page}" class="btn btn-green">NEXT MISSION →</a>
  </div>
</div>
<script>
/* Call centralized engine with JSON data */
(function() {{
  var options = {json.dumps(quiz_data)};
  var fact    = {json.dumps(fact_content)};
  
  function start() {{
    if (window.initQuiz) {{
      initQuiz({mission_id}, options, "{next_page}", {mission_xp}, fact);
    }} else {{
      setTimeout(start, 50); // Engine might still be loading in head
    }}
  }}
  start();
}})();
</script>"""
