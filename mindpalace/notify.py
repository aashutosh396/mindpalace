"""Shim so `python3 -m mindpalace.notify 'msg'` works (delegates to core.notify).

The system prompt documents this short path; the implementation lives in core.notify.
"""
from .core.notify import main

if __name__ == "__main__":
    main()
