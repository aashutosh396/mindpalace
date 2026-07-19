"""Folder scanning — a project is a FOLDER, not just one git repo.

Attaching a folder tracks the folder itself as the project root (the agent's
working directory) and auto-discovers every git repo nested inside it, so a
workspace like  myproject/{frontend,backend,infra}  is fully tracked from one
attach.
"""
from __future__ import annotations

import os
from pathlib import Path

_SKIP = {"node_modules", ".venv", "venv", ".git", "__pycache__", ".next", ".nuxt",
         "dist", "build", ".output", "target", ".cache", "Library", ".Trash",
         "vendor", ".tox", ".mypy_cache", "site-packages"}

MAX_REPOS = 20


def discover_repos(root: str, max_depth: int = 3) -> list[str]:
    """Git repos inside `root` (including root itself), nearest-first, capped."""
    rootp = Path(root).expanduser().resolve()
    if not rootp.is_dir():
        return []
    found: list[str] = []
    base_depth = len(rootp.parts)

    for dirpath, dirnames, _ in os.walk(rootp):
        depth = len(Path(dirpath).parts) - base_depth
        if depth > max_depth:
            dirnames[:] = []
            continue
        if ".git" in dirnames or (Path(dirpath) / ".git").is_file():   # worktrees too
            found.append(dirpath)
            dirnames[:] = []            # don't descend into a repo for nested ones
            continue
        dirnames[:] = [d for d in dirnames if d not in _SKIP and not d.startswith(".")]
        if len(found) >= MAX_REPOS:
            break
    return found[:MAX_REPOS]
