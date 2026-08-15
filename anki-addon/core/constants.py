"""
Application Constants and Protocol Definitions for Anki Discord Toolkit.
"""

# Add-on Identification
ADDON_NAME = "Anki Discord Toolkit"
ADDON_SHORT_NAME = "ADT"
ADDON_PACKAGE = "anki-discord-toolkit"
ADDON_VERSION = "1.0.0"
ADDON_AUTHOR = "Antigravity Engineering"

# Filenames and Paths
DEFAULT_CONFIG_FILENAME = "config.json"
LOG_FILENAME = "anki_discord_toolkit.log"
PROCESSED_MESSAGES_FILENAME = "processed_messages.json"
QUEUE_DATA_FILENAME = "queue.json"

# Menu & UI
MAIN_MENU_TITLE = "Anki Discord Toolkit"
TOOLS_MENU_ENTRY = "&Anki Discord Toolkit"

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

# Theme Colors (Pure Black OLED / AMOLED Palette)
COLOR_PURE_BLACK = "#000000"
COLOR_SURFACE_DARK = "#0C0D0E"
COLOR_SURFACE_SECONDARY = "#16181A"
COLOR_SURFACE_TERTIARY = "#212427"
COLOR_BORDER = "#2A2E33"
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "#A0AAB4"
COLOR_TEXT_MUTED = "#6B7280"
COLOR_ACCENT_PRIMARY = "#3B82F6"      # Modern Vibrant Blue
COLOR_ACCENT_HOVER = "#2563EB"
COLOR_ACCENT_ACTIVE = "#1D4ED8"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_ERROR = "#EF4444"

# Default Network & Bridge Ports
DEFAULT_HTTP_BRIDGE_PORT = 8765
DEFAULT_HTTP_BRIDGE_HOST = "127.0.0.1"
DEFAULT_POLLING_INTERVAL_SECONDS = 5
MAX_PAYLOAD_SIZE_BYTES = 100 * 1024  # 100 KB
MAX_MESSAGE_CHARACTERS = 4000
