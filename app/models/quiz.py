"""
app/models/quiz.py
------------------
Quiz / boss-battle dataclass — one per mission.
Each quiz has exactly one correct option (c=True).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    text:    str
    correct: bool   # True for exactly ONE option per quiz


@dataclass(frozen=True)
class Quiz:
    mission_id:  int
    question:    str
    options:     tuple["Option", ...]  # exactly 4 options
    win_text:    str   # feedback shown after correct answer
    lose_text:   str   # feedback shown after wrong answer
    hint:        str   # shown after 20 seconds of inaction
    fun_fact:    str   # extra depth shown in win feedback
    difficulty:  int   # 1–3; affects XP bonus


QUIZZES: list[Quiz] = [
    Quiz(0,
        "How does PresentMon collect frame data WITHOUT slowing your game down?",
        (
            Option("Injects a DLL into the game process to hook rendering calls",               False),
            Option("Reads Windows ETW — a built-in OS event log GPU drivers already write to",  True),
            Option("Samples GPU memory usage every millisecond via the vendor API",              False),
            Option("Uses a kernel driver to intercept Direct3D Present() calls",                False),
        ),
        "Correct! ETW (Event Tracing for Windows) is baked into Windows. GPU drivers write events "
        "to it automatically. PresentMon just subscribes and reads — zero injection, zero overhead.",
        "Not quite. PresentMon is a passive observer. It reads Windows ETW — an OS-level log that "
        "already exists. No injection, no game slowdown.",
        "Think about how PresentMon avoids adding overhead to the game process...",
        "ETW has existed since Windows XP. It's the same mechanism used by Windows Performance Analyzer (WPA).",
        1,
    ),
    Quiz(1,
        "MsCPUBusy = 3ms, MsGPUBusy = 14ms. Target is 60fps (16.7ms budget). What is the bottleneck?",
        (
            Option("CPU — because 3ms is a very small number",                              False),
            Option("GPU — because 14ms is closest to the 16.7ms frame budget",             True),
            Option("Neither — both values are comfortably under budget",                    False),
            Option("Display — the monitor refresh rate is the limiting factor here",        False),
        ),
        "Correct! At 60fps the budget is 16.7ms. MsGPUBusy at 14ms consumes most of it. "
        "CPU at 3ms has tons of headroom. Lower GPU-heavy settings to gain FPS.",
        "Remember: whichever metric is CLOSEST to the frame budget is the bottleneck. "
        "14ms (GPU) is far closer to 16.7ms than 3ms (CPU).",
        "Which metric is eating most of the 16.7ms frame budget?",
        "At 120fps the budget is 8.33ms, so GPU at 14ms would be even more critical.",
        1,
    ),
    Quiz(2,
        'DisplayedTime shows "NA" for a frame. What does this mean?',
        (
            Option("The game crashed while rendering that frame",                                        False),
            Option("The frame was fully rendered by CPU+GPU but was never shown on screen",             True),
            Option("MsGPUBusy was zero — the GPU skipped the frame entirely",                           False),
            Option("The frame took longer than 1 second and was auto-discarded by the driver",          False),
        ),
        "Exactly! NA means the frame completed CPU+GPU work but was superseded — a newer frame was "
        "ready. With vsync ON, lots of NAs = lots of missed vblanks = stutter.",
        "NA does NOT mean crash. The frame was fully rendered but arrived too late. "
        "With vsync ON this is a missed vblank — a dropped frame you can feel as a hitch.",
        "The frame completed GPU work but something happened before it reached the screen...",
        "NA frames are especially costly with vsync ON — each one doubles the frame time from 16.7ms to 33.4ms.",
        2,
    ),
    Quiz(3,
        'Borderless windowed mode. PresentMode shows "Hardware: Independent Flip". Good or bad?',
        (
            Option("Bad — Independent Flip means the GPU cannot keep up with the display",              False),
            Option("Great — Windows promoted the app to bypass DWM and flip directly in hardware",      True),
            Option("Neutral — Present Mode only matters in exclusive fullscreen",                       False),
            Option("Bad — this mode adds extra latency compared to Composed: Flip",                     False),
        ),
        "This is the BEST mode for borderless windowed! Windows promoted your app to bypass DWM "
        "and flip frames directly in GPU hardware — lowest possible latency without exclusive fullscreen.",
        "Hardware: Independent Flip is the goal! It means Windows bypassed the DWM compositor "
        "and flips your frames directly in hardware.",
        "Think about what 'Hardware' and 'Independent' mean in the context of bypassing the compositor...",
        "DX12 and DX11 games are most likely to get Independent Flip in modern borderless windowed mode.",
        2,
    ),
    Quiz(4,
        "CSV row: MsCPUBusy = 42ms, MsGPUBusy = 13ms, DisplayedTime = 33ms. What caused this stutter?",
        (
            Option("GPU overload — MsGPUBusy should be much higher than 13ms",                         False),
            Option("CPU spike — MsCPUBusy blew past the 16.7ms budget, causing a missed vblank",       True),
            Option("Network latency — the game was waiting for a server tick",                          False),
            Option("VRAM exhaustion — the GPU had to page memory which caused the delay",               False),
        ),
        "CPU spike! GPU was fine at 13ms. CPU took 42ms — blown past the 16.7ms budget. "
        "The frame missed its vblank and was shown for 33ms (two display refreshes). Classic CPU-side hitch.",
        "Look at which metric SPIKED: MsCPUBusy = 42ms is the culprit — it blew the frame budget. "
        "GPU was normal at 13ms.",
        "Which value exceeded the 16.7ms budget for 60fps?",
        "CPU spikes like this often come from asset streaming, shader compilation, or garbage collection pauses.",
        2,
    ),
    Quiz(5,
        "FPS = 90. MsGPULatency = 22ms. MsClickToPhotonLatency = 75ms. MsCPUBusy = 4ms. Which enemy?",
        (
            Option("CPU Bottleneck — MsCPUBusy needs to be higher to feed the GPU",                    False),
            Option("Excessive frame buffering — GPU queue is too deep, adding huge latency",            True),
            Option("Frame pacing issue — frames arriving unevenly at the display",                      False),
            Option("GPU Bottleneck — the GPU cannot process frames fast enough for 90fps",              False),
        ),
        "Enemy D — Excessive buffering! MsGPULatency = 22ms means frames queue 22ms before GPU starts. "
        "Fix: Anti-Lag, cap FPS, max pre-rendered frames = 1.",
        "The key clue is MsGPULatency = 22ms. Frames sit in the GPU queue for 22ms before processing. "
        "Classic over-buffering: great FPS but terrible input latency.",
        "FPS is fine. CPU is fast. But something is adding 75ms of total latency...",
        "NVIDIA Reflex, AMD Anti-Lag, and Intel Anti-Lag all work by reducing the GPU queue depth.",
        3,
    ),
    Quiz(6,
        "Game A: Avg 90fps, 1% Low 85fps. Game B: Avg 90fps, 1% Low 42fps. Which feels smoother?",
        (
            Option("Game B — it has moments of higher performance that feel snappy",                    False),
            Option("Game A — its 1% Low is close to average, meaning very consistent frametimes",       True),
            Option("They feel identical — average FPS is all that matters for smoothness",              False),
            Option("Game B — higher variance means more dynamic rendering which looks better",          False),
        ),
        "Game A by a mile! Same average but Game B's 1% Low of 42fps means awful occasional frames. "
        "Game A's 85fps 1% Low is only 5fps below average — near-perfect consistency.",
        "Game A wins. Both average 90fps, but Game B's 1% Low (42fps) reveals terrible spikes. "
        "1% Low is far more honest than average FPS. Average lies; 1% Low tells the truth.",
        "Both average 90fps — so look at what happens in the worst 1% of frames...",
        "Some games intentionally sacrifice 1% Low for higher averages. Competitive games should prioritize 1% Low.",
        3,
    ),
    Quiz(7,
        "You want to test if lowering shadows improves performance. What is the correct approach?",
        (
            Option("Lower shadows mid-game and watch the live FPS counter go up in real time",          False),
            Option("Capture CSV with shadows ON in a fixed scene, then OFF, then compare both CSVs",   True),
            Option("Run any benchmark and compare the single final average FPS number",                 False),
            Option("Enable PresentMon overlay and toggle the setting to see instant changes",           False),
        ),
        "The scientific method! Same fixed scene, one variable changed, two CSVs compared. "
        "Check: did MsGPUBusy drop? Did 1% Low improve? That's how real analysis works.",
        "Correct approach: same fixed scene, change ONE setting, capture two CSVs, compare side by side. "
        "Live readings fluctuate too much. Control everything except the one setting.",
        "What makes a comparison scientifically valid? Think about variables...",
        "Professionals call this A/B testing. The GPU trace with shadows ON is your control group.",
        3,
    ),
]
