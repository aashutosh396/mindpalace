"""AI providers — every engine sits behind the ONE Provider interface.

v3.0 ships claude_max only; other sources (Claude API, Codex, Codex API,
custom OpenAI-compatible) are later adapters, never rewrites.
"""
from __future__ import annotations

from .base import Provider, ProviderEvent
from .claude_max import ClaudeMaxProvider
from .echo import EchoProvider

_REGISTRY = {"claude_max": ClaudeMaxProvider, "echo": EchoProvider}


def get_provider(name: str | None = None) -> Provider:
    """The configured primary provider (claude_max until Settings exists)."""
    from .. import config
    key = name or config.load_config().get("ai_source", "claude_max")
    cls = _REGISTRY.get(key, ClaudeMaxProvider)
    return cls()
