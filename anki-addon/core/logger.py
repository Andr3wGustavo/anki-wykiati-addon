"""
Structured, Production-Ready Logger for Anki Discord Toolkit.
"""

import logging
import os
import sys
from typing import Optional

from .constants import ADDON_NAME, ADDON_SHORT_NAME, LOG_FILENAME


class ToolkitLogger:
    """
    Standardized logger supporting console and rotating file output.
    """
    def __init__(self, name: str = ADDON_SHORT_NAME):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self._initialized = False
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        if self._initialized:
            return

        formatter = logging.Formatter(
            fmt="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 1. Console Stream Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 2. File Handler
        try:
            log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_path = os.path.join(log_dir, LOG_FILENAME)
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception:
            # Fallback if directory is write-restricted
            pass

        self._initialized = True

    def set_level(self, level: str) -> None:
        """Dynamically set logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')."""
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(numeric_level)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self.logger.exception(msg, *args, **kwargs)


# Global singleton instance
logger = ToolkitLogger()
