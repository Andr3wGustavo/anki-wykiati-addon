"""
Stylesheet Generators for Native Qt (QSS) and Webviews (CSS).
Implements modern iOS Liquid Glass / Frosted Glassmorphism aesthetics with AMOLED black backdrop.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate comprehensive iOS Liquid Glass Qt StyleSheet (QSS).
    Features translucent frosted surfaces, rounded glass buttons, and crisp typography.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK
    surf = palette.BACKGROUND_SURFACE
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    surf_hov = palette.BACKGROUND_SURFACE_HOVER
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* --- iOS Liquid Glass Global Base --- */
    QWidget {{
        background-color: {bg};
        color: {text};
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
        font-size: 13px;
        selection-background-color: {acc};
        selection-color: #FFFFFF;
    }}

    QMainWindow, QDialog {{
        background-color: {bg};
        color: {text};
    }}

    /* --- Menus & Navigation --- */
    QMenuBar {{
        background-color: rgba(15, 17, 22, 0.85);
        color: {text};
        border-bottom: 1px solid {border_subtle};
        padding: 4px 6px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: 6px 12px;
        border-radius: 6px;
    }}
    QMenuBar::item:selected {{
        background-color: {surf_hov};
        color: {text};
    }}
    QMenu {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 12px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 6px 24px 6px 14px;
        border-radius: 6px;
    }}
    QMenu::item:selected {{
        background-color: {acc};
        color: #FFFFFF;
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {border_subtle};
        margin: 4px 8px;
    }}

    /* --- Modern iOS Glass Buttons --- */
    QPushButton {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 7px 18px;
        font-weight: 500;
        min-height: 24px;
    }}
    QPushButton:hover {{
        background-color: {surf_hov};
        border-color: {border_strong};
    }}
    QPushButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: {acc};
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: {palette.ACCENT_HOVER};
        border-color: rgba(255, 255, 255, 0.4);
    }}
    QPushButton:disabled {{
        background-color: rgba(255, 255, 255, 0.03);
        color: {palette.TEXT_DISABLED};
        border-color: {border_subtle};
    }}

    /* --- Glass Input Fields --- */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: rgba(12, 14, 18, 0.85);
        color: {text};
        border: 1px solid {border};
        border-radius: 8px;
        padding: 7px 12px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: rgba(18, 20, 26, 0.95);
    }}
    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QComboBox:disabled {{
        background-color: rgba(10, 10, 12, 0.5);
        color: {palette.TEXT_DISABLED};
    }}

    /* --- Combo Boxes Dropdown --- */
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 8px;
        padding: 4px;
        selection-background-color: {acc};
        selection-color: #FFFFFF;
        outline: none;
    }}

    /* --- iOS Frosted Group Boxes & Cards --- */
    QGroupBox {{
        background-color: rgba(18, 20, 26, 0.65);
        border: 1px solid {border};
        border-radius: 12px;
        margin-top: 24px;
        padding: 18px 14px 14px 14px;
        font-weight: bold;
        color: {text};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 14px;
        top: 6px;
        padding: 0 8px;
        background-color: transparent;
        color: {acc};
    }}

    /* --- Tables, Trees, Lists --- */
    QTableView, QListView, QTreeView {{
        background-color: rgba(12, 14, 18, 0.8);
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        gridline-color: {border_subtle};
        selection-background-color: {palette.ACCENT_SUBTLE};
        selection-color: {text};
        outline: none;
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover {{
        background-color: {surf_hov};
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected {{
        background-color: {palette.ACCENT_SUBTLE};
        color: {acc};
        font-weight: 600;
        border-radius: 4px;
    }}
    QHeaderView::section {{
        background-color: rgba(22, 26, 34, 0.85);
        color: {text_sec};
        border: none;
        border-bottom: 1px solid {border};
        border-right: 1px solid {border_subtle};
        padding: 8px 12px;
        font-weight: 600;
    }}

    /* --- Floating Capsule Tabs --- */
    QTabWidget::pane {{
        border: 1px solid {border};
        background-color: rgba(14, 16, 20, 0.7);
        border-radius: 12px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: rgba(24, 28, 36, 0.6);
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 8px 18px;
        margin-right: 4px;
    }}
    QTabBar::tab:selected {{
        background-color: rgba(14, 16, 20, 0.95);
        color: {acc};
        border: 1px solid {border};
        border-bottom: 1px solid transparent;
        font-weight: 600;
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {surf_hov};
        color: {text};
    }}

    /* --- Thin Pill Scrollbars --- */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.2);
        min-height: 28px;
        border-radius: 4px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.35);
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: transparent;
        height: 8px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.2);
        min-width: 28px;
        border-radius: 4px;
        margin: 2px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* --- Checkboxes & Switches --- */
    QCheckBox, QRadioButton {{
        color: {text};
        spacing: 10px;
    }}
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {border_strong};
        background-color: rgba(20, 22, 28, 0.7);
        border-radius: 5px;
    }}
    QRadioButton::indicator {{
        border-radius: 9px;
    }}
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: {acc};
        border-color: {acc};
    }}
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
        border-color: {acc};
    }}

    /* --- Tooltips --- */
    QToolTip {{
        background-color: rgba(28, 32, 42, 0.95);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 6px;
        padding: 6px 10px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate CSS for Anki's WebViews (Deck Browser, Card Reviewer, etc.)
    with frosted glass card containers and high contrast readability.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK
    surf = palette.BACKGROUND_SURFACE
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    border = palette.BORDER_DEFAULT
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY

    return f"""
    /* --- iOS Liquid Glass Webview Styles --- */
    html, body, #qa, .card, .nightMode, .night_mode, body.nightMode {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif !important;
    }}

    /* Card Container with Frosted Glass */
    .card {{
        background: rgba(18, 20, 26, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
    }}

    /* Images */
    img {{
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        margin: 12px 0 !important;
        display: block !important;
    }}

    /* Links and Buttons */
    a {{
        color: {acc} !important;
        text-decoration: none !important;
    }}
    a:hover {{
        text-decoration: underline !important;
    }}

    /* Cloze Deletions */
    .cloze {{
        color: {palette.CLOZE_COLOR} !important;
        font-weight: 700 !important;
        background: rgba(94, 92, 230, 0.15) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }}

    /* Tables & Boxes */
    table, th, td {{
        border-color: {border} !important;
    }}
    th {{
        background-color: {surf_el} !important;
        color: {text} !important;
    }}
    tr:nth-child(even) td {{
        background-color: {surf} !important;
    }}

    /* Deck Browser Counts */
    .new-count {{
        color: {acc} !important;
        font-weight: bold !important;
    }}
    .learn-count {{
        color: {palette.ERROR} !important;
        font-weight: bold !important;
    }}
    .review-count {{
        color: {palette.SUCCESS} !important;
        font-weight: bold !important;
    }}

    /* Code Blocks */
    pre, code {{
        background-color: rgba(14, 16, 22, 0.9) !important;
        border: 1px solid {border} !important;
        color: #64D2FF !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        font-family: "SF Mono", "Fira Code", "JetBrains Mono", Consolas, monospace !important;
    }}
    pre code {{
        padding: 12px !important;
        display: block !important;
    }}
    """
