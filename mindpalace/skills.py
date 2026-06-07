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
import re
from . import config


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


SKILL_INSTRUCTIONS = f"""
SKILLS & LEARNING (be a Hermes-style agent that grows — capture what you do):
- Before a multi-step task, SEARCH for a matching skill (yours first, then the bundled library
  via `grep -ril <keyword> {config.GLOBAL_SKILLS}`), and read its SKILL.md before acting. (The owner
  sees a "⚡ using skill · <name>" chip when you read one, so reach for them.)
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
