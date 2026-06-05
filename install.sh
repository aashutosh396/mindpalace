#!/usr/bin/env bash
# mindpalace installer — installs the `mindpalace` command, then runs onboarding.
# Core only; your data lives separately in ~/.mindpalace (or $MINDPALACE_HOME).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== mindpalace install ==="

# 1. Python 3.10+
PY=$(command -v python3 || true)
[ -z "$PY" ] && { echo "need python3 (3.10+)"; exit 1; }
echo "  python: $PY ($($PY -V))"

# 2. Claude CLI (the engine — your Max subscription)
if command -v claude >/dev/null 2>&1; then
  echo "  claude: $(command -v claude)"
else
  echo "  ⚠ Claude CLI not found — install it + log in to your Max plan:"
  echo "    https://docs.claude.com/claude-code"
fi

# 3. install the package (with Discord extra if requested:  ./install.sh discord)
EXTRA=""
[ "${1:-}" = "discord" ] && EXTRA="[discord]"
if command -v pipx >/dev/null 2>&1; then
  pipx install "$HERE$EXTRA" 2>/dev/null || pipx install --force "$HERE$EXTRA"
else
  "$PY" -m pip install --user "$HERE$EXTRA"
fi

echo
echo "✓ installed. Start it with:"
echo "    mindpalace"
echo "  (first run walks you through gateway + identity setup)"
