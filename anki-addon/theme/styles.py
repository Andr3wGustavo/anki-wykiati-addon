"""
Comprehensive Stylesheet Generators for Native Qt (QSS) and Webviews (CSS).
Implements True Full Black (#000000 OLED) with modern iOS Liquid Glass surfaces.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate comprehensive Full Black (#000000) and iOS Liquid Glass Qt StyleSheet (QSS).
    Targets all standard Qt widgets, Anki custom frames, and modal dialogs.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    surf = palette.BACKGROUND_SURFACE   # rgba(18, 21, 28, 0.75)
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    surf_hov = palette.BACKGROUND_SURFACE_HOVER
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       GLOBAL FULL BLACK (#000000) BASE & TYPOGRAPHY
       ========================================================================= */
    * {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
        outline: none;
    }}

    QWidget, QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea {{
        background-color: {bg};
        color: {text};
        selection-background-color: {acc};
        selection-color: #FFFFFF;
    }}

    /* Main Window and Dock Areas */
    QMainWindow::separator {{
        background-color: {border_subtle};
        width: 1px;
        height: 1px;
    }}
    QDockWidget {{
        background-color: {bg};
        color: {text};
        titlebar-close-icon: none;
        titlebar-normal-icon: none;
    }}
    QDockWidget::title {{
        background-color: rgba(14, 16, 22, 0.85);
        color: {text_sec};
        padding: 6px 10px;
        border-bottom: 1px solid {border_subtle};
    }}

    /* =========================================================================
       TOOLBARS, STATUS BARS & MENUS
       ========================================================================= */
    QToolBar {{
        background-color: {bg};
        border-bottom: 1px solid {border_subtle};
        padding: 4px 8px;
        spacing: 6px;
    }}
    QToolBar QToolButton {{
        background-color: {surf};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 8px;
        padding: 6px 12px;
        font-weight: 500;
    }}
    QToolBar QToolButton:hover {{
        background-color: {surf_hov};
        border-color: {border_strong};
    }}
    QToolBar QToolButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}

    QStatusBar {{
        background-color: {bg};
        color: {text_muted};
        border-top: 1px solid {border_subtle};
    }}

    QMenuBar {{
        background-color: {bg};
        color: {text};
        border-bottom: 1px solid {border_subtle};
        padding: 4px 8px;
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
        background-color: rgba(22, 26, 34, 0.95);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 12px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 7px 24px 7px 12px;
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

    /* =========================================================================
       MODERN LIQUID GLASS BUTTONS
       ========================================================================= */
    QPushButton {{
        background-color: {surf_el};
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 500;
        min-height: 22px;
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
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: {palette.ACCENT_HOVER};
        border-color: rgba(255, 255, 255, 0.5);
    }}
    QPushButton:disabled {{
        background-color: rgba(255, 255, 255, 0.03);
        color: {palette.TEXT_DISABLED};
        border-color: {border_subtle};
    }}

    /* =========================================================================
       GLASS INPUT FIELDS
       ========================================================================= */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: rgba(12, 14, 18, 0.9);
        color: {text};
        border: 1px solid {border};
        border-radius: 9px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: rgba(18, 22, 30, 0.95);
    }}
    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QComboBox:disabled {{
        background-color: rgba(10, 10, 12, 0.4);
        color: {palette.TEXT_DISABLED};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: rgba(22, 26, 34, 0.98);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 8px;
        padding: 4px;
        selection-background-color: {acc};
        selection-color: #FFFFFF;
    }}

    /* =========================================================================
       GROUP BOXES & CONTAINERS
       ========================================================================= */
    QGroupBox {{
        background-color: rgba(16, 18, 24, 0.7);
        border: 1px solid {border};
        border-radius: 14px;
        margin-top: 24px;
        padding: 20px 16px 16px 16px;
        font-weight: 600;
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

    /* =========================================================================
       TABLES, LISTS & TREES (BROWSER / DECK LIST)
       ========================================================================= */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border};
        border-radius: 12px;
        gridline-color: {border_subtle};
        selection-background-color: {palette.ACCENT_SUBTLE};
        selection-color: {text};
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
        background-color: rgba(18, 21, 28, 0.95);
        color: {text_sec};
        border: none;
        border-bottom: 1px solid {border};
        border-right: 1px solid {border_subtle};
        padding: 8px 12px;
        font-weight: 600;
    }}

    /* =========================================================================
       FLOATING CAPSULE TABS
       ========================================================================= */
    QTabWidget::pane {{
        border: 1px solid {border};
        background-color: rgba(14, 16, 22, 0.75);
        border-radius: 12px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: rgba(22, 26, 34, 0.6);
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 8px 18px;
        margin-right: 4px;
    }}
    QTabBar::tab:selected {{
        background-color: rgba(14, 16, 22, 0.95);
        color: {acc};
        border: 1px solid {border};
        border-bottom: 1px solid transparent;
        font-weight: 600;
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {surf_hov};
        color: {text};
    }}

    /* =========================================================================
       THIN PILL SCROLLBARS
       ========================================================================= */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 8px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.18);
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
        background-color: rgba(255, 255, 255, 0.18);
        min-width: 28px;
        border-radius: 4px;
        margin: 2px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* =========================================================================
       CHECKBOXES & RADIO BUTTONS
       ========================================================================= */
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
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate comprehensive Full Black (#000000) and Frosted Glass CSS for ALL Anki WebViews:
    - Deck Browser & Home Page
    - Card Reviewer (Front & Back)
    - Bottom Action Toolbar
    - Statistics & Graphs
    - Overview Screen
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    surf = palette.BACKGROUND_SURFACE
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    border = palette.BORDER_DEFAULT
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY

    return f"""
    /* =========================================================================
       ROOT CSS CUSTOM PROPERTIES OVERRIDE FOR MODERN ANKI (2.1.50+ / 23.x / 24.x)
       ========================================================================= */
    :root, html, body, .night_mode, .nightMode, [data-bs-theme="dark"] {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: rgba(18, 21, 28, 0.8) !important;
        --surface-overlay: rgba(28, 33, 44, 0.9) !important;
        --fg: {text} !important;
        --fg-muted: {text_sec} !important;
        --card-bg: {bg} !important;
        --card-border: {border} !important;
        --border: {border} !important;
        --border-subtle: rgba(255, 255, 255, 0.08) !important;
        --window-bg: {bg} !important;
        --toolbar-bg: {bg} !important;
        --header-bg: {bg} !important;
        --footer-bg: {bg} !important;
        --link: {acc} !important;
        --accent: {acc} !important;
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
    }}

    /* Force Full Black Background Everywhere */
    html, body, #outer, #main, #main-content, #header, #footer, #qa, #content,
    .nightMode, body.nightMode, body:not(.nightMode), #deckbrowser, .deck-table,
    #overview, .overview, #stats, .stats {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
    }}

    /* =========================================================================
       DECK BROWSER & DECK LIST STYLES
       ========================================================================= */
    #deckbrowser, .deck-table, table.deck-table {{
        background-color: {bg} !important;
        border-collapse: separate !important;
        border-spacing: 0 4px !important;
        width: 100% !important;
    }}

    tr.deck {{
        background-color: rgba(16, 18, 24, 0.75) !important;
        border-radius: 10px !important;
        transition: background-color 0.15s ease !important;
    }}
    tr.deck:hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
    }}
    td.decktd {{
        padding: 10px 14px !important;
        border: none !important;
    }}
    a.deckname {{
        color: {text} !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        font-size: 14px !important;
    }}
    a.deckname:hover {{
        color: {acc} !important;
    }}

    /* Study Counts Badges */
    .new-count, .count-new, .new-count-badge {{
        color: {acc} !important;
        font-weight: 700 !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: {palette.WARNING} !important;
        font-weight: 700 !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: {palette.SUCCESS} !important;
        font-weight: 700 !important;
    }}

    /* =========================================================================
       CARD REVIEWER (FRONT & BACK)
       ========================================================================= */
    .card {{
        background: rgba(18, 21, 28, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 18px !important;
        padding: 28px !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8) !important;
        max-width: 860px !important;
        margin: 20px auto !important;
        text-align: left !important;
    }}

    /* Responsive Images Ingested from Discord */
    img {{
        max-width: 100% !important;
        height: auto !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7) !important;
        margin: 14px 0 !important;
        display: block !important;
    }}

    /* Cloze Deletion Highlights */
    .cloze {{
        color: #BF5AF2 !important;
        font-weight: 700 !important;
        background: rgba(191, 90, 242, 0.15) !important;
        padding: 2px 6px !important;
        border-radius: 5px !important;
        border: 1px solid rgba(191, 90, 242, 0.3) !important;
    }}

    /* Code Blocks */
    pre, code {{
        background-color: rgba(12, 14, 18, 0.9) !important;
        border: 1px solid {border} !important;
        color: #64D2FF !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        font-family: "SF Mono", "JetBrains Mono", Consolas, monospace !important;
    }}
    pre code {{
        padding: 14px !important;
        display: block !important;
    }}

    /* =========================================================================
       BOTTOM ACTION BAR & REVIEW BUTTONS
       ========================================================================= */
    #bottomWeb, #outer, #bottomBar, footer {{
        background-color: {bg} !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}

    button, .btn, .button, input[type="button"], input[type="submit"] {{
        background: rgba(28, 33, 44, 0.85) !important;
        color: {text} !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
    }}
    button:hover, .btn:hover {{
        background: rgba(255, 255, 255, 0.14) !important;
        border-color: rgba(255, 255, 255, 0.28) !important;
    }}
    """
