"""
Anki Discord Toolkit Entry Point.
Initializes configuration, Pure Black AMOLED theme engine, Discord bridge, and GUI hooks.
"""

from .core.config import config
from .core.constants import ADDON_NAME, ADDON_VERSION
from .core.logger import logger
from .hooks import register_all_hooks
from .theme.engine import theme_engine
from .ui.menu import menu_manager


def init_toolkit() -> None:
    """
    Main bootstrapping sequence for Anki Discord Toolkit.
    """
    try:
        logger.info(f"=== Initializing {ADDON_NAME} v{ADDON_VERSION} ===")

        # 1. Verify if addon is enabled
        if not config.get("addon_enabled", True):
            logger.info(f"{ADDON_NAME} is disabled in configuration. Skipping initialization.")
            return

        # 2. Initialize Theme Engine
        theme_engine.initialize()

        # 3. Register Event & Lifecycle Hooks
        register_all_hooks()

        # 4. Setup GUI Menu bar
        menu_manager.setup_menu()

        logger.info(f"=== {ADDON_NAME} v{ADDON_VERSION} Bootstrapped Successfully ===")

    except Exception as e:
        logger.critical(f"Critical error during {ADDON_NAME} bootstrap: {e}", exc_info=True)


# Execute add-on initialization
init_toolkit()
