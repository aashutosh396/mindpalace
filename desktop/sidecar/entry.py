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


def main():
    port = None
    args = sys.argv[1:]
    if "--port" in args:
        i = args.index("--port")
        if i + 1 < len(args) and args[i + 1].isdigit():
            port = int(args[i + 1])
    web.run(port=port, open_browser=False)   # the Tauri window IS the browser


if __name__ == "__main__":
    main()
