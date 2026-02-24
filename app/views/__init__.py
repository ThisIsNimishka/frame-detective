"""
app/views/__init__.py
---------------------
Central route registry.  Maps URL path → page renderer function.

Every renderer returns a complete HTML string.
"""
from .index    import render_index
from .map      import render_map
from .win      import render_win
from .missions import (
    render_mission_1, render_mission_2, render_mission_3, render_mission_4,
    render_mission_5, render_mission_6, render_mission_7, render_mission_8,
)

MISSION_RENDERS = [
    render_mission_1, render_mission_2, render_mission_3, render_mission_4,
    render_mission_5, render_mission_6, render_mission_7, render_mission_8,
]
from .quit     import render_quit

# Route table: path → callable
ROUTES: dict[str, callable] = {
    "/":               render_index,
    "/index.html":     render_index,
    "/map.html":       render_map,
    "/mission-1.html": render_mission_1,
    "/mission-2.html": render_mission_2,
    "/mission-3.html": render_mission_3,
    "/mission-4.html": render_mission_4,
    "/mission-5.html": render_mission_5,
    "/mission-6.html": render_mission_6,
    "/mission-7.html": render_mission_7,
    "/mission-8.html": render_mission_8,
    "/win.html":       render_win,
    "/quit":           render_quit,
}

__all__ = ["ROUTES"]
