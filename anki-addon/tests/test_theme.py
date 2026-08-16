"""
Unit tests for Pure Black Theme Palette and Style Generation.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from theme.engine import ThemeEngine
from theme.palette import PALETTE, ThemePalette, is_light_color, get_adaptive_palette
from theme.styles import generate_qss, generate_webview_css


class TestTheme(unittest.TestCase):
    def test_palette_pure_black(self):
        self.assertEqual(PALETTE.BACKGROUND_PURE_BLACK, "#000000")
        self.assertEqual(PALETTE.TEXT_PRIMARY, "#FFFFFF")

    def test_is_light_color_detection(self):
        self.assertTrue(is_light_color("#FFFFFF"))
        self.assertTrue(is_light_color("#F3F4F6"))
        self.assertTrue(is_light_color("#E0E7FF"))
        self.assertFalse(is_light_color("#000000"))
        self.assertFalse(is_light_color("#0B0E14"))
        self.assertFalse(is_light_color("#121214"))

    def test_adaptive_light_palette_contrast(self):
        light_pal = get_adaptive_palette("#FFFFFF")
        self.assertEqual(light_pal.TEXT_PRIMARY, "#09090B")
        self.assertIn("rgba(0, 0, 0", light_pal.BORDER_SUBTLE)

        dark_pal = get_adaptive_palette("#000000")
        self.assertEqual(dark_pal.TEXT_PRIMARY, "#FFFFFF")
        self.assertIn("rgba(255, 255, 255", dark_pal.BORDER_SUBTLE)

    def test_generate_qss(self):
        # Test Dark QSS
        qss_dark = generate_qss(PALETTE, accent="#3B82F6", bg_color="#000000")
        self.assertIn("#000000", qss_dark)
        self.assertIn("#FFFFFF", qss_dark)
        self.assertIn("QMainWindow", qss_dark)

        # Test Light QSS (Adapts to #09090B font)
        qss_light = generate_qss(PALETTE, accent="#0A84FF", bg_color="#FFFFFF")
        self.assertIn("#FFFFFF", qss_light)
        self.assertIn("#09090B", qss_light)

    def test_generate_webview_css(self):
        css = generate_webview_css(PALETTE, accent="#10B981", bg_color="#000000")
        self.assertIn("#000000 !important", css)
        self.assertIn(".cloze", css)
        self.assertIn(".nightMode", css)

    def test_theme_engine_headless(self):
        engine = ThemeEngine()
        engine.activate()
        self.assertTrue(engine.is_active())
        engine.deactivate()
        self.assertFalse(engine.is_active())


if __name__ == "__main__":
    unittest.main()
