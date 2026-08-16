"""
Structured, Production-Ready Logger for Anki Discord Toolkit.
Provides rotating file logs, exception telemetry, and runtime diagnostic inspection.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import traceback
from typing import List, Optional

from .constants import ADDON_NAME, ADDON_SHORT_NAME, LOG_FILENAME


class ToolkitLogger:
    """
    Standardized logger supporting console, rotating file output, and runtime inspection.
    """
    def __init__(self, name: str = ADDON_SHORT_NAME):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self._initialized = False
        self._log_path: Optional[str] = None
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

        # 2. Rotating File Handler (Max 2MB per file, 3 backups)
        try:
            log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._log_path = os.path.join(log_dir, LOG_FILENAME)
            file_handler = RotatingFileHandler(
                self._log_path,
                maxBytes=2 * 1024 * 1024,
                backupCount=3,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception:
            # Fallback if directory is write-restricted
            pass

        self._initialized = True

    def get_log_filepath(self) -> Optional[str]:
        """Return the absolute path to the active log file."""
        return self._log_path

    def read_recent_logs(self, max_lines: int = 50) -> List[str]:
        """Read and return the latest log entries for runtime diagnostics."""
        if not self._log_path or not os.path.exists(self._log_path):
            return []
        try:
            with open(self._log_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                return [line.rstrip() for line in lines[-max_lines:]]
        except Exception:
            return []

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

    def log_exception(self, exc: Exception, context: str = "") -> None:
        """Record a structured exception with full traceback details."""
        ctx_prefix = f"[{context}] " if context else ""
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(f"{ctx_prefix}{exc}\n{tb}")


# Global singleton instance
logger = ToolkitLogger()

