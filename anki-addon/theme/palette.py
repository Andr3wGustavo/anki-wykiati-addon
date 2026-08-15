"""
Centralized Color Tokens and iOS Liquid Glass Theme Palette.
Provides translucent glassmorphism layers, neon accents, and AMOLED black backdrop.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ThemePalette:
    """Immutable color palette definitions for iOS Liquid Glass styling."""
    # Backgrounds & Glass Backdrops
    BACKGROUND_PURE_BLACK: str = "#000000"
    BACKGROUND_SURFACE: str = "rgba(18, 20, 26, 0.75)"
    BACKGROUND_SURFACE_ELEVATED: str = "rgba(28, 32, 42, 0.78)"
    BACKGROUND_SURFACE_HOVER: str = "rgba(255, 255, 255, 0.12)"
    BACKGROUND_SURFACE_ACTIVE: str = "rgba(255, 255, 255, 0.20)"

    # Glass Borders & Highlights
    BORDER_SUBTLE: str = "rgba(255, 255, 255, 0.08)"
    BORDER_DEFAULT: str = "rgba(255, 255, 255, 0.14)"
    BORDER_STRONG: str = "rgba(255, 255, 255, 0.28)"
    BORDER_FOCUS: str = "#0A84FF"

    # Typography
    TEXT_PRIMARY: str = "#FFFFFF"
    TEXT_SECONDARY: str = "#EBEBF5"
    TEXT_MUTED: str = "rgba(235, 235, 245, 0.6)"
    TEXT_DISABLED: str = "rgba(235, 235, 245, 0.3)"
    TEXT_INVERSE: str = "#000000"

    # iOS Vibrant Accents
    ACCENT_PRIMARY: str = "#0A84FF"       # Apple iOS Blue
    ACCENT_HOVER: str = "#409CFF"
    ACCENT_ACTIVE: str = "#0066CC"
    ACCENT_SUBTLE: str = "rgba(10, 132, 255, 0.18)"

    # Semantic Status Colors
    SUCCESS: str = "#30D158"              # iOS Green
    SUCCESS_SUBTLE: str = "rgba(48, 209, 88, 0.18)"
    WARNING: str = "#FF9F0A"              # iOS Orange
    WARNING_SUBTLE: str = "rgba(255, 159, 10, 0.18)"
    ERROR: str = "#FF453A"                # iOS Red
    ERROR_SUBTLE: str = "rgba(255, 69, 58, 0.18)"
    INFO: str = "#64D2FF"                 # iOS Cyan

    # Reviewer Card Cloze
    CLOZE_COLOR: str = "#5E5CE6"          # iOS Indigo

    def to_dict(self) -> Dict[str, str]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


# Default palette instance
PALETTE = ThemePalette()
