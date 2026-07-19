"""PyInstaller entry point for the daemon sidecar.

The desktop app (Tauri) spawns this binary on launch and kills it on quit.
It runs ONLY the web gateway — the GUI's backend — on localhost.

  mindpalaced [--port N]
"""
import sys

# top-level imports so PyInstaller's static analysis bundles the whole graph
# (the package uses lazy in-function imports everywhere else)
from mindpalace.gateways import web
from mindpalace.projects import store, worker      # noqa: F401
from mindpalace import providers                   # noqa: F401


def _watch_parent():
    """Exit when the Tauri shell dies — force-quit and crashes included. An
    orphaned daemon keeps port 7777 and serves a STALE build to the next app
    launch (the shell reuses a busy port), which is worse than no daemon."""
    import os
    import threading
    import time

    parent = os.getppid()

    def loop():
        while True:
            if os.getppid() != parent:      # reparented to init/launchd = parent died
                os._exit(0)
            time.sleep(2)

    threading.Thread(target=loop, daemon=True).start()


def main():
    port = None
    args = sys.argv[1:]
    if "--port" in args:
        i = args.index("--port")
        if i + 1 < len(args) and args[i + 1].isdigit():
            port = int(args[i + 1])
    _watch_parent()
    web.run(port=port, open_browser=False)   # the Tauri window IS the browser


if __name__ == "__main__":
    main()
