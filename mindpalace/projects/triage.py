"""Intent triage — is a corridor message WORK or CONVERSATION?

Not everything typed in a room is a ticket: "why did you do it that way?",
"thanks, looks good", "what's the status?" are conversation. Two layers keep it
fast: instant heuristics for the obvious cases, a small-model call (haiku)
for the ambiguous middle. On any doubt or failure we fall back to TASK — a
question turned into a card is an annoyance; work turned into chat is work
that silently never happens.
"""
from __future__ import annotations

import asyncio
import re

# clear imperatives → task, no model call
_TASK_VERBS = (
    "add|fix|create|build|make|update|remove|delete|implement|write|refactor|"
    "deploy|change|rename|move|install|setup|set up|convert|migrate|upgrade|"
    "test|run|generate|integrate|optimize|improve|redesign|rewrite|configure")
_TASK_RE = re.compile(rf"(?i)^(?:please\s+|pls\s+|now\s+)?(?:{_TASK_VERBS})\b")

# small talk / acknowledgements → chat, no model call
_ACK_RE = re.compile(
    r"(?i)^(ok(ay)?|k|nice|cool|great|good|perfect|thanks?|thank you|ty|lol|"
    r"hm+|hi|hello|hey|yo|sure|yes|no|yep|nope|got it|understood|awesome|wow|"
    r"good job|well done|👍|🙏|❤️)[.!\s]*$")

# state/why/how questions → chat (work phrased as a question — "can you add X?" —
# does NOT match this; it falls through to the model)
_QUESTION_RE = re.compile(r"(?i)^(what|why|how|when|where|who|which|is|are|was|were|does|did)\b.*\?\s*$")

_PROMPT = (
    "You route messages in a project workspace. The owner typed this in a project "
    "chat. Decide: is it an INSTRUCTION TO DO WORK on the project (task), or is it "
    "conversation — a question, feedback, discussion, or small talk (chat)?\n"
    "Message:\n{text}\n\n"
    "Reply with exactly one word: TASK or CHAT.")


def heuristic(text: str) -> str | None:
    t = text.strip()
    if _ACK_RE.match(t):
        return "chat"
    if len(t.split()) <= 2 and not _TASK_RE.match(t):
        return "chat"                      # two words are never a workable ticket
    if _TASK_RE.match(t):
        return "task"
    if _QUESTION_RE.match(t):
        return "chat"
    return None


async def classify(text: str) -> str:
    lane = heuristic(text)
    if lane:
        return lane
    from ..core import brain
    try:
        from .home import _neutral_cwd
        proc = await asyncio.create_subprocess_exec(
            brain.claude_bin(), "-p", _PROMPT.format(text=text.strip()[:600]),
            "--model", "haiku",
            env=brain._env(), cwd=_neutral_cwd(),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=15)
        return "chat" if "CHAT" in out.decode(errors="replace").upper() else "task"
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
        return "task"                      # doubt → card; work must never silently vanish
