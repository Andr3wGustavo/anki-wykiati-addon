"""
Core Interfaces and Abstract Base Classes (ABCs) to enforce SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class IService(ABC):
    """
    Interface for all modular services/plugins registered in the addon.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier name for the service."""
        pass

    @abstractmethod
    def initialize(self) -> None:
        """Initialize resources, event subscriptions, and dependencies."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Clean up resources upon addon teardown."""
        pass


class IConfigManager(ABC):
    """
    Interface for reactive Configuration Management.
    """
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration option using dot-notation (e.g. 'features.auto_sync')."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set a configuration option and notify subscribers."""
        pass

    @abstractmethod
    def subscribe(self, key: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to changes of a specific configuration key."""
        pass


class IEventBus(ABC):
    """
    Interface for internal Pub/Sub Event System.
    """
    @abstractmethod
    def publish(self, event_name: str, **payload: Any) -> None:
        """Broadcast an event with keyword payload to all listeners."""
        pass

    @abstractmethod
    def subscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        """Subscribe a callback listener to a specific event."""
        pass

    @abstractmethod
    def unsubscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        """Unsubscribe a callback listener from an event."""
        pass
