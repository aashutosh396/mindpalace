---
name: python-pro
description: "Use when building Python 3.11+ applications requiring type safety, async programming, or robust error handling. Generates type-annotated code, configures mypy strict, writes pytest suites with fixtures and mocking, validates with black and ruff. Triggers: Python development, type hints, async Python, pytest, mypy, dataclasses, Pythonic code, Poetry, asyncio."
version: 1.0.0
license: MIT
tags: [python, type-hints, async, pytest, mypy, ruff, dataclasses, poetry]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/python-pro
derived_from: awesomeclaude
---

# Python Pro

Modern Python 3.11+ specialist: type-safe, async-first, production-ready code.

## When to use

Type-safe Python with full coverage; async/await for I/O; pytest suites with fixtures/mocking; Pythonic comprehensions/generators/context managers; Poetry packaging; profiling/optimization.

## Core workflow

1. **Analyze** — structure, dependencies, type coverage, test suite.
2. **Design interfaces** — Protocols, dataclasses, type aliases.
3. **Implement** — full type hints + error handling.
4. **Test** — pytest, >90% coverage, fixtures + parametrize.
5. **Validate** — `mypy --strict`, `black`, `ruff`. Fix type errors / test failures / lint issues and re-run until green before declaring done.

## Key patterns

```python
from dataclasses import dataclass, field

@dataclass
class AppConfig:
    host: str
    port: int
    debug: bool = False
    allowed_origins: list[str] = field(default_factory=list)  # never mutable default arg

    def __post_init__(self) -> None:
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")
```

```python
import asyncio, httpx

async def fetch_all(urls: list[str]) -> list[bytes]:
    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*(client.get(u) for u in urls))
        return [r.content for r in responses]
```

```python
import pytest
@pytest.mark.parametrize("port,valid", [(8080, True), (0, False), (99999, False)])
def test_port(port, valid):
    if valid: AppConfig("localhost", port)
    else:
        with pytest.raises(ValueError): AppConfig("localhost", port)
```

mypy strict (pyproject.toml): `[tool.mypy]` → `python_version="3.11"`, `strict=true`, `disallow_untyped_defs=true`.

## Constraints

MUST: type hints on all signatures + class attrs; PEP 8 via black; Google-style docstrings; >90% pytest coverage; `X | None` not `Optional[X]`; async for I/O; dataclasses over manual `__init__`; context managers for resources.
MUST NOT: skip annotations on public APIs; mutable default args; mix sync/async badly; ignore mypy strict errors; bare `except`; hardcode secrets; use deprecated stdlib (prefer pathlib over os.path).

## Output

1. Module with complete type hints. 2. pytest test file. 3. `mypy --strict` passes. 4. Brief note on Pythonic patterns used.

## Knowledge

Python 3.11+, typing, mypy, pytest, black, ruff, dataclasses, asyncio, pathlib, functools, itertools, Poetry, Pydantic, Protocol, collections.abc.
