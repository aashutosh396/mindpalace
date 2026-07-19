"""Echo provider — a no-cost engine for developing/testing the ticket loop.

Enable with  config.json: {"ai_source": "echo"} . It streams two fake progress
steps and echoes the instruction back — the full board lifecycle without a
model call. Never the default; strictly a dev tool.
"""
from __future__ import annotations

import asyncio

from .base import Provider, ProviderEvent, TaskContext, OnEvent


class EchoProvider(Provider):
    name = "echo"

    async def run_task(self, instruction: str, ctx: TaskContext,
                       on_event: OnEvent | None = None) -> str:
        for step in ("reading the ticket", "pretending to work"):
            if on_event:
                await on_event(ProviderEvent(kind="step", text=step))
            await asyncio.sleep(0.4)
        # the ticket text sits between the wrap's intro and outro paragraphs
        parts = instruction.split("\n\n")
        head = (parts[1] if len(parts) > 2 else instruction).splitlines()[0][:120]
        return f"Done:\n✓ (echo) received the ticket in room '{ctx.project_slug}'\n✓ {head}"
