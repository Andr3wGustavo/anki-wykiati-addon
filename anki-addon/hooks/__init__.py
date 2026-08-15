"""
Hooks registration aggregator for Anki Discord Toolkit.
"""

from .main_window_hooks import register_main_window_hooks
from .profile_hooks import register_profile_hooks
from .reviewer_hooks import register_reviewer_hooks


def register_all_hooks() -> None:
    """Register all lifecycle hooks with Anki's gui_hooks system."""
    register_profile_hooks()
    register_main_window_hooks()
    register_reviewer_hooks()


__all__ = [
    "register_all_hooks",
    "register_profile_hooks",
    "register_main_window_hooks",
    "register_reviewer_hooks",
]
