# 🕵️ Frame Detective — PresentMon Learning Game

A retro-style RPG learning game that teaches Intel PresentMon through 8 missions,
boss battles, XP, and a certificate of mastery. Built in pure Python — zero external
runtime dependencies.

---

## Quick Start

```bash
python main.py
```

Opens automatically in your default browser at `http://127.0.0.1:<port>`.  
Press **Ctrl+C** to quit.

**Requirements:** Python 3.9+

---

## Project Structure

```
FrameDetective/
├── main.py                     # Entry point — run this
│
├── app/
│   ├── server.py               # HTTP server + URL router
│   │
│   ├── models/                 # Data layer (pure Python dataclasses)
│   │   ├── mission.py          # Mission — id, name, badge, XP, boss info
│   │   └── quiz.py             # Quiz — question, 3 options, win/lose text
│   │
│   ├── templates/              # HTML generation layer
│   │   ├── base.py             # Page shell — wraps every page in DOCTYPE + CSS + JS
│   │   ├── styles.py           # CSS (inlined into every page)
│   │   ├── scripts.py          # Shared JS — localStorage state, HUD, XP, HP
│   │   └── components.py       # Reusable HTML components (HUD, boss, cards...)
│   │
│   └── views/                  # Page renderers — one per URL route
│       ├── __init__.py         # Route registry { path: renderer }
│       ├── index.py            # / and /index.html — Title screen
│       ├── map.py              # /map.html — Mission select
│       ├── missions.py         # /mission-1.html … /mission-8.html
│       └── win.py              # /win.html — Certificate screen
│
├── tests/
│   └── test_all.py             # 43 unit tests (models, templates, views, server)
│
└── requirements.txt
```

---

## Architecture

### Layer separation

| Layer | Responsibility | Files |
|---|---|---|
| **Models** | Pure data — no HTML, no rendering | `models/mission.py`, `models/quiz.py` |
| **Templates** | HTML string builders — no business logic | `templates/*.py` |
| **Views** | Compose models + templates into full pages | `views/*.py` |
| **Server** | Route HTTP requests to views | `server.py` |

### Request flow

```
Browser GET /mission-3.html
    └─▶ server.py         looks up route in ROUTES dict
    └─▶ views/missions.py render_mission(2)
            ├─▶ models    reads MISSIONS[2], QUIZZES[2]
            ├─▶ templates/components.py  builds HUD, boss section, content blocks
            └─▶ templates/base.py        wraps in full HTML shell
    └─▶ server.py         sends 200 response with HTML bytes
```

### State management

Game progress (XP, HP, completed missions) lives in browser **localStorage** — 
no server-side sessions, no database. Each page reads and writes the same JSON key.

```js
// Shared across all pages via templates/scripts.py
getState()       // → { xp, level, hp, done[], answered{} }
saveState(s)     // persists to localStorage
clearState()     // called on "Begin Mission" and "Play Again"
```

---

## Game Pages (11 routes)

| URL | Page |
|---|---|
| `/` or `/index.html` | Title screen → Begin Mission |
| `/map.html` | Mission select map |
| `/mission-1.html` | Mission 1: What Is PresentMon? |
| `/mission-2.html` | Mission 2: The Frame Pipeline |
| `/mission-3.html` | Mission 3: Metrics Deep Dive |
| `/mission-4.html` | Mission 4: Present Modes |
| `/mission-5.html` | Mission 5: Reading Raw Traces |
| `/mission-6.html` | Mission 6: Diagnose & Fix |
| `/mission-7.html` | Mission 7: Graphs & Stats |
| `/mission-8.html` | Mission 8: The Final Mission |
| `/win.html` | Certificate of Mastery |

---

## Adding a New Mission

1. **Add data** — append a `Mission` to `app/models/mission.py` and a `Quiz` to `app/models/quiz.py`
2. **Add content** — add `_m8()` function in `app/views/missions.py`
3. **Register route** — add `/mission-9.html` in `app/views/__init__.py`
4. **Run tests** — `python tests/test_all.py`

---

## Running Tests

```bash
# With stdlib unittest (no install needed)
python tests/test_all.py

# With pytest (optional)
pip install pytest
pytest tests/ -v
```

43 tests covering models, templates, views, and server.
