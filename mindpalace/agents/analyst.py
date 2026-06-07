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
    task = (
        "[REFLECTION — reason about the task just completed, then act.]\n"
        f"OWNER: {owner_text}\nAGENT: {agent_reply}\n\n"
        "1. FILE durable facts into the vault: infra/<host>.md, accounts/<owner>.md, "
        "projects/<slug>.md, runbooks/<name>.md; raw secrets/tokens → secrets/ (referenced, not "
        "pasted); append one line to vault/LOG.md. Cross-link (a cred to its project, a host to "
        "its project).\n"
        "2. SKILLIFY: was a REUSABLE procedure done with no matching skill yet (e.g. opening an "
        "SSH connection to a host, a deploy, a backup, a cron setup)? If yes, CREATE a user skill "
        "at skills/<verb>-<noun>.md (frontmatter: name, description, derived_from a global if "
        "relevant, created, use_count: 1) capturing the exact steps for instant reuse.\n"
        "Reply ONE natural line on what you saved/created (e.g. \"saved repairmate creds → "
        "accounts/, created skill ssh-repairmate\"), or exactly NOTHING."
    )
    return await brain.ask_async(task, [], system=_system(), permissions="full")


async def compact() -> str:
    """Distill USER.md + MEMORY.md in place — sharper over time, not just smaller. This is how
    the agent moves toward 'persona perfection': keep the owner's essence, lose the noise."""
    from .. import config
    ub, mb = config.user_budget(), config.memory_budget()
    task = (
        "[MEMORY COMPACTION — distill, don't just trim. Rewrite two files IN PLACE so the system "
        "gets sharper, not just smaller. Preserve every still-true durable fact; lose nothing that "
        "matters.]\n"
        f"1. USER.md ({config.USER_FILE()}): rewrite into the tightest, highest-fidelity PORTRAIT of "
        "the owner — who they are, how they think and work, what they value, their voice and "
        "preferences, standing context (org, projects, tools, conventions). Merge duplicates, "
        "resolve contradictions in favour of the NEWEST info, cut anything ephemeral or one-off. "
        f"Capture their ESSENCE so you act more like them. Keep it under ~{ub} characters.\n"
        f"2. MEMORY.md ({config.MEMORY_FILE()}): same treatment for durable general facts / "
        f"conventions / gotchas — dedupe, merge, newest-wins, drop stale. Keep under ~{mb} chars.\n"
        "Overwrite the files directly with clean, well-structured markdown. Reply ONE short line on "
        "what you tightened (e.g. \"distilled USER.md 2.6k->1.8k, merged 3 dupes\"), or exactly NOTHING."
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
