#!/usr/bin/env bash
# Publish a rolling dev build to the v3-latest prerelease FROM THIS MACHINE.
# Same channel the app's "⟳ Get update" button reads. Use while GitHub Actions
# is unavailable (or for a quick local push); CI does the same thing on green.
#
#   ./publish-rolling.sh [python-with-pyinstaller]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
PY="${1:-python3}"

SHA=$(git -C "$REPO" rev-parse HEAD)
echo "== rolling build of ${SHA:0:12} =="

cd "$HERE/sidecar" && ./build.sh "$PY"
mkdir -p "$HERE/src-tauri/binaries"
cp "$HERE/sidecar/dist/mindpalaced-"* "$HERE/src-tauri/binaries/"

cd "$HERE" && npx tauri build

DMG=$(ls "$HERE"/src-tauri/target/release/bundle/dmg/*.dmg)
BODY="Rolling dev build of branch v3 — commit ${SHA:0:12}"
gh release view v3-latest --repo aashutosh396/mindpalace >/dev/null 2>&1 \
  || gh release create v3-latest --repo aashutosh396/mindpalace --prerelease \
       --title "v3 rolling (dev channel)" --notes "$BODY"
gh release edit v3-latest --repo aashutosh396/mindpalace --notes "$BODY"
gh release upload v3-latest "$DMG" --repo aashutosh396/mindpalace --clobber
echo "✓ published $(basename "$DMG") (${SHA:0:12}) to v3-latest"
