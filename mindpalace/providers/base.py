"""The ONE provider interface — the brain calls engines only through this.

Design rule (docs/v3-architecture.md): no engine-specific calls anywhere else in
the codebase. Adding an AI source = subclass Provider + register it. Events flow
back through an async callback so gateways can stream progress live (WS, Discord).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable


@dataclass
class ProviderEvent:
    """One progress signal from a running task: a tool step, a status line, text."""
    kind: str                 # "step" | "text" | "error"
    text: str = ""
    data: dict = field(default_factory=dict)


@dataclass
class TaskContext:
    """What a task is allowed to see: the project's own + linked repo paths,
    its asset folder, and the persona/system prompt for the project room."""
    project_slug: str = ""
    repo_paths: list[str] = field(default_factory=list)
    asset_dir: str = ""
    system: str | None = None
    model: str | None = None
    readonly: bool = False        # chat-lane turns may read the project, never modify it
    session_id: str | None = None         # resume this engine session (room continuity)
    result_session_id: str | None = None  # set by the provider: session used/created


OnEvent = Callable[[ProviderEvent], Awaitable[None]]


class Provider:
    name = "base"

    async def run_task(self, instruction: str, ctx: TaskContext,
                       on_event: OnEvent | None = None) -> str:
        """Run one instruction to completion; return the final reply text.
        Implementations stream progress via on_event and must not raise for
        engine-side failures — return an '(error: …)' string instead, so the
        ticket loop can move the card to review with the failure attached."""
        raise NotImplementedError

    def available(self) -> tuple[bool, str]:
        """(usable?, human reason) — lets Settings/first-run show source health."""
        return True, "ok"
