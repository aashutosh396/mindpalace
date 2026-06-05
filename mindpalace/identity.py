"""
Identity & soul — the first-run ritual (self-learning).

We interview the owner, then (optionally) ask Claude to synthesize a richer "soul":
  USER.md  — who the owner is, how they work, what they want.
  AGENT.md — the agent's name, voice, and operating principles for THIS owner.

These live in USER-DATA. They seed every future turn, so the agent feels like it
already knows the person and has a consistent personality from message one.
"""
from . import config
from .core import brain


def _ask(prompt: str, default: str = "") -> str:
    try:
        v = input(prompt).strip()
    except EOFError:
        v = ""
    return v or default


def interview() -> dict:
    print("\n— Let's create your mindpalace's identity. A few quick questions —\n")
    return {
        "owner_name":  _ask("Your name: ", "friend"),
        "owner_role":  _ask("What do you do (role / work)? "),
        "focus":       _ask("What should the agent mainly help you with? "),
        "style":       _ask("How should it talk to you (e.g. terse, warm, technical)? ", "concise and direct"),
        "agent_name":  _ask("Name your agent [mindpalace]: ", "mindpalace"),
    }


def _fallback_user_md(a: dict) -> str:
    return (
        f"# {a['owner_name']}\n\n"
        f"- **Role:** {a['owner_role']}\n"
        f"- **Wants the agent for:** {a['focus']}\n"
        f"- **Preferred communication:** {a['style']}\n\n"
        "_(The agent updates this as it learns more about you.)_\n"
    )


def _fallback_agent_md(a: dict) -> str:
    return (
        f"# {a['agent_name']}\n\n"
        f"You are **{a['agent_name']}**, {a['owner_name']}'s always-on personal agent.\n\n"
        "## Voice\n"
        f"- {a['style']}.\n"
        "- Prefer doing over explaining. Short by default; go deep when asked.\n\n"
        "## Principles\n"
        f"- Optimize for {a['owner_name']}'s goals around: {a['focus']}.\n"
        "- Act only on explicit request for anything destructive.\n"
        "- Learn relentlessly: write durable facts to memory, draft skills from globals.\n"
    )


def _soul_via_claude(a: dict):
    """Ask Claude to synthesize a richer USER.md + AGENT.md. Falls back to templates."""
    prompt = (
        "Create two short markdown profiles from this onboarding intake. "
        "Output EXACTLY two sections separated by a line containing only '=====AGENT====='.\n"
        "First section = USER.md: a crisp profile of the person (who they are, how they work, "
        "what they want). Second = AGENT.md: the agent's persona/soul — name, voice, operating "
        "principles — written in second person ('You are ...'), tuned to serve this person.\n\n"
        f"Intake:\n{a}\n"
    )
    try:
        out = brain.ask_sync(prompt, [])
        if "=====AGENT=====" in out:
            user_md, agent_md = out.split("=====AGENT=====", 1)
            if len(user_md.strip()) > 40 and len(agent_md.strip()) > 40:
                return user_md.strip() + "\n", agent_md.strip() + "\n"
    except Exception:
        pass
    return None


def create(use_claude: bool = True) -> dict:
    a = interview()
    config.ensure_dirs()
    soul = _soul_via_claude(a) if use_claude else None
    if soul:
        user_md, agent_md = soul
        print("  ✓ soul synthesized by Claude")
    else:
        user_md, agent_md = _fallback_user_md(a), _fallback_agent_md(a)
        print("  ✓ identity written (template)")
    config.USER_FILE().write_text(user_md)
    config.AGENT_FILE().write_text(agent_md)
    config.MEMORY_FILE().write_text(
        f"# Memory\n\n- {config.MEMORY_FILE().name} seeds the agent's durable knowledge. "
        "It appends facts here as it learns.\n")
    return a
