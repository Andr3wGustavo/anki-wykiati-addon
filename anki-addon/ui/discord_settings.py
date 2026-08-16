"""
Discord Settings Dialog for Anki Wykiati Toolkit.
Configures Discord Bot Token, Image Channel Auto-Ingestion, User Permissions, and Local HTTP Bridge.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..discord.client import pull_recent_discord_images
    from ..theme.palette import PALETTE, is_light_color
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from discord.client import pull_recent_discord_images
    from theme.palette import PALETTE, is_light_color
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox,
            QComboBox,
            QFormLayout,
            QFrame,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QMessageBox,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QCheckBox,
                QComboBox,
                QFormLayout,
                QFrame,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QMessageBox,
                QPushButton,
                QSpinBox,
                QVBoxLayout,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QCheckBox,
                QComboBox,
                QFormLayout,
                QFrame,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QMessageBox,
                QPushButton,
                QSpinBox,
                QVBoxLayout,
            )
else:
    QCheckBox = QComboBox = QFormLayout = QFrame = QGroupBox = QHBoxLayout = QLabel = QLineEdit = QMessageBox = QPushButton = QSpinBox = QVBoxLayout = object


class DiscordSettingsDialog(BaseToolkitDialog):
    """
    Interface for setting up Discord Bot, Image Ingestion Channels, and Local Webhook Bridge.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Discord and Image Ingestion Settings",
            subtitle="Configure automatic image channels, target decks, front-only cards, and local HTTP bridge.",
            width=580,
            height=480,
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(460, 340)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)

        # 0. Modern Minimalist Setup Guide (English)
        guide_frame = QFrame(self)
        guide_frame.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.03); "
            "border: 1px solid rgba(56, 189, 248, 0.25); "
            "border-radius: 8px; padding: 14px;"
        )
        guide_layout = QVBoxLayout(guide_frame)
        guide_layout.setSpacing(8)

        lbl_guide_title = QLabel("⚡ Quick Setup Guide", guide_frame)
        lbl_guide_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #38BDF8; letter-spacing: -0.01em;")
        guide_layout.addWidget(lbl_guide_title)

        lbl_guide_body = QLabel(
            "• <b>1. Channel ID:</b> In Discord, enable <i>User Settings &gt; Advanced &gt; Developer Mode</i>. "
            "Right-click your image channel and select <b>Copy Channel ID</b>.<br>"
            "• <b>2. Target Deck:</b> Enter your desired Anki deck (e.g. <code>Medicine::Anatomy</code>). It will be auto-created if it doesn't exist.<br>"
            "• <b>3. Visual Cards:</b> Select <b>Image on Front Only (Empty Back)</b> to display images on the front with no back text required.<br>"
            "• <b>4. Integration:</b> Use <b>Bot Poller</b> for automatic cloud polling or <b>Local HTTP Bridge</b> (port 8765) for local script automation.",
            guide_frame,
        )
        lbl_guide_body.setWordWrap(True)
        lbl_guide_body.setStyleSheet("font-size: 11px; color: #D4D4D8; line-height: 1.5;")
        guide_layout.addWidget(lbl_guide_body)

        main_layout.addWidget(guide_frame)

        # 1. Dedicated Image Ingestion Channels
        group_images = QGroupBox("Image Channels & Ingestion Rules", self)
        img_layout = QFormLayout(group_images)
        img_layout.setSpacing(12)

        self.txt_image_channels = QLineEdit(self)
        self.txt_image_channels.setPlaceholderText("e.g. 119283746509182736, 987654321098765432")
        img_layout.addRow("Image Channels (IDs):", self.txt_image_channels)

        self.txt_image_deck = QLineEdit(self)
        self.txt_image_deck.setPlaceholderText("e.g. Medicine::Anatomy or Images::Discord")
        img_layout.addRow("Target Deck:", self.txt_image_deck)

        self.combo_img_layout = QComboBox(self)
        self.combo_img_layout.addItem("Image on Front Only (Empty Back / Visual Card)", "image_only_front")
        self.combo_img_layout.addItem("Image on Front / Caption on Back", "image_front")
        self.combo_img_layout.addItem("Question on Front / Image on Back", "image_back")
        img_layout.addRow("Card Layout Mode:", self.combo_img_layout)

        self.txt_image_tags = QLineEdit(self)
        self.txt_image_tags.setPlaceholderText("e.g. discord, anatomy, visual")
        img_layout.addRow("Automatic Tags:", self.txt_image_tags)

        # Image Compression & WebP Optimizer Row
        self.chk_optimize_images = QCheckBox("⚡ Auto-Optimize & Convert to WebP (Saves up to 85% Disk Space)", self)
        self.chk_optimize_images.setStyleSheet("font-weight: 600;")
        img_layout.addRow("Image Optimizer:", self.chk_optimize_images)

        self.lbl_savings_stats = QLabel("", self)
        self.lbl_savings_stats.setStyleSheet("font-size: 11px; color: #4ADE80; font-weight: 500;")
        img_layout.addRow("Storage Saved:", self.lbl_savings_stats)

        # On-Demand Sync Row
        sync_row = QHBoxLayout()
        sync_row.setSpacing(8)
        self.btn_pull_images = QPushButton("📥 Pull Recent Discord Images Now", self)
        self.btn_pull_images.setStyleSheet("font-weight: 600; padding: 7px 14px;")
        self.btn_pull_images.clicked.connect(self._pull_images_now)
        sync_row.addWidget(self.btn_pull_images)
        sync_row.addStretch()
        img_layout.addRow("On-Demand Sync:", sync_row)

        # Feedback Banner
        self.lbl_sync_feedback = QLabel("", self)
        self.lbl_sync_feedback.setWordWrap(True)
        self.lbl_sync_feedback.setVisible(False)
        img_layout.addRow("", self.lbl_sync_feedback)

        main_layout.addWidget(group_images)

        # 2. General Discord Bot Poller
        group_bot = QGroupBox("Discord Bot Credentials (Cloud Poller)", self)
        bot_layout = QFormLayout(group_bot)
        bot_layout.setSpacing(12)

        self.chk_bot_enabled = QCheckBox("Enable Discord Bot Background Poller", self)
        self.chk_bot_enabled.setStyleSheet("font-weight: 600;")
        bot_layout.addRow("Poller Status:", self.chk_bot_enabled)

        self.txt_token = QLineEdit(self)
        if hasattr(QLineEdit, "EchoMode") and hasattr(QLineEdit.EchoMode, "Password"):
            self.txt_token.setEchoMode(QLineEdit.EchoMode.Password)
        elif hasattr(QLineEdit, "Password"):
            self.txt_token.setEchoMode(QLineEdit.Password)
        self.txt_token.setPlaceholderText("Bot Secret Token from Discord Developer Portal")
        bot_layout.addRow("Bot Token:", self.txt_token)

        self.txt_channels = QLineEdit(self)
        self.txt_channels.setPlaceholderText("Text channels allowed for !anki commands (comma-separated)")
        bot_layout.addRow("Allowed Channels:", self.txt_channels)

        self.txt_users = QLineEdit(self)
        self.txt_users.setPlaceholderText("Authorized Discord User IDs (leave empty to allow all)")
        bot_layout.addRow("Authorized Users:", self.txt_users)

        self.spin_interval = QSpinBox(self)
        self.spin_interval.setRange(2, 60)
        self.spin_interval.setSuffix(" seconds")
        bot_layout.addRow("Polling Interval:", self.spin_interval)

        main_layout.addWidget(group_bot)

        # 3. Local HTTP Bridge
        group_http = QGroupBox("Local HTTP REST Bridge Server", self)
        http_layout = QFormLayout(group_http)
        http_layout.setSpacing(12)

        self.chk_http_enabled = QCheckBox("Enable Local HTTP Webhook Server (127.0.0.1)", self)
        http_layout.addRow("Bridge Status:", self.chk_http_enabled)

        self.spin_http_port = QSpinBox(self)
        self.spin_http_port.setRange(1024, 65535)
        http_layout.addRow("Bridge Port:", self.spin_http_port)

        main_layout.addWidget(group_http)

        self.body_layout.addLayout(main_layout)

    def _load_values(self) -> None:
        img_channels = config.get("discord.image_channels", [])
        self.txt_image_channels.setText(", ".join(str(c) for c in img_channels))
        self.txt_image_deck.setText(config.get("discord.image_default_deck", "Images::Discord"))
        self.txt_image_tags.setText(", ".join(config.get("discord.image_default_tags", ["discord", "image"])))

        layout = config.get("discord.image_card_layout", "image_front")
        for i in range(self.combo_img_layout.count()):
            if self.combo_img_layout.itemData(i) == layout:
                self.combo_img_layout.setCurrentIndex(i)
                break

        self.chk_optimize_images.setChecked(config.get("discord.optimize_images", True))
        
        saved_bytes = config.get("stats.bytes_saved", 0)
        ingested_count = config.get("stats.images_ingested", 0)
        if saved_bytes > 1024 * 1024:
            savings_str = f"⚡ {saved_bytes / (1024*1024):.2f} MB saved ({ingested_count} images compressed)"
        elif saved_bytes > 0:
            savings_str = f"⚡ {saved_bytes / 1024:.1f} KB saved ({ingested_count} images compressed)"
        else:
            savings_str = "⚡ 0 KB saved (Ready to compress incoming images)"
        self.lbl_savings_stats.setText(savings_str)

        self.chk_bot_enabled.setChecked(config.get("discord.enabled", False))
        self.txt_token.setText(config.get("discord.bot_token", ""))

        channels = config.get("discord.channel_ids", [])
        self.txt_channels.setText(", ".join(str(c) for c in channels))

        users = config.get("discord.authorized_users", [])
        self.txt_users.setText(", ".join(str(u) for u in users))

        self.spin_interval.setValue(config.get("discord.polling_interval_seconds", 5))
        self.chk_http_enabled.setChecked(config.get("discord.http_bridge_enabled", True))
        self.spin_http_port.setValue(config.get("discord.http_bridge_port", 8765))

    def _pull_images_now(self) -> None:
        """Trigger instant on-demand image pull from Discord channel."""
        token = self.txt_token.text().strip()
        raw_channels = self.txt_image_channels.text().strip()
        ch_ids = [c.strip() for c in raw_channels.split(",") if c.strip()]
        ch_id = ch_ids[0] if ch_ids else ""
        deck = self.txt_image_deck.text().strip() or "Images::Discord"
        layout_mode = self.combo_img_layout.currentData() or "image_only_front"

        if not token:
            self.lbl_sync_feedback.setText("❌ Please enter your Discord Bot Token before synchronizing.")
            self.lbl_sync_feedback.setStyleSheet("color: #F87171; font-size: 11px; font-weight: 600;")
            self.lbl_sync_feedback.setVisible(True)
            return

        if not ch_id:
            self.lbl_sync_feedback.setText("❌ Please enter a Channel ID in 'Image Channels (IDs)' above.")
            self.lbl_sync_feedback.setStyleSheet("color: #F87171; font-size: 11px; font-weight: 600;")
            self.lbl_sync_feedback.setVisible(True)
            return

        self.lbl_sync_feedback.setText(f"⏳ Connecting to Discord channel {ch_id} and downloading recent images...")
        self.lbl_sync_feedback.setStyleSheet("color: #38BDF8; font-size: 11px;")
        self.lbl_sync_feedback.setVisible(True)
        if hasattr(self.lbl_sync_feedback, "repaint"):
            self.lbl_sync_feedback.repaint()

        # Temporarily apply layout mode in config
        config.set("discord.image_card_layout", layout_mode, save=False)

        res = pull_recent_discord_images(
            channel_id=ch_id,
            target_deck=deck,
            limit=50,
            bot_token=token,
        )

        if res.get("success"):
            ingested = res.get("ingested", 0)
            skipped = res.get("skipped", 0)
            msg = f"✓ Synchronized successfully! Ingested {ingested} image card(s) into deck '{deck}' ({skipped} skipped duplicates)."
            self.lbl_sync_feedback.setText(msg)
            self.lbl_sync_feedback.setStyleSheet("color: #4ADE80; font-size: 11px; font-weight: 600;")
        else:
            err = res.get("error", "Unknown synchronization error")
            self.lbl_sync_feedback.setText(f"❌ Synchronization failed: {err}")
            self.lbl_sync_feedback.setStyleSheet("color: #F87171; font-size: 11px; font-weight: 600;")

    def accept(self) -> None:
        try:
            # Parse image channels
            raw_img_channels = self.txt_image_channels.text().strip()
            image_channels = [c.strip() for c in raw_img_channels.split(",") if c.strip()]

            # Parse image tags
            raw_tags = self.txt_image_tags.text().strip()
            image_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

            # Parse standard channels
            raw_channels = self.txt_channels.text().strip()
            channel_ids = [c.strip() for c in raw_channels.split(",") if c.strip()]

            # Parse users
            raw_users = self.txt_users.text().strip()
            user_ids = [u.strip() for u in raw_users.split(",") if u.strip()]

            config.set("discord.image_channels", image_channels, save=False)
            config.set("discord.image_default_deck", self.txt_image_deck.text().strip() or "Images::Discord", save=False)
            config.set("discord.image_default_tags", image_tags, save=False)
            config.set("discord.image_card_layout", self.combo_img_layout.currentData(), save=False)
            config.set("discord.optimize_images", self.chk_optimize_images.isChecked(), save=False)

            config.set("discord.enabled", self.chk_bot_enabled.isChecked(), save=False)
            config.set("discord.bot_token", self.txt_token.text().strip(), save=False)
            config.set("discord.channel_ids", channel_ids, save=False)
            config.set("discord.authorized_users", user_ids, save=False)
            config.set("discord.polling_interval_seconds", self.spin_interval.value(), save=False)
            config.set("discord.http_bridge_enabled", self.chk_http_enabled.isChecked(), save=False)
            config.set("discord.http_bridge_port", self.spin_http_port.value(), save=True)

            logger.info("[DiscordSettingsDialog] Discord image and bot settings saved successfully.")
            super().accept()
        except Exception as e:
            logger.error(f"[DiscordSettingsDialog] Error saving Discord settings: {e}")

