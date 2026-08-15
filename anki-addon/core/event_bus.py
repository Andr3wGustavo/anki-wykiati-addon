"""
Thread-safe Publish/Subscribe Event Bus for decoupled internal communication.
"""

import threading
from typing import Any, Callable, Dict, List

from .logger import logger


class EventBus:
    """
    Publish-Subscribe broker for cross-module events.
    """
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[..., None]]] = {}
        self._lock = threading.RLock()

    def subscribe(self, event_name: str, handler: Callable[..., None]) -> None:
        """Register a handler for a specific event."""
        with self._lock:
            if event_name not in self._subscribers:
                self._subscribers[event_name] = []
            if handler not in self._subscribers[event_name]:
                self._subscribers[event_name].append(handler)
                logger.debug(f"[EventBus] Subscribed {getattr(handler, '__name__', str(handler))} to '{event_name}'")

    def unsubscribe(self, event_name: str, handler: Callable[..., None]) -> None:
        """Remove a previously registered handler."""
        with self._lock:
            if event_name in self._subscribers and handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                logger.debug(f"[EventBus] Unsubscribed {getattr(handler, '__name__', str(handler))} from '{event_name}'")

    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """Dispatch event synchronously to all registered listeners."""
        with self._lock:
            listeners = list(self._subscribers.get(event_name, []))

        if not listeners:
            return

        logger.debug(f"[EventBus] Publishing '{event_name}' to {len(listeners)} listener(s)")
        for listener in listeners:
            try:
                listener(*args, **kwargs)
            except Exception as e:
                logger.error(f"[EventBus] Error in listener '{getattr(listener, '__name__', str(listener))}' for '{event_name}': {e}", exc_info=True)

    def clear(self) -> None:
        """Clear all event subscribers."""
        with self._lock:
            self._subscribers.clear()


# Global event bus singleton
event_bus = EventBus()
