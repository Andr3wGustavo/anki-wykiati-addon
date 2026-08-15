"""
Ultra-Minimalist Void Black (#000000) & Floating Glass Stylesheet Generators.
Linear/Vercel-inspired desktop aesthetics for Qt widgets and Anki WebViews.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate ultra-minimalist Qt StyleSheet (QSS).
    Features floating transparent pill buttons, void black surfaces, and crisp Inter typography.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    surf = palette.BACKGROUND_SURFACE   # rgba(255, 255, 255, 0.03)
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
       ULTRA-MINIMALIST VOID BLACK (#000000) BASE & TYPOGRAPHY
       ========================================================================= */
    * {{
        font-family: "Inter", "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        outline: none;
        letter-spacing: -0.01em;
    }}

    QWidget, QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea {{
        background-color: {bg};
        color: {text};
        selection-background-color: {acc};
        selection-color: #FFFFFF;
    }}

    /* Main Window Separator */
    QMainWindow::separator {{
        background-color: {border_subtle};
        width: 1px;
        height: 1px;
    }}

    /* Dock Widgets */
    QDockWidget {{
        background-color: {bg};
        color: {text};
        titlebar-close-icon: none;
        titlebar-normal-icon: none;
    }}
    QDockWidget::title {{
        background-color: {bg};
        color: {text_sec};
        padding: 8px 12px;
        border-bottom: 1px solid {border_subtle};
        font-weight: 500;
    }}

    /* =========================================================================
       TOOLBARS, STATUS BARS & MENUS
       ========================================================================= */
    QToolBar {{
        background-color: {bg};
        border-bottom: 1px solid {border_subtle};
        padding: 6px 10px;
        spacing: 8px;
    }}
    QToolBar QToolButton {{
        background-color: {surf};
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 16px;
        padding: 6px 14px;
        font-weight: 500;
    }}
    QToolBar QToolButton:hover {{
        background-color: {surf_hov};
        color: {text};
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
        color: {text_sec};
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
        background-color: rgba(14, 14, 16, 0.98);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 10px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 7px 22px 7px 12px;
        border-radius: 6px;
        color: {text_sec};
    }}
    QMenu::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
    }}
    QMenu::separator {{
        height: 1px;
        background-color: {border_subtle};
        margin: 4px 6px;
    }}

    /* =========================================================================
       FLOATING TRANSPARENT PILL BUTTONS
       ========================================================================= */
    QPushButton {{
        background-color: {surf};
        color: {text};
        border: 1px solid {border};
        border-radius: 18px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: 500;
        min-height: 20px;
    }}
    QPushButton:hover {{
        background-color: {surf_hov};
        border-color: {border_strong};
    }}
    QPushButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: #E4E4E7;
        border-color: #E4E4E7;
    }}
    QPushButton:disabled {{
        background-color: transparent;
        color: {palette.TEXT_DISABLED};
        border-color: {border_subtle};
    }}

    /* =========================================================================
       MINIMALIST INPUT FIELDS
       ========================================================================= */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: rgba(255, 255, 255, 0.02);
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: rgba(255, 255, 255, 0.04);
    }}
    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QComboBox:disabled {{
        background-color: transparent;
        color: {palette.TEXT_DISABLED};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: rgba(14, 14, 16, 0.98);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 8px;
        padding: 4px;
        selection-background-color: rgba(255, 255, 255, 0.08);
        selection-color: #FFFFFF;
    }}

    /* =========================================================================
       GROUP BOXES & CONTAINERS
       ========================================================================= */
    QGroupBox {{
        background-color: {surf};
        border: 1px solid {border_subtle};
        border-radius: 14px;
        margin-top: 24px;
        padding: 20px 16px 16px 16px;
        font-weight: 500;
        color: {text};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 14px;
        top: 6px;
        padding: 0 6px;
        background-color: transparent;
        color: {text_sec};
        font-weight: 600;
    }}

    /* =========================================================================
       TABLES, LISTS & TREES
       ========================================================================= */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 12px;
        gridline-color: {border_subtle};
        selection-background-color: rgba(255, 255, 255, 0.06);
        selection-color: {text};
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover {{
        background-color: {surf_hov};
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        font-weight: 500;
    }}
    QHeaderView::section {{
        background-color: {bg};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_subtle};
        border-right: 1px solid {border_subtle};
        padding: 8px 12px;
        font-weight: 500;
        font-size: 11px;
        text-transform: uppercase;
    }}

    /* =========================================================================
       FLOATING CAPSULE TABS
       ========================================================================= */
    QTabWidget::pane {{
        border: 1px solid {border_subtle};
        background-color: {bg};
        border-radius: 12px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {text_muted};
        border: none;
        border-radius: 16px;
        padding: 6px 16px;
        margin: 4px;
    }}
    QTabBar::tab:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
        font-weight: 600;
    }}
    QTabBar::tab:hover:!selected {{
        background-color: rgba(255, 255, 255, 0.04);
        color: {text_sec};
    }}

    /* =========================================================================
       THIN PILL SCROLLBARS
       ========================================================================= */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.12);
        min-height: 24px;
        border-radius: 3px;
        margin: 1px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.25);
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.12);
        min-width: 24px;
        border-radius: 3px;
        margin: 1px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* =========================================================================
       CHECKBOXES
       ========================================================================= */
    QCheckBox, QRadioButton {{
        color: {text_sec};
        spacing: 8px;
    }}
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {border_strong};
        background-color: transparent;
        border-radius: 4px;
    }}
    QRadioButton::indicator {{
        border-radius: 8px;
    }}
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: #FFFFFF;
        border-color: #FFFFFF;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate ultra-minimalist Void Black (#000000) & Glass CSS for ALL Anki WebViews.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       ROOT CSS CUSTOM PROPERTIES OVERRIDE
       ========================================================================= */
    :root, html, body, .night_mode, .nightMode, [data-bs-theme="dark"] {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: rgba(255, 255, 255, 0.02) !important;
        --surface-overlay: rgba(14, 14, 16, 0.95) !important;
        --fg: {text} !important;
        --fg-muted: {text_sec} !important;
        --card-bg: {bg} !important;
        --card-border: {border_subtle} !important;
        --border: {border_subtle} !important;
        --border-subtle: {border_subtle} !important;
        --window-bg: {bg} !important;
        --toolbar-bg: {bg} !important;
        --header-bg: {bg} !important;
        --footer-bg: {bg} !important;
        --link: {acc} !important;
        --accent: {acc} !important;
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: "Inter", "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        letter-spacing: -0.01em !important;
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
        border-spacing: 0 2px !important;
        width: 100% !important;
    }}

    tr.deck {{
        background-color: transparent !important;
        border-radius: 8px !important;
        transition: background-color 0.1s ease !important;
    }}
    tr.deck:hover {{
        background-color: rgba(255, 255, 255, 0.04) !important;
    }}
    td.decktd {{
        padding: 9px 12px !important;
        border: none !important;
    }}
    a.deckname {{
        color: {text_sec} !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        font-size: 13px !important;
    }}
    a.deckname:hover {{
        color: #FFFFFF !important;
    }}

    /* Minimalist Counters */
    .new-count, .count-new, .new-count-badge {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: #FBBF24 !important;
        font-weight: 600 !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: #4ADE80 !important;
        font-weight: 600 !important;
    }}

    /* =========================================================================
       CARD REVIEWER (FRONT & BACK)
       ========================================================================= */
    .card {{
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 32px !important;
        max-width: 820px !important;
        margin: 24px auto !important;
        text-align: left !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9) !important;
    }}

    /* Clean Ingested Images */
    img {{
        max-width: 100% !important;
        height: auto !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin: 16px 0 !important;
        display: block !important;
    }}

    /* Minimal Cloze Deletion */
    .cloze {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        background: rgba(56, 189, 248, 0.10) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid rgba(56, 189, 248, 0.20) !important;
    }}

    /* Code Blocks */
    pre, code {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {border_subtle} !important;
        color: #E4E4E7 !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        font-family: "JetBrains Mono", Consolas, monospace !important;
        font-size: 12px !important;
    }}
    pre code {{
        padding: 12px !important;
        display: block !important;
    }}

    /* =========================================================================
       BOTTOM ACTION BAR & FLOATING BUTTONS
       ========================================================================= */
    #bottomWeb, #outer, #bottomBar, footer {{
        background-color: {bg} !important;
        border-top: 1px solid {border_subtle} !important;
    }}

    button, .btn, .button, input[type="button"], input[type="submit"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: {text} !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 20px !important;
        padding: 8px 22px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        cursor: pointer !important;
        transition: all 0.12s ease !important;
    }}
    button:hover, .btn:hover {{
        background: rgba(255, 255, 255, 0.10) !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
    }}
    """
