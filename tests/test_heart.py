import unittest
import math
import sys
import os

# Ensure repo root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from heart import (
    heart_points,
    compute_pulse_scale,
    compute_pulse_scale_bpm,
    generate_sparkle_points,
    resolve_word_list,
    render_to_svg,
    export_heart_metadata_json,
    outline_positions_headless,
    PRESETS,
    PALETTES,
    WORDS,
    LANGUAGE_GROUPS,
)


class TestHeartCore(unittest.TestCase):
    def test_heart_points_count_and_closure(self):
        steps = 100
        points = heart_points(scale=10, steps=steps)
        self.assertEqual(len(points), steps + 1)
        # Symmetrical property: points at x=0 or mirrored
        start_x, _ = points[0]
        self.assertAlmostEqual(start_x, 0.0, places=2)

    def test_compute_pulse_scale_bounds(self):
        # Resting phase (t > 0.35) should be 1.0
        self.assertEqual(compute_pulse_scale(0.5), 1.0)
        self.assertEqual(compute_pulse_scale(0.8), 1.0)
        # Peak of first beat (t ~ 0.08) should be > 1.0
        scale_peak = compute_pulse_scale(0.08)
        self.assertGreater(scale_peak, 1.0)
        self.assertLessEqual(scale_peak, 1.15)

    def test_generate_sparkle_points(self):
        poly = heart_points(scale=20, steps=50)
        sparkles = generate_sparkle_points(poly, count=15, jitter=10)
        self.assertEqual(len(sparkles), 15)
        for x, y, symbol, size in sparkles:
            self.assertIn(symbol, ["✦", "•", "✨", "*"])
            self.assertGreaterEqual(size, 8)
            self.assertLessEqual(size, 14)

    def test_resolve_word_list_default(self):
        words = resolve_word_list(None, "all")
        self.assertEqual(words, WORDS)

    def test_resolve_word_list_custom_csv(self):
        words = resolve_word_list("alpha,beta,gamma", "all")
        self.assertGreaterEqual(len(words), 40)
        self.assertIn("alpha", words)
        self.assertIn("beta", words)

    def test_resolve_word_list_family_filter(self):
        words = resolve_word_list(None, "romance")
        self.assertGreaterEqual(len(words), 40)
        self.assertIn("amour", words)
        self.assertIn("amore", words)

    def test_presets_structure(self):
        for name, cfg in PRESETS.items():
            self.assertIn("palette", cfg)
            self.assertIn("sparkles", cfg)
            self.assertIn("pulse", cfg)
            self.assertIn("speed", cfg)
            self.assertLess(cfg["palette"], len(PALETTES))

    def test_render_to_svg(self):
        sample_words = ["Love", "Amour", "Liebe", "Amore"]
        svg = render_to_svg(
            words=sample_words,
            scale=30,
            bg_color="#000000",
            text_color="#ff4f91",
            message="Unit Test <Heart>",
            include_sparkles=True,
        )
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.strip().endswith("</svg>"))
        # Escaped message
        self.assertIn("Unit Test &lt;Heart&gt;", svg)
        self.assertIn("fill=\"#ff4f91\"", svg)

    def test_compute_pulse_scale_bpm(self):
        scale_60 = compute_pulse_scale_bpm(t_seconds=0.08, bpm=60)
        self.assertGreater(scale_60, 1.0)
        self.assertLessEqual(scale_60, 1.15)
        # Clamped limits verification
        scale_low = compute_pulse_scale_bpm(0.08, bpm=10)
        self.assertGreater(scale_low, 1.0)

    def test_render_to_svg_gradient(self):
        sample_words = ["Love", "Peace"]
        svg = render_to_svg(
            words=sample_words,
            scale=30,
            bg_color="#000000",
            text_color="#ff4f91",
            gradient_colors=("#ff007f", "#7928ca"),
        )
        self.assertIn("<linearGradient id=\"heartGrad\"", svg)
        self.assertIn("stop-color=\"#ff007f\"", svg)
        self.assertIn("fill=\"url(#heartGrad)\"", svg)

    def test_export_heart_metadata_json(self):
        words = ["amor", "liebe", "amour"]
        poly = heart_points(scale=20, steps=30)
        spots, _, angles = outline_positions_headless(words, poly)
        json_str = export_heart_metadata_json(words, 20, spots, angles, "#000000", "#ffffff")
        self.assertIn('"scale": 20', json_str)
        self.assertIn('"word_count": 3', json_str)
        self.assertIn('"word": "amor"', json_str)


if __name__ == "__main__":
    unittest.main()
