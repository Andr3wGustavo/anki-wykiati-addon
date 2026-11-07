"""
Filesystem locations for runtime data.

Anki replaces the whole add-on folder on update, except for the `user_files`
sub-folder. Anything that must survive updates (sync state, dedup registry,
job queue, staged media) lives there.
"""

import os
import shutil


def addon_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def user_files_dir(*parts: str) -> str:
    """Return (and create) a directory inside `user_files`."""
    path = os.path.join(addon_root(), "user_files", *parts)
    os.makedirs(path, exist_ok=True)
    return path


def user_file(name: str, legacy_name: str = "") -> str:
    """
    Path of a persistent data file in `user_files`. If it does not exist yet but a
    legacy copy exists in the old `data/` folder, it is migrated once.
    """
    target = os.path.join(user_files_dir(), name)
    if not os.path.exists(target):
        legacy = os.path.join(addon_root(), "data", legacy_name or name)
        if os.path.exists(legacy):
            try:
                shutil.copy2(legacy, target)
            except OSError:
                pass
    return target
