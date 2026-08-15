"""
Packaging Script for Anki Discord Toolkit.
Packages the addon into a clean, distributable .ankiaddon (ZIP) file,
excluding cache, tests, git artifacts, and temporary runtime data.
"""

import os
import shutil
import sys
import zipfile

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADDON_SOURCE_DIR = os.path.join(BASE_DIR, "anki-addon")
RELEASE_DIR = os.path.join(BASE_DIR, "release")
OUTPUT_ZIP = os.path.join(RELEASE_DIR, "anki-discord-toolkit.ankiaddon")

EXCLUDED_NAMES = {
    "__pycache__",
    ".pytest_cache",
    "tests",
    "data",
    ".git",
    ".gitignore",
    ".gitkeep",
    "anki_addon.log",
    "anki_discord_toolkit.log",
}

EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
}


def package_addon() -> None:
    os.makedirs(RELEASE_DIR, exist_ok=True)
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    print(f"[*] Packaging '{ADDON_SOURCE_DIR}' into '{OUTPUT_ZIP}'...")

    total_files = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ADDON_SOURCE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_NAMES and not d.startswith(".")]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if file in EXCLUDED_NAMES or ext in EXCLUDED_EXTENSIONS or file.endswith(".log"):
                    continue

                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, ADDON_SOURCE_DIR)

                zf.write(abs_file_path, rel_path)
                total_files += 1
                print(f"  + Added: {rel_path}")

    # Also create a standard .zip for manual extraction
    zip_copy = os.path.join(RELEASE_DIR, "anki-discord-toolkit.zip")
    shutil.copyfile(OUTPUT_ZIP, zip_copy)

    print(f"[OK] Package built successfully! ({total_files} files packaged)")
    print(f"   * Anki Package: {OUTPUT_ZIP}")
    print(f"   * Standard ZIP: {zip_copy}")


if __name__ == "__main__":
    package_addon()
