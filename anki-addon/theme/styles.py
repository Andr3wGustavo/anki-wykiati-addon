"""
Stylesheet Generators for Native Qt (QSS) and Webviews (CSS).
Ensures Pure Black (#000000) AMOLED compliance with high contrast legibility.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate comprehensive Qt StyleSheet (QSS) for Anki's main window and dialogs.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK
    surf = palette.BACKGROUND_SURFACE
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    surf_hov = palette.BACKGROUND_SURFACE_HOVER
    border = palette.BORDER_DEFAULT
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* --- Pure Black Global Reset --- */
    QWidget {{
        background-color: {bg};
        color: {text};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 13px;
        selection-background-color: {acc};
        selection-color: {palette.TEXT_PRIMARY};
    }}

    QMainWindow, QDialog {{
        background-color: {bg};
        color: {text};
    }}

    /* --- Menus & Toolbars --- */
    QMenuBar {{
        background-color: {bg};
        color: {text};
        border-bottom: 1px solid {palette.BORDER_SUBTLE};
        padding: 2px 4px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: 4px 8px;
        border-radius: 4px;
    }}
    QMenuBar::item:selected {{
        background-color: {surf_hov};
        color: {text};
    }}
    QMenu {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 4px 0px;
    }}
    QMenu::item {{
        padding: 6px 24px 6px 12px;
    }}
    QMenu::item:selected {{
        background-color: {acc};
        color: #FFFFFF;
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {palette.BORDER_SUBTLE};
        margin: 4px 8px;
    }}

    /* --- Buttons --- */
    QPushButton {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 6px 16px;
        font-weight: 500;
        min-height: 22px;
    }}
    QPushButton:hover {{
        background-color: {surf_hov};
        border-color: {palette.BORDER_STRONG};
    }}
    QPushButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: {acc};
        border-color: {acc};
        color: #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: {palette.ACCENT_HOVER};
        border-color: {palette.ACCENT_HOVER};
    }}
    QPushButton:disabled {{
        background-color: {surf};
        color: {palette.TEXT_DISABLED};
        border-color: {palette.BORDER_SUBTLE};
    }}

    /* --- Inputs & Text Controls --- */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {surf};
        color: {text};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 6px 10px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: {bg};
    }}
    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QComboBox:disabled {{
        background-color: {surf};
        color: {palette.TEXT_DISABLED};
    }}

    /* --- Combo Boxes --- */
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        selection-background-color: {acc};
        selection-color: #FFFFFF;
        outline: none;
    }}

    /* --- Group Box & Frames --- */
    QGroupBox {{
        background-color: {bg};
        border: 1px solid {border};
        border-radius: 8px;
        margin-top: 24px;
        padding: 16px 12px 12px 12px;
        font-weight: bold;
        color: {text};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        top: 6px;
        padding: 0 6px;
        background-color: {bg};
        color: {acc};
    }}

    /* --- Tables, Trees, Lists --- */
    QTableView, QListView, QTreeView {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 6px;
        gridline-color: {palette.BORDER_SUBTLE};
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
    }}
    QHeaderView::section {{
        background-color: {surf_el};
        color: {text_sec};
        border: none;
        border-bottom: 1px solid {border};
        border-right: 1px solid {palette.BORDER_SUBTLE};
        padding: 6px 10px;
        font-weight: 600;
    }}

    /* --- Tab Widget --- */
    QTabWidget::pane {{
        border: 1px solid {border};
        background-color: {bg};
        border-radius: 6px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: {surf};
        color: {text_sec};
        border: 1px solid {border};
        border-bottom: none;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 8px 16px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background-color: {bg};
        color: {acc};
        border-bottom: 1px solid {bg};
        font-weight: bold;
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {surf_hov};
        color: {text};
    }}

    /* --- Scrollbars --- */
    QScrollBar:vertical {{
        background-color: {bg};
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: {palette.BORDER_DEFAULT};
        min-height: 24px;
        border-radius: 5px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {palette.BORDER_STRONG};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: {bg};
        height: 10px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {palette.BORDER_DEFAULT};
        min-width: 24px;
        border-radius: 5px;
        margin: 2px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* --- Checkboxes & Radio Buttons --- */
    QCheckBox, QRadioButton {{
        color: {text};
        spacing: 8px;
    }}
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {border};
        background-color: {surf};
        border-radius: 4px;
    }}
    QRadioButton::indicator {{
        border-radius: 8px;
    }}
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: {acc};
        border-color: {acc};
    }}
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
        border-color: {palette.BORDER_STRONG};
    }}

    /* --- Tooltips --- */
    QToolTip {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 4px 8px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate CSS to inject into Anki's WebViews (Deck Browser, Card Reviewer, etc.)
    forcing #000000 true black background and crisp styling.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK
    surf = palette.BACKGROUND_SURFACE
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    border = palette.BORDER_DEFAULT
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY

    return f"""
    /* --- Pure Black OLED Webview Styles --- */
    html, body, #qa, .card, .nightMode, .night_mode, body.nightMode {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
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
        background-color: {surf} !important;
        border: 1px solid {border} !important;
        color: #93C5FD !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-family: "Fira Code", "JetBrains Mono", Consolas, monospace !important;
    }}
    pre code {{
        padding: 8px !important;
        display: block !important;
    }}
    """
