"""
Profile Lifecycle Hooks.
Activates ThemeEngine and DiscordClient when user profile is loaded.
"""

from typing import Any

from ..core.config import config
from ..core.event_bus import event_bus
from ..core.logger import logger
from ..discord.client import discord_client_manager
from ..sync.worker import sync_worker
from ..theme.engine import theme_engine

try:
    from aqt import gui_hooks
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = None
    ANKI_AVAILABLE = False


def _on_profile_loaded() -> None:
    """Invoked when user profile finishes loading in Anki."""
    logger.info("[Hooks:Profile] Profile loaded. Initializing services...")

    # 1. Initialize & Apply Theme
    if config.get("theme.enabled", True):
        theme_engine.activate()

    # 2. Start Background Sync Worker
    sync_worker.start()

    # 3. Start Discord Client & HTTP Bridge
    discord_client_manager.initialize()

    # 4. Notify event bus
    event_bus.publish("profile:loaded")


def _on_profile_will_close() -> None:
    """Invoked before profile closes."""
    logger.info("[Hooks:Profile] Profile closing. Shutting down background tasks...")
    sync_worker.stop()
    discord_client_manager.shutdown()
    event_bus.publish("profile:closing")


def register_profile_hooks() -> None:
    if not ANKI_AVAILABLE or gui_hooks is None:
        logger.debug("[Hooks:Profile] Anki not detected. Skipping profile hook registration.")
        return

    try:
        if hasattr(gui_hooks, "profile_did_open"):
            gui_hooks.profile_did_open.append(_on_profile_loaded)
        if hasattr(gui_hooks, "profile_will_close"):
            gui_hooks.profile_will_close.append(_on_profile_will_close)
        logger.info("[Hooks:Profile] Registered profile lifecycle hooks.")
    except Exception as e:
        logger.error(f"[Hooks:Profile] Failed registering profile hooks: {e}")
