"""Dev-channel updates for the desktop app — straight from the v3 branch.

The daemon is a compiled sidecar, so it can't `git pull` itself. Instead:
CI builds a rolling installer on every push to v3 (prerelease tag `v3-latest`),
and this module checks the branch head + fetches that installer on demand.
This is the unsigned dev channel; the real Tauri updater (signed) replaces the
APPLY step later — the CHECK logic stays.
"""
from __future__ import annotations

import json
import platform
import subprocess
import urllib.request
from pathlib import Path

from .. import config

REPO = "aashutosh396/mindpalace"
BRANCH = "v3"
ROLLING_TAG = "v3-latest"


def local_commit() -> str:
    """The commit this build was made from: build stamp (packaged app) or git (dev)."""
    stamp = config.PKG_ROOT / "build_commit.txt"
    try:
        c = stamp.read_text().strip()
        if c and c != "unknown":
            return c
    except OSError:
        pass
    try:
        return subprocess.run(["git", "-C", str(config.REPO_ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=5).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _gh(path: str) -> dict | list:
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "mindpalace"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def _platform_asset(assets: list[dict]) -> dict | None:
    m, s = platform.machine().lower(), platform.system()
    arch = "aarch64" if m in ("arm64", "aarch64") else "x86_64"
    want = {"Darwin": ".dmg", "Windows": ".exe", "Linux": ".AppImage"}.get(s, ".dmg")
    for a in assets:
        if a["name"].endswith(want) and (arch in a["name"] or s != "Darwin"):
            return a
    return None


def check() -> dict:
    """Compare this build against the branch head; find the rolling installer."""
    local = local_commit()
    remote = _gh(f"repos/{REPO}/branches/{BRANCH}")["commit"]["sha"]
    asset, asset_fresh = None, False
    try:
        rel = _gh(f"repos/{REPO}/releases/tags/{ROLLING_TAG}")
        asset = _platform_asset(rel.get("assets", []))
        # the rolling build lags the branch by one CI run; body carries its commit
        asset_fresh = remote[:12] in (rel.get("body") or "")
    except Exception:
        pass
    return {
        "local": local[:12], "remote": remote[:12],
        "behind": local != "unknown" and not remote.startswith(local),
        "installer": asset["browser_download_url"] if asset else None,
        "installer_name": asset["name"] if asset else None,
        "installer_current": asset_fresh,
    }


def apply() -> dict:
    """Download the rolling installer to ~/Downloads and open it (macOS mounts the
    dmg — the user drags to Applications; other platforms just get the file)."""
    info = check()
    if not info["installer"]:
        return {"ok": False, "error": "no rolling installer published yet — push to v3 and let CI build one"}
    dest = Path.home() / "Downloads" / info["installer_name"]
    req = urllib.request.Request(info["installer"], headers={"User-Agent": "mindpalace"})
    with urllib.request.urlopen(req, timeout=300) as r, dest.open("wb") as out:
        while chunk := r.read(1 << 20):
            out.write(chunk)
    if platform.system() == "Darwin":
        subprocess.Popen(["open", str(dest)])
    return {"ok": True, "path": str(dest), **info}
