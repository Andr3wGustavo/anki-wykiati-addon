"""
Discord Settings Dialog.
Configures Discord Bot Token, Channel Whitelist, User Permissions, and Local HTTP Bridge.
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
    QCheckBox = QFormLayout = QGroupBox = QHBoxLayout = QLabel = QLineEdit = QMessageBox = QPushButton = QSpinBox = QVBoxLayout = object


class DiscordSettingsDialog(BaseToolkitDialog):
    """
    Interface for setting up Discord Bot and Local Webhook Bridge.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Configurações do Discord",
            subtitle="Conecte seu Anki diretamente ao Discord através de Bot ou Webhook Local HTTP.",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)

        # 1. Integration Mode & Bridges
        group_mode = QGroupBox("Canais de Entrada", self)
        mode_layout = QVBoxLayout(group_mode)
        mode_layout.setSpacing(8)

        self.chk_http_enabled = QCheckBox("Habilitar Servidor Webhook Local HTTP (Recomendado)", self)
        self.chk_http_enabled.setStyleSheet("font-weight: 600;")
        mode_layout.addWidget(self.chk_http_enabled)

        http_info = QLabel("Permite receber cartões via requisições HTTP POST em http://127.0.0.1:8765/api/card", self)
        http_info.setStyleSheet(f"color: {PALETTE.TEXT_MUTED}; font-size: 11px; margin-left: 20px;")
        mode_layout.addWidget(http_info)

        self.chk_bot_enabled = QCheckBox("Habilitar Leitor Automático de Mensagens do Discord Bot", self)
        self.chk_bot_enabled.setStyleSheet("font-weight: 600; margin-top: 6px;")
        mode_layout.addWidget(self.chk_bot_enabled)

        main_layout.addWidget(group_mode)

        # 2. Discord Bot Credentials & Channels
        group_bot = QGroupBox("Credenciais do Discord Bot", self)
        bot_layout = QFormLayout(group_bot)
        bot_layout.setSpacing(8)

        self.txt_token = QLineEdit(self)
        if hasattr(QLineEdit, "EchoMode"):
            self.txt_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_token.setPlaceholderText("Cole o Token do Bot criado no Discord Developer Portal")
        bot_layout.addRow("Bot Token:", self.txt_token)

        self.txt_channels = QLineEdit(self)
        self.txt_channels.setPlaceholderText("Ex: 123456789012345678, 987654321098765432")
        bot_layout.addRow("Canais Autorizados (IDs):", self.txt_channels)

        self.txt_users = QLineEdit(self)
        self.txt_users.setPlaceholderText("Ex: 112233445566778899 (deixe vazio para autorizar todos)")
        bot_layout.addRow("Usuários Autorizados (IDs):", self.txt_users)

        self.spin_interval = QSpinBox(self)
        self.spin_interval.setRange(2, 60)
        self.spin_interval.setSuffix(" segundos")
        bot_layout.addRow("Intervalo de Verificação:", self.spin_interval)

        main_layout.addWidget(group_bot)

        # 3. HTTP Server Config
        group_http = QGroupBox("Configurações do Servidor Local", self)
        http_layout = QFormLayout(group_http)
        http_layout.setSpacing(8)

        self.txt_http_host = QLineEdit(self)
        http_layout.addRow("Endereço Local (Host):", self.txt_http_host)

        self.spin_http_port = QSpinBox(self)
        self.spin_http_port.setRange(1024, 65535)
        http_layout.addRow("Porta HTTP:", self.spin_http_port)

        self.spin_rate_limit = QSpinBox(self)
        self.spin_rate_limit.setRange(5, 300)
        self.spin_rate_limit.setSuffix(" cartões / min")
        http_layout.addRow("Limite de Envio (Rate Limit):", self.spin_rate_limit)

        main_layout.addWidget(group_http)

        self.body_layout.addLayout(main_layout)

    def _load_values(self) -> None:
        self.chk_http_enabled.setChecked(config.get("discord.http_bridge_enabled", True))
        self.chk_bot_enabled.setChecked(config.get("discord.enabled", False))

        self.txt_token.setText(config.get("discord.bot_token", ""))

        channels = config.get("discord.channel_ids", [])
        self.txt_channels.setText(", ".join(str(c) for c in channels))

        users = config.get("discord.authorized_users", [])
        self.txt_users.setText(", ".join(str(u) for u in users))

        self.spin_interval.setValue(config.get("discord.polling_interval_seconds", 5))
        self.txt_http_host.setText(config.get("discord.http_bridge_host", "127.0.0.1"))
        self.spin_http_port.setValue(config.get("discord.http_bridge_port", 8765))
        self.spin_rate_limit.setValue(config.get("discord.rate_limit_per_minute", 60))

    def accept(self) -> None:
        try:
            raw_channels = self.txt_channels.text().strip()
            channel_ids = [c.strip() for c in raw_channels.split(",") if c.strip()]

            raw_users = self.txt_users.text().strip()
            user_ids = [u.strip() for u in raw_users.split(",") if u.strip()]

            config.set("discord.http_bridge_enabled", self.chk_http_enabled.isChecked(), save=False)
            config.set("discord.enabled", self.chk_bot_enabled.isChecked(), save=False)
            config.set("discord.bot_token", self.txt_token.text().strip(), save=False)
            config.set("discord.channel_ids", channel_ids, save=False)
            config.set("discord.authorized_users", user_ids, save=False)
            config.set("discord.polling_interval_seconds", self.spin_interval.value(), save=False)
            config.set("discord.http_bridge_host", self.txt_http_host.text().strip(), save=False)
            config.set("discord.http_bridge_port", self.spin_http_port.value(), save=False)
            config.set("discord.rate_limit_per_minute", self.spin_rate_limit.value(), save=True)

            logger.info("[DiscordSettingsDialog] Discord configuration updated successfully.")
            super().accept()
        except Exception as e:
            logger.error(f"[DiscordSettingsDialog] Error saving Discord settings: {e}")
