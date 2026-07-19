#!/usr/bin/env bash
# Build the daemon sidecar binary (mindpalaced) with PyInstaller.
#
#   ./build.sh [python-with-pyinstaller]
#
# Output: desktop/sidecar/dist/mindpalaced-<target-triple>
# The target-triple suffix is what Tauri's externalBin expects.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PY="${1:-python3}"

# target triple for Tauri sidecar naming (mac arm/intel, linux, windows via CI)
TRIPLE=$("$PY" - <<'EOF'
import platform
m, s = platform.machine().lower(), platform.system()
arch = {"arm64": "aarch64", "aarch64": "aarch64", "x86_64": "x86_64", "amd64": "x86_64"}.get(m, m)
osname = {"Darwin": "apple-darwin", "Linux": "unknown-linux-gnu", "Windows": "pc-windows-msvc"}[s]
print(f"{arch}-{osname}")
EOF
)

echo "building mindpalaced for $TRIPLE"
cd "$HERE"
# --paths: resolve mindpalace from repo SOURCE (editable installs' PEP 660
# finder hooks are invisible to PyInstaller's analysis)
"$PY" -m PyInstaller --noconfirm --clean --onefile \
  --name "mindpalaced-$TRIPLE" \
  --paths "$REPO" \
  --add-data "$REPO/mindpalace/web_dist:mindpalace/web_dist" \
  --add-data "$REPO/mindpalace/skills:mindpalace/skills" \
  --collect-submodules mindpalace \
  --hidden-import uvicorn.logging \
  --hidden-import uvicorn.protocols.http.auto \
  --hidden-import uvicorn.protocols.websockets.auto \
  --hidden-import uvicorn.lifespan.on \
  entry.py

echo "✓ $HERE/dist/mindpalaced-$TRIPLE"
