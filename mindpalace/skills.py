"""
Skills — the learning substrate.

Two layers, never mixed:
  • GLOBAL  (core repo, skills/global/*.md) — pristine reference recipes shipped to
    everyone. Read-only. Updated via `git pull` of the core. Never edited per user.
  • USER    (user-data, skills/*.md)        — concrete skills the agent DRAFTS for THIS
    person from a global reference + their real context. Each carries `derived_from`.

The agent reads a global as a template, then writes a tailored user skill. Over time
the user-skill set is what makes the agent precise for that individual.
"""
import json
import re
import time
from . import config


def _usage_path():
    return config.user_skills() / ".usage.json"


def load_usage() -> dict:
    """Per-skill telemetry sidecar: use_count, last_used, created — feeds the curator."""
    try:
        return json.loads(_usage_path().read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def bump_use(name: str) -> None:
    """Record that a skill was loaded/used (called when the agent reads a SKILL.md)."""
    if not name:
        return
    try:
        d = load_usage()
        rec = d.get(name) or {"created": time.strftime("%Y-%m-%d"), "use_count": 0}
        rec["use_count"] = int(rec.get("use_count", 0)) + 1
        rec["last_used"] = time.strftime("%Y-%m-%d")
        d[name] = rec
        config.user_skills().mkdir(parents=True, exist_ok=True)
        _usage_path().write_text(json.dumps(d, indent=2))
    except OSError:
        pass


def _frontmatter(path):
    """Cheap YAML-ish frontmatter read: name + description only."""
    name, desc = path.stem, ""
    try:
        text = path.read_text()
    except OSError:
        return name, desc
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S | re.M)
    block = m.group(1) if m else text[:400]
    for line in block.splitlines():
        if line.lower().startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.lower().startswith("description:"):
            desc = line.split(":", 1)[1].strip()
    return name, desc


def _list(dir_):
    out = []
    if dir_.exists():
        for p in sorted(dir_.glob("*.md")):
            n, d = _frontmatter(p)
            out.append((n, d, p))
    return out


def global_skills():
    """Top-level *.md (our recipes) + nested <…>/SKILL.md (bundled library)."""
    out, root = [], config.GLOBAL_SKILLS
    if not root.exists():
        return out
    for p in sorted(root.glob("*.md")):
        out.append((*_frontmatter(p), p))
    for p in sorted(root.rglob("SKILL.md")):
        n, d = _frontmatter(p)
        if n in ("SKILL", ""):
            n = p.parent.name
        out.append((n, d, p))
    return out


def user_skills():
    return _list(config.user_skills())


def _categories():
    root = config.GLOBAL_SKILLS
    return sorted({p.parent.parent.name for p in root.rglob("SKILL.md")}) if root.exists() else []


def index_block() -> str:
    """Compact: list the owner's own skills; for the big bundled library, point + search
    (never dump hundreds of skills into the prompt)."""
    u = user_skills()
    root = config.GLOBAL_SKILLS
    n_global = len(list(root.glob("*.md"))) + len(list(root.rglob("SKILL.md"))) if root.exists() else 0
    if not u and not n_global:
        return ""
    lines = ["SKILLS:"]
    if u:
        lines.append("  YOUR skills (tailored to the owner — prefer these):")
        for n, d, p in u:
            lines.append(f"    - {n}: {d}")
    if n_global:
        cats = ", ".join(_categories())
        lines.append(
            f"  + {n_global} bundled reference skills at {root} (categories: {cats}). "
            f"Before a multi-step task, SEARCH them: `grep -ril <keyword> {root}` or "
            f"`ls {root}/*/`, then read the matching SKILL.md. Derive a user skill when you use one.")
    return "\n".join(lines)


# ---- deterministic per-task retrieval -------------------------------------
# Instead of hoping the model remembers to grep, we grep the library for the task's
# keywords every turn and surface the best matches into the prompt. Recall over recall-luck.

_KW_STOP = {"the","and","you","your","that","this","have","with","what","when","make","need",
            "want","from","into","just","like","about","would","could","should","please","then",
            "them","they","there","here","help","does","done","also","some","more","most","very",
            "give","gets","got","can","will","now","run","use","using","task","thing","mind","okay"}


def _keywords(text, k=10):
    out = []
    for w in re.findall(r"[a-z0-9]{4,}", (text or "").lower()):
        if w not in _KW_STOP and w not in out:
            out.append(w)
    return out[:k]


_search_index = None    # cached global-skill haystacks (static within a process)


def _global_index():
    global _search_index
    if _search_index is None:
        idx = []
        try:
            for n, d, p in global_skills():
                try:
                    body = p.read_text(errors="ignore")[:4000]
                except OSError:
                    body = ""
                idx.append((n, d, p, f"{n} {d} {body}".lower()))
        except Exception:
            idx = []
        _search_index = idx
    return _search_index


def match(query: str, limit: int = 5) -> str:
    """Auto-retrieval: grep user + global skills for the task's keywords and surface the best
    matches (titles + descriptions + paths — NOT full bodies) so the brain reliably sees what's
    available before acting. Returns '' when nothing matches (adds zero tokens). Fails safe."""
    try:
        kws = _keywords(query)
        if not kws:
            return ""
        scored = []

        def consider(n, d, p, hay, kind, bias):
            title_hits = {k for k in kws if k in f"{n} {d}".lower()}   # high-signal: name/description
            distinct = {k for k in kws if k in hay}                    # any distinct keyword present
            # gate out noise: surface only on a NAME/DESCRIPTION hit (real relevance) OR a strong
            # body overlap (3+ distinct keywords). Two stray common words in a body don't qualify.
            if not title_hits and len(distinct) < 3:
                return
            scored.append((len(distinct) + 3 * len(title_hits) + bias, kind, n, d, p))

        for n, d, p in user_skills():                 # owner's own skills (fresh; few) — tie-break win
            try:
                body = p.read_text(errors="ignore")[:4000]
            except OSError:
                body = ""
            consider(n, d, p, f"{n} {d} {body}".lower(), "your", 3)
        for n, d, p, hay in _global_index():          # bundled reference library (cached)
            consider(n, d, p, hay, "ref", 0)
        if not scored:
            return ""
        scored.sort(key=lambda x: -x[0])
        lines = ["RELEVANT SKILLS auto-matched to this task — READ the SKILL.md before acting "
                 "(prefer [your] skills):"]
        for _, kind, n, d, p in scored[:limit]:
            desc = (d[:90] + "…") if d and len(d) > 90 else d
            lines.append(f"  - [{kind}] {n}{' — ' + desc if desc else ''}  ({p})")
        return "\n".join(lines)
    except Exception:
        return ""


SKILL_INSTRUCTIONS = f"""
SKILLS & LEARNING (be a Hermes-style agent that grows — capture what you do):
- A "RELEVANT SKILLS auto-matched to this task" list may already be in your context — those were
  grepped from the library for THIS request. If one fits, READ its SKILL.md and follow it before
  acting. If none were surfaced (or none fit), search yourself: `grep -ril <keyword> {config.GLOBAL_SKILLS}`.
  (The owner sees a "⚡ using skill · <name>" chip when you read one, so reach for them.)
- CAPTURE PROACTIVELY: whenever you do a concrete, repeatable task — even a "simple" one like an
  ssh routine, a download, a deploy, a fix, a scrape — and there's no skill for it yet, WRITE a
  tailored user skill at {config.user_skills()}/<verb>-<noun>.md so next time is faster. Don't wait
  to be asked. (Skip only truly one-off trivia that will never recur.)
- When you USE a reference skill, also draft a tailored user skill from it (do NOT edit bundled
  skills). Frontmatter: name, description, derived_from: <skill or "scratch">, created, use_count.
- ANNOUNCE IT: when you create a new skill, tell the owner in your reply in one short line —
  e.g. "📓 Saved a skill: <name> — I'll be faster at this next time." (The "⚡ skill saved · <name>"
  chip shows live as you write it; the reply line confirms it stuck.)
""".strip()
