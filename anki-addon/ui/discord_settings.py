"""
Discord Settings Dialog.
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
            title="Configurações do Discord & Imagens",
            subtitle="Conecte canais do Discord com ingestão automática de imagens e webhook HTTP.",
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(600, 520)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)

        # 1. Image Channels & Auto-Ingestion (Top Priority Feature)
        group_images = QGroupBox("📸 Canal Dedicado de Imagens (Auto-Ingestão)", self)
        img_layout = QFormLayout(group_images)
        img_layout.setSpacing(8)

        self.txt_image_channels = QLineEdit(self)
        self.txt_image_channels.setPlaceholderText("IDs dos canais que recebem apenas imagens (ex: 123456789012345678)")
        img_layout.addRow("Canais de Imagens (IDs):", self.txt_image_channels)

        self.txt_image_deck = QLineEdit(self)
        self.txt_image_deck.setPlaceholderText("Baralho de destino para as imagens (ex: Images::Discord)")
        img_layout.addRow("Deck para Imagens:", self.txt_image_deck)

        self.combo_img_layout = QComboBox(self)
        self.combo_img_layout.addItem("Imagem na Frente / Legenda no Verso", "image_front")
        self.combo_img_layout.addItem("Pergunta na Frente / Imagem no Verso", "image_back")
        img_layout.addRow("Layout do Cartão:", self.combo_img_layout)

        self.txt_image_tags = QLineEdit(self)
        self.txt_image_tags.setPlaceholderText("Tags automáticas (ex: discord, image, wykiati)")
        img_layout.addRow("Tags Automáticas:", self.txt_image_tags)

        main_layout.addWidget(group_images)

        # 2. General Discord Bot Credentials
        group_bot = QGroupBox("🤖 Credenciais do Discord Bot", self)
        bot_layout = QFormLayout(group_bot)
        bot_layout.setSpacing(8)

        self.chk_bot_enabled = QCheckBox("Habilitar Leitor Automático do Discord Bot", self)
        self.chk_bot_enabled.setStyleSheet("font-weight: 600;")
        bot_layout.addRow("Status do Bot:", self.chk_bot_enabled)

        self.txt_token = QLineEdit(self)
        if hasattr(QLineEdit, "EchoMode"):
            self.txt_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_token.setPlaceholderText("Token do Bot (Discord Developer Portal)")
        bot_layout.addRow("Bot Token:", self.txt_token)

        self.txt_channels = QLineEdit(self)
        self.txt_channels.setPlaceholderText("Canais gerais autorizados para !anki (separados por vírgula)")
        bot_layout.addRow("Canais Gerais de Texto (IDs):", self.txt_channels)

        self.txt_users = QLineEdit(self)
        self.txt_users.setPlaceholderText("IDs de usuários autorizados (vazio = todos permitidos)")
        bot_layout.addRow("Usuários Autorizados (IDs):", self.txt_users)

        self.spin_interval = QSpinBox(self)
        self.spin_interval.setRange(2, 60)
        self.spin_interval.setSuffix(" segundos")
        bot_layout.addRow("Intervalo de Consulta:", self.spin_interval)

        main_layout.addWidget(group_bot)

        # 3. Local HTTP Bridge
        group_http = QGroupBox("🌐 Servidor Webhook Local HTTP (127.0.0.1)", self)
        http_layout = QFormLayout(group_http)
        http_layout.setSpacing(8)

        self.chk_http_enabled = QCheckBox("Habilitar Servidor Webhook HTTP", self)
        http_layout.addRow("Servidor Local:", self.chk_http_enabled)

        self.spin_http_port = QSpinBox(self)
        self.spin_http_port.setRange(1024, 65535)
        http_layout.addRow("Porta HTTP:", self.spin_http_port)

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

            logger.info("[DiscordSettingsDialog] Discord image & bot settings updated successfully.")
            super().accept()
        except Exception as e:
            logger.error(f"[DiscordSettingsDialog] Error saving Discord settings: {e}")
