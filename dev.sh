#!/usr/bin/env bash
# mindpalace v3 dev loop — browser + hot reload, no compiling.
#
#   ./dev.sh          → backend on :7777 (auto-reloads on python edits)
#                       + Nuxt dev on :3000 (instant HMR on UI edits)
#
# Work at  http://localhost:3000  — UI changes appear on save, python changes
# restart the backend automatically. Quit the desktop app first (it also uses
# :7777). Ship later with:  ./desktop/publish-rolling.sh  (dmg) or CI (all OS).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! [ -x "$HERE/.venv-dev/bin/mindpalace" ]; then
  echo "setting up dev venv…"
  python3 -m venv "$HERE/.venv-dev"
  "$HERE/.venv-dev/bin/pip" -q install -e "$HERE[web]" 'uvicorn[standard]' watchfiles
fi

cleanup() { kill 0 2>/dev/null; }
trap cleanup EXIT

"$HERE/.venv-dev/bin/mindpalace" serve --port 7777 --no-open --dev &
cd "$HERE/web" && npm run dev
