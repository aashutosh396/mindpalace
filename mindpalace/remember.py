"""
Remember — save a durable fact LIVE, the moment you learn it (Hermes-style).

  python3 -m mindpalace.remember user "Prefers to be called Aashu; runs RepairMate."
      → appends to USER.md   (your profile of the owner)
  python3 -m mindpalace.remember "Backups run nightly at 2am to the Hostinger box."
      → appends to MEMORY.md  (durable general facts/conventions/gotchas)

Use this in-conversation so profiling/memory happens visibly (the owner sees a chip) and you
never re-ask what you've already been told. Save only durable, reusable facts — skip session noise.
"""
from __future__ import annotations

import sys
import time

from . import config

_PROFILE_FLAGS = {"user", "--user", "-u", "+user"}


def _append(path, fact: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(f"- {time.strftime('%Y-%m-%d')}: {fact.strip()}\n")


def remember(fact: str, profile: bool = False) -> str:
    fact = (fact or "").strip()
    if not fact:
        return "(nothing to remember)"
    _append(config.USER_FILE() if profile else config.MEMORY_FILE(), fact)
    return f"saved to {'USER.md (profile)' if profile else 'MEMORY.md'}"


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    profile = bool(argv) and argv[0] in _PROFILE_FLAGS
    if profile:
        argv = argv[1:]
    print(remember(" ".join(argv), profile))


if __name__ == "__main__":
    main()
