"""
Thread Dispatcher and Background Operations for Anki.
Guarantees UI responsiveness and thread safety when manipulating Collection or Qt widgets.
"""

import threading
from typing import Any, Callable, Optional

try:
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.logger import logger

try:
    from aqt import mw
    from aqt.operations import QueryOp
    from aqt.qt import QTimer
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    QueryOp = None
    QTimer = None
    ANKI_AVAILABLE = False


def run_on_main_thread(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    """
    Ensure the callable executes on Qt / Anki's main GUI thread.
    """
    if not ANKI_AVAILABLE or mw is None:
        fn(*args, **kwargs)
        return

    try:
        if hasattr(mw, "taskman") and hasattr(mw.taskman, "run_on_main"):
            mw.taskman.run_on_main(lambda: fn(*args, **kwargs))
        elif QTimer:
            QTimer.singleShot(0, lambda: fn(*args, **kwargs))
        else:
            fn(*args, **kwargs)
    except Exception as e:
        logger.error(f"[Operations] Error dispatching to main thread: {e}")
        fn(*args, **kwargs)


def run_in_background(
    task_fn: Callable[[], Any],
    on_success: Optional[Callable[[Any], None]] = None,
    on_failure: Optional[Callable[[Exception], None]] = None,
) -> None:
    """
    Run long-running tasks in a background worker thread and return result to main thread.
    """
    def _runner():
        try:
            result = task_fn()
            if on_success:
                run_on_main_thread(on_success, result)
        except Exception as e:
            logger.error(f"[Operations] Background task failed: {e}", exc_info=True)
            if on_failure:
                run_on_main_thread(on_failure, e)

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
