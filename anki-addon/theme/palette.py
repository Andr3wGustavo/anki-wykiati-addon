"""
Centralized Color Tokens and Theme Palette for Pure Black OLED / AMOLED Theme.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ThemePalette:
    """Immutable color palette definitions."""
    # Backgrounds
    BACKGROUND_PURE_BLACK: str = "#000000"
    BACKGROUND_SURFACE: str = "#0C0D0E"
    BACKGROUND_SURFACE_ELEVATED: str = "#141618"
    BACKGROUND_SURFACE_HOVER: str = "#1C1F22"
    BACKGROUND_SURFACE_ACTIVE: str = "#24282D"

    # Borders & Dividers
    BORDER_SUBTLE: str = "#1E2226"
    BORDER_DEFAULT: str = "#2A2E34"
    BORDER_STRONG: str = "#3A4048"
    BORDER_FOCUS: str = "#3B82F6"

    # Text & Foreground
    TEXT_PRIMARY: str = "#FFFFFF"
    TEXT_SECONDARY: str = "#A0AAB4"
    TEXT_MUTED: str = "#6B7280"
    TEXT_DISABLED: str = "#4B5563"
    TEXT_INVERSE: str = "#000000"

    # Accent & Branding
    ACCENT_PRIMARY: str = "#3B82F6"       # Vivid Blue
    ACCENT_HOVER: str = "#2563EB"
    ACCENT_ACTIVE: str = "#1D4ED8"
    ACCENT_SUBTLE: str = "rgba(59, 130, 246, 0.15)"

    # Semantic Status Colors
    SUCCESS: str = "#10B981"
    SUCCESS_SUBTLE: str = "rgba(16, 185, 129, 0.15)"
    WARNING: str = "#F59E0B"
    WARNING_SUBTLE: str = "rgba(245, 158, 11, 0.15)"
    ERROR: str = "#EF4444"
    ERROR_SUBTLE: str = "rgba(239, 68, 68, 0.15)"
    INFO: str = "#06B6D4"

    # Reviewer Card Cloze
    CLOZE_COLOR: str = "#60A5FA"

    def to_dict(self) -> Dict[str, str]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


# Default palette instance
PALETTE = ThemePalette()
