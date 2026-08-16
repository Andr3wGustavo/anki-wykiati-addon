"""
Centralized Configuration Manager for Anki Discord Toolkit.
Handles JSON schema defaults, dot-notation access, corruption auto-repair, and reactive subscriptions.
"""

import copy
import json
import os
from typing import Any, Callable, Dict, List, Optional

from .constants import ADDON_PACKAGE, DEFAULT_CONFIG_FILENAME
from .exceptions import ConfigurationError
from .logger import logger

# Conditional import of Anki's main window
try:
    from aqt import mw
except ImportError:
    mw = None

DEFAULT_CONFIG: Dict[str, Any] = {
    "addon_enabled": True,
    "debug_mode": False,
    "log_level": "INFO",
    "theme": {
        "enabled": True,
        "style_variant": "liquid_glass",
        "background": "#000000",
        "surface": "rgba(20, 22, 28, 0.75)",
        "surface_secondary": "rgba(30, 34, 42, 0.6)",
        "accent": "#0A84FF",
        "text_primary": "#FFFFFF",
        "text_secondary": "#EBEBF5",
        "border": "rgba(255, 255, 255, 0.12)",
        "apply_to_webviews": True,
        "pure_black_reviewer": True,
    },
    "discord": {
        "enabled": False,
        "mode": "http",
        "bot_token": "",
        "channel_ids": [],
        "image_channels": [],
        "auto_ingest_images": True,
        "image_card_layout": "image_front",
        "image_default_deck": "Images::Discord",
        "image_default_tags": ["discord", "image"],
        "authorized_users": [],
        "guild_ids": [],
        "polling_interval_seconds": 5,
        "http_bridge_enabled": True,
        "http_bridge_host": "127.0.0.1",
        "http_bridge_port": 8765,
        "secret_token": "",
        "rate_limit_per_minute": 60,
        "max_message_length": 4000,
    },
    "anki": {
        "default_deck": "Default",
        "default_template": "Basic",
        "tags_prefix": "",
        "auto_create_decks": True,
        "duplicate_policy": "skip",
    },
    "routing": {
        "enabled": True,
        "rules": [
            {"type": "tag", "pattern": "python", "deck": "Programming::Python"},
            {"type": "tag", "pattern": "docker", "deck": "DevOps::Docker"},
            {"type": "tag", "pattern": "linux", "deck": "Operating Systems::Linux"},
            {"type": "keyword", "pattern": "algorithm", "deck": "Computer Science::Algorithms"},
        ],
    },
    "stats": {
        "cards_created": 0,
        "messages_processed": 0,
        "failed_jobs": 0,
        "last_sync_timestamp": 0,
    },
}

# Fix Python true/false literals in dict definition
DEFAULT_CONFIG["theme"]["enabled"] = True
DEFAULT_CONFIG["theme"]["apply_to_webviews"] = True
DEFAULT_CONFIG["theme"]["pure_black_reviewer"] = True


def _deep_merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge source dictionary into target without modifying keys missing in source."""
    result = copy.deepcopy(target)
    for key, value in source.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


class ConfigManager:
    """
    Manages add-on configuration with schema healing and reactive events.
    """
    def __init__(self) -> None:
        self._config: Dict[str, Any] = copy.deepcopy(DEFAULT_CONFIG)
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}
        self.load_config()

    def _get_local_config_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, DEFAULT_CONFIG_FILENAME)

    def _get_addon_package_name(self) -> str:
        """Dynamically resolve the installed addon folder name."""
        try:
            parts = __name__.split(".")
            if parts and parts[0] and parts[0] != "core":
                return parts[0]
            if mw and hasattr(mw, "addonManager") and mw.addonManager:
                # Try to get folder from module or fallback to constants
                mod = getattr(mw.addonManager, "addonFromModule", lambda m: "")(__name__)
                if mod:
                    return str(mod)
        except Exception:
            pass
        return "anki_wykiati_toolkit"

    def load_config(self) -> None:
        """Load configuration from Anki AddonManager or fallback to config.json."""
        loaded_data: Optional[Dict[str, Any]] = None

        if mw and hasattr(mw, "addonManager") and mw.addonManager:
            try:
                pkg = self._get_addon_package_name()
                anki_config = mw.addonManager.getConfig(pkg)
                if isinstance(anki_config, dict) and anki_config:
                    loaded_data = anki_config
                    logger.info(f"[ConfigManager] Loaded configuration from Anki AddonManager for '{pkg}'.")
            except Exception as e:
                logger.debug(f"[ConfigManager] Notice on read from Anki AddonManager: {e}")

        if loaded_data is None:
            config_path = self._get_local_config_path()
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)
                        if isinstance(raw_data, dict):
                            loaded_data = raw_data
                            logger.info(f"[ConfigManager] Loaded local config from '{config_path}'.")
                except Exception as e:
                    logger.error(f"[ConfigManager] Corrupted config file detected ({e}). Recovering with defaults.")

        if loaded_data:
            # Merge loaded data on top of defaults to guarantee all schema fields exist
            self._config = _deep_merge(DEFAULT_CONFIG, loaded_data)
        else:
            self._config = copy.deepcopy(DEFAULT_CONFIG)
            self.save_config()

        # Update logger level
        log_level = self.get("log_level", "INFO")
        logger.set_level(log_level)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value using dot-notation (e.g. 'theme.background').
        """
        keys = key.split(".")
        curr = self._config
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return default
        return curr

    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Set config value using dot-notation and notify subscribers.
        """
        keys = key.split(".")
        curr = self._config
        for k in keys[:-1]:
            curr = curr.setdefault(k, {})

        old_val = curr.get(keys[-1])
        curr[keys[-1]] = value

        if save:
            self.save_config()

        # Notify subscribers
        if old_val != value:
            if key in self._subscribers:
                for callback in self._subscribers[key]:
                    try:
                        callback(value)
                    except Exception as e:
                        logger.error(f"[ConfigManager] Callback error on '{key}': {e}")

            # Also check if root key changed (e.g. 'theme' when setting 'theme.enabled')
            root_key = keys[0]
            if root_key != key and root_key in self._subscribers:
                for callback in self._subscribers[root_key]:
                    try:
                        callback(self._config.get(root_key))
                    except Exception as e:
                        logger.error(f"[ConfigManager] Root callback error on '{root_key}': {e}")

    def save_config(self) -> None:
        """Persist current configuration to Anki AddonManager and config.json."""
        if mw and hasattr(mw, "addonManager") and mw.addonManager:
            try:
                pkg = self._get_addon_package_name()
                mw.addonManager.writeConfig(pkg, self._config)
                logger.debug(f"[ConfigManager] Configuration persisted via Anki AddonManager for '{pkg}'.")
            except Exception as e:
                logger.debug(f"[ConfigManager] Anki writeConfig notice: {e}")

        # Always save locally as safe fallback
        config_path = self._get_local_config_path()
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)
            logger.debug(f"[ConfigManager] Configuration written to '{config_path}'.")
        except Exception as e:
            logger.error(f"[ConfigManager] Failed saving configuration to disk: {e}")

    def subscribe(self, key: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to config changes for a specific key."""
        if key not in self._subscribers:
            self._subscribers[key] = []
        if callback not in self._subscribers[key]:
            self._subscribers[key].append(callback)

    def unsubscribe(self, key: str, callback: Callable[[Any], None]) -> None:
        """Unsubscribe a callback."""
        if key in self._subscribers and callback in self._subscribers[key]:
            self._subscribers[key].remove(callback)

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = copy.deepcopy(DEFAULT_CONFIG)
        self.save_config()
        logger.info("[ConfigManager] Reset configuration to default schema.")

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of the entire configuration dictionary."""
        return copy.deepcopy(self._config)


# Global singleton instance
config = ConfigManager()
