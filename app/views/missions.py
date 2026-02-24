"""app/views/missions.py — One render function per mission."""
from app.templates.base import base
from app.templates.components import hud, briefing, card, pipeline, boss_section
from app.models import MISSIONS, QUIZZES

# Build lookup maps from model data
_QUIZ  = {q.mission_id: q for q in QUIZZES}
_M     = {m.id: m         for m in MISSIONS}


# Shared quiz data dict injected into every page
_QUIZ_JS = """
window.QUIZ_WIN  = {QUIZ_WIN_PH};
window.QUIZ_LOSE = {QUIZ_LOSE_PH};
window.QUIZ_HINT = {QUIZ_HINT_PH};
"""

def _quiz_data_js() -> str:
    win_map  = {q.mission_id: q.win_text  for q in QUIZZES}
    lose_map = {q.mission_id: q.lose_text for q in QUIZZES}
    hint_map = {q.mission_id: q.hint      for q in QUIZZES}
    def js_obj(d):
        pairs = ",".join(f'{k}:{repr(v)}' for k, v in d.items())
        return "{" + pairs + "}"
    return (
        f"window.QUIZ_WIN  = {js_obj(win_map)};\n"
        f"window.QUIZ_LOSE = {js_obj(lose_map)};\n"
        f"window.QUIZ_HINT = {js_obj(hint_map)};\n"
    )


def render_mission(idx: int) -> str:
    """Generic mission renderer — builds the correct page for mission idx (0-based)."""
    m = _M[idx]
    q = _QUIZ[idx]
    opts = [(o.text, o.correct) for o in q.options]

    # Mission-specific teaching content
    content_blocks = _MISSION_CONTENT.get(idx, "")

    body = hud(quit_href="map.html") + f"""
<div class="page-wrap">
  <div class="mission-hdr">
    <div>
      <div class="mission-id">CASE {m.id + 1:02d} OF 08</div>
      <div class="mission-title">{m.icon} {m.name}</div>
    </div>
    <a href="map.html" class="btn btn-ghost" style="margin-left:auto">← MAP</a>
  </div>

  {briefing("AGENT DIRECTIVE", m.desc)}

  {content_blocks}

  {boss_section(
      m.id, m.boss_emoji, m.boss_name,
      q.question, opts, m.next_page, m.xp,
      q.hint, q.fun_fact
  )}
</div>"""

    extra_js = _quiz_data_js()
    return base(m.name, body, extra_js)


# ── Per-mission educational content ────────────────────────────
_MISSION_CONTENT = {
    0: card("📖 INTEL BRIEF", "What is PresentMon?", """
<p><strong>PresentMon</strong> is Intel's open-source frame-analysis tool.
It taps into <em>Windows ETW</em> (Event Tracing for Windows) — an OS-level
event log that GPU drivers write to automatically. PresentMon subscribes and
reads without injecting into your game.</p>
<p>Result: <strong>zero overhead</strong> on the game process, accurate
frame-time data in a simple <em>CSV file</em>.</p>""") +
    card("🔧 HOW TO USE", "Quick Start", """
<p><strong>1.</strong> Run <em>PresentMon.exe --output_file trace.csv</em></p>
<p><strong>2.</strong> Play your game for 30–60 seconds</p>
<p><strong>3.</strong> Stop capture — open <em>trace.csv</em> in Excel or Python</p>
<p><strong>4.</strong> Compare <em>MsGPUBusy</em> vs <em>MsCPUBusy</em> to find your bottleneck</p>"""),

    1: pipeline() +
    card("⚙️ FRAME LIFE", "Birth → Death of a Frame", """
<p>Every frame starts on the <strong>CPU</strong> — game logic, physics, draw calls — then
handed off to the <strong>GPU</strong> for rendering. The GPU finishes and
hands the finished image to the <strong>display queue</strong>.</p>
<p><strong>MsCPUBusy</strong> measures CPU work time.
<strong>MsGPUBusy</strong> measures GPU render time.
Whichever is closer to your frame budget is your bottleneck.</p>"""),

    2: card("📊 KEY METRICS", "PresentMon CSV Columns", """
<p><strong>MsGPUBusy</strong> — milliseconds the GPU spent rendering this frame.</p>
<p><strong>MsCPUBusy</strong> — milliseconds the CPU spent on game logic & draw calls.</p>
<p><strong>DisplayedTime</strong> — how long this frame was actually on screen.
<em>NA</em> = frame was rendered but never shown (dropped).</p>
<p><strong>MsClickToPhotonLatency</strong> — full input-to-display round trip. Lower = more responsive.</p>"""),

    3: card("🔀 PRESENT MODES", "Six Routes from GPU to Screen", """
<p><strong>Composed: Flip</strong> — frame goes through DWM compositor. Safe but adds latency.</p>
<p><strong>Hardware: Independent Flip</strong> — Windows bypasses DWM entirely. Best for borderless windowed.</p>
<p><strong>Hardware: Legacy Flip</strong> — Exclusive fullscreen. Very low latency, game owns the display.</p>
<p>Goal: aim for <em>Hardware: Independent Flip</em> or <em>Hardware: Legacy Flip</em>.</p>"""),

    4: card("🔬 READING TRACES", "Find the Stutter", """
<p>Open your CSV and sort by <strong>DisplayedTime</strong> descending.
Any row ≥ <em>33ms</em> at 60fps target is a dropped frame you felt.</p>
<p>Cross-reference with <strong>MsCPUBusy</strong> and <strong>MsGPUBusy</strong>
on that same row — whichever spiked is the culprit.</p>
<p>One rogue row in thousands can cause a visible hitch. That's why raw trace reading matters.</p>"""),

    5: card("🩺 DIAGNOSE & FIX", "Five Enemy Types", """
<p><strong>GPU Bound</strong> — MsGPUBusy near frame budget. Lower resolution / quality settings.</p>
<p><strong>CPU Bound</strong> — MsCPUBusy near budget. Reduce draw calls, entities, physics ticks.</p>
<p><strong>Stutter</strong> — one-off spikes in DisplayedTime. Check for shader compilation, GC pauses.</p>
<p><strong>Latency</strong> — high MsGPULatency. Enable Anti-Lag / Reflex, cap FPS below GPU limit.</p>
<p><strong>Frame Gen</strong> — MsCPUBusy low, FPS high but latency high. Generated frames add lag.</p>"""),

    6: card("📈 GRAPHS & STATS", "Why Average FPS Lies", """
<p><strong>Average FPS</strong> looks great on benchmarks but hides spikes.
A game at <em>90 avg / 45 1% Low</em> feels terrible despite good averages.</p>
<p><strong>1% Low</strong> = the FPS in the worst 1% of frames. This is what you feel as stutter.</p>
<p><strong>0.1% Low</strong> = worst 0.1% — the most extreme hitches.</p>
<p>A flat <em>frame-time graph</em> (consistent millisecond values) is the true sign of smoothness.</p>"""),

    7: card("🛠️ FULL WORKFLOW", "The Detective's Checklist", """
<p><strong>Step 1:</strong> Capture baseline — <em>PresentMon.exe --output trace_before.csv</em></p>
<p><strong>Step 2:</strong> Change ONE setting only (e.g. lower shadows)</p>
<p><strong>Step 3:</strong> Capture again — <em>trace_after.csv</em></p>
<p><strong>Step 4:</strong> Compare: Did MsGPUBusy drop? Did 1% Low improve?</p>
<p><strong>Step 5:</strong> Repeat until you find the setting with biggest impact per visual quality lost.</p>"""),
}


# ── Named exports required by tests ────────────────────────────
def render_mission_1(): return render_mission(0)
def render_mission_2(): return render_mission(1)
def render_mission_3(): return render_mission(2)
def render_mission_4(): return render_mission(3)
def render_mission_5(): return render_mission(4)
def render_mission_6(): return render_mission(5)
def render_mission_7(): return render_mission(6)
def render_mission_8(): return render_mission(7)
