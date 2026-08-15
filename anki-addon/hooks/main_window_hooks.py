"""
Main Window Lifecycle Hooks.
"""

from ..core.logger import logger
from ..ui.menu import menu_manager

try:
    from aqt import gui_hooks
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = None
    ANKI_AVAILABLE = False


def _on_main_window_init() -> None:
    logger.info("[Hooks:MainWindow] Main window ready. Setting up menus...")
    menu_manager.setup_menu()


def register_main_window_hooks() -> None:
    if not ANKI_AVAILABLE or gui_hooks is None:
        logger.debug("[Hooks:MainWindow] Anki not detected. Skipping main window hooks.")
        return

    try:
        if hasattr(gui_hooks, "main_window_did_init"):
            gui_hooks.main_window_did_init.append(_on_main_window_init)
        else:
            # Fallback direct call if already initialized
            menu_manager.setup_menu()
    except Exception as e:
        logger.error(f"[Hooks:MainWindow] Error registering main window hook: {e}")
