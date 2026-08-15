"""
Test Suite for Anki Discord Toolkit.
Configures python path for standalone test discovery.
"""

import os
import sys

# Ensure addon root is in sys.path
addon_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_root not in sys.path:
    sys.path.insert(0, addon_root)
