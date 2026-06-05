"""Resolve MINDPALACE_HOME for standalone skill scripts.

Skill scripts may run outside the mindpalace process (e.g. system Python,
nix env, CI) where ``mindpalace_constants`` is not importable.  This module
provides the same ``get_mindpalace_home()`` and ``display_mindpalace_home()``
contracts as ``mindpalace_constants`` without requiring it on ``sys.path``.

When ``mindpalace_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``mindpalace_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``MINDPALACE_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from mindpalace_constants import display_mindpalace_home as display_mindpalace_home
    from mindpalace_constants import get_mindpalace_home as get_mindpalace_home
except (ModuleNotFoundError, ImportError):

    def get_mindpalace_home() -> Path:
        """Return the mindpalace home directory (default: ~/.mindpalace).

        Mirrors ``mindpalace_constants.get_mindpalace_home()``."""
        val = os.environ.get("MINDPALACE_HOME", "").strip()
        return Path(val) if val else Path.home() / ".mindpalace"

    def display_mindpalace_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``mindpalace_constants.display_mindpalace_home()``."""
        home = get_mindpalace_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
