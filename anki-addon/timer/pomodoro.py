"""
Pomodoro and Speed Focus Timer Engine for Anki Wykiati Toolkit.
Provides interval tracking, session statistics, speed focus mode, and state transitions.
"""

from enum import Enum
import time
from typing import Callable, Dict, List, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger


class PomodoroState(str, Enum):
    IDLE = "IDLE"
    WORK = "WORK"
    SHORT_BREAK = "SHORT_BREAK"
    LONG_BREAK = "LONG_BREAK"
    PAUSED = "PAUSED"


class PomodoroEngine:
    """
    State machine and countdown engine for Pomodoro study sessions and Speed Focus recall.
    """
    def __init__(self) -> None:
        self.state: PomodoroState = PomodoroState.IDLE
        self._previous_state: PomodoroState = PomodoroState.WORK
        self.current_seconds: int = 25 * 60
        self.target_seconds: int = 25 * 60
        self.session_count: int = 0
        self.cards_reviewed_in_session: int = 0
        self.is_running: bool = False
        self._last_tick_time: float = 0.0

        # Speed focus mode (seconds per card)
        self.card_timer_active: bool = False
        self.card_seconds_remaining: int = 10

        # Observers for reactive UI updates
        self._state_callbacks: List[Callable[[PomodoroState, int, int], None]] = []
        self._completion_callbacks: List[Callable[[PomodoroState], None]] = []
        
        self.reset_to_work()

    def add_observer(self, callback: Callable[[PomodoroState, int, int], None]) -> None:
        """Register a callback for tick and state changes: callback(state, remaining_sec, target_sec)."""
        if callback not in self._state_callbacks:
            self._state_callbacks.append(callback)

    def remove_observer(self, callback: Callable[[PomodoroState, int, int], None]) -> None:
        if callback in self._state_callbacks:
            self._state_callbacks.remove(callback)

    def on_interval_completed(self, callback: Callable[[PomodoroState], None]) -> None:
        """Register a callback when a work/break interval finishes."""
        if callback not in self._completion_callbacks:
            self._completion_callbacks.append(callback)

    def get_work_duration(self) -> int:
        return int(config.get("pomodoro.work_minutes", 25)) * 60

    def get_short_break_duration(self) -> int:
        return int(config.get("pomodoro.short_break_minutes", 5)) * 60

    def get_long_break_duration(self) -> int:
        return int(config.get("pomodoro.long_break_minutes", 15)) * 60

    def get_long_break_interval(self) -> int:
        return int(config.get("pomodoro.long_break_interval", 4))

    def start(self) -> None:
        """Start or resume the timer."""
        if self.state == PomodoroState.PAUSED:
            self.state = self._previous_state
        elif self.state == PomodoroState.IDLE:
            self.state = PomodoroState.WORK
            self.target_seconds = self.get_work_duration()
            self.current_seconds = self.target_seconds

        self.is_running = True
        self._last_tick_time = time.time()
        logger.info(f"[Pomodoro] Started session in state {self.state.value} ({self.current_seconds}s remaining).")
        self._notify_observers()

    def pause(self) -> None:
        """Pause the active countdown."""
        if self.is_running:
            self._previous_state = self.state
            self.state = PomodoroState.PAUSED
            self.is_running = False
            logger.info(f"[Pomodoro] Paused at {self.current_seconds}s.")
            self._notify_observers()

    def toggle(self) -> None:
        """Toggle between Running and Paused."""
        if self.is_running:
            self.pause()
        else:
            self.start()

    def reset_to_work(self) -> None:
        """Reset countdown to Work mode."""
        self.is_running = False
        self.state = PomodoroState.IDLE
        self.target_seconds = self.get_work_duration()
        self.current_seconds = self.target_seconds
        self._notify_observers()

    def skip_interval(self) -> None:
        """Skip the current interval to the next logical phase."""
        self._advance_phase(forced_skip=True)

    def tick(self) -> None:
        """Decrement counter by 1 second (invoked by QTimer or background thread)."""
        if not self.is_running:
            return

        if self.current_seconds > 0:
            self.current_seconds -= 1
            self._notify_observers()
        else:
            self._advance_phase(forced_skip=False)

    def _advance_phase(self, forced_skip: bool = False) -> None:
        """Advance to next Pomodoro phase."""
        prev = self.state
        if prev == PomodoroState.PAUSED:
            prev = self._previous_state

        if prev == PomodoroState.WORK or prev == PomodoroState.IDLE:
            self.session_count += 1
            self._record_completed_session()
            
            interval = self.get_long_break_interval()
            if self.session_count > 0 and self.session_count % interval == 0:
                self.state = PomodoroState.LONG_BREAK
                self.target_seconds = self.get_long_break_duration()
            else:
                self.state = PomodoroState.SHORT_BREAK
                self.target_seconds = self.get_short_break_duration()

            self.current_seconds = self.target_seconds
            auto_break = config.get("pomodoro.auto_start_breaks", True)
            self.is_running = auto_break

        else:
            # Completing Break -> Go to Work
            self.state = PomodoroState.WORK
            self.target_seconds = self.get_work_duration()
            self.current_seconds = self.target_seconds
            auto_work = config.get("pomodoro.auto_start_work", False)
            self.is_running = auto_work

        logger.info(f"[Pomodoro] Phase transition {prev.value} -> {self.state.value} (Session #{self.session_count}).")
        
        for cb in self._completion_callbacks:
            try:
                cb(prev)
            except Exception as e:
                logger.error(f"[Pomodoro] Error in completion callback: {e}")

        self._notify_observers()

    def record_card_reviewed(self) -> None:
        """Record a card review event during an active Pomodoro session."""
        if self.is_running and self.state == PomodoroState.WORK:
            self.cards_reviewed_in_session += 1

    def _record_completed_session(self) -> None:
        try:
            total = int(config.get("pomodoro.completed_sessions", 0)) + 1
            config.set("pomodoro.completed_sessions", total, save=False)
            
            work_sec = self.get_work_duration()
            total_sec = int(config.get("pomodoro.total_focus_seconds", 0)) + work_sec
            config.set("pomodoro.total_focus_seconds", total_sec, save=True)
        except Exception as e:
            logger.error(f"[Pomodoro] Failed persisting session stats: {e}")

    def _notify_observers(self) -> None:
        for cb in self._state_callbacks:
            try:
                cb(self.state, self.current_seconds, self.target_seconds)
            except Exception as e:
                logger.error(f"[Pomodoro] Error in state callback: {e}")

    def format_time(self) -> str:
        """Format current seconds as MM:SS."""
        mins = self.current_seconds // 60
        secs = self.current_seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def get_progress_ratio(self) -> float:
        """Return ratio from 0.0 to 1.0."""
        if self.target_seconds <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (self.current_seconds / self.target_seconds)))


# Global singleton instance
pomodoro_engine = PomodoroEngine()
