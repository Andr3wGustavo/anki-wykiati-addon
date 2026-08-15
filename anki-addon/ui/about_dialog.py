"""
About and Diagnostics Dialog for Anki Wykiati Toolkit.
Displays version metadata, license, active theme status, and diagnostic paths.
"""

import sys
from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.constants import ADDON_AUTHOR, ADDON_NAME, ADDON_VERSION
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.constants import ADDON_AUTHOR, ADDON_NAME, ADDON_VERSION
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt import mw
        from aqt.qt import QFrame, QLabel, QTextEdit, QVBoxLayout
    except ImportError:
        try:
            from PyQt6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout
        except ImportError:
            from PyQt5.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout
        mw = None
else:
    QFrame = QLabel = QTextEdit = QVBoxLayout = object
    mw = None


class AboutDialog(BaseToolkitDialog):
    """
    Informational dialog displaying add-on metadata, system diagnostics, and documentation links.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="About Anki Wykiati Toolkit",
            subtitle=f"{ADDON_NAME} v{ADDON_VERSION} - System Information",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Info Box
        info_frame = QFrame(self)
        info_frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 12px; padding: 14px;"
        )
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(6)

        title = QLabel(f"{ADDON_NAME} v{ADDON_VERSION}", info_frame)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        info_layout.addWidget(title)

        author = QLabel(f"Author: {ADDON_AUTHOR} | License: MIT", info_frame)
        author.setStyleSheet(f"color: {PALETTE.TEXT_MUTED}; font-size: 12px;")
        info_layout.addWidget(author)

        desc = QLabel(
            "Modular Anki toolkit providing automated Discord image and card ingestion, "
            "REST Webhooks, and a modern Full Black #000000 AMOLED & iOS Liquid Glass visual theme.",
            info_frame,
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {PALETTE.TEXT_SECONDARY}; margin-top: 6px;")
        info_layout.addWidget(desc)

        layout.addWidget(info_frame)

        # Diagnostic Details
        anki_ver = getattr(mw, "pm", None) and getattr(mw, "version", "Unknown") if mw else "Standalone Test Mode"
        diag_text = (
            f"--- System Diagnostics ---\n"
            f"Add-on Version: {ADDON_VERSION}\n"
            f"Python Version: {sys.version.split()[0]}\n"
            f"Anki Environment: {anki_ver}\n"
            f"Active Theme: Full Black (#000000 OLED) with iOS Liquid Glass\n"
            f"Theme Enabled: {config.get('theme.enabled', True)}\n"
            f"Accent Color: {config.get('theme.accent', '#0A84FF')}\n"
            f"HTTP Bridge: http://{config.get('discord.http_bridge_host', '127.0.0.1')}:{config.get('discord.http_bridge_port', 8765)}\n"
            f"Discord Poller Enabled: {config.get('discord.enabled', False)}\n"
            f"Image Channels Configured: {len(config.get('discord.image_channels', []))}\n"
            f"Total Cards Created: {config.get('stats.cards_created', 0)}\n"
            f"Total Images Ingested: {config.get('stats.images_ingested', 0)}\n"
        )

        txt_diag = QTextEdit(self)
        txt_diag.setPlainText(diag_text)
        txt_diag.setReadOnly(True)
        txt_diag.setStyleSheet("font-family: monospace; font-size: 11px;")
        layout.addWidget(txt_diag)

        # Custom buttons
        self.btn_save.setVisible(False)
        self.btn_cancel.setText("Close")

        self.body_layout.addLayout(layout)
