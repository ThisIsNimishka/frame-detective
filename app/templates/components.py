"""
app/templates/components.py
----------------------------
Pure functions → HTML string snippets.

KEY FIX: hud() no longer has an inline <script>renderHUD()</script>
         That call now lives at the bottom of base.py AFTER all JS loads.
"""
from app.models import MISSIONS, QUIZZES


# ─────────────────────────────────────────────────────────────
# HUD
# ─────────────────────────────────────────────────────────────
def hud() -> str:
    badges = "".join(
        f'<span id="bdg{m.id}" class="bdg locked" title="{m.badge_name}">{m.badge}</span>'
        for m in MISSIONS
    )
    return f"""
<div class="hud">
  <span class="hud-logo">🕵️ FD</span>
  <span class="hud-div">│</span>
  <span class="hud-lvl" id="hud-lvl">LVL 1</span>
  <div class="xp-wrap">
    <span class="xp-lbl">XP</span>
    <div class="xp-bar"><div class="xp-fill" id="xp-fill" style="width:0%"></div></div>
    <span class="xp-num" id="xp-num">0 / 200 XP</span>
  </div>
  <div class="hp-wrap">
    <span class="hp-lbl">HP</span>
    <div class="hearts">
      <span class="ht" id="ht0">❤️</span>
      <span class="ht" id="ht1">❤️</span>
      <span class="ht" id="ht2">❤️</span>
    </div>
  </div>
  <span class="streak-num" id="hud-streak"></span>
  <div class="badges">{badges}</div>
  <a href="map.html" class="hud-quit" onclick="playSound('click')">⬅ MAP</a>
</div>"""


# ─────────────────────────────────────────────────────────────
# BRIEFING
# ─────────────────────────────────────────────────────────────
def briefing(speaker: str, text: str) -> str:
    """Render a case-file briefing block.

    If `text` contains HTML tags the typewriter effect is skipped entirely
    (HTML inside a data-* attribute gets entity-encoded by the browser which
    makes the raw tag text visible).  Plain-text strings still get the
    typewriter animation.
    """
    import re as _re
    has_html = bool(_re.search(r'<[a-zA-Z/]', text))
    if has_html:
        inner = f'<span>{text}</span>'
    else:
        # Escape any quotes so they don't break the attribute
        safe = text.replace('"', '&quot;').replace("'", '&#39;')
        inner = f'<span data-tw="{safe}">{text}</span>'
    return (
        f'<div class="cutscene blk">'
        f'<span class="spkr">{speaker}</span>'
        f'{inner}'
        f'</div>'
    )



# ─────────────────────────────────────────────────────────────
# CARD
# ─────────────────────────────────────────────────────────────
def card(label: str, title: str, body_html: str) -> str:
    return (
        f'<div class="card blk">'
        f'<span class="card-lbl">{label}</span>'
        f'<h3>{title}</h3>'
        f'{body_html}'
        f'</div>'
    )


# ─────────────────────────────────────────────────────────────
# METRIC CARD
# ─────────────────────────────────────────────────────────────
def metric_card(kind: str, name: str, plain: str, desc: str, ranges_html: str = "") -> str:
    return (
        f'<div class="mc {kind}">'
        f'<div class="mc-name">{name}</div>'
        f'<div class="mc-plain">{plain}</div>'
        f'<div class="mc-desc">{desc}</div>'
        f'<div class="mc-ranges">{ranges_html}</div>'
        f'</div>'
    )


def range_tag(cls: str, text: str) -> str:
    return f'<span class="rt {cls}">{text}</span>'


# ─────────────────────────────────────────────────────────────
# SCENARIO
# ─────────────────────────────────────────────────────────────
def scenario(emoji: str, title: str, subtitle: str,
             signs_html: str, fix_html: str) -> str:
    return (
        f'<div class="scenario blk">'
        f'<div class="sc-head">'
        f'<span class="sc-em">{emoji}</span>'
        f'<div><div class="sc-title">{title}</div>'
        f'<div class="sc-sub">{subtitle}</div></div>'
        f'</div>'
        f'<div class="sc-signs">{signs_html}</div>'
        f'<div class="sc-fix">{fix_html}</div>'
        f'</div>'
    )


def sign(kind: str, text: str) -> str:
    return f'<span class="sign {kind}">{text}</span>'


# ─────────────────────────────────────────────────────────────
# PIPELINE VISUAL
# ─────────────────────────────────────────────────────────────
def pipeline() -> str:
    stages = [
        ("ps-cpu",  "CPU",      "Game Logic",       "MsCPUBusy"),
        ("ps-wait", "▶▶",       "GPU Queue",        "MsGPULatency"),
        ("ps-gpu",  "GPU",      "Render",           "MsGPUBusy"),
        ("ps-disp", "DISPLAY",  "Frame on screen",  "DisplayedTime"),
    ]
    row = ""
    for i, (cls, label, sub, metric) in enumerate(stages):
        row += f'<div id="pst{i}" class="pipe-stage {cls}">'
        row += f'<strong>{label}</strong><br>'
        row += f'<small>{sub}</small>'
        row += f'<small style="color:inherit;opacity:.55">{metric}</small>'
        row += '</div>'
        if i < len(stages) - 1:
            row += '<div class="pipe-arr">→</div>'
    return f"""<div class="blk pipe-visual">
  <div class="pipe-label">▸ FRAME PIPELINE — EACH STEP ADDS LATENCY</div>
  <div class="pipe-row">{row}</div>
  <div class="pipe-legend">
    💡 Every millisecond spent here adds to <strong style="color:#00f5ff">MsClickToPhotonLatency</strong>.
    The pipeline animates to show where time is typically lost.
  </div>
</div>
<script>
(function(){{
  var stages = [0,1,2,3];
  var cur = 0;
  function tick(){{
    stages.forEach(function(i){{document.getElementById('pst'+i).classList.remove('active');}});
    document.getElementById('pst'+cur).classList.add('active');
    cur = (cur+1) % stages.length;
  }}
  tick(); setInterval(tick, 900);
}})();
</script>"""


# ─────────────────────────────────────────────────────────────
# BOSS SECTION
# ─────────────────────────────────────────────────────────────
def boss_section(mission_id: int, boss_emoji: str, boss_name: str,
                 question: str, options: list[tuple[str, bool]],
                 next_page: str, mission_xp: int,
                 hint: str = "", fun_fact: str = "") -> str:

    # Build option buttons A B C D
    labels   = ["A", "B", "C", "D"]
    opts_html = ""
    for i, (text, correct) in enumerate(options):
        label = labels[i] if i < len(labels) else str(i + 1)
        dc    = '1' if correct else '0'
        opts_html += (
            f'<button class="qbtn" data-correct="{dc}" onclick="doAnswer(this)">'
            f'<span class="qkey">{label}</span>'
            f'<span>{text}</span>'
            f'</button>'
        )

    hint_html = f'<div id="hint-box" class="hint-box"><span class="hint-lbl">💡 HINT</span>{hint}</div>' if hint else ''
    fun_html  = f'<div class="fun-fact">🔬 <strong>FUN FACT:</strong> {fun_fact}</div>' if fun_fact else ''

    quiz_js = f"""
var _mid  = {mission_id};
var _mxp  = {mission_xp};
var _next = '{next_page}';
var _t0   = Date.now();

function doAnswer(btn) {{
  if (document.getElementById('q-opts').classList.contains('done')) return;
  stopTimer();

  var isCorrect = btn.getAttribute('data-correct') === '1';
  var opts      = document.querySelectorAll('.qbtn');
  var fb        = document.getElementById('q-fb');
  var nx        = document.getElementById('next-banner');

  document.getElementById('q-opts').classList.add('done');
  opts.forEach(function(b) {{
    b.classList.add('done');
    if (b.getAttribute('data-correct') === '1') b.classList.add('ok');
  }});

  if (isCorrect) {{
    btn.classList.add('ok');
    var elapsed  = (Date.now() - _t0) / 1000;
    var bonus    = elapsed < 30 ? 25 : 0;
    var totalXP  = {mission_xp} + 50 + bonus;
    addXP(totalXP);
    incrementStreak();
    markDone(_mid, 0);   // mission xp already added above
    spawnParticles(btn.offsetLeft + btn.offsetWidth/2,
                   btn.getBoundingClientRect().top + window.scrollY,
                   28, ['#39ff14','#ffe600','#00f5ff','#ffffff']);
    playSound('boss_defeated');
    /* drain boss HP bar */
    var bh = document.getElementById('boss-hpfill');
    if (bh) {{ bh.style.width='0%'; }}
    fb.className = 'qfb win';
    fb.innerHTML = '<strong>✅ CORRECT!</strong>' +
      (bonus ? ' <span style="color:var(--yellow)">⚡ +' + bonus + ' SPEED BONUS!</span>' : '') +
      '<br>' + (QUIZ_WIN[_mid] || '') + '{fun_html}';
  }} else {{
    btn.classList.add('bad');
    loseHP();
    markDone(_mid, 0);
    fb.className = 'qfb lose';
    fb.innerHTML = '<strong>❌ WRONG.</strong><br>' + (QUIZ_LOSE[_mid] || '') + '{fun_html}';
  }}

  fb.style.display = 'block';
  if (nx) {{ nx.style.display = 'block'; nx.classList.add('show'); }}
}}

/* keyboard shortcuts A B C D */
document.addEventListener('keydown', function(e) {{
  var map = {{'a':0,'b':1,'c':2,'d':3,'1':0,'2':1,'3':2,'4':3}};
  var idx = map[e.key.toLowerCase()];
  if (idx !== undefined) {{
    var opts = document.querySelectorAll('.qbtn:not(.done)');
    var all  = document.querySelectorAll('.qbtn');
    if (!document.getElementById('q-opts').classList.contains('done') && all[idx]) {{
      all[idx].click();
    }}
  }}
}});

/* hint timer */
var _hintTimer = setTimeout(function() {{
  var hb = document.getElementById('hint-box');
  if (hb && !document.getElementById('q-opts').classList.contains('done')) {{
    hb.classList.add('show');
    playSound('hint');
  }}
}}, 20000);

/* Start countdown timer */
startTimer(60, function() {{
  /* Time's up — force loss if not answered */
  if (!document.getElementById('q-opts').classList.contains('done')) {{
    var first = document.querySelector('.qbtn');
    if (first) {{
      document.getElementById('q-opts').classList.add('done');
      document.querySelectorAll('.qbtn').forEach(function(b) {{
        b.classList.add('done');
        if (b.getAttribute('data-correct') === '1') b.classList.add('ok');
        else b.classList.add('bad');
      }});
      loseHP();
      markDone(_mid, 0);
      var fb = document.getElementById('q-fb');
      var nx = document.getElementById('next-banner');
      fb.className = 'qfb lose';
      fb.innerHTML = '⏰ <strong>TIME UP!</strong> ' + (QUIZ_LOSE[_mid] || '');
      fb.style.display = 'block';
      if (nx) {{ nx.style.display='block'; nx.classList.add('show'); }}
    }}
  }}
}});
"""


    return f"""
<div class="boss-arena blk">
  <div class="boss-hdr">
    <div class="boss-em">{boss_emoji}</div>
    <div>
      <div class="boss-name">{boss_name}</div>
      <div class="boss-sub">Defeat the boss to complete this mission.</div>
      <div class="boss-hp-wrap">
        <div class="boss-hp-lbl">BOSS HP</div>
        <div class="boss-hpbg"><div class="boss-hpfill" id="boss-hpfill" style="width:100%"></div></div>
      </div>
    </div>
  </div>

  <div class="quiz-timer-wrap">
    <span class="quiz-timer-lbl">TIME</span>
    <div class="quiz-timer-bar"><div class="quiz-timer-fill" id="timer-fill" style="width:100%"></div></div>
    <span class="quiz-timer-num" id="timer-num">60</span>
  </div>

  <div class="q-txt">{question}</div>
  <div class="q-opts" id="q-opts">{opts_html}</div>
  {hint_html}
  <div class="qfb" id="q-fb" style="display:none"></div>
  <div class="next-banner" id="next-banner">
    <a href="{next_page}" class="btn-green" onclick="playSound('click')">NEXT MISSION →</a>
  </div>
</div>
<script>{quiz_js}</script>"""
