"""
Unit Tests for Pomodoro & Speed Focus Timer Engine and UI.
"""

import os
import sys
import unittest

# Add addon directory to path
ADDON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ADDON_DIR not in sys.path:
    sys.path.insert(0, ADDON_DIR)

from core.config import config
from timer.pomodoro import PomodoroEngine, PomodoroState
from ui.pomodoro_dialog import PomodoroDialog
from ui.components.pomodoro_widget import PomodoroPillWidget


class TestPomodoro(unittest.TestCase):
    def setUp(self) -> None:
        config.reset_to_defaults()
        self.engine = PomodoroEngine()

    def test_pomodoro_initial_state(self) -> None:
        self.assertEqual(self.engine.state, PomodoroState.IDLE)
        self.assertEqual(self.engine.current_seconds, 25 * 60)
        self.assertEqual(self.engine.target_seconds, 25 * 60)
        self.assertFalse(self.engine.is_running)

    def test_pomodoro_start_and_pause(self) -> None:
        self.engine.start()
        self.assertEqual(self.engine.state, PomodoroState.WORK)
        self.assertTrue(self.engine.is_running)

        self.engine.pause()
        self.assertEqual(self.engine.state, PomodoroState.PAUSED)
        self.assertFalse(self.engine.is_running)

        self.engine.start()
        self.assertEqual(self.engine.state, PomodoroState.WORK)
        self.assertTrue(self.engine.is_running)

    def test_pomodoro_tick_and_progress(self) -> None:
        self.engine.start()
        initial_sec = self.engine.current_seconds
        self.engine.tick()
        self.assertEqual(self.engine.current_seconds, initial_sec - 1)
        self.assertGreater(self.engine.get_progress_ratio(), 0.0)

    def test_pomodoro_work_to_short_break_transition(self) -> None:
        self.engine.start()
        self.engine.current_seconds = 1
        self.engine.tick()  # 1 -> 0
        self.engine.tick()  # 0 -> transition to SHORT_BREAK
        
        self.assertEqual(self.engine.state, PomodoroState.SHORT_BREAK)
        self.assertEqual(self.engine.session_count, 1)
        self.assertEqual(self.engine.target_seconds, 5 * 60)

    def test_pomodoro_long_break_transition(self) -> None:
        # Simulate 3 completed sessions
        self.engine.session_count = 3
        self.engine.state = PomodoroState.WORK
        self.engine.is_running = True
        self.engine.current_seconds = 0
        self.engine.tick()  # 4th session completed -> LONG_BREAK

        self.assertEqual(self.engine.state, PomodoroState.LONG_BREAK)
        self.assertEqual(self.engine.session_count, 4)
        self.assertEqual(self.engine.target_seconds, 15 * 60)

    def test_pomodoro_card_review_recording(self) -> None:
        self.engine.start()
        self.assertEqual(self.engine.cards_reviewed_in_session, 0)
        self.engine.record_card_reviewed()
        self.engine.record_card_reviewed()
        self.assertEqual(self.engine.cards_reviewed_in_session, 2)

    def test_pomodoro_ui_instantiations(self) -> None:
        dialog = PomodoroDialog()
        self.assertIsNotNone(dialog)

        pill = PomodoroPillWidget()
        self.assertIsNotNone(pill)


if __name__ == "__main__":
    unittest.main()
