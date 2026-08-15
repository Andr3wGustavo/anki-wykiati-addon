"""
Unit tests for Pure Black Theme Palette and Style Generation.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from theme.engine import ThemeEngine
from theme.palette import PALETTE, ThemePalette
from theme.styles import generate_qss, generate_webview_css


class TestTheme(unittest.TestCase):
    def test_palette_pure_black(self):
        self.assertEqual(PALETTE.BACKGROUND_PURE_BLACK, "#000000")
        self.assertEqual(PALETTE.TEXT_PRIMARY, "#FFFFFF")

    def test_generate_qss(self):
        qss = generate_qss(PALETTE, accent="#3B82F6")
        self.assertIn("#000000", qss)
        self.assertIn("#3B82F6", qss)
        self.assertIn("QMainWindow", qss)
        self.assertIn("QPushButton", qss)
        self.assertIn("QScrollBar", qss)

    def test_generate_webview_css(self):
        css = generate_webview_css(PALETTE, accent="#10B981")
        self.assertIn("#000000 !important", css)
        self.assertIn("#10B981 !important", css)
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
