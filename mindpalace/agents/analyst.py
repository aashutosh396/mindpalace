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

ROLE = (
    "You are mindpalace's ANALYST — a background agent that exists to make the system smarter "
    "after every task and on every heartbeat. Reason hard, then ACT: file durable facts into "
    "the vault, turn first-time reusable procedures into skills, cross-link knowledge, spot "
    "patterns + gaps, and propose improvements. Only durable/true facts + genuinely reusable "
    "skills. You are what makes mindpalace compound into something superb."
)


def _system() -> str:
    # full operating context (doctrine, vault rules, skills, capabilities) + the analyst role
    return brain.system_prompt() + "\n\n" + ROLE


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
    return await brain.ask_async(task, [], system=_system(), permissions="full")


async def compact() -> str:
    """Memory consolidation, brain-style: keep the long-term stores clean, then refresh a TINY
    working memory (CORE.md) from them. Lose nothing durable; keep the present light."""
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
    return await brain.ask_async(task, [], system=_system(), permissions="full")


async def review() -> str:
    task = (
        "[AUTONOMOUS REVIEW — you woke yourself on a timer; no human is asking.]\n"
        "Do a quick proactive pass: skim the vault (infra/, projects/, recent LOG.md) and run "
        "cheap, safe health checks on services you have notes on. File anything new + append to "
        "LOG.md. If something needs attention or you did something, write a SHORT report with a "
        "proposed next action. Do NOT take destructive/irreversible actions unprompted — propose "
        "them. If all quiet, reply EXACTLY: NOTHING"
    )
    return await brain.ask_async(task, [], system=_system(), permissions="full")
