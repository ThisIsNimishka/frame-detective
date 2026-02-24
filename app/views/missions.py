"""
app/views/missions.py
---------------------
Renders all 8 mission pages. Each page = educational content + boss battle.
"""
from app.templates import base, hud, pipeline
from app.templates.components import (
    briefing, card, metric_card, range_tag,
    scenario, sign, boss_section,
)
from app.models import MISSIONS, QUIZZES
from typing import Dict


# ── shared quiz data tables injected into every page ─────────
def _quiz_js() -> str:
    from app.models import QUIZZES
    win_dict  = {q.mission_id: q.win_text  for q in QUIZZES}
    lose_dict = {q.mission_id: q.lose_text for q in QUIZZES}
    hint_dict = {q.mission_id: q.hint      for q in QUIZZES}
    fun_dict  = {q.mission_id: q.fun_fact  for q in QUIZZES}

    def js_str(d: dict) -> str:
        items = ", ".join(f'{k}: {repr(v)}' for k, v in sorted(d.items()))
        return "{" + items + "}"

    return (
        f"var QUIZ_WIN  = {js_str(win_dict)};\n"
        f"var QUIZ_LOSE = {js_str(lose_dict)};\n"
        f"var QUIZ_HINT = {js_str(hint_dict)};\n"
        f"var QUIZ_FUN  = {js_str(fun_dict)};\n"
    )


def _back_link(text: str = "← MAP") -> str:
    return f'<a href="map.html" class="btn-back" onclick="playSound(\'click\')">{text}</a>'


def _mission_header(m_num: int, icon: str, name: str) -> str:
    return (
        f'<div class="mission-hdr">'
        f'{_back_link()}'
        f'<div>'
        f'<div class="mission-num">MISSION {str(m_num).zfill(2)}</div>'
        f'<div class="mission-name">{icon} {name}</div>'
        f'</div>'
        f'</div>'
    )


def _boss(m_id: int) -> str:
    q = next(q for q in QUIZZES if q.mission_id == m_id)
    m = next(m for m in MISSIONS if m.id == m_id)
    opts = [(o.text, o.correct) for o in q.options]
    return boss_section(m_id, m.boss_emoji, m.boss_name,
                        q.question, opts, m.next_page, m.xp,
                        q.hint, q.fun_fact)


# ─────────────────────────────────────────────────────────────
# MISSION 1 — What Is PresentMon?
# ─────────────────────────────────────────────────────────────
def render_mission_1() -> str:
    m = MISSIONS[0]
    content = _mission_header(1, m.icon, m.name)
    content += briefing("▸ CASE FILE #001",
        "Intel PresentMon is a <em>frame capture tool</em> that runs invisibly alongside your game. "
        "It reads <u>ETW (Event Tracing for Windows)</u> — a real-time diagnostic log that "
        "Windows GPU drivers write to automatically. Zero injection. Zero overhead.")
    content += card("HOW IT WORKS", "The ETW Spy Mechanism",
        "<p>When you run a game, the GPU driver writes tiny <strong>event records</strong> into the "
        "Windows kernel log every single frame. PresentMon <em>subscribes</em> to those streams "
        "without injecting any code into your process.</p>"
        "<p>This is why PresentMon can measure <strong>frame timing to microsecond precision</strong> "
        "without affecting FPS. It's like tapping a phone line — the call still happens normally.</p>"
        "<p class='rule'>&#x26A1; ETW has existed since Windows XP. GPU vendors like Intel, AMD, "
        "and NVIDIA all write to it. PresentMon just listens.</p>")
    content += card("WHAT IT CAPTURES", "Every Column, Decoded",
        "<p><strong>MsBetweenPresents</strong> — time from one frame's Present() call to the next. "
        "This is your raw framerate data.</p>"
        "<p><strong>MsCPUBusy / MsGPUBusy</strong> — exactly how long CPU and GPU actively worked.</p>"
        "<p><strong>DisplayedTime</strong> — how long a frame was actually visible on screen.</p>"
        "<p><strong>MsClickToPhotonLatency</strong> — how long from your mouse click to pixel change.</p>"
        "<p class='rule'>&#x26A1; A single CSV can contain <strong>tens of thousands of rows</strong>, "
        "each representing one frame.</p>")
    content += card("WHY IT MATTERS", "Beyond FPS Counters",
        "<p>Most FPS overlays just count frames per second. PresentMon shows you the "
        "<strong>complete journey</strong> of each frame — where time was spent, where it was wasted, "
        "and how late it arrived at your monitor.</p>"
        "<p class='rule'>&#x2139; PresentMon is free, open-source, and maintained by Intel's "
        "game developer tools team on GitHub.</p>")
    content += _boss(0)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 1", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 2 — The Frame Pipeline
# ─────────────────────────────────────────────────────────────
def render_mission_2() -> str:
    m = MISSIONS[1]
    content = _mission_header(2, m.icon, m.name)
    content += briefing("▸ CASE FILE #002",
        "Every frame starts as <em>game logic</em> on your CPU and dies — or triumphs — "
        "as <u>pixels on your screen</u>. Miss one phase of this pipeline and you feel it as lag.")
    content += pipeline()
    content += card("PHASE 1 — CPU Work", "MsCPUBusy",
        "<p>The CPU runs game logic: AI decisions, physics, animation updates, and finally "
        "the <strong>draw call submission</strong> — packaging all the render commands and "
        "handing them to the GPU driver.</p>"
        "<p>PresentMon captures this as <strong>MsCPUBusy</strong>. If this exceeds your frame "
        "budget (16.7ms at 60fps), you have a <em>CPU bottleneck</em>.</p>")
    content += card("PHASE 2 — Queue and GPU", "MsGPUBusy + MsGPULatency",
        "<p>Draw calls sit in a <strong>GPU queue</strong> before the GPU processes them. "
        "The time waiting in queue is <strong>MsGPULatency</strong> — invisible delay "
        "before rendering even starts.</p>"
        "<p><strong>MsGPUBusy</strong> is the actual GPU execution time — running shaders, "
        "rendering lighting, tracing rays. This is the most common bottleneck in GPU-limited games.</p>")
    content += card("PHASE 3 — Presentation", "Present() → DisplayedTime",
        "<p>When the GPU finishes, the frame is passed to the <strong>OS compositor</strong> "
        "or flipped directly (see Mission 4: Present Modes). The frame waits for the next "
        "vertical blanking interval (vblank) if vsync is on.</p>"
        "<p><strong>DisplayedTime</strong> = how many milliseconds that frame was shown. "
        "At 60fps each frame should display for ~16.7ms. Double that = dropped frame.</p>"
        "<p class='rule'>&#x26A1; MsClickToPhotonLatency measures the <strong>entire chain</strong> "
        "from input → CPU → GPU → display. That's the real 'feel' of input lag.</p>")
    content += _boss(1)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 2", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 3 — Metrics Deep Dive
# ─────────────────────────────────────────────────────────────
def render_mission_3() -> str:
    m = MISSIONS[2]
    content = _mission_header(3, m.icon, m.name)
    content += briefing("▸ CASE FILE #003",
        "The CSV has <em>many columns</em>. Most detectives look only at FPS. "
        "You look at <u>all of it</u>. This mission is your field manual.")
    content += '<div class="blk"><div class="section-hdr">COMPLETE METRIC REFERENCE</div>'
    content += '<div class="metric-grid">'
    content += metric_card("cpu", "MsCPUBusy", "How hard your CPU worked",
        "Total time (ms) the CPU spent actively processing game logic and submitting draw calls for this frame.",
        range_tag("rg","< 8ms OK") + range_tag("ry","8-16ms Caution") + range_tag("rr","16ms+ Bottleneck"))
    content += metric_card("gpu", "MsGPUBusy", "How hard your GPU worked",
        "Time the GPU spent rendering this frame. If this is close to your frame budget — GPU is your bottleneck.",
        range_tag("rg","< budget OK") + range_tag("rr","≥ budget Bottleneck"))
    content += metric_card("disp", "DisplayedTime", "How long was this frame shown?",
        "How many ms this frame was actually displayed. NA = frame was never shown (superseded by the next).",
        range_tag("rg","~16.7ms @ 60fps") + range_tag("ry","33.4ms = 1 skip") + range_tag("rr","NA = dropped"))
    content += metric_card("lat", "MsBetweenPresents", "Raw frametime",
        "Time between consecutive Present() calls. Inverted gives you FPS. High variance = frame pacing issues.",
        range_tag("rg","Consistent = Good") + range_tag("rr","Spiky = Stutter"))
    content += metric_card("lat", "MsGPULatency", "GPU queue wait time",
        "How long the frame waited in the GPU command queue before the GPU started working on it. Tuned by Anti-Lag.",
        range_tag("rg","<5ms Good") + range_tag("ry","5-15ms High") + range_tag("rr","15ms+ Severe"))
    content += metric_card("lat", "MsClickToPhoton", "Total input-to-display latency",
        "The complete end-to-end latency from a click event to its corresponding pixel change on screen.",
        range_tag("rg","<50ms Competitive") + range_tag("ry","50-100ms Normal") + range_tag("rr","100ms+ Sluggish"))
    content += metric_card("cpu", "AllowsTearing", "Is tearing enabled?",
        "1 = the display allows screen tearing (Immediate Present Mode, no vsync). 0 = vsync or compositor is active.",
        range_tag("rg","1 = low latency") + range_tag("ry","0 = vsync on"))
    content += metric_card("gpu", "FrameType", "Real or generated?",
        "Whether this frame was natively rendered or generated by Frame Generation (DLSS, XeSS, FSR). "
        "Generated frames have GPU rendering cost but no CPU simulation cost.",
        range_tag("rg","Application = Real") + range_tag("ry","Generated = AI"))
    content += '</div></div>'
    content += _boss(2)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 3", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 4 — Present Modes
# ─────────────────────────────────────────────────────────────
def render_mission_4() -> str:
    m = MISSIONS[3]
    content = _mission_header(4, m.icon, m.name)
    content += briefing("▸ CASE FILE #004",
        "A rendered frame doesn't teleport to your screen. It takes a <em>route</em>. "
        "The route it takes drastically affects <u>latency and smoothness</u>.")
    modes = [
        ("Hardware: Independent Flip", "pb-best", "Borderless-windowed; bypasses DWM. Best latency, like exclusive FS.",  "Low",  "Lowest", "DirectX 11/12 in borderless"),
        ("Hardware: Flip Discard",      "pb-best", "Full exclusive fullscreen. GPU flips directly to display — zero compositor.",  "Low", "Lowest", "Exclusive fullscreen"),
        ("Hardware: Composed: Flip",    "pb-good", "DWM composes the frame but uses efficient GPU-side copy.",  "Med", "Low",    "Windowed mode games"),
        ("Composed: Copy GPU GDI",      "pb-ok",   "Older path: GPU surface copied to system memory, then to DWM.",  "High", "Med",  "Legacy / DX9 apps"),
        ("Composed: Copy CPU GDI",      "pb-bad",  "CPU copies frame data. Very slow. Only used by GDI apps.",  "Very High", "High",  "Very old applications"),
    ]
    tbl = '<table class="mode-tbl"><tr><th>Mode</th><th>Rating</th><th>Description</th><th>CPU Cost</th><th>Latency</th><th>When</th></tr>'
    for name, cls, desc, cpu, lat, when in modes:
        tbl += f'<tr><td class="mm">{name}</td><td><span class="pb {cls}">{cls.replace("pb-","").upper()}</span></td><td>{desc}</td><td>{cpu}</td><td>{lat}</td><td>{when}</td></tr>'
    tbl += '</table>'
    content += f'<div class="blk card"><span class="card-lbl">ALL PRESENT MODES</span>{tbl}</div>'
    content += card("THE TARGET MODE", "Hardware: Independent Flip",
        "<p>For borderless windowed games on modern Windows, <strong>Hardware: Independent Flip</strong> "
        "is the gold standard. Windows promotes your game past the Desktop Window Manager (DWM) "
        "and allows the GPU to flip directly to the display — same as exclusive fullscreen.</p>"
        "<p>To get this: run in <strong>borderless windowed</strong>, use <strong>DirectX 11 or DX12</strong>, "
        "and ensure no other window is overlapping your game.</p>"
        "<p class='rule'>&#x26A1; Check your PresentMode column. If it says anything other than "
        "Independent Flip or Flip Discard — you're paying extra latency for nothing.</p>")
    content += _boss(3)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 4", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 5 — Reading Raw Traces
# ─────────────────────────────────────────────────────────────
def render_mission_5() -> str:
    m = MISSIONS[4]
    content = _mission_header(5, m.icon, m.name)
    content += briefing("▸ CASE FILE #005",
        "The CSV is your crime scene. Every row is one frame. "
        "Your job: find the <em>guilty frame</em> — the one that caused the stutter.")
    content += card("HOW TO CAPTURE", "PresentMon Command Line",
        "<p>Open an elevated command prompt (Admin) and run:</p>"
        "<div class='codeblock'><pre>"
        "<span class='ck'>PresentMon64.exe</span> "
        "<span class='cf'>--output_file</span> <span class='cv'>capture.csv</span> "
        "<span class='cf'>--process_name</span> <span class='cv'>Game.exe</span> "
        "<span class='cf'>--delay</span> <span class='cv'>2</span> "
        "<span class='cf'>--timed</span> <span class='cv'>30</span>\n"
        "<span class='cm'># --delay 2 = wait 2s before capturing</span>\n"
        "<span class='cm'># --timed 30 = capture 30 seconds then stop</span>"
        "</pre></div>"
        "<p>The resulting CSV has one row per frame presented during the capture window.</p>")
    content += card("READING THE CSV", "What a Normal Frame Looks Like",
        "<p>A healthy frame at 60fps looks like this:</p>"
        "<div class='codeblock'><pre>"
        "<span class='ck'>MsBetweenPresents</span> <span class='cv'>16.7</span>  "
        "<span class='cm'>← right on target</span>\n"
        "<span class='ck'>MsCPUBusy        </span> <span class='cv'>4.2</span>   "
        "<span class='cm'>← CPU has headroom</span>\n"
        "<span class='ck'>MsGPUBusy        </span> <span class='cv'>14.9</span>  "
        "<span class='cm'>← GPU is the bottleneck but below budget</span>\n"
        "<span class='ck'>DisplayedTime    </span> <span class='cv'>16.7</span>  "
        "<span class='cm'>← perfect: shown for one vblank</span>"
        "</pre></div>")
    content += card("SPOTTING A STUTTER", "The Guilty Row",
        "<p>A stutter frame looks like one of these:</p>"
        "<div class='codeblock'><pre>"
        "<span class='cf'>MsBetweenPresents</span> <span class='cv'>33.4</span>  "
        "<span class='cm'>← double vblank = 1 dropped frame!</span>\n"
        "<span class='cf'>MsCPUBusy        </span> <span class='cv'>42.1</span>  "
        "<span class='cm'>← CPU spiked: shader compile? GC? Asset load?</span>\n"
        "<span class='cf'>DisplayedTime    </span> <span class='cv'>NA</span>    "
        "<span class='cm'>← this frame was never shown!</span>"
        "</pre></div>"
        "<p class='rule'>&#x26A1; NA in DisplayedTime = frame was rendered but <strong>never shown</strong>. "
        "With vsync on, this is the signature of a missed vblank.</p>")
    content += _boss(4)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 5", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 6 — Diagnose & Fix
# ─────────────────────────────────────────────────────────────
def render_mission_6() -> str:
    m = MISSIONS[5]
    content = _mission_header(6, m.icon, m.name)
    content += briefing("▸ CASE FILE #006",
        "Five real-world scenarios. Real data. Real enemies. "
        "Read the numbers — <em>identify the killer</em> — prescribe the cure.")
    content += scenario(
        "🔴", "Enemy Alpha — GPU Bottleneck", "MsGPUBusy ≈ 16ms, MsCPUBusy ≈ 3ms @ 60fps target",
        sign("bad","MsGPUBusy near budget") + sign("ok","CPU has headroom") + sign("bad","FPS cap can't overcome"),
        "<strong>FIX:</strong> Lower resolution, reduce shadow quality, disable ray tracing, "
        "lower draw distance. GPU-limited means throwing CPU resources at it won't help.")
    content += scenario(
        "🟡", "Enemy Beta — CPU Bottleneck", "MsCPUBusy > 16ms, MsGPUBusy ≈ 5ms",
        sign("bad","MsCPUBusy over budget") + sign("ok","GPU wide open") + sign("bad","Low CPU-core threads"),
        "<strong>FIX:</strong> Lower NPC counts, reduce physics complexity, close background apps, "
        "check if game uses multi-threading well. High-frequency content stresses one CPU core heavily.")
    content += scenario(
        "💜", "Enemy Gamma — Frame Pacing / Stutter", "Avg FPS fine but MsBetweenPresents varies 5–35ms",
        sign("bad","High variance frametime") + sign("bad","DisplayedTime inconsistent") + sign("ok","Neither CPU nor GPU maxed"),
        "<strong>FIX:</strong> Enable V-sync or RTSS frame cap, check for shader compilation stutters "
        "(precompile shaders in settings), ensure DirectStorage or asset streaming isn't causing hitches.")
    content += scenario(
        "🔵", "Enemy Delta — Input Latency Monster", "FPS=90, MsClickToPhoton=90ms, MsGPULatency=22ms",
        sign("bad","GPU queue depth too deep") + sign("bad","Pre-rendered frames too many") + sign("ok","Raw FPS looks fine"),
        "<strong>FIX:</strong> Enable NVIDIA Reflex / AMD Anti-Lag / Intel Anti-Lag. "
        "Set Max Pre-Rendered Frames = 1 in driver. Cap FPS ~10 below max refresh. "
        "MsGPULatency should drop below 5ms.")
    content += scenario(
        "⚡", "Enemy Epsilon — Frame Generation Chaos", "FrameType=Generated rows, MsClickToPhoton spikes",
        sign("bad","Generated frames inflate FPS") + sign("bad","Latency increases") + sign("ok","GPU rendering frames fast"),
        "<strong>FIX:</strong> Frame generation adds visual FPS but also latency. "
        "Always pair it with NVIDIA Reflex or Anti-Lag. Look at only Application FrameType rows "
        "for true render FPS. Generated frames don't reduce input lag.")
    content += _boss(5)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 6", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 7 — Graphs & Stats
# ─────────────────────────────────────────────────────────────
def render_mission_7() -> str:
    m = MISSIONS[6]
    content = _mission_header(7, m.icon, m.name)
    content += briefing("▸ CASE FILE #007",
        "Average FPS is a <em>lie</em>. One frame at 2ms, one at 31ms — average = 16.5ms = '60fps'. "
        "But you <u>felt</u> that 31ms frame. This mission teaches you to see the real picture.")
    content += '<div class="blk"><div class="section-hdr">THE HONEST STATS</div><div class="pct-row">'
    pcts = [
        ("#00f5ff", "AVG FPS",  "avg", "The mean over all frames. Hides outliers completely. Games feel smooth when consistent, not just when average is high."),
        ("#ffe600", "1% Low",   "P99", "FPS at the 99th frametime percentile. The worst 1% of your frames. Shows that painful occasional stutter."),
        ("#39ff14", "0.1% Low", "P99.9","The very worst frames. Useful for detecting rare, severe hitches like shader compiles or loading spikes."),
        ("#bf5fff", "Median",   "50th","Half your frames were faster, half slower. More representative than average, less dramatic than 1% low."),
    ]
    for color, name, pct_id, desc in pcts:
        content += (
            f'<div class="pct-card">'
            f'<div class="pct-num" style="color:{color}">{pct_id}</div>'
            f'<div class="pct-name">{name}</div>'
            f'<div class="pct-desc">{desc}</div>'
            f'</div>'
        )
    content += '</div></div>'
    content += card("FRAMETIME GRAPH", "The Truth Teller",
        "<p>Instead of graphing FPS (which inverts and compresses problems), graph "
        "<strong>frametime in ms</strong> on the Y axis with frame number on X.</p>"
        "<p>A <strong>flat line near 16.7ms</strong> = perfect. "
        "A <strong>spike</strong> = the exact frame that stuttered. "
        "A <strong>sawtooth pattern</strong> = frame pacing issues.</p>"
        "<div class='codeblock' style='font-size:12px'><pre>"
        "ms │\n"
        "33 │                  ▐▌\n"
        "25 │                  ▐▌\n"
        "17 │▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▐▌▄▄▄▄▄▄▄  ← target\n"
        "   └─────────────────────────→ frame #\n"
        "               ↑ stutter spike"
        "</pre></div>"
        "<p class='rule'>&#x26A1; You can generate this graph from a PresentMon CSV with "
        "<strong>PresentMon Analysis</strong> in the GUI, or plot with pandas + matplotlib.</p>")
    content += card("PYTHON ANALYSIS", "From CSV to Insights in 5 Lines",
        "<div class='codeblock'><pre>"
        "<span class='ck'>import</span> <span class='cv'>pandas</span> <span class='ck'>as</span> pd\n"
        "df = pd.read_csv(<span class='cv'>'capture.csv'</span>)\n"
        "ft = df[<span class='cv'>'MsBetweenPresents'</span>]\n"
        "<span class='ck'>print</span>(<span class='cv'>f'Avg: {ft.mean():.1f}ms  1%Low: {ft.quantile(.99):.1f}ms  0.1%Low: {ft.quantile(.999):.1f}ms'</span>)\n"
        "df[df[<span class='cv'>'MsCPUBusy'</span>] > 16].to_csv(<span class='cv'>'cpu_spikes.csv'</span>)"
        "</pre></div>"
        "<p>The last line exports only the frames where CPU exceeded the 16ms budget — your stutter suspects.</p>")
    content += _boss(6)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 7", body, _quiz_js())


# ─────────────────────────────────────────────────────────────
# MISSION 8 — The Final Mission
# ─────────────────────────────────────────────────────────────
def render_mission_8() -> str:
    m = MISSIONS[7]
    content = _mission_header(8, m.icon, m.name)
    content += briefing("▸ CASE FILE #008 — FINAL",
        "This is the complete <em>detective workflow</em>. "
        "From running PresentMon to reading the data, diagnosing the problem, and fixing it. "
        "This is your <u>cheat sheet for life</u>.")
    content += card("STEP 1 — CAPTURE", "Collect the Evidence",
        "<div class='codeblock'><pre>"
        "<span class='cm'># Full capture: 30s of gameplay, 2s warmup</span>\n"
        "<span class='ck'>PresentMon64.exe</span> <span class='cf'>-process_name</span> <span class='cv'>Game.exe</span> "
        "<span class='cf'>-output_file</span> <span class='cv'>run_A.csv</span> "
        "<span class='cf'>-delay</span> <span class='cv'>2</span> "
        "<span class='cf'>-timed</span> <span class='cv'>30</span>\n\n"
        "<span class='cm'># Capture all running processes at once</span>\n"
        "<span class='ck'>PresentMon64.exe</span> <span class='cf'>-output_file</span> <span class='cv'>all_procs.csv</span> "
        "<span class='cf'>-timed</span> <span class='cv'>15</span>"
        "</pre></div>")
    content += card("STEP 2 — ANALYSE", "Python Analysis Script",
        "<div class='codeblock'><pre>"
        "<span class='ck'>import</span> pandas <span class='ck'>as</span> pd\n\n"
        "df = pd.read_csv(<span class='cv'>'run_A.csv'</span>)\n"
        "<span class='cm'># Filter to real frames only (exclude generated)</span>\n"
        "df = df[df[<span class='cv'>'FrameType'</span>] != <span class='cv'>'Generated'</span>]\n\n"
        "ft = df[<span class='cv'>'MsBetweenPresents'</span>]\n"
        "cpu = df[<span class='cv'>'MsCPUBusy'</span>]\n"
        "gpu = df[<span class='cv'>'MsGPUBusy'</span>]\n\n"
        "<span class='ck'>print</span>(<span class='cv'>'=== SUMMARY ==='</span>)\n"
        "<span class='ck'>print</span>(<span class='cv'>f'Avg FPS:    {1000/ft.mean():.0f}'</span>)\n"
        "<span class='ck'>print</span>(<span class='cv'>f'1% Low ft:  {ft.quantile(.99):.1f}ms'</span>)\n"
        "<span class='ck'>print</span>(<span class='cv'>f'Max CPU:    {cpu.max():.1f}ms'</span>)\n"
        "<span class='ck'>print</span>(<span class='cv'>f'Max GPU:    {gpu.max():.1f}ms'</span>)\n"
        "<span class='ck'>print</span>(<span class='cv'>f'GPU-bound:  {(gpu>cpu).mean()*100:.0f}% of frames'</span>)"
        "</pre></div>")
    content += card("STEP 3 — DIAGNOSE", "The Decision Tree",
        "<p><strong>Is MsGPUBusy near the frame budget?</strong> → GPU bottleneck. Lower visual settings.</p>"
        "<p><strong>Is MsCPUBusy over budget?</strong> → CPU bottleneck. Reduce simulation load.</p>"
        "<p><strong>Is MsClickToPhoton high despite low GPU/CPU load?</strong> → Queue depth. Enable Anti-Lag.</p>"
        "<p><strong>Is 1% Low much worse than average, with normal GPU/CPU?</strong> → Frame pacing. Cap FPS or fix vsync.</p>"
        "<p class='rule'>&#x26A1; Change <strong>one setting at a time</strong>, capture before and after, compare CSVs. "
        "That is the scientific method of performance testing.</p>")
    content += card("THE PERFECT DETECTIVE CHECKLIST", "Your Lifetime Cheat Sheet",
        "<p>&#x2705; <strong>Capture a baseline</strong> before changing any settings.</p>"
        "<p>&#x2705; <strong>Check PresentMode</strong> — target Hardware: Independent Flip.</p>"
        "<p>&#x2705; <strong>GPU or CPU bound?</strong> Compare MsGPUBusy vs MsCPUBusy vs frame budget.</p>"
        "<p>&#x2705; <strong>Look for NA DisplayedTime</strong> — frame drops hiding in plain sight.</p>"
        "<p>&#x2705; <strong>Check MsGPULatency</strong> — over 10ms means your GPU queue is too deep.</p>"
        "<p>&#x2705; <strong>Only change ONE variable</strong> per test. Capture a new CSV. Compare.</p>"
        "<p>&#x2705; <strong>Look at 1% Low, NOT just average FPS</strong>. Average is a lie.</p>"
        "<p class='rule'>&#x1F3C6; You are now a Frame Detective.</p>")
    content += _boss(7)
    body = hud() + f'<div class="wrap">{content}</div>'
    return base("Mission 8", body, _quiz_js())
