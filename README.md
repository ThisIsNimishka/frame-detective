# Frame Detective 🕵️

**A cyberpunk quiz game for learning Intel PresentMon frame analysis** — 8 missions, boss battles, XP system, and a Certificate of Mastery.

---

## What Is It?

Frame Detective is a browser-based learning game served locally via Python. You play as a detective solving frame-rate crimes using PresentMon, Intel's open-source frame-analysis tool.

**8 Cases to Crack:**
| Case | Topic |
|------|-------|
| 01 | What Is PresentMon? |
| 02 | The Frame Pipeline |
| 03 | Metrics Deep Dive |
| 04 | Present Modes |
| 05 | Reading Raw Traces |
| 06 | Diagnose & Fix |
| 07 | Graphs & Stats |
| 08 | The Final Mission |

---

## How to Run

```bash
# 1 — Install Python 3.10+
# 2 — Clone and launch:
python main.py
# 3 — Open your browser:
#     http://localhost:5050
```

No external dependencies. No npm. No build step.

---

## Game Features

- 🎮 **8 Boss Battle Quizzes** — 60-second countdown timer, keyboard shortcuts (A/B/C/D)
- ⚡ **XP & Level System** — earn XP, speed bonuses, level up
- ❤️ **3 Lives (HP)** — wrong answers cost HP with damage effects
- 🔥 **Streak Tracker** — build a combo for bonus XP
- 🏅 **8 Mission Badges** — collected in the HUD
- 🏆 **Certificate of Mastery** — printable at the end
- 💡 **Timed Hints** — appear after 20 seconds of inaction
- ✨ **Particle FX, confetti, screen-shake animations**
- 🌌 **Animated starfield background** with CRT scanlines

---

## Architecture

```
FD/
├── main.py                  ← Launch: python main.py
├── app/
│   ├── server/              ← Minimal HTTP server (stdlib only)
│   ├── models/              ← Mission + Quiz data
│   ├── views/               ← Page renderers (index, map, missions, win)
│   └── templates/
│       ├── base.py          ← HTML shell (CSS + JS inline)
│       ├── styles.py        ← Full CSS (sci-fi cyberpunk theme)
│       ├── scripts.py       ← Game engine JS (XP, timer, FX)
│       └── components.py    ← HUD, boss section, briefing, cards
└── tests/
    └── test_all.py          ← 53 unit tests
```

---

## Running Tests

```bash
python -m unittest discover tests
# Expected: ...53 tests... OK
```

---

## GitHub

Repository: [github.com/ThisIsNimishka/frame-detective](https://github.com/ThisIsNimishka/frame-detective)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+ stdlib (http.server) |
| Frontend | Vanilla HTML / CSS / JS — no frameworks |
| Fonts | Google Fonts (Orbitron, Rajdhani) |
| FX | Canvas starfield, CSS animations, Web Audio ready |

---

*"Every frame leaves a trace. You just have to know where to look."*
