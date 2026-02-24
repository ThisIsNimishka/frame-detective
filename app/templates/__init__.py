"""app/templates — HTML generation layer"""
from .base       import base
from .components import (hud, briefing, card, metric_card, range_tag,
                         scenario, sign, pipeline, boss_section)
from .styles     import CSS
from .scripts    import SHARED_JS

__all__ = [
    "base", "hud", "briefing", "card", "metric_card", "range_tag",
    "scenario", "sign", "pipeline", "boss_section", "CSS", "SHARED_JS",
]
