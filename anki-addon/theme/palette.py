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

def is_light_color(hex_code: str) -> bool:
    """
    Computes WCAG relative luminance / perceived brightness of a hex color.
    Returns True if the background is light (requiring dark text/borders), False if dark.
    """
    try:
        clean = hex_code.strip().lstrip("#")
        if len(clean) == 3:
            clean = "".join([c * 2 for c in clean])
        if len(clean) != 6:
            return False
        r = int(clean[0:2], 16)
        g = int(clean[2:4], 16)
        b = int(clean[4:6], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000.0
        return brightness >= 135.0
    except Exception:
        return False


def get_adaptive_palette(bg_hex: str) -> ThemePalette:
    """
    Return a ThemePalette tailored specifically for the chosen background luminance.
    If the background is light, text and borders automatically adapt to dark tones.
    """
    if is_light_color(bg_hex):
        return ThemePalette(
            BACKGROUND_PURE_BLACK=bg_hex,
            BACKGROUND_SURFACE="rgba(0, 0, 0, 0.04)",
            BACKGROUND_SURFACE_ELEVATED="rgba(0, 0, 0, 0.08)",
            BACKGROUND_SURFACE_HOVER="rgba(0, 0, 0, 0.12)",
            BACKGROUND_SURFACE_ACTIVE="rgba(0, 0, 0, 0.18)",
            BORDER_SUBTLE="rgba(0, 0, 0, 0.10)",
            BORDER_DEFAULT="rgba(0, 0, 0, 0.15)",
            BORDER_STRONG="rgba(0, 0, 0, 0.25)",
            BORDER_FOCUS="rgba(0, 0, 0, 0.50)",
            TEXT_PRIMARY="#09090B",
            TEXT_SECONDARY="#3F3F46",
            TEXT_MUTED="#71717A",
            TEXT_DISABLED="rgba(0, 0, 0, 0.30)",
            TEXT_INVERSE="#FFFFFF",
            ACCENT_PRIMARY="#09090B",
            ACCENT_HOVER="#27272A",
            ACCENT_ACTIVE="#3F3F46",
            ACCENT_SUBTLE="rgba(0, 0, 0, 0.08)",
        )
    return ThemePalette(
        BACKGROUND_PURE_BLACK=bg_hex,
        BACKGROUND_SURFACE="rgba(255, 255, 255, 0.03)",
        BACKGROUND_SURFACE_ELEVATED="rgba(255, 255, 255, 0.06)",
        BACKGROUND_SURFACE_HOVER="rgba(255, 255, 255, 0.10)",
        BACKGROUND_SURFACE_ACTIVE="rgba(255, 255, 255, 0.16)",
        BORDER_SUBTLE="rgba(255, 255, 255, 0.08)",
        BORDER_DEFAULT="rgba(255, 255, 255, 0.12)",
        BORDER_STRONG="rgba(255, 255, 255, 0.22)",
        BORDER_FOCUS="rgba(255, 255, 255, 0.45)",
        TEXT_PRIMARY="#FFFFFF",
        TEXT_SECONDARY="#E4E4E7",
        TEXT_MUTED="#A1A1AA",
        TEXT_DISABLED="rgba(255, 255, 255, 0.20)",
        TEXT_INVERSE="#000000",
        ACCENT_PRIMARY="#FFFFFF",
        ACCENT_HOVER="#E4E4E7",
        ACCENT_ACTIVE="#D4D4D8",
        ACCENT_SUBTLE="rgba(255, 255, 255, 0.08)",
    )


# Default palette instance
PALETTE = ThemePalette()

