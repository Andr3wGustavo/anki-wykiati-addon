"""
Translucent Glass Pomodoro Pill Widget for Anki's Main Window and Reviewer Bar.
Displays real-time countdown, session state, and quick play/pause controls.
"""

from typing import Any, Optional

try:
    from ...timer.pomodoro import PomodoroEngine, PomodoroState, pomodoro_engine
    from .base_dialog import QT_AVAILABLE
except (ImportError, ValueError):
    from timer.pomodoro import PomodoroEngine, PomodoroState, pomodoro_engine
    from ui.components.base_dialog import QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCursor,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QTimer,
            QWidget,
            Qt,
        )
    except ImportError:
        try:
            from PyQt6.QtCore import Qt, QTimer
            from PyQt6.QtGui import QCursor
            from PyQt6.QtWidgets import (
                QHBoxLayout,
                QLabel,
                QPushButton,
                QWidget,
            )
        except ImportError:
            from PyQt5.QtCore import Qt, QTimer
            from PyQt5.QtGui import QCursor
            from PyQt5.QtWidgets import (
                QHBoxLayout,
                QLabel,
                QPushButton,
                QWidget,
            )
else:
    QCursor = QHBoxLayout = QLabel = QPushButton = QTimer = QWidget = Qt = object


class PomodoroPillWidget(QWidget):
    """
    Sleek floating glass capsule widget displaying current Pomodoro timer status.
    """
    def __init__(self, parent: Optional[Any] = None, on_open_dialog: Optional[Any] = None) -> None:
        if not QT_AVAILABLE:
            return
        super().__init__(parent)
        self._on_open_dialog = on_open_dialog

        self._build_ui()
        self._setup_timer()

        # Connect to engine observer
        pomodoro_engine.add_observer(self._on_engine_update)
        self._update_display(pomodoro_engine.state, pomodoro_engine.current_seconds)

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(6)

        # Translucent glass capsule styling
        self.setStyleSheet(
            "PomodoroPillWidget { "
            "  background-color: rgba(255, 255, 255, 0.05); "
            "  border: 1px solid rgba(255, 255, 255, 0.12); "
            "  border-radius: 12px; "
            "}"
        )

        # Timer Icon & Label
        self.lbl_timer = QLabel("🍅 25:00", self)
        self.lbl_timer.setStyleSheet(
            "font-size: 12px; font-weight: 700; color: #FFFFFF; font-family: monospace;"
        )
        if hasattr(Qt, "CursorShape"):
            self.lbl_timer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_timer.mousePressEvent = lambda e: self._handle_open_dialog()
        layout.addWidget(self.lbl_timer)

        # Quick Toggle Play / Pause Button
        self.btn_toggle = QPushButton("▶", self)
        self.btn_toggle.setFixedSize(20, 20)
        self.btn_toggle.setStyleSheet(
            "QPushButton { background: transparent; border: none; color: #FFFFFF; font-size: 11px; } "
            "QPushButton:hover { color: #38BDF8; }"
        )
        self.btn_toggle.clicked.connect(self._toggle_timer)
        layout.addWidget(self.btn_toggle)

    def _setup_timer(self) -> None:
        self._qtimer = QTimer(self)
        self._qtimer.setInterval(1000)
        self._qtimer.timeout.connect(pomodoro_engine.tick)
        self._qtimer.start()

    def _toggle_timer(self) -> None:
        pomodoro_engine.toggle()
        self._update_btn_state()

    def _handle_open_dialog(self) -> None:
        if callable(self._on_open_dialog):
            self._on_open_dialog()

    def _on_engine_update(self, state: PomodoroState, remaining_sec: int, target_sec: int) -> None:
        self._update_display(state, remaining_sec)

    def _update_display(self, state: PomodoroState, remaining_sec: int) -> None:
        mins = remaining_sec // 60
        secs = remaining_sec % 60
        time_str = f"{mins:02d}:{secs:02d}"

        if state == PomodoroState.WORK:
            emoji = "🍅"
            color = "#38BDF8"  # Cyan Work
        elif state == PomodoroState.SHORT_BREAK:
            emoji = "☕"
            color = "#4ADE80"  # Green Break
        elif state == PomodoroState.LONG_BREAK:
            emoji = "🌴"
            color = "#A78BFA"  # Violet Long Break
        elif state == PomodoroState.PAUSED:
            emoji = "⏸️"
            color = "#FBBF24"  # Amber Paused
        else:
            emoji = "🍅"
            color = "#FFFFFF"

        self.lbl_timer.setText(f"{emoji} {time_str}")
        self.lbl_timer.setStyleSheet(
            f"font-size: 12px; font-weight: 700; color: {color}; font-family: monospace;"
        )
        self._update_btn_state()

    def _update_btn_state(self) -> None:
        if pomodoro_engine.is_running:
            self.btn_toggle.setText("⏸")
        else:
            self.btn_toggle.setText("▶")
