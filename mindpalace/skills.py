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


def _fm_block(text: str) -> str:
    """The frontmatter region (name + description + tags) — the HIGH-SIGNAL part for matching."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 2:
            return parts[1].lower()
    return text[:400].lower()


def _global_index():
    global _search_index
    if _search_index is None:
        idx = []
        try:
            for n, d, p in global_skills():
                try:
                    text = p.read_text(errors="ignore")
                except OSError:
                    text = ""
                hay = f"{n} {d} {text[:4000]}".lower()
                idx.append((n, d, p, hay, _fm_block(text)))
        except Exception:
            idx = []
        _search_index = idx
    return _search_index


_STRONG_MATCH = 6        # top score at/above this (a name hit, or ≥3 fm/tag hits) ⇒ auto-inject the body
_INJECT_CHARS = 2600     # cap on the injected method (keep the turn lean)


def _skill_body(path, max_chars: int = _INJECT_CHARS) -> str:
    """The skill's METHOD (frontmatter stripped), trimmed — for inlining the top match so the brain
    APPLIES it instead of merely being told it exists."""
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return ""
    if text.startswith("---"):                       # drop the YAML frontmatter block
        parts = text.split("---", 2)
        text = parts[2] if len(parts) >= 3 else text
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit("\n", 1)[0] + "\n… (truncated — open the file for the rest)"
    return text


def match(query: str, limit: int = 5) -> str:
    """Auto-retrieval: grep user + global skills for the task's keywords and surface the best matches.
    For a STRONG, clear leader it also AUTO-INJECTS that skill's method inline (so the brain applies it,
    not just hears it exists); weaker matches are listed as pointers. '' when nothing matches. Fails safe."""
    try:
        kws = _keywords(query)
        if not kws:
            return ""
        scored = []

        def consider(n, d, p, hay, fm, kind, bias):
            name_l = n.lower()
            name_hits = sum(1 for k in kws if k in name_l)     # strongest: keyword in the slug/name
            fm_hits = sum(1 for k in kws if k in fm)           # high-signal: name + description + TAGS
            distinct = {k for k in kws if k in hay}            # any distinct keyword anywhere
            # gate out noise: surface only on a frontmatter (name/desc/tag) hit OR a strong body
            # overlap (3+ distinct keywords). A stray common word in the body alone doesn't qualify.
            if not fm_hits and len(distinct) < 3:
                return
            # weight name >> tags/description >> body, so the on-topic skill ranks above lexical noise.
            # carry the components too — injection is gated on signal QUALITY, not the blended score.
            scored.append((4 * name_hits + 2 * fm_hits + len(distinct) + bias, kind, n, d, p,
                           name_hits, fm_hits, len(distinct)))

        for n, d, p in user_skills():                 # owner's own skills (fresh; few) — tie-break win
            try:
                text = p.read_text(errors="ignore")
            except OSError:
                text = ""
            consider(n, d, p, f"{n} {d} {text[:4000]}".lower(), _fm_block(text), "your", 3)
        for n, d, p, hay, fm in _global_index():      # bundled reference library (cached)
            consider(n, d, p, hay, fm, "ref", 0)
        if not scored:
            return ""
        scored.sort(key=lambda x: -x[0])
        top_score, _tk, top_n, _td, top_p = scored[0][:5]
        t_nh, t_fh, t_dd = scored[0][5:8]            # name-hits, frontmatter-hits, distinct-keyword count
        runner = scored[1][0] if len(scored) > 1 else 0
        # Inject only on a HIGH-QUALITY top match: its name carries a task keyword AND the task shares
        # ≥2 keywords with it (or ≥3 tag/desc hits, or a 2-word name hit) — so a single common word
        # like "time" never inlines a body — AND it's strictly the leader (ties stay listed, not inlined).
        strong = (t_nh >= 1 and t_dd >= 2) or t_fh >= 3 or t_nh >= 2
        inject = strong and top_score >= _STRONG_MATCH and (len(scored) == 1 or top_score > runner)
        out = []
        if inject:
            body = _skill_body(top_p)
            if body:
                try:
                    bump_use(top_n)                  # auto-applied counts as used (feeds the curator)
                except Exception:
                    pass
                out.append(
                    f"ACTIVE SKILL — apply this method NOW as your first step (don't improvise a "
                    f"different approach when this fits): **{top_n}**  ({top_p})\n{body}")
        lines = ["RELEVANT SKILLS auto-matched to this task. If the top one fits the request, you "
                 "MUST follow its method as your FIRST step — before answering from memory or asking "
                 "scoping questions. Don't wing it when a skill exists. (Prefer [your] over [ref].)"]
        for row in scored[:limit]:
            _, kind, n, d, p = row[:5]
            desc = (d[:90] + "…") if d and len(d) > 90 else d
            tag = " ⟵ ACTIVE (injected above)" if (inject and p == top_p) else ""
            lines.append(f"  - [{kind}] {n}{' — ' + desc if desc else ''}  ({p}){tag}")
        out.append("\n".join(lines))
        # skill-chaining: if the top is injected AND ≥2 OTHER strong skills also fit, the request is
        # likely multi-step — suggest applying them in order rather than just the one.
        strong_others = [r for r in scored[1:4] if r[0] >= _STRONG_MATCH]
        if inject and len(strong_others) >= 2:
            chain = " → ".join([top_n] + [r[2] for r in strong_others[:2]])
            out.append(f"MULTI-STEP HINT: several skills fit — if this is a multi-part task, plan it "
                       f"as a chain and apply each in order: {chain}.")
        return "\n\n".join(out)
    except Exception:
        return ""


SKILL_INSTRUCTIONS = f"""
SKILLS & LEARNING (be a Hermes-style agent that grows — capture what you do):
- USE SKILLS — this is not optional. You have two libraries: YOUR tailored skills at
  {config.user_skills()} and the bundled reference skills at {config.GLOBAL_SKILLS} (both are
  searched and surfaced for you). Two things may appear in your context:
  (1) an "ACTIVE SKILL" block — the top match's method, already inlined for you. APPLY it as your
  FIRST step; don't improvise a different approach when it fits. (2) a "RELEVANT SKILLS auto-matched"
  list — pointers; `Read` the best one's SKILL.md and follow it before answering from memory or asking
  scoping questions. If a "MULTI-STEP HINT" appears, plan the task as that chain and apply each in order.
  A request like "keyword research" or "SEO audit" must go through the matching skill, not improvised.
- If nothing was surfaced (or none fit), search BOTH yourself: `grep -ril <keyword> {config.user_skills()}`
  and `grep -ril <keyword> {config.GLOBAL_SKILLS}`, then read the best match.
  (The owner sees a "📚 using skill · <name>" chip when you open one — so reach for them every time.)
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
