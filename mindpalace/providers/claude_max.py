"""Claude Max adapter — wraps the existing brain (claude CLI on the owner's
subscription). The first and, in v3.0, only engine behind the Provider interface."""
from __future__ import annotations

import shutil

from .base import Provider, ProviderEvent, TaskContext, OnEvent


class ClaudeMaxProvider(Provider):
    name = "claude_max"

    def available(self) -> tuple[bool, str]:
        from ..core import brain
        if shutil.which(brain.claude_bin()):
            return True, "claude CLI found"
        return False, "claude CLI not installed — install Claude Code and log in to your plan"

    async def run_task(self, instruction: str, ctx: TaskContext,
                       on_event: OnEvent | None = None) -> str:
        from ..core import brain

        async def _progress(line: str):
            await on_event(ProviderEvent(kind="step", text=line))

        try:
            if on_event:                          # someone is watching → stream tool steps
                return await brain.ask_async_streaming(
                    instruction, [], _progress, system=ctx.system, model=ctx.model)
            return await brain.ask_async(
                instruction, [], system=ctx.system, model=ctx.model,
                timeout=None)
        except Exception as e:                    # brain already stringifies its own errors;
            return f"(error: {str(e)[:200]})"     # this catches adapter-level surprises
