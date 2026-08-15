"""
Application Constants and Protocol Definitions for Anki Wykiati Toolkit.
"""

# Add-on Identification
ADDON_NAME = "Anki Wykiati Toolkit"
ADDON_SHORT_NAME = "AWT"
ADDON_PACKAGE = "anki-wykiati-toolkit"
ADDON_VERSION = "1.1.0"
ADDON_AUTHOR = "Wykiati Engineering"

# Filenames and Paths
DEFAULT_CONFIG_FILENAME = "config.json"
LOG_FILENAME = "anki_wykiati_toolkit.log"
PROCESSED_MESSAGES_FILENAME = "processed_messages.json"
QUEUE_DATA_FILENAME = "queue.json"

# Menu & UI
MAIN_MENU_TITLE = "Anki Wykiati Toolkit"
TOOLS_MENU_ENTRY = "&Anki Wykiati Toolkit"

# Discord Protocol Constants
DISCORD_COMMAND_PREFIX = "!anki"
DISCORD_COMMAND_HELP = "!anki-help"
DISCORD_COMMAND_STATUS = "!anki-status"
DISCORD_COMMAND_DECKS = "!anki-decks"
DISCORD_COMMAND_PING = "!anki-ping"

# Discord Protocol Field Keys
FIELD_FRONT = "front"
FIELD_BACK = "back"
FIELD_DECK = "deck"
FIELD_TAGS = "tags"
FIELD_TYPE = "type"
FIELD_NOTE_TYPE = "note_type"
FIELD_TEMPLATE = "template"
FIELD_EXTRA = "extra"
FIELD_CLOZE = "cloze"

# Supported Note Types
SUPPORTED_TEMPLATES = [
    "Basic",
    "Basic (and reversed card)",
    "Basic (optional reversed card)",
    "Cloze",
]

# Theme Colors (Pure Black OLED / AMOLED & Liquid Glass Palette)
COLOR_PURE_BLACK = "#000000"
COLOR_SURFACE_DARK = "rgba(18, 21, 28, 0.75)"
COLOR_SURFACE_SECONDARY = "rgba(28, 33, 44, 0.78)"
COLOR_SURFACE_TERTIARY = "rgba(36, 42, 54, 0.8)"
COLOR_BORDER = "rgba(255, 255, 255, 0.14)"
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "#EBEBF5"
COLOR_TEXT_MUTED = "rgba(235, 235, 245, 0.55)"
COLOR_ACCENT_PRIMARY = "#0A84FF"      # Apple iOS Blue
COLOR_ACCENT_HOVER = "#409CFF"
COLOR_ACCENT_ACTIVE = "#0066CC"
COLOR_SUCCESS = "#30D158"
COLOR_WARNING = "#FF9F0A"
COLOR_ERROR = "#FF453A"

# Default Network & Bridge Ports
DEFAULT_HTTP_BRIDGE_PORT = 8765
DEFAULT_HTTP_BRIDGE_HOST = "127.0.0.1"
DEFAULT_POLLING_INTERVAL_SECONDS = 5
MAX_PAYLOAD_SIZE_BYTES = 100 * 1024  # 100 KB
MAX_MESSAGE_CHARACTERS = 4000
