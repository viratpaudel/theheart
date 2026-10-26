import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from heart import heart_points, outline_positions_headless


class TestGeometryAndContour(unittest.TestCase):
    def test_bounding_box_symmetry(self):
        pts = heart_points(scale=10, steps=360)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # X should be approximately symmetric across x=0
        min_x, max_x = min(xs), max(xs)
        self.assertAlmostEqual(min_x + max_x, 0.0, delta=1.5)
        # Top of the heart should be higher than center
        self.assertGreater(max(ys), 0)

    def test_perimeter_continuity(self):
        pts = heart_points(scale=10, steps=200)
        # Verify no sudden distance jumps between adjacent points
        max_dist = 0
        for i in range(len(pts) - 1):
            d = math.hypot(pts[i+1][0] - pts[i][0], pts[i+1][1] - pts[i][1])
            if d > max_dist:
                max_dist = d
        self.assertLess(max_dist, 10.0)

    def test_headless_positions_angles_range(self):
        words = ["A", "B", "C", "D", "E"]
        poly = heart_points(scale=15, steps=100)
        spots, size, angles = outline_positions_headless(words, poly, font_size=20)
        self.assertEqual(len(spots), len(words))
        self.assertEqual(len(angles), len(words))
        for ang in angles:
            self.assertGreaterEqual(ang, -180.0)
            self.assertLessEqual(ang, 180.0)


if __name__ == "__main__":
    unittest.main()
