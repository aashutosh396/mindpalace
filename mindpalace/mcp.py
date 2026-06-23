"""
MCP registry — a catalog of MCP servers, run exactly like the skills library.

  • BUNDLED catalog: mindpalace/mcp/<category>/<slug>.md — name + "Use when…" description + a
    ```json``` block holding the server's mcpServers entry (command/args/env or url). Read-only ref.
  • USER enabled:    ~/.mindpalace/mcp/enabled.json — {slug: {env:{KEY:val}}} the owner turned on
    (creds live here, outside the repo). Only ENABLED servers are wired into turns.

match()  surfaces relevant servers per turn (like skills.match) so the agent knows what's available.
build_config() writes a merged {"mcpServers":{…}} file for the enabled set → passed to claude as
--mcp-config on every turn (alongside any per-project .mcp.json).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import config


def _catalog_dir() -> Path:
    return Path(__file__).parent / "mcp"


def _enabled_path() -> Path:
    return config.home() / "mcp" / "enabled.json"


def _parse(path: Path):
    """Frontmatter (name/description/category/env/homepage/transport) + the ```json``` config block."""
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return {}, {}
    fm = {}
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S | re.M)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip().lower()] = v.strip().strip('"\'')
    cfg = {}
    jm = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if jm:
        try:
            cfg = json.loads(jm.group(1))
        except json.JSONDecodeError:
            cfg = {}
    return fm, cfg


_cat_cache = None


def catalog() -> list:
    """All bundled MCP server entries (cached within a process)."""
    global _cat_cache
    if _cat_cache is not None:
        return _cat_cache
    out, root = [], _catalog_dir()
    if root.exists():
        for p in sorted(root.rglob("*.md")):
            if p.name.upper().startswith(("README", "ATTRIB")):
                continue
            fm, cfg = _parse(p)
            slug = (fm.get("slug") or p.stem).lower()
            out.append({
                "slug": slug, "name": fm.get("name", slug),
                "description": fm.get("description", ""), "category": p.parent.name,
                "env": [e.strip() for e in fm.get("env", "").split(",") if e.strip()],
                "homepage": fm.get("homepage", ""), "config": cfg, "path": str(p),
            })
    _cat_cache = out
    return out


def get(slug: str):
    slug = (slug or "").lower()
    return next((c for c in catalog() if c["slug"] == slug), None)


def enabled() -> dict:
    try:
        return json.loads(_enabled_path().read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_enabled(d: dict) -> None:
    p = _enabled_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2))


def enable(slug: str, env: dict | None = None) -> bool:
    """Turn a catalog server on (optionally with creds). Returns False if slug isn't in the catalog."""
    if not get(slug):
        return False
    e = enabled()
    rec = e.get(slug, {})
    if env:
        rec.setdefault("env", {}).update(env)
    e[slug.lower()] = rec
    _save_enabled(e)
    return True


def disable(slug: str) -> None:
    e = enabled()
    if e.pop(slug.lower(), None) is not None:
        _save_enabled(e)


def missing_env(slug: str) -> list:
    """Required env vars a server needs that the owner hasn't supplied yet (for nudging on enable)."""
    c = get(slug)
    if not c:
        return []
    have = set((enabled().get(slug.lower(), {}).get("env") or {}).keys())
    return [k for k in c["env"] if k not in have]


def build_config() -> str | None:
    """Write the merged {"mcpServers":{…}} for all enabled servers (creds substituted) to the state
    dir; return its path, or None when nothing's enabled. Passed to claude as --mcp-config."""
    e = enabled()
    if not e:
        return None
    by = {c["slug"]: c for c in catalog()}
    servers = {}
    for slug, rec in e.items():
        c = by.get(slug)
        if not c or not c["config"]:
            continue
        cfg = json.loads(json.dumps(c["config"]))      # deep copy
        env = dict(cfg.get("env") or {})
        env.update(rec.get("env") or {})               # owner creds override the placeholders
        if env:
            cfg["env"] = env
        servers[slug] = cfg
    if not servers:
        return None
    out = config.state_dir() / "mcp_enabled.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"mcpServers": servers}, indent=1))
    return str(out)


def config_args() -> list:
    """['--mcp-config', <path>] for the enabled set, or [] — brain adds this to every turn."""
    p = build_config()
    return ["--mcp-config", p] if p else []


def match(query: str, limit: int = 4) -> str:
    """Surface MCP servers relevant to this task (enabled ones flagged ON) so the agent knows what it
    can reach + how to turn more on. '' when nothing relevant. Fails safe."""
    try:
        kws = {w for w in re.findall(r"[a-z0-9]{3,}", (query or "").lower())}
        if not kws:
            return ""
        en = set(enabled())
        scored = []
        for c in catalog():
            hay = f"{c['slug']} {c['name']} {c['description']} {c['category']}".lower()
            hits = sum(1 for k in kws if k in hay)
            nm = sum(1 for k in kws if k in c["slug"].lower())
            if hits:
                scored.append((hits + 2 * nm + (1 if c["slug"] in en else 0), c))
        if not scored:
            return ""
        scored.sort(key=lambda x: -x[0])
        top = [c for s, c in scored[:limit] if s >= 2]
        if not top:
            return ""
        lines = ["MCP SERVERS available for this task (ON = wired in now; off = enable with "
                 "`!mcp enable <slug>`):"]
        for c in top:
            on = "ON " if c["slug"] in en else "off"
            lines.append(f"  - [{on}] {c['slug']} — {c['description'][:80]}")
        return "\n".join(lines)
    except Exception:
        return ""
