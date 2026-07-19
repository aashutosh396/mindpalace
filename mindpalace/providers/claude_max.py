"""Claude Max adapter — wraps the claude CLI on the owner's subscription.

Two paths:
  • run_task WITH project repos (v3 tickets): our own one-shot invocation,
    grounded in the project — cwd = primary repo, --add-dir for the other repos
    + the assets folder, room persona via --append-system-prompt, progress
    streamed from stream-json events. Engine-specific plumbing lives HERE, in
    the adapter — that's the point of the provider interface.
  • no repos attached: fall back to the brain's chat-turn runner (vault cwd),
    same as v2 background workers.

Scoping honesty: cwd + --add-dir grounds the agent in the project's world; with
full permissions it is guidance, not a wall. A hard fence (allowed-tools mode)
can layer on later without touching callers.
"""
from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path

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
        dirs = [d for d in ctx.repo_paths if Path(d).is_dir()]
        if dirs:
            return await self._run_grounded(instruction, ctx, dirs, on_event)
        # no repos yet → the room's world is just its assets folder; run via the
        # brain's standard turn (vault cwd, full skills/MCP context)
        from ..core import brain
        perms = "readonly" if ctx.readonly else "full"
        try:
            if on_event:
                async def _progress(line: str):
                    await on_event(ProviderEvent(kind="step", text=line))
                return await brain.ask_async_streaming(
                    instruction, [], _progress, system=ctx.system, model=ctx.model,
                    permissions=perms)
            return await brain.ask_async(instruction, [], system=ctx.system,
                                         model=ctx.model, permissions=perms)
        except Exception as e:
            return f"(error: {str(e)[:200]})"

    async def _run_grounded(self, instruction: str, ctx: TaskContext,
                            dirs: list[str], on_event: OnEvent | None) -> str:
        from .. import config
        from ..core import brain

        args = [brain.claude_bin(), "-p", instruction,
                "--output-format", "stream-json", "--verbose"]
        if ctx.readonly:                              # chat lane: look, don't touch
            args += ["--allowedTools", brain.READONLY_TOOLS]
        else:
            args += ["--dangerously-skip-permissions"]
        model = ctx.model or config.power_model()     # tickets are real work — power model,
        if model:                                     # like v2's background workers
            args += ["--model", model]
        if ctx.system:
            args += ["--append-system-prompt", ctx.system]
        cwd = dirs[0]                                 # primary repo (store orders primary first)
        for d in dirs[1:]:
            args += ["--add-dir", d]
        if ctx.asset_dir and Path(ctx.asset_dir).is_dir():
            args += ["--add-dir", ctx.asset_dir]

        tmo = config.agent_job_timeout()
        final, err = "", ""
        try:
            async with brain._semaphore():            # same cap as every other claude proc
                proc = await asyncio.create_subprocess_exec(
                    *args, cwd=cwd, env=brain._env(),
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

                async def _drain():
                    nonlocal final
                    async for raw in proc.stdout:
                        try:
                            ev = json.loads(raw.decode(errors="replace"))
                        except json.JSONDecodeError:
                            continue
                        if ev.get("type") == "assistant":
                            for blk in (ev.get("message") or {}).get("content", []):
                                if blk.get("type") == "tool_use" and on_event:
                                    await on_event(ProviderEvent(kind="step", text=_chip(blk)))
                        elif ev.get("type") == "result":
                            final = ev.get("result") or ""

                await asyncio.wait_for(_drain(), timeout=tmo)
                err = (await proc.stderr.read()).decode(errors="replace")
                await proc.wait()
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except Exception:
                pass
            return f"(timed out after {tmo}s — break the ticket into smaller steps)"
        except Exception as e:
            return f"(error: {str(e)[:200]})"
        return final.strip() or f"(empty; {err[:200]})"


def _chip(blk: dict) -> str:
    """'⚡ Tool · target' progress line; reuse the brain's rich chip when it works."""
    try:
        from ..core import brain
        return brain._chip(blk)
    except Exception:
        name = blk.get("name", "tool")
        inp = blk.get("input") or {}
        target = str(inp.get("file_path") or inp.get("command") or inp.get("pattern") or "")[:60]
        return f"⚡ {name}" + (f" · {target}" if target else "")
