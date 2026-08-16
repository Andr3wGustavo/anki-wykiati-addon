"""
Discord Settings Dialog for Anki Wykiati Toolkit.
Configures Discord Bot Token, Image Channel Auto-Ingestion, User Permissions, and Local HTTP Bridge.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox,
            QComboBox,
            QFormLayout,
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
    QCheckBox = QComboBox = QFormLayout = QGroupBox = QHBoxLayout = QLabel = QLineEdit = QMessageBox = QPushButton = QSpinBox = QVBoxLayout = object


class DiscordSettingsDialog(BaseToolkitDialog):
    """
    Interface for setting up Discord Bot, Image Ingestion Channels, and Local Webhook Bridge.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Discord and Image Ingestion Settings",
            subtitle="Configure automatic image channels, target decks, front-only cards, and local HTTP bridge.",
            width=680,
            height=580,
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(520, 420)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)

        # 0. Didactic Step-by-Step Setup Guide
        guide_frame = QFrame(self)
        guide_frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 6px; padding: 12px;"
        )
        guide_layout = QVBoxLayout(guide_frame)
        guide_layout.setSpacing(6)

        lbl_guide_title = QLabel("💡 Guia Rápido de Configuração / Quick Setup Guide", guide_frame)
        lbl_guide_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF;")
        guide_layout.addWidget(lbl_guide_title)

        lbl_guide_body = QLabel(
            "• <b>1. Copiar ID do Canal no Discord:</b> No Discord, ative <i>Configurações do Usuário > Avançado > Modo Desenvolvedor</i>. "
            "Depois, clique com botão direito no canal onde você envia as imagens e clique em <b>Copiar ID do Canal</b>.<br>"
            "• <b>2. Deck de Destino:</b> Digite o nome do Deck do Anki (ex: <code>Medicina::Anatomia</code> ou <code>Imagens::Discord</code>). Se o deck não existir, ele será criado automaticamente.<br>"
            "• <b>3. Somente Imagem na Frente:</b> Para que a imagem apareça sozinha na frente do card sem verso, selecione <b>Image on Front Only (Empty Back)</b>.<br>"
            "• <b>4. Bot Poller vs HTTP Bridge:</b> Para polling em nuvem, insira o <i>Bot Token</i> do Discord Developer Portal. Para usar scripts locais, mantenha o <i>Local HTTP Bridge</i> ativo (porta 8765).",
            guide_frame,
        )
        lbl_guide_body.setWordWrap(True)
        lbl_guide_body.setStyleSheet(f"font-size: 11px; color: {PALETTE.TEXT_SECONDARY}; line-height: 1.45;")
        guide_layout.addWidget(lbl_guide_body)

        main_layout.addWidget(guide_frame)

        # 1. Image Channels & Auto-Ingestion (Top Priority Feature)
        group_images = QGroupBox("Dedicated Image Channels (Auto-Ingestion)", self)
        img_layout = QFormLayout(group_images)
        img_layout.setSpacing(10)

        self.txt_image_channels = QLineEdit(self)
        self.txt_image_channels.setPlaceholderText("Channel IDs (comma-separated, e.g. 119283746509182736)")
        img_layout.addRow("Image Channels (IDs):", self.txt_image_channels)

        self.txt_image_deck = QLineEdit(self)
        self.txt_image_deck.setPlaceholderText("Target Deck (e.g. Medicine::Anatomy or Images::Discord)")
        img_layout.addRow("Target Image Deck:", self.txt_image_deck)

        self.combo_img_layout = QComboBox(self)
        self.combo_img_layout.addItem("Image on Front Only (Empty Back / Visual Card)", "image_only_front")
        self.combo_img_layout.addItem("Image on Front / Caption on Back", "image_front")
        self.combo_img_layout.addItem("Question/Caption on Front / Image on Back", "image_back")
        img_layout.addRow("Card Layout Mode:", self.combo_img_layout)

        self.txt_image_tags = QLineEdit(self)
        self.txt_image_tags.setPlaceholderText("Automatic tags (comma-separated, e.g. discord, anatomy, visual)")
        img_layout.addRow("Auto Tags:", self.txt_image_tags)

        main_layout.addWidget(group_images)

        # 2. General Discord Bot Credentials
        group_bot = QGroupBox("Discord Bot Credentials (Background Poller)", self)
        bot_layout = QFormLayout(group_bot)
        bot_layout.setSpacing(10)

        self.chk_bot_enabled = QCheckBox("Enable Discord Bot Background Poller", self)
        self.chk_bot_enabled.setStyleSheet("font-weight: 600;")
        bot_layout.addRow("Bot Poller Status:", self.chk_bot_enabled)

        self.txt_token = QLineEdit(self)
        if hasattr(QLineEdit, "EchoMode"):
            self.txt_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_token.setPlaceholderText("Bot Secret Token from Discord Developer Portal")
        bot_layout.addRow("Bot Token:", self.txt_token)

        self.txt_channels = QLineEdit(self)
        self.txt_channels.setPlaceholderText("General text channels allowed for !anki commands (comma-separated)")
        bot_layout.addRow("Text Channels (IDs):", self.txt_channels)

        self.txt_users = QLineEdit(self)
        self.txt_users.setPlaceholderText("Authorized Discord User IDs (leave empty to allow all)")
        bot_layout.addRow("Authorized Users (IDs):", self.txt_users)

        self.spin_interval = QSpinBox(self)
        self.spin_interval.setRange(2, 60)
        self.spin_interval.setSuffix(" seconds")
        bot_layout.addRow("Polling Interval:", self.spin_interval)

        main_layout.addWidget(group_bot)

        # 3. Local HTTP Bridge
        group_http = QGroupBox("Local HTTP Webhook Bridge (127.0.0.1)", self)
        http_layout = QFormLayout(group_http)
        http_layout.setSpacing(10)

        self.chk_http_enabled = QCheckBox("Enable Local REST Webhook Server", self)
        http_layout.addRow("HTTP Server Status:", self.chk_http_enabled)

        self.spin_http_port = QSpinBox(self)
        self.spin_http_port.setRange(1024, 65535)
        http_layout.addRow("HTTP Port:", self.spin_http_port)

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

        self.chk_bot_enabled.setChecked(config.get("discord.enabled", False))
        self.txt_token.setText(config.get("discord.bot_token", ""))

        channels = config.get("discord.channel_ids", [])
        self.txt_channels.setText(", ".join(str(c) for c in channels))

        users = config.get("discord.authorized_users", [])
        self.txt_users.setText(", ".join(str(u) for u in users))

        self.spin_interval.setValue(config.get("discord.polling_interval_seconds", 5))
        self.chk_http_enabled.setChecked(config.get("discord.http_bridge_enabled", True))
        self.spin_http_port.setValue(config.get("discord.http_bridge_port", 8765))

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
