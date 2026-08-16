"""
Pomodoro & Speed Focus Studio Modal Dialog for Anki Wykiati Toolkit.
Minimalist, didactic interface for managing study intervals, statistics, and speed focus.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.constants import ADDON_NAME
    from ..core.logger import logger
    from ..theme.palette import PALETTE
    from ..timer.pomodoro import PomodoroEngine, PomodoroState, pomodoro_engine
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.constants import ADDON_NAME
    from core.logger import logger
    from theme.palette import PALETTE
    from timer.pomodoro import PomodoroEngine, PomodoroState, pomodoro_engine
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox,
            QFormLayout,
            QFrame,
            QGridLayout,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
            QWidget,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QCheckBox,
                QFormLayout,
                QFrame,
                QGridLayout,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QSpinBox,
                QVBoxLayout,
                QWidget,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QCheckBox,
                QFormLayout,
                QFrame,
                QGridLayout,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QSpinBox,
                QVBoxLayout,
                QWidget,
            )
else:
    QCheckBox = QFormLayout = QFrame = QGridLayout = QHBoxLayout = QLabel = QPushButton = QSpinBox = QVBoxLayout = QWidget = object


class PomodoroDialog(BaseToolkitDialog):
    """
    Focus and Pomodoro Studio modal dialog.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Focus Timer & Pomodoro Studio",
            subtitle="Optimize your active recall sessions with structured work/break intervals and speed focus.",
            width=580,
            height=480,
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(460, 360)
        self._build_ui()
        self._load_values()

        # Connect to engine observer
        pomodoro_engine.add_observer(self._on_engine_update)
        self._refresh_timer_display(pomodoro_engine.state, pomodoro_engine.current_seconds)

    def closeEvent(self, event: Any) -> None:
        pomodoro_engine.remove_observer(self._on_engine_update)
        super().closeEvent(event)

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # 1. Big Center Display Card
        timer_card = QFrame(self)
        timer_card.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.03); "
            "border: 1px solid rgba(255, 255, 255, 0.08); "
            "border-radius: 8px; padding: 14px;"
        )
        t_layout = QVBoxLayout(timer_card)
        t_layout.setContentsMargins(10, 8, 10, 8)
        t_layout.setSpacing(6)

        # Phase Badge
        self.lbl_phase_badge = QLabel("🍅 WORK SESSION", timer_card)
        self.lbl_phase_badge.setStyleSheet(
            "font-size: 11px; font-weight: 700; color: #38BDF8; letter-spacing: 0.06em; text-transform: uppercase;"
        )
        t_layout.addWidget(self.lbl_phase_badge)

        # Big Countdown Display
        self.lbl_big_timer = QLabel("25:00", timer_card)
        self.lbl_big_timer.setStyleSheet(
            "font-size: 42px; font-weight: 800; color: #FFFFFF; font-family: monospace; letter-spacing: -0.02em;"
        )
        t_layout.addWidget(self.lbl_big_timer)

        # Action Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_toggle_play = QPushButton("Start Focus Session", timer_card)
        self.btn_toggle_play.setProperty("primary", "true")
        self.btn_toggle_play.clicked.connect(self._toggle_timer)
        btn_row.addWidget(self.btn_toggle_play)

        self.btn_skip = QPushButton("Skip Phase", timer_card)
        self.btn_skip.clicked.connect(self._skip_phase)
        btn_row.addWidget(self.btn_skip)

        self.btn_reset = QPushButton("Reset", timer_card)
        self.btn_reset.clicked.connect(self._reset_timer)
        btn_row.addWidget(self.btn_reset)

        btn_row.addStretch()
        t_layout.addLayout(btn_row)
        main_layout.addWidget(timer_card)

        # 2. Configuration Settings Card
        group_config = QFrame(self)
        group_config.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.025); "
            "border: 1px solid rgba(255, 255, 255, 0.08); "
            "border-radius: 8px; padding: 12px;"
        )
        cfg_layout = QVBoxLayout(group_config)
        cfg_layout.setContentsMargins(10, 8, 10, 8)
        cfg_layout.setSpacing(10)

        cfg_title = QLabel("Interval & Mode Configuration", group_config)
        cfg_title.setStyleSheet("font-size: 12px; font-weight: 700; color: #FFFFFF;")
        cfg_layout.addWidget(cfg_title)

        form = QFormLayout()
        form.setSpacing(8)

        # Work Duration
        self.spin_work = QSpinBox(group_config)
        self.spin_work.setRange(1, 120)
        self.spin_work.setSuffix(" min")
        form.addRow("Work Duration:", self.spin_work)

        # Short Break
        self.spin_short_break = QSpinBox(group_config)
        self.spin_short_break.setRange(1, 60)
        self.spin_short_break.setSuffix(" min")
        form.addRow("Short Break:", self.spin_short_break)

        # Long Break
        self.spin_long_break = QSpinBox(group_config)
        self.spin_long_break.setRange(1, 90)
        self.spin_long_break.setSuffix(" min")
        form.addRow("Long Break:", self.spin_long_break)

        # Long Break Interval
        self.spin_interval = QSpinBox(group_config)
        self.spin_interval.setRange(1, 12)
        self.spin_interval.setSuffix(" sessions")
        form.addRow("Long Break Interval:", self.spin_interval)

        # Auto-start breaks
        self.chk_auto_breaks = QCheckBox("Auto-start break countdown when work interval finishes", group_config)
        form.addRow("Auto Breaks:", self.chk_auto_breaks)

        # Speed focus mode
        self.chk_speed_focus = QCheckBox("Enable Speed Focus (Max 10s per card recall)", group_config)
        form.addRow("Speed Focus:", self.chk_speed_focus)

        cfg_layout.addLayout(form)
        main_layout.addWidget(group_config)

        # 3. Session Statistics Grid
        stats_frame = QFrame(self)
        stats_frame.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.025); "
            "border: 1px solid rgba(255, 255, 255, 0.08); "
            "border-radius: 8px; padding: 10px;"
        )
        s_layout = QGridLayout(stats_frame)
        s_layout.setContentsMargins(8, 6, 8, 6)
        s_layout.setSpacing(10)

        self.lbl_stat_sessions = self._create_stat_widget("Sessions Done", "0", "#38BDF8", s_layout, 0, 0)
        self.lbl_stat_focus_time = self._create_stat_widget("Total Focus Time", "0 min", "#4ADE80", s_layout, 0, 1)
        self.lbl_stat_cards = self._create_stat_widget("Cards in Session", "0", "#FBBF24", s_layout, 0, 2)

        main_layout.addWidget(stats_frame)

        self.body_layout.addLayout(main_layout)

    def _create_stat_widget(self, title: str, val: str, color: str, grid: QGridLayout, row: int, col: int) -> QLabel:
        w = QWidget(self)
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(2)

        lbl_t = QLabel(title, w)
        lbl_t.setStyleSheet("font-size: 10px; color: #A1A1AA; text-transform: uppercase; font-weight: 600;")
        l.addWidget(lbl_t)

        lbl_v = QLabel(val, w)
        lbl_v.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {color};")
        l.addWidget(lbl_v)

        grid.addWidget(w, row, col)
        return lbl_v

    def _load_values(self) -> None:
        self.spin_work.setValue(int(config.get("pomodoro.work_minutes", 25)))
        self.spin_short_break.setValue(int(config.get("pomodoro.short_break_minutes", 5)))
        self.spin_long_break.setValue(int(config.get("pomodoro.long_break_minutes", 15)))
        self.spin_interval.setValue(int(config.get("pomodoro.long_break_interval", 4)))
        self.chk_auto_breaks.setChecked(bool(config.get("pomodoro.auto_start_breaks", True)))
        self.chk_speed_focus.setChecked(bool(config.get("pomodoro.speed_focus_mode", False)))
        self._refresh_stats()

    def _refresh_stats(self) -> None:
        sessions = config.get("pomodoro.completed_sessions", 0)
        total_sec = config.get("pomodoro.total_focus_seconds", 0)
        mins = total_sec // 60
        cards = pomodoro_engine.cards_reviewed_in_session

        self.lbl_stat_sessions.setText(str(sessions))
        self.lbl_stat_focus_time.setText(f"{mins} min")
        self.lbl_stat_cards.setText(str(cards))

    def _toggle_timer(self) -> None:
        pomodoro_engine.toggle()
        self._update_play_button_text()

    def _skip_phase(self) -> None:
        pomodoro_engine.skip_interval()

    def _reset_timer(self) -> None:
        pomodoro_engine.reset_to_work()
        self._update_play_button_text()

    def _update_play_button_text(self) -> None:
        if pomodoro_engine.is_running:
            self.btn_toggle_play.setText("Pause Session")
        else:
            self.btn_toggle_play.setText("Start Focus Session")

    def _on_engine_update(self, state: PomodoroState, remaining_sec: int, target_sec: int) -> None:
        self._refresh_timer_display(state, remaining_sec)
        self._refresh_stats()

    def _refresh_timer_display(self, state: PomodoroState, remaining_sec: int) -> None:
        mins = remaining_sec // 60
        secs = remaining_sec % 60
        self.lbl_big_timer.setText(f"{mins:02d}:{secs:02d}")

        if state == PomodoroState.WORK:
            self.lbl_phase_badge.setText(f"🍅 WORK SESSION (Streak: #{pomodoro_engine.session_count + 1})")
            self.lbl_phase_badge.setStyleSheet("font-size: 11px; font-weight: 700; color: #38BDF8; letter-spacing: 0.06em;")
        elif state == PomodoroState.SHORT_BREAK:
            self.lbl_phase_badge.setText("☕ SHORT BREAK — REST & HYDRATE")
            self.lbl_phase_badge.setStyleSheet("font-size: 11px; font-weight: 700; color: #4ADE80; letter-spacing: 0.06em;")
        elif state == PomodoroState.LONG_BREAK:
            self.lbl_phase_badge.setText("🌴 LONG BREAK — RELAX YOUR EYES")
            self.lbl_phase_badge.setStyleSheet("font-size: 11px; font-weight: 700; color: #A78BFA; letter-spacing: 0.06em;")
        elif state == PomodoroState.PAUSED:
            self.lbl_phase_badge.setText("⏸️ SESSION PAUSED")
            self.lbl_phase_badge.setStyleSheet("font-size: 11px; font-weight: 700; color: #FBBF24; letter-spacing: 0.06em;")
        else:
            self.lbl_phase_badge.setText("🍅 READY TO FOCUS")
            self.lbl_phase_badge.setStyleSheet("font-size: 11px; font-weight: 700; color: #A1A1AA; letter-spacing: 0.06em;")

        self._update_play_button_text()

    def accept(self) -> None:
        try:
            config.set("pomodoro.work_minutes", self.spin_work.value(), save=False)
            config.set("pomodoro.short_break_minutes", self.spin_short_break.value(), save=False)
            config.set("pomodoro.long_break_minutes", self.spin_long_break.value(), save=False)
            config.set("pomodoro.long_break_interval", self.spin_interval.value(), save=False)
            config.set("pomodoro.auto_start_breaks", self.chk_auto_breaks.isChecked(), save=False)
            config.set("pomodoro.speed_focus_mode", self.chk_speed_focus.isChecked(), save=True)

            logger.info("[PomodoroDialog] Updated Pomodoro preferences.")
            super().accept()
        except Exception as e:
            logger.error(f"[PomodoroDialog] Failed saving Pomodoro preferences: {e}")
