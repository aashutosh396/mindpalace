---
name: MCP Server Builder
description: Use when exposing an existing REST/OpenAPI API as an MCP server, building tool integrations for Claude/Codex/Cursor, or scaffolding an MCP project — OpenAPI-as-source-of-truth, Python or TypeScript.
tags: [mcp, model-context-protocol, openapi, tool-integration, api, server-scaffolding, schema-validation, python, typescript]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/mcp-server-builder
---

# MCP Server Builder

Design and ship production-ready MCP servers from API contracts instead of hand-written one-off tool wrappers. OpenAPI is the source of truth. Supports Python and TypeScript.

## When to use
- Expose an internal/external REST API to an LLM agent
- Replace brittle browser automation with typed tools
- One MCP server shared across teams and assistants
- Repeatable quality checks before publishing MCP tools

## Core workflows

### 1. OpenAPI → MCP scaffold
1. Start from a valid OpenAPI spec.
2. Convert paths/operations into MCP tool definitions + starter server code.
3. Review naming and auth strategy.
4. Add endpoint-specific runtime logic.

### 2. Validate tool definitions (before integration tests)
Check for: duplicate tool names, invalid schema shape, missing descriptions, empty required fields, naming hygiene. Strict mode returns non-zero exit when errors exist.

### 3. Runtime selection
- **Python** — fast iteration, data-heavy backends.
- **TypeScript** — unified JS stacks, tighter frontend/backend contract reuse.
- Keep tool contracts stable even if transport/runtime changes (separate transport decisions from tool-contract design).

### 4. Harden for production
- Keep secrets in env vars, NOT tool schemas.
- Prefer outbound host allowlists over open proxies.
- Use additive-only changes; **never rename tool names in place** (breaks consumers — version instead).

## Quality gates for tool contracts
- Every tool has a clear name + description
- Required fields are non-empty and correctly typed
- No duplicate names
- Backward-compatible evolution (additive only)
- Auth strategy explicit, secrets out of the schema
