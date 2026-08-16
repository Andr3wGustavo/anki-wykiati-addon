"""
Standalone GUI Preview Runner for Anki Discord Toolkit.
Allows inspecting the iOS Liquid Glass dialogs directly without running Anki Desktop.
"""

import os
import sys

# Ensure addon root is in sys.path
ADDON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "anki-addon")
if ADDON_DIR not in sys.path:
    sys.path.insert(0, ADDON_DIR)

from theme.palette import PALETTE
from theme.styles import generate_qss

try:
    from PyQt6.QtWidgets import QApplication
    QT_LIB = "PyQt6"
except ImportError:
    try:
        from PyQt5.QtWidgets import QApplication
        QT_LIB = "PyQt5"
    except ImportError:
        try:
            from PySide6.QtWidgets import QApplication
            QT_LIB = "PySide6"
        except ImportError:
            print("[ERROR] Neither PyQt6, PyQt5, nor PySide6 is installed.")
            print("To preview the native Qt window standalone, run: pip install PyQt6")
            print("Or view the HTML live preview by opening 'preview.html' in your browser!")
            sys.exit(0)

from ui.about_dialog import AboutDialog
from ui.dashboard import DashboardDialog
from ui.deck_rules_dialog import DeckRulesDialog
from ui.discord_settings import DiscordSettingsDialog
from ui.help_dialog import HelpDialog
from ui.theme_settings import ThemeSettingsDialog


def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "dashboard"
    print(f"[*] Starting Standalone GUI Preview ({target}) with {QT_LIB}...")
    app = QApplication(sys.argv)
    
    # Apply Liquid Glass theme
    qss = generate_qss()
    app.setStyleSheet(qss)
    
    if target in ("theme", "rgb", "color"):
        dlg = ThemeSettingsDialog()
    elif target in ("discord", "image", "images"):
        dlg = DiscordSettingsDialog()
    elif target in ("help", "guide"):
        dlg = HelpDialog()
    elif target in ("rules", "deck"):
        dlg = DeckRulesDialog()
    elif target in ("about", "info"):
        dlg = AboutDialog()
    else:
        dlg = DashboardDialog()
        
    dlg.show()
    
    print(f"[OK] Preview Dialog ({target}) is now active on your screen!")
    sys.exit(app.exec() if hasattr(app, "exec") else app.exec_())


if __name__ == "__main__":
    main()
