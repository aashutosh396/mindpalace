"""
The Analyst — a dedicated background agent whose ONLY job is to make mindpalace smarter.

It runs in parallel to the chat:
  • reflect(task)  — after every real task: reason about it, then ACT — file durable facts
    into the vault, and turn a first-time reusable procedure into a SKILL.
  • review()       — on each heartbeat: proactively review the vault + service health, file,
    and surface anything worth attention.

Reasoning is the backbone: the Analyst thinks first, then writes the result into the vault /
skills / memory so the whole system compounds and gets more capable over time.
"""
from __future__ import annotations

from ..core import brain
from .. import config

ROLE = (
    "You are mindpalace's ANALYST — a background agent that exists to make the system smarter "
    "after every task and on every heartbeat. Reason hard, then ACT: file durable facts into "
    "the vault, turn first-time reusable procedures into skills, cross-link knowledge, spot "
    "patterns + gaps, and propose improvements. Only durable/true facts + genuinely reusable "
    "skills. You are what makes mindpalace compound into something superb."
)


def _system() -> str:
    # LEAN context — only what's needed to file facts + skillify (vault rules, self-knowledge,
    # skills doctrine). Drops voice/capabilities/automation/async blocks the analyst never uses,
    # so every background call (now on the cheaper model) carries far fewer tokens.
    from ..core.brain import _doctrine, _self_knowledge, SELF_LEARN
    from .. import skills
    return "\n\n".join([ROLE, _doctrine(), _self_knowledge(), skills.SKILL_INSTRUCTIONS, SELF_LEARN])


async def reflect(owner_text: str, agent_reply: str) -> str:
    from .. import config
    task = (
        "[REFLECTION — reason about the task just completed, then act. Be ACTIVE: most real "
        "tasks leave at least one durable fact or skill behind. A pass that saves nothing is a "
        "missed learning opportunity, not a neutral outcome — but never invent something to save.]\n"
        f"OWNER: {owner_text}\nAGENT: {agent_reply}\n\n"
        "1. FILE durable facts into the vault: infra/<host>.md, accounts/<owner>.md, "
        "projects/<slug>.md, runbooks/<name>.md; raw secrets/tokens → secrets/ (referenced, not "
        "pasted); append one line to vault/LOG.md. Cross-link (a cred to its project, a host to "
        "its project).\n"
        "   WRITE FACTS AS DECLARATIVE STATE, not commands: 'Owner prefers terse replies' ✓ not "
        "'Always be terse' ✗; 'Backups run nightly at 2am' ✓. If a fact will be stale in a week, "
        "it does NOT belong in memory — no PR numbers, SHAs, 'phase N done', or one-off run details.\n"
        "2. SKILLIFY (procedural memory). Was a REUSABLE procedure done — ssh to a host, a deploy, "
        "a backup, a cron setup, a scrape? Capture it, in this PREFERENCE ORDER (only escalate if "
        "nothing earlier fits):\n"
        "   a) PATCH an existing user skill that already covers this class of task;\n"
        "   b) add a supporting reference/template/script file beside an existing skill;\n"
        f"   c) only if nothing fits, CREATE a new user skill at {config.user_skills()}/<verb>-<noun>.md "
        "(frontmatter: name, description, derived_from a global or \"scratch\", created, use_count: 1).\n"
        "   NAMING: skills must be CLASS-LEVEL and reusable ('deploy-django-app', 'ssh-to-host') — "
        "NEVER a one-off artifact ('fix-bug-1234', 'debug-today', a PR number, an error string, or a "
        "bare library name).\n"
        "   NEGATIVE-KNOWLEDGE GUARDRAIL (critical): do NOT save environment-specific failures, "
        "transient errors, or 'tool/service X is broken' as durable facts or skills. Those harden "
        "into refusals the agent cites against itself for months after the problem is long fixed.\n"
        "Reply ONE natural line on what you saved/created/patched (e.g. \"saved repairmate creds → "
        "accounts/, patched skill ssh-to-host\"), or exactly NOTHING."
    )
    return await brain.ask_async(task, [], system=_system(), permissions="full",
                                 model=config.background_model())


async def compact(session_id: str | None = None) -> str:
    """Memory consolidation, brain-style: keep the long-term stores clean, then refresh a TINY
    working memory (CORE.md) from them. Lose nothing durable; keep the present light.

    session_id: if given (session continuity on), FORK that live session so consolidation reasons
    over the REAL conversation, not just the current file state. Falls back to the legacy
    contextless pass if the fork fails."""
    from .. import config
    ub, mb, cb = config.user_budget(), config.memory_budget(), config.core_budget()
    task = (
        "[MEMORY CONSOLIDATION — work like a brain: keep long-term clean, refresh a tiny WORKING "
        "memory from it. Distill, don't just trim. Lose nothing durable.]\n"
        f"1. LONG-TERM, deduped (rewrite IN PLACE): USER.md ({config.USER_FILE()}) = the full high-"
        f"fidelity profile of the owner (keep under ~{ub} chars); MEMORY.md ({config.MEMORY_FILE()}) "
        f"= durable facts / conventions / gotchas (under ~{mb} chars). Merge duplicates, resolve "
        "contradictions in favour of the NEWEST info, drop ephemera.\n"
        "   DIALECTIC PASS on the owner profile: don't just append — (i) derive new inferences about "
        "how they think/work from recent exchanges, (ii) self-audit for gaps or vagueness, (iii) "
        "CHECK new inferences against what's already there and RECONCILE contradictions (newest wins) "
        "so stale or conflicting beliefs about the owner never coexist.\n"
        f"2. WORKING memory (rewrite IN PLACE): CORE.md ({config.CORE_FILE()}) — this loads on EVERY "
        f"prompt, so keep it UNDER ~{cb} characters, high-signal only. Two parts: (a) the owner's "
        "ESSENCE in a few tight lines — who they are, how they work, voice, key preferences, what's "
        "currently active; and (b) a compact MAP of what you know and WHERE the detail lives "
        "(topic → USER.md / MEMORY.md section / vault file) so you can recall on demand.\n"
        "Overwrite all three with clean markdown. Reply ONE short line on what you consolidated "
        "(e.g. \"refreshed CORE 1.4k; USER 3k->2k, merged 2 dupes\"), or exactly NOTHING."
    )
    if session_id:                               # consolidate from the REAL conversation (forked)
        out = await brain.ask_resumed(task, session_id, permissions="full",
                                      model=config.background_model())
        if out and not out.startswith(("(error", "(timed out", "(empty")):
            return out                           # else fall through to the legacy contextless pass
    return await brain.ask_async(task, [], system=_system(), permissions="full",
                                 model=config.background_model())


async def curate() -> str:
    """Periodic skill housekeeping (slow cadence, distinct from per-task reflect). Consolidate
    overlapping skills into umbrellas, archive the stale — never delete a reusable procedure."""
    from .. import config, skills as sk
    usage = sk.load_usage()
    task = (
        "[SKILL CURATION — periodic housekeeping of your USER skills ONLY (never touch bundled "
        "global skills). Goal: a tight library of CLASS-LEVEL skills, not a junk drawer.]\n"
        f"User skills dir: {config.user_skills()}\nUsage telemetry (.usage.json): {usage}\n\n"
        "1. CONSOLIDATE overlapping or overly-narrow skills into a broader umbrella — judge by "
        "CONTENT overlap, NOT by use_count. Fold the detail in, then move the absorbed file to "
        "skills/_archive/ and note 'absorbed_into: <name>' in the survivor.\n"
        "2. ARCHIVE the clearly stale (not used in ~90 days AND superseded/irrelevant) into "
        "skills/_archive/ — ARCHIVE, never delete. Reactivate on next use.\n"
        "3. RENAME any skill with a one-off name (PR#, error string, 'fix-X-today') to a reusable "
        "class-level name.\n"
        "Be conservative — never lose a genuinely reusable procedure. Reply ONE line on what you "
        "consolidated/archived, or exactly NOTHING."
    )
    return await brain.ask_async(task, [], system=_system(), permissions="full",
                                 model=config.background_model())


async def review() -> str:
    task = (
        "[AUTONOMOUS HEALTH CHECK — you woke yourself on a timer; no human is asking.]\n"
        "Run a quick proactive pass: go through the services/hosts/projects you have vault notes on "
        "and run cheap, SAFE checks (reachability, process up, disk, recent errors — read-only). "
        "Note each as a PASS (✓), a WARNING (⚠ degraded/worth watching), or a PROBLEM (✗ broken/down). "
        "File any new durable facts + append a LOG.md line.\n"
        "Write a SHORT report: list only the ⚠ and ✗ items with what's wrong + a proposed next action "
        "(✓ items don't need lines). Do NOT take destructive/irreversible actions — propose them.\n"
        "Your LAST line MUST be exactly this machine-readable tally (real counts of checks you ran):\n"
        "    SUMMARY ✓<passed> ⚠<warnings> ✗<problems>\n"
        "e.g.  SUMMARY ✓45 ⚠2 ✗1 . Always include this line — it's the owner's at-a-glance signal."
    )
    return await brain.ask_async(task, [], system=_system(), permissions="full",
                                 model=config.background_model())
