"""
tests/test_all.py
-----------------
Full test suite for Frame Detective.
Run with:  python tests/test_all.py   (or pytest from project root)
"""
import sys, os, threading, time, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest

# ── Model imports ────────────────────────────────────────────
from app.models.mission import MISSIONS, Mission
from app.models.quiz    import QUIZZES, Quiz, Option


class TestMissions(unittest.TestCase):

    def test_mission_count(self):
        self.assertEqual(len(MISSIONS), 8)

    def test_mission_ids_sequential(self):
        for i, m in enumerate(MISSIONS):
            self.assertEqual(m.id, i)

    def test_missions_have_required_fields(self):
        for m in MISSIONS:
            self.assertTrue(m.icon)
            self.assertTrue(m.name)
            self.assertTrue(m.desc)
            self.assertTrue(m.badge)
            self.assertTrue(m.badge_name)
            self.assertGreater(m.xp, 0)
            self.assertTrue(m.boss_emoji)
            self.assertTrue(m.boss_name)
            self.assertTrue(m.next_page)

    def test_mission_flavor_quote_nonempty(self):
        for m in MISSIONS:
            self.assertTrue(m.flavor_quote, f"Mission {m.id} missing flavor_quote")

    def test_mission_difficulty_stars_valid(self):
        for m in MISSIONS:
            self.assertIn(m.difficulty_stars, (1, 2, 3),
                          f"Mission {m.id} difficulty_stars out of range")

    def test_last_mission_links_to_win(self):
        self.assertEqual(MISSIONS[-1].next_page, "win.html")

    def test_non_last_missions_link_sequentially(self):
        for i, m in enumerate(MISSIONS[:-1]):
            expected = f"mission-{i + 2}.html"
            self.assertEqual(m.next_page, expected, f"Mission {i} next_page mismatch")


class TestQuizzes(unittest.TestCase):

    def test_quiz_count(self):
        self.assertEqual(len(QUIZZES), 8)

    def test_quiz_matches_mission_ids(self):
        mission_ids = {m.id for m in MISSIONS}
        quiz_ids    = {q.mission_id for q in QUIZZES}
        self.assertEqual(mission_ids, quiz_ids)

    def test_exactly_four_options_per_quiz(self):
        for q in QUIZZES:
            self.assertEqual(len(q.options), 4,
                             f"Quiz {q.mission_id} has {len(q.options)} options, expected 4")

    def test_exactly_one_correct_per_quiz(self):
        for q in QUIZZES:
            correct_count = sum(1 for o in q.options if o.correct)
            self.assertEqual(correct_count, 1,
                             f"Quiz {q.mission_id} has {correct_count} correct options, expected 1")

    def test_quiz_hint_nonempty(self):
        for q in QUIZZES:
            self.assertTrue(q.hint, f"Quiz {q.mission_id} missing hint")

    def test_quiz_fun_fact_nonempty(self):
        for q in QUIZZES:
            self.assertTrue(q.fun_fact, f"Quiz {q.mission_id} missing fun_fact")

    def test_quiz_difficulty_valid(self):
        for q in QUIZZES:
            self.assertIn(q.difficulty, (1, 2, 3),
                          f"Quiz {q.mission_id} difficulty {q.difficulty} out of range")

    def test_quiz_win_lose_text_nonempty(self):
        for q in QUIZZES:
            self.assertTrue(q.win_text,  f"Quiz {q.mission_id} missing win_text")
            self.assertTrue(q.lose_text, f"Quiz {q.mission_id} missing lose_text")


# ── Template imports ──────────────────────────────────────────
from app.templates.base     import base
from app.templates.styles   import CSS
from app.templates.scripts  import SHARED_JS
from app.templates.components import (
    hud, briefing, card, boss_section, pipeline,
)


class TestTemplates(unittest.TestCase):

    def test_css_nonempty(self):
        self.assertGreater(len(CSS), 100)

    def test_shared_js_nonempty(self):
        self.assertGreater(len(SHARED_JS), 100)

    def test_base_returns_html(self):
        html = base("Test", "<p>hello</p>")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Test", html)
        self.assertIn("<p>hello</p>", html)

    def test_base_inlines_css(self):
        html = base("T", "")
        self.assertIn("<style>", html)
        self.assertIn(CSS[:30], html)

    def test_base_inlines_js(self):
        html = base("T", "")
        self.assertIn(SHARED_JS[:30], html)

    def test_base_has_starfield(self):
        html = base("T", "")
        self.assertIn('id="bgcanvas"', html)

    def test_hud_has_hearts(self):
        h = hud()
        self.assertIn('id="ht0"', h)
        self.assertIn('id="ht2"', h)

    def test_hud_has_streak(self):
        h = hud()
        self.assertIn('id="hud-streak"', h)

    def test_hud_has_badges(self):
        h = hud()
        for i in range(8):
            self.assertIn(f'id="bdg{i}"', h)

    def test_hud_has_xp_bar(self):
        h = hud()
        self.assertIn('id="xp-fill"', h)

    def test_briefing_renders_speaker(self):
        b = briefing("AGENT X", "some text")
        self.assertIn("AGENT X", b)
        self.assertIn("some text", b)

    def test_card_renders_label(self):
        c = card("LABEL", "Title", "<p>Body</p>")
        self.assertIn("LABEL", c)
        self.assertIn("Title", c)

    def test_boss_section_renders_four_options(self):
        opts = [
            ("Option A", False),
            ("Option B", True),
            ("Option C", False),
            ("Option D", False),
        ]
        bs = boss_section(0, "👻", "Ghost", "Question?", opts, "win.html", 100, "hint text", "fun fact")
        opt_buttons = bs.count('class="qbtn"')
        self.assertEqual(opt_buttons, 4)

    def test_boss_section_correct_has_data_attr(self):
        opts = [("A",False),("B",True),("C",False),("D",False)]
        bs = boss_section(0,"👻","G","Q?",opts,"next.html",100)
        self.assertIn('data-correct="1"', bs)

    def test_boss_section_has_timer(self):
        opts = [("A",False),("B",True),("C",False),("D",False)]
        bs = boss_section(0,"👻","G","Q?",opts,"next.html",100)
        self.assertIn('timer-fill', bs)

    def test_boss_section_has_hint(self):
        opts = [("A",False),("B",True),("C",False),("D",False)]
        bs = boss_section(0,"👻","G","Q?",opts,"next.html",100,"my hint")
        self.assertIn("my hint", bs)

    def test_pipeline_renders(self):
        p = pipeline()
        self.assertIn("pipe-row", p)
        self.assertIn("pipe-stage", p)

    def test_base_extra_js_injected(self):
        html = base("T", "", "var x = 1;")
        self.assertIn("var x = 1;", html)


# ── Views ─────────────────────────────────────────────────────
from app.views.index    import render_index
from app.views.map      import render_map
from app.views.win      import render_win
from app.views.missions import (
    render_mission_1, render_mission_2, render_mission_3, render_mission_4,
    render_mission_5, render_mission_6, render_mission_7, render_mission_8,
)

MISSION_RENDERS = [
    render_mission_1, render_mission_2, render_mission_3, render_mission_4,
    render_mission_5, render_mission_6, render_mission_7, render_mission_8,
]


class TestViews(unittest.TestCase):

    def test_index_renders(self):
        html = render_index()
        self.assertIn("FRAME", html)
        self.assertIn("DETECTIVE", html)
        self.assertIn("BEGIN MISSION", html)

    def test_index_has_continue_logic(self):
        html = render_index()
        self.assertIn("btn-continue", html)

    def test_map_renders_all_eight_missions(self):
        html = render_map()
        for m in MISSIONS:
            self.assertIn(m.name, html)

    def test_map_has_progress_bar(self):
        html = render_map()
        self.assertIn("map-prog-fill", html)

    def test_map_has_flavor_quotes(self):
        html = render_map()
        for m in MISSIONS:
            self.assertIn(m.flavor_quote[:20], html)

    def test_win_renders(self):
        html = render_win()
        self.assertIn("CERTIFICATE OF MASTERY", html)

    def test_win_has_confetti(self):
        html = render_win()
        self.assertIn("spawnConfetti", html)

    def test_win_has_all_badges(self):
        html = render_win()
        for m in MISSIONS:
            self.assertIn(m.badge, html)

    def test_win_has_stats_grid(self):
        html = render_win()
        self.assertIn("stat-xp", html)
        self.assertIn("stat-lvl", html)

    def test_all_mission_pages_render(self):
        for i, fn in enumerate(MISSION_RENDERS):
            html = fn()
            self.assertIn("<!DOCTYPE html>", html, f"Mission {i + 1} render failed")
            self.assertIn("boss-arena", html, f"Mission {i + 1} missing boss arena")

    def test_all_mission_pages_have_four_options(self):
        for i, fn in enumerate(MISSION_RENDERS):
            html = fn()
            count = html.count('class="qbtn"')
            self.assertEqual(count, 4,
                             f"Mission {i + 1} has {count} quiz buttons, expected 4")

    def test_timer_js_present_in_missions(self):
        for i, fn in enumerate(MISSION_RENDERS):
            html = fn()
            self.assertIn("startTimer", html,
                          f"Mission {i + 1} missing timer JS")

    def test_quiz_data_injected(self):
        for i, fn in enumerate(MISSION_RENDERS):
            html = fn()
            self.assertIn("QUIZ_WIN", html,  f"Mission {i + 1} missing QUIZ_WIN")
            self.assertIn("QUIZ_LOSE", html, f"Mission {i + 1} missing QUIZ_LOSE")
            self.assertIn("QUIZ_HINT", html, f"Mission {i + 1} missing QUIZ_HINT")

    def test_mission_pages_have_back_link(self):
        for i, fn in enumerate(MISSION_RENDERS):
            html = fn()
            self.assertIn("map.html", html, f"Mission {i + 1} missing back link")


# ── Routes ────────────────────────────────────────────────────
from app.views import ROUTES


class TestRoutes(unittest.TestCase):

    def test_required_routes_registered(self):
        expected = ["/", "/index.html", "/map.html",
                    "/mission-1.html", "/mission-2.html", "/mission-3.html",
                    "/mission-4.html", "/mission-5.html", "/mission-6.html",
                    "/mission-7.html", "/mission-8.html", "/win.html"]
        for path in expected:
            self.assertIn(path, ROUTES, f"Route {path} not registered")

    def test_all_routes_callable(self):
        for path, fn in ROUTES.items():
            self.assertTrue(callable(fn), f"Route {path} is not callable")

    def test_all_routes_return_html(self):
        for path, fn in ROUTES.items():
            html = fn()
            self.assertIn("<!DOCTYPE html>", html, f"Route {path} didn't return HTML")

    def test_route_count(self):
        self.assertGreaterEqual(len(ROUTES), 12)


# ── Server ────────────────────────────────────────────────────
from app.server import Server


class TestServer(unittest.TestCase):

    def test_can_instantiate_server(self):
        s = Server(port=0)
        self.assertIsNotNone(s)

    def test_server_has_free_port_method(self):
        port = Server._free_port()
        self.assertGreater(port, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
