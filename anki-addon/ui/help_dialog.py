"""
Interactive Help and Didactic Setup Guide for Anki Wykiati Toolkit.
Provides step-by-step instructions for Discord bot configuration, image channel ingestion,
front-only card setup, RGB background customization, and REST Webhook integration.
"""

from typing import Any, Optional

try:
    from ..core.constants import ADDON_NAME, ADDON_VERSION
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.constants import ADDON_NAME, ADDON_VERSION
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QFrame,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QTextBrowser,
            QVBoxLayout,
            QWidget,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextBrowser,
                QVBoxLayout,
                QWidget,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextBrowser,
                QVBoxLayout,
                QWidget,
            )
else:
    QFrame = QHBoxLayout = QLabel = QPushButton = QTextBrowser = QVBoxLayout = QWidget = object


HELP_HTML_CONTENT = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #FFFFFF; line-height: 1.6; padding: 4px;">
    
    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px; margin-bottom: 18px;">
        <h2 style="color: #38BDF8; margin: 0 0 6px 0; font-size: 15px; font-weight: 700;">🚀 Quick Start Guide</h2>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0;">
            Welcome to <b>Anki Wykiati Toolkit</b>. This guide provides concise, step-by-step instructions for ingesting Discord images, configuring card layouts, customizing the RGB background, and using the local REST bridge.
        </p>
    </div>

    <!-- SECTION 1: DISCORD IMAGE AUTO-INGESTION -->
    <div style="border-left: 3px solid #38BDF8; padding-left: 12px; margin-bottom: 22px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">1. Automatic Image Ingestion (Discord Channel ➔ Anki Deck)</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Automatically download all images posted in dedicated Discord channels and convert them directly into Anki flashcards:
        </p>
        <ol style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px; line-height: 1.7;">
            <li><b>Enable Discord Developer Mode:</b> In Discord, go to <i>User Settings &gt; Advanced &gt; Developer Mode</i> and turn it on.</li>
            <li><b>Copy Channel ID:</b> Right-click your image channel in Discord and select <b>Copy Channel ID</b> (e.g. <code>119283746509182736</code>).</li>
            <li><b>Configure Add-on:</b> In Anki, open <i>Tools &gt; Anki Wykiati Toolkit &gt; Discord and Image Settings</i> and paste the ID into <b>Image Channels (IDs)</b>.</li>
            <li><b>Set Target Deck:</b> Enter your desired deck name (e.g. <code>Medicine::Anatomy</code>). The add-on creates the deck automatically if it does not exist.</li>
            <li><b>Front-Only Visual Cards:</b> Set <b>Card Layout Mode</b> to <code>Image on Front Only (Empty Back)</code> for visual identification flashcards.</li>
        </ol>
    </div>

    <!-- SECTION 2: DISCORD BOT SETUP -->
    <div style="border-left: 3px solid #4ADE80; padding-left: 12px; margin-bottom: 22px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">2. Discord Bot Poller Setup (Cloud Sync)</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            To allow Anki to monitor Discord channels in the background:
        </p>
        <ol style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px; line-height: 1.7;">
            <li>Open the <a href="https://discord.com/developers/applications" style="color: #38BDF8; text-decoration: none;">Discord Developer Portal</a> and create a <b>New Application</b>.</li>
            <li>In the left sidebar, click <b>Bot</b>, then click <b>Reset Token</b> to generate and copy your <b>Bot Token</b>.</li>
            <li>Scroll down on the Bot page and enable <b>Message Content Intent</b> (required to read message text and image attachments).</li>
            <li>Under <b>OAuth2 &gt; URL Generator</b>, select the <code>bot</code> scope with <code>Read Messages/View Channels</code>, <code>Send Messages</code>, and <code>Attach Files</code> permissions, and use the generated link to invite the bot to your server.</li>
            <li>Paste your token in <b>Bot Token</b> and check <b>Enable Discord Bot Background Poller</b>.</li>
        </ol>
    </div>

    <!-- SECTION 3: RGB THEME STUDIO -->
    <div style="border-left: 3px solid #FBBF24; padding-left: 12px; margin-bottom: 22px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">3. Theme Studio &amp; RGB Color Wheel</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Customize the global background color and accents with real-time preview:
        </p>
        <ul style="color: #D4D4D8; font-size: 12px; margin: 0; padding-left: 20px; line-height: 1.7;">
            <li><b>RGB Color Wheel:</b> Open <i>Theme &amp; Appearance Studio</i> and click or drag anywhere on the circular wheel to select any custom background hue.</li>
            <li><b>OLED &amp; Dark Presets:</b> Click any preset swatch: <i>Void Black (#000000)</i>, <i>Midnight (#0B0E14)</i>, <i>Forest (#08120C)</i>, <i>Obsidian (#121214)</i>, or <i>Cosmic (#0E0B14)</i>.</li>
            <li><b>Accent Colors:</b> Select accent colors for interactive highlights (Apple iOS Blue, Emerald Green, Violet, Amber, Crimson).</li>
            <li><b>Instant Shortcut:</b> Press <kbd style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 3px; padding: 1px 5px; font-family: monospace;">Ctrl+Shift+B</kbd> at any time to toggle the theme on/off.</li>
        </ul>
    </div>

    <!-- SECTION 4: TEXT COMMANDS PROTOCOL -->
    <div style="border-left: 3px solid #A78BFA; padding-left: 12px; margin-bottom: 22px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">4. Text Card Creation Protocol (!anki)</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Send structured flashcard messages in any authorized Discord channel using the <code>!anki</code> prefix:
        </p>
        <pre style="background: #060608; border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 10px; color: #E4E4E7; font-size: 11px; font-family: 'JetBrains Mono', Consolas, monospace;">
!anki
front: What is the primary function of mitochondria?
back: ATP generation via oxidative phosphorylation.
deck: Biology::Cellular
tags: biology, cellular, energy
        </pre>
        <p style="color: #71717A; font-size: 11px; margin: 6px 0 0 0;">
            Quick chat operational commands: <code>!anki-help</code>, <code>!anki-status</code>, <code>!anki-decks</code>, <code>!anki-ping</code>.
        </p>
    </div>

    <!-- SECTION 5: LOCAL HTTP REST WEBHOOK -->
    <div style="border-left: 3px solid #F472B6; padding-left: 12px; margin-bottom: 22px;">
        <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">5. Local HTTP REST API Webhook</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            The add-on embeds an asynchronous HTTP server on <code>http://127.0.0.1:8765/api/card</code> for direct integration with Python scripts, browser extensions, or command-line tools:
        </p>
        <pre style="background: #060608; border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 10px; color: #E4E4E7; font-size: 11px; font-family: 'JetBrains Mono', Consolas, monospace;">
curl -X POST http://127.0.0.1:8765/api/card \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/diagram.png", "deck": "Medicine::Anatomy"}'
        </pre>
    </div>

    <!-- SECTION 6: SUPPORT & COMMUNITY -->
    <div style="border-left: 3px solid #FFDD00; padding-left: 12px; margin-bottom: 10px;">
        <h3 style="color: #FFDD00; margin: 0 0 6px 0; font-size: 13px; font-weight: 600;">☕ 6. Support &amp; Contributions</h3>
        <p style="color: #A1A1AA; font-size: 12px; margin: 0 0 8px 0;">
            Enjoying Anki Wykiati Toolkit? Support continuous development, new AI image occlusion features, and official AnkiWeb releases:
        </p>
        <p style="margin: 0; font-size: 12px;">
            👉 <a href="https://buymeacoffee.com/wykiati" style="color: #FFDD00; font-weight: bold; text-decoration: none;">buymeacoffee.com/wykiati</a> &nbsp;|&nbsp; 
            ⭐ <a href="https://github.com/Andr3wGustavo/anki-wykiati-addon" style="color: #38BDF8; text-decoration: none;">GitHub Repository</a>
        </p>
    </div>

</div>
"""


class HelpDialog(BaseToolkitDialog):
    """
    Didactic documentation and step-by-step setup guide modal dialog.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Help & Setup Guide",
            subtitle=f"{ADDON_NAME} v{ADDON_VERSION} — Documentation and Setup Reference",
            width=620,
            height=500,
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(480, 360)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(10)

        browser = QTextBrowser(self)
        browser.setHtml(HELP_HTML_CONTENT)
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet(
            "QTextBrowser { background-color: #050507; border: 1px solid rgba(255,255,255,0.10); border-radius: 6px; padding: 12px; }"
            "QScrollBar:vertical { background: transparent; width: 6px; }"
            "QScrollBar::handle:vertical { background: rgba(255,255,255,0.20); border-radius: 3px; min-height: 20px; }"
        )
        layout.addWidget(browser)

        # Footer button customize
        self.btn_save.setVisible(False)
        self.btn_cancel.setText("Close")

        self.body_layout.addLayout(layout)
