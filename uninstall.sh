#!/usr/bin/env bash
# mindpalace uninstaller — removes the command. Your data is kept unless you say so.
set -uo pipefail

echo "=== mindpalace uninstall ==="
if command -v pipx >/dev/null 2>&1 && pipx list 2>/dev/null | grep -q mindpalace; then
  pipx uninstall mindpalace || true
else
  python3 -m pip uninstall -y mindpalace || true
fi
echo "  ✓ command removed"

HOME_DIR="${MINDPALACE_HOME:-$HOME/.mindpalace}"
if [ -d "$HOME_DIR" ]; then
  read -r -p "Also delete your data + memory at $HOME_DIR ? [y/N] " ans
  if [ "${ans:-N}" = "y" ] || [ "${ans:-N}" = "Y" ]; then
    rm -rf "$HOME_DIR"; echo "  ✓ data removed"
  else
    echo "  data kept at $HOME_DIR (reinstall to resume where you left off)"
  fi
fi
