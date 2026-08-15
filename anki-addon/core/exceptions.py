"""
Domain Exceptions for Anki Discord Toolkit.
"""


class DiscordToolkitError(Exception):
    """Base exception for all Anki Discord Toolkit errors."""

    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class ConfigurationError(DiscordToolkitError):
    """Raised when configuration is invalid, corrupted, or missing required fields."""
    pass


class ParserError(DiscordToolkitError):
    """Raised when parsing a message fails (e.g. missing required fields, syntax error)."""
    pass


class ValidationError(DiscordToolkitError):
    """Raised when a card payload fails schema or content validation."""
    pass


class SecurityError(DiscordToolkitError):
    """Raised when an unauthorized user, channel, or malicious payload is rejected."""
    pass


class RateLimitExceededError(SecurityError):
    """Raised when request rate exceeds allowed threshold."""
    pass


class RoutingError(DiscordToolkitError):
    """Raised when resolving a target deck fails."""
    pass


class AnkiAdapterError(DiscordToolkitError):
    """Raised when interacting with Anki's Collection/Notes/Decks fails."""
    pass


class DuplicateCardError(AnkiAdapterError):
    """Raised when a card is recognized as duplicate and policy is set to reject."""
    pass


class SyncQueueError(DiscordToolkitError):
    """Raised when adding or processing a queue job fails."""
    pass


class ThemeEngineError(DiscordToolkitError):
    """Raised when applying or restoring visual themes fails."""
    pass
