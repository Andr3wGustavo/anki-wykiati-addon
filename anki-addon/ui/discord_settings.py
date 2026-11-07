"""
Discord → Anki settings panel.

Minimal flow for the common case (an automation posting images to one channel):
token + channel → Test connection → deck & card format → Save. Network actions run
in the background so Anki never freezes. Less common options live under "Advanced".
"""

import time
from typing import Any, Callable, Dict, List, Optional

try:
    from ..anki.operations import run_in_background
    from ..core.config import config
    from ..core.logger import logger
    from ..discord.client import discord_client_manager, test_discord_connection
    from ..theme.palette import PALETTE, is_light_color, normalize_hex, semantic_colors
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from anki.operations import run_in_background
    from core.config import config
    from core.logger import logger
    from discord.client import discord_client_manager, test_discord_connection
    from theme.palette import PALETTE, is_light_color, normalize_hex, semantic_colors
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
            QPushButton, QSpinBox, QTimer, QVBoxLayout, QWidget,
        )
    except ImportError:
        try:
            from PyQt6.QtCore import QTimer
            from PyQt6.QtWidgets import (
                QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                QPushButton, QSpinBox, QVBoxLayout, QWidget,
            )
        except ImportError:
            from PyQt5.QtCore import QTimer
            from PyQt5.QtWidgets import (
                QCheckBox, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                QPushButton, QSpinBox, QVBoxLayout, QWidget,
            )
else:
    QCheckBox = QComboBox = QFormLayout = QHBoxLayout = QLabel = QLineEdit = object
    QPushButton = QSpinBox = QTimer = QVBoxLayout = QWidget = object


CARD_FORMATS = [
    ("Image only (empty back)", "image_only_front"),
    ("Image on front, message text on back", "image_front"),
    ("Message text on front, image on back", "image_back"),
]

SETUP_STEPS = (
    "<b>1.</b> Open <i>discord.com/developers/applications</i> → <b>New Application</b> → "
    "<b>Bot</b> → <b>Reset Token</b> and paste it above.<br>"
    "<b>2.</b> Same page → <b>Privileged Gateway Intents</b> → enable <b>Message Content Intent</b>.<br>"
    "<b>3.</b> <b>OAuth2 → URL Generator</b>: scope <b>bot</b>, permissions <b>View Channels</b> + "
    "<b>Read Message History</b>. Open the URL and add the bot to your server.<br>"
    "<b>4.</b> Discord → Settings → Advanced → <b>Developer Mode</b>. Right-click the channel → "
    "<b>Copy Channel ID</b>."
)


def _split_ids(text: str) -> List[str]:
    out: List[str] = []
    for part in text.replace(";", ",").replace(" ", ",").split(","):
        part = part.strip()
        if part and part not in out:
            out.append(part)
    return out


def _password_mode(line_edit: Any) -> None:
    if hasattr(QLineEdit, "EchoMode") and hasattr(QLineEdit.EchoMode, "Password"):
        line_edit.setEchoMode(QLineEdit.EchoMode.Password)
    elif hasattr(QLineEdit, "Password"):
        line_edit.setEchoMode(QLineEdit.Password)


class DiscordSettingsDialog(BaseToolkitDialog):
    """Discord image import settings."""

    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Discord → Anki",
            subtitle="Images posted in your Discord channel become Anki cards automatically.",
            width=600,
            height=680,
        )
        if not QT_AVAILABLE:
            return

        bg = normalize_hex(config.get("theme.background"), PALETTE.BACKGROUND_PURE_BLACK)
        self._light = is_light_color(bg)
        self._sem = semantic_colors(self._light)
        self._muted = "#71717A" if self._light else "#A1A1AA"
        self._busy = False

        self._build_ui()
        self._load_values()

        self._status_timer = QTimer(self)
        self._status_timer.timeout.connect(self._refresh_live_status)
        self._status_timer.start(2000)
        self._refresh_live_status()

    # ------------------------------------------------------------------ ui

    def _section(self, text: str) -> Any:
        lbl = QLabel(text.upper(), self)
        lbl.setStyleSheet(f"color: {self._muted}; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        return lbl

    def _note(self, text: str = "") -> Any:
        lbl = QLabel(text, self)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {self._muted}; font-size: 11px;")
        return lbl

    def _toggle_button(self, text: str, target: Any) -> Any:
        btn = QPushButton(f"▸ {text}", self)
        btn.setFlat(True)
        btn.setAutoDefault(False)
        btn.setStyleSheet(
            f"QPushButton {{ border: none; background: transparent; color: {self._muted};"
            f" padding: 2px 0px; text-align: left; font-weight: 600; }}"
        )

        def toggle() -> None:
            visible = not target.isVisible()
            target.setVisible(visible)
            btn.setText(("▾ " if visible else "▸ ") + text)

        btn.clicked.connect(toggle)
        target.setVisible(False)
        return btn

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(8)

        self.chk_enabled = QCheckBox("Import images automatically", self)
        self.chk_enabled.setToolTip("Checks the channel every few seconds while Anki is open, "
                                    "and catches up on anything posted while it was closed.")
        layout.addWidget(self.chk_enabled)
        self.lbl_live = self._note()
        layout.addWidget(self.lbl_live)
        layout.addSpacing(6)

        # --- Connection
        layout.addWidget(self._section("Connection"))
        form = QFormLayout()
        form.setSpacing(8)
        self.txt_token = QLineEdit(self)
        _password_mode(self.txt_token)
        self.txt_token.setPlaceholderText("Bot token from the Discord Developer Portal")
        form.addRow("Bot token", self.txt_token)
        self.txt_channel = QLineEdit(self)
        self.txt_channel.setPlaceholderText("e.g. 1234567890123456789")
        self.txt_channel.setToolTip("Right-click the channel in Discord → Copy Channel ID. Separate several with commas.")
        form.addRow("Channel ID", self.txt_channel)
        layout.addLayout(form)

        test_row = QHBoxLayout()
        self.btn_test = QPushButton("Test connection", self)
        self.btn_test.setAutoDefault(False)
        self.btn_test.clicked.connect(self._test_connection)
        test_row.addWidget(self.btn_test)
        test_row.addStretch(1)
        layout.addLayout(test_row)
        self.lbl_test = self._note()
        self.lbl_test.setVisible(False)
        layout.addWidget(self.lbl_test)

        self.help_box = QLabel(SETUP_STEPS, self)
        self.help_box.setWordWrap(True)
        self.help_box.setStyleSheet(f"color: {self._muted}; font-size: 11px; line-height: 1.5;")
        layout.addWidget(self._toggle_button("How to create the bot", self.help_box))
        layout.addWidget(self.help_box)
        layout.addSpacing(8)

        # --- Cards
        layout.addWidget(self._section("Cards"))
        cards = QFormLayout()
        cards.setSpacing(8)
        self.txt_deck = QLineEdit(self)
        self.txt_deck.setPlaceholderText("e.g. Pinterest::Mental")
        self.txt_deck.setToolTip("Created automatically if it does not exist. Use :: for sub-decks.")
        cards.addRow("Deck", self.txt_deck)
        self.txt_tags = QLineEdit(self)
        self.txt_tags.setPlaceholderText("e.g. pinterest, visual")
        cards.addRow("Tags", self.txt_tags)
        self.combo_format = QComboBox(self)
        for label, value in CARD_FORMATS:
            self.combo_format.addItem(label, value)
        cards.addRow("Card format", self.combo_format)
        layout.addLayout(cards)
        self.chk_optimize = QCheckBox("Compress images (WebP, max 1920 px) to keep the collection small", self)
        layout.addWidget(self.chk_optimize)
        layout.addSpacing(8)

        # --- Import existing
        layout.addWidget(self._section("Existing images"))
        import_row = QHBoxLayout()
        import_row.setSpacing(8)
        import_row.addWidget(QLabel("Import from the last", self))
        self.spin_import = QSpinBox(self)
        self.spin_import.setRange(10, 1000)
        self.spin_import.setSingleStep(50)
        self.spin_import.setValue(100)
        import_row.addWidget(self.spin_import)
        import_row.addWidget(QLabel("messages", self))
        import_row.addStretch(1)
        self.btn_import = QPushButton("Import now", self)
        self.btn_import.setAutoDefault(False)
        self.btn_import.setToolTip("Saves these settings, then imports. Already imported images are skipped.")
        self.btn_import.clicked.connect(self._import_history)
        import_row.addWidget(self.btn_import)
        layout.addLayout(import_row)
        self.lbl_import = self._note()
        self.lbl_import.setVisible(False)
        layout.addWidget(self.lbl_import)
        layout.addSpacing(8)

        # --- Advanced
        self.advanced = QWidget(self)
        adv = QFormLayout(self.advanced)
        adv.setContentsMargins(0, 0, 0, 0)
        adv.setSpacing(8)
        self.spin_interval = QSpinBox(self.advanced)
        self.spin_interval.setRange(3, 300)
        self.spin_interval.setSuffix(" s")
        adv.addRow("Check every", self.spin_interval)
        self.txt_cmd_channels = QLineEdit(self.advanced)
        self.txt_cmd_channels.setPlaceholderText("Channels for !anki text commands (optional)")
        adv.addRow("Command channels", self.txt_cmd_channels)
        self.txt_users = QLineEdit(self.advanced)
        self.txt_users.setPlaceholderText("User IDs allowed to use !anki (empty = everyone)")
        adv.addRow("Allowed users", self.txt_users)
        self.chk_reply = QCheckBox("Reply in command channels", self.advanced)
        adv.addRow("", self.chk_reply)
        self.chk_http = QCheckBox("Local HTTP bridge (127.0.0.1)", self.advanced)
        adv.addRow("HTTP bridge", self.chk_http)
        self.spin_port = QSpinBox(self.advanced)
        self.spin_port.setRange(1024, 65535)
        adv.addRow("Bridge port", self.spin_port)
        self.txt_secret = QLineEdit(self.advanced)
        _password_mode(self.txt_secret)
        self.txt_secret.setPlaceholderText("Required for the bridge to start")
        adv.addRow("Bridge token", self.txt_secret)
        layout.addWidget(self._toggle_button("Advanced", self.advanced))
        layout.addWidget(self.advanced)

        layout.addStretch(1)
        self.body_layout.addLayout(layout)

    # --------------------------------------------------------------- values

    def _load_values(self) -> None:
        self.chk_enabled.setChecked(bool(config.get("discord.enabled", False)))
        self.txt_token.setText(str(config.get("discord.bot_token", "") or ""))
        self.txt_channel.setText(", ".join(str(c) for c in config.get("discord.image_channels", [])))
        self.txt_deck.setText(config.get("discord.image_default_deck", "Images::Discord"))
        self.txt_tags.setText(", ".join(config.get("discord.image_default_tags", [])))
        current = config.get("discord.image_card_layout", "image_only_front")
        for i in range(self.combo_format.count()):
            if self.combo_format.itemData(i) == current:
                self.combo_format.setCurrentIndex(i)
        self.chk_optimize.setChecked(bool(config.get("discord.optimize_images", True)))
        self.spin_interval.setValue(int(config.get("discord.polling_interval_seconds", 5) or 5))
        self.txt_cmd_channels.setText(", ".join(str(c) for c in config.get("discord.channel_ids", [])))
        self.txt_users.setText(", ".join(str(u) for u in config.get("discord.authorized_users", [])))
        self.chk_reply.setChecked(bool(config.get("discord.reply_in_channel", True)))
        self.chk_http.setChecked(bool(config.get("discord.http_bridge_enabled", False)))
        self.spin_port.setValue(int(config.get("discord.http_bridge_port", 8765)))
        self.txt_secret.setText(str(config.get("discord.secret_token", "") or ""))

    def _apply_settings(self) -> None:
        tags = [t.strip() for t in self.txt_tags.text().split(",") if t.strip()]
        values: Dict[str, Any] = {
            "discord.bot_token": self.txt_token.text().strip(),
            "discord.image_channels": _split_ids(self.txt_channel.text()),
            "discord.image_default_deck": self.txt_deck.text().strip() or "Images::Discord",
            "discord.image_default_tags": tags,
            "discord.image_card_layout": self.combo_format.currentData() or "image_only_front",
            "discord.optimize_images": self.chk_optimize.isChecked(),
            "discord.polling_interval_seconds": self.spin_interval.value(),
            "discord.channel_ids": _split_ids(self.txt_cmd_channels.text()),
            "discord.authorized_users": _split_ids(self.txt_users.text()),
            "discord.reply_in_channel": self.chk_reply.isChecked(),
            "discord.http_bridge_enabled": self.chk_http.isChecked(),
            "discord.http_bridge_port": self.spin_port.value(),
            "discord.secret_token": self.txt_secret.text().strip(),
        }
        for key, value in values.items():
            config.set(key, value, save=False)
        # Last: toggling "enabled" (re)starts the poller with all values above in place
        config.set("discord.enabled", self.chk_enabled.isChecked(), save=True)

    # ------------------------------------------------------------- feedback

    def _show(self, label: Any, text: str, kind: str = "info") -> None:
        color = {"ok": self._sem["review"], "error": self._sem["again"], "info": self._muted}[kind]
        label.setStyleSheet(f"color: {color}; font-size: 11px;")
        label.setText(text)
        label.setVisible(True)

    def _refresh_live_status(self) -> None:
        try:
            poller = discord_client_manager.poller
            status = poller.status
            if not config.get("discord.enabled", False):
                self.lbl_live.setText("Off — turn on and save to start importing.")
                return
            if not poller.is_running():
                self.lbl_live.setText("Waiting for a bot token and channel ID.")
                return
            parts = []
            if status.get("last_poll"):
                parts.append(f"Last check {int(time.time() - status['last_poll'])}s ago")
            parts.append(f"{status.get('imported', 0)} image(s) imported this session")
            text = " · ".join(parts)
            if status.get("last_error"):
                text += f"\n⚠ {status['last_error']}"
            self.lbl_live.setText(text)
        except RuntimeError:
            pass  # dialog closing

    def _run_async(self, task: Callable[[], Any], done: Callable[[Any], None], buttons: List[Any]) -> None:
        for b in buttons:
            b.setEnabled(False)

        def finish(result: Any) -> None:
            try:
                for b in buttons:
                    b.setEnabled(True)
                done(result)
            except RuntimeError:
                pass  # dialog was closed meanwhile

        def fail(error: Exception) -> None:
            finish({"success": False, "ok": False, "error": str(error), "lines": [f"✗ {error}"]})

        run_in_background(task, on_success=finish, on_failure=fail)

    # -------------------------------------------------------------- actions

    def _test_connection(self) -> None:
        token = self.txt_token.text().strip()
        channels = _split_ids(self.txt_channel.text())
        self._show(self.lbl_test, "Connecting to Discord…")
        channel = channels[0] if channels else ""

        def done(result: Dict[str, Any]) -> None:
            self._show(self.lbl_test, "\n".join(result.get("lines", [])), "ok" if result.get("ok") else "error")

        self._run_async(lambda: test_discord_connection(token, channel), done, [self.btn_test])

    def _import_history(self) -> None:
        channels = _split_ids(self.txt_channel.text())
        if not self.txt_token.text().strip() or not channels:
            self._show(self.lbl_import, "Enter the bot token and channel ID first.", "error")
            return
        self._apply_settings()
        limit = self.spin_import.value()
        deck = self.txt_deck.text().strip() or "Images::Discord"
        self._show(self.lbl_import, f"Importing from the last {limit} messages… (Anki stays usable)")

        def task() -> Dict[str, Any]:
            totals = {"success": True, "scanned": 0, "with_images": 0, "imported": 0, "skipped": 0}
            for ch in channels:
                res = discord_client_manager.import_history(ch, limit)
                if not res.get("success"):
                    return res
                for k in ("scanned", "with_images", "imported", "skipped"):
                    totals[k] += res.get(k, 0)
            return totals

        def done(res: Dict[str, Any]) -> None:
            if not res.get("success"):
                self._show(self.lbl_import, f"✗ {res.get('error', 'Import failed')}", "error")
                return
            self._show(
                self.lbl_import,
                f"✓ {res['imported']} new image(s) queued for '{deck}' · "
                f"{res['skipped']} already imported or failed · {res['scanned']} messages checked.\n"
                "Cards appear in a few seconds.",
                "ok",
            )

        self._run_async(task, done, [self.btn_import, self.btn_test])

    def accept(self) -> None:
        try:
            self._apply_settings()
            logger.info("[DiscordSettingsDialog] Discord settings saved.")
            super().accept()
        except Exception as e:
            logger.error(f"[DiscordSettingsDialog] Error saving Discord settings: {e}", exc_info=True)

    def done(self, result: int) -> None:  # stop the status timer on accept/reject
        try:
            self._status_timer.stop()
        except Exception:
            pass
        super().done(result)
