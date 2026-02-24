"""
app/models/mission.py
---------------------
Mission dataclass — one per playable level.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Mission:
    id:              int
    icon:            str
    name:            str
    desc:            str
    badge:           str
    badge_name:      str
    xp:              int
    boss_emoji:      str
    boss_name:       str
    next_page:       str   # which HTML page to go to after completing this mission
    flavor_quote:    str   # noir-style quote shown on mission card
    difficulty_stars: int  # 1–3


MISSIONS: list["Mission"] = [
    Mission(0, "🕵️", "What Is PresentMon?",
            "Learn what the tool is and how it secretly watches every frame without slowing anything down.",
            "🔍", "Rookie Detective",  200, "👻", "The Mystery of Lag",       "mission-2.html",
            "\"Every frame leaves a trace. You just have to know where to look.\"", 1),
    Mission(1, "🏭", "The Frame Pipeline",
            "Follow a frame from birth on the CPU to the display. Every millisecond counted.",
            "🏭", "Pipeline Master",   200, "🤖", "The Pipeline Boss",        "mission-3.html",
            "\"A frame is born on the CPU and must survive the GPU to reach the screen.\"", 1),
    Mission(2, "📊", "Metrics Deep Dive",
            "Every CSV column decoded. MsGPUBusy, DisplayedTime, MsClickToPhoton — plain English first.",
            "📊", "Metric Guru",       250, "🧮", "The Numbers Demon",        "mission-4.html",
            "\"The numbers don't lie. But they do whisper — you have to learn to listen.\"", 2),
    Mission(3, "🔀", "Present Modes",
            "Six delivery routes from GPU to screen. Some fast, some painfully slow.",
            "🔀", "Mode Expert",       250, "📦", "The Delivery Boss",        "mission-5.html",
            "\"The fastest frame is worthless if it takes the wrong route to your screen.\"", 2),
    Mission(4, "🔬", "Reading Raw Traces",
            "Open the CSV. Decode the rows. Find the stutter hiding in plain sight.",
            "🔬", "Trace Reader",      300, "🦠", "The Stutter Virus",        "mission-6.html",
            "\"One rogue row in 6000. And yet you felt every millisecond of it.\"", 2),
    Mission(5, "🩺", "Diagnose & Fix",
            "Five real-world scenarios. GPU bound, CPU bound, stutter, latency, frame gen.",
            "🩺", "Frame Doctor",      300, "💀", "The Performance Killer",   "mission-7.html",
            "\"A good detective doesn't guess. They read the evidence and follow the data.\"", 3),
    Mission(6, "📈", "Graphs & Stats",
            "Average FPS lies. Learn 1% lows, percentiles, and what a flat frame-time graph means.",
            "📈", "Graph Wizard",      300, "🌊", "The Stutter Wave",         "mission-8.html",
            "\"Average FPS is a confession. 1% Low is the truth.\"", 3),
    Mission(7, "🛠️", "The Final Mission",
            "Full workflow, commands, Python script, and a cheat sheet for life.",
            "🕵️", "Detective Master", 400, "👑", "The Ultimate Lag Boss",    "win.html",
            "\"You came here chasing lag. You'll leave knowing exactly where it hides.\"", 3),
]
