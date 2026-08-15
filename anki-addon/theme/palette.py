"""
Ultra-Minimalist Monochromatic Dark Palette for Anki Wykiati Toolkit.
Linear/Vercel-inspired Deep Void Black (#000000), whisper-thin glass borders, and high-contrast typography.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ThemePalette:
    """Immutable color tokens for ultra-dark minimalist glassmorphism."""
    # Absolute Void Backgrounds
    BACKGROUND_PURE_BLACK: str = "#000000"
    BACKGROUND_SURFACE: str = "rgba(255, 255, 255, 0.03)"
    BACKGROUND_SURFACE_ELEVATED: str = "rgba(255, 255, 255, 0.06)"
    BACKGROUND_SURFACE_HOVER: str = "rgba(255, 255, 255, 0.10)"
    BACKGROUND_SURFACE_ACTIVE: str = "rgba(255, 255, 255, 0.16)"

    # Whisper-Thin Glass Borders
    BORDER_SUBTLE: str = "rgba(255, 255, 255, 0.06)"
    BORDER_DEFAULT: str = "rgba(255, 255, 255, 0.10)"
    BORDER_STRONG: str = "rgba(255, 255, 255, 0.20)"
    BORDER_FOCUS: str = "rgba(255, 255, 255, 0.40)"

    # Monochromatic Typography
    TEXT_PRIMARY: str = "#FFFFFF"
    TEXT_SECONDARY: str = "#A1A1AA"
    TEXT_MUTED: str = "#71717A"
    TEXT_DISABLED: str = "rgba(255, 255, 255, 0.20)"
    TEXT_INVERSE: str = "#000000"

    # Minimalist Clean Accents
    ACCENT_PRIMARY: str = "#FFFFFF"       # Clean Monochromatic White
    ACCENT_HOVER: str = "#E4E4E7"
    ACCENT_ACTIVE: str = "#D4D4D8"
    ACCENT_SUBTLE: str = "rgba(255, 255, 255, 0.08)"

    # Status / Indicators (Subtle & De-saturated)
    SUCCESS: str = "#4ADE80"              # Muted Mint
    SUCCESS_SUBTLE: str = "rgba(74, 222, 128, 0.12)"
    WARNING: str = "#FBBF24"              # Muted Amber
    WARNING_SUBTLE: str = "rgba(251, 191, 36, 0.12)"
    ERROR: str = "#F87171"                # Muted Rose
    ERROR_SUBTLE: str = "rgba(248, 113, 113, 0.12)"
    INFO: str = "#38BDF8"                 # Slate Ice Blue

    # Reviewer Card Cloze
    CLOZE_COLOR: str = "#38BDF8"

    def to_dict(self) -> Dict[str, str]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


# Default palette instance
PALETTE = ThemePalette()
