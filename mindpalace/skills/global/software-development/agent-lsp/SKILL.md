---
name: agent-lsp
description: "Use when you need semantic code intelligence on a real codebase — find all callers/references, rename a symbol safely across the workspace, assess blast radius/impact before changing a function or type, preview an edit's diagnostics before touching disk, go-to-implementation, detect dead code, or run LSP-diagnostics + build + tests to verify a change. Trigger words: blast radius, find callers, rename symbol, who calls this, impact analysis, safe edit, preview edit, simulate, go to implementation, LSP, language server, gopls/rust-analyzer/tsserver, refactor across files."
version: 1.0.0
license: MIT
tags: [lsp, code-intelligence, refactor, rename, references, mcp, diagnostics, dead-code]
source: https://github.com/blackwell-systems/agent-lsp
derived_from: awesomeclaude
prerequisites:
  commands: [agent-lsp]
---

# agent-lsp

`agent-lsp` is an **MCP server** that orchestrates real language servers (gopls,
rust-analyzer, tsserver, pyright, jdtls, etc.) into agent-native workflows.
It is **not** itself a language server — it manages them, keeps a warm index
across sessions, and exposes batch operations, speculative (in-memory) editing,
and multi-step pipelines as MCP tools (65 tools, 30 CI-verified languages).

Use it instead of grep/read loops whenever you need *semantic* answers about
code: who calls X, what implements an interface, what breaks if I rename Y,
does this edit introduce errors. One `blast_radius` call replaces 20+ sequential
LSP calls; structured responses use far fewer tokens than grep on large repos.

## When to use

- "Find all callers / references of this symbol" → semantic, not text search.
- Renaming a function/type/variable across a whole workspace, safely.
- Before changing/deleting a signature: assess blast radius / impact first.
- Preview an edit's diagnostic delta *before* writing to disk (speculative).
- Go-to-implementation (type-checked interface satisfaction grep cannot do).
- Detect dead code; verify a change with diagnostics + build + tests.

Skip it for trivial single-file text tweaks where grep/Edit is enough.

## Setup

```bash
curl -fsSL https://raw.githubusercontent.com/blackwell-systems/agent-lsp/main/install.sh | sh
agent-lsp init          # registers the MCP server with your agent
```

Register as an MCP server in the agent config; tools then appear as
`mcp__lsp__<tool>`. Language servers (gopls, rust-analyzer, …) must be installed
for the languages you target. GCF token-compact output is on by default; set
`AGENT_LSP_OUTPUT_FORMAT=json` to revert to JSON.

If LSP is not yet running for a workspace, call `mcp__lsp__start_lsp` with the
workspace root. Workspace is auto-inferred from file paths; explicit start is
only needed when switching roots.

## Key tools

- `blast_radius` — one call: all exported symbols in a file + callers
  (test vs non-test partitioned) + reference counts.
- `go_to_symbol` — resolve a dot-notation symbol (`"pkg.Func"`, `"Type.Method"`)
  to file/line/column.
- `find_references`, `find_callers` (incoming/outgoing), `type_hierarchy`.
- `inspect_symbol` (hover), `go_to_implementation`, `list_symbols`.
- `prepare_rename` + `rename_symbol` (supports `dry_run: true`) → `apply_edit`.
- `preview_edit` — speculative single-file edit, returns `net_delta` (errors
  introduced minus resolved) without touching disk.
- `simulate_chain` — speculative sequence of dependent edits; returns
  `cumulative_delta` and `safe_to_apply_through_step`.
- `get_diagnostics`, `suggest_fixes` (code actions), `format_document`.
- `run_build`, `run_tests`, `get_tests_for_file` (source→test correlation).
- `replace_symbol_body` — replace a whole function/method by name, no position math.
- `get_server_capabilities` — check which optional tools the server supports.

## Core workflows (the 24 bundled skills)

The repo ships per-task skills under `skills/<name>/SKILL.md`. The high-value ones:

- **lsp-impact** (read-only): `blast_radius` for a file, or `go_to_symbol` →
  `find_references` → `find_callers`/`type_hierarchy` for a symbol. Decide risk:
  0 refs = likely dead code; 1–5 files low; 6–20 medium; >20 high (use deprecation path).
- **lsp-explore** (read-only): hover + implementations + call hierarchy +
  references in one pass to understand an unfamiliar symbol.
- **lsp-rename**: Phase 1 preview — `prepare_rename`, `find_references`,
  `rename_symbol(dry_run=true)`; HARD STOP for user `[y/n]`. Phase 2 execute —
  capture diagnostics, `rename_symbol`, `apply_edit`, re-check diagnostics.
- **lsp-safe-edit**: capture BEFORE diagnostics → `preview_edit`/`simulate_chain`
  → apply only if `net_delta ≤ 0` → AFTER diagnostics → `suggest_fixes` if new errors.
- **lsp-refactor**: end-to-end pipeline = impact → speculative preview → apply →
  build verify → run correlated tests, with abort gates at each phase.
- **lsp-verify**: three layers (diagnostics + `run_build` + `run_tests`), run in
  parallel, ranked by severity; build errors and test failures are blocking.

Others: lsp-dead-code, lsp-cross-repo, lsp-extract-function, lsp-fix-all,
lsp-format-code, lsp-generate, lsp-implement, lsp-onboard, lsp-test-correlation,
lsp-understand, lsp-architecture, lsp-concurrency-audit, etc. Pull a specific
skill from `skills/<name>/SKILL.md` in the source repo when needed.

## Gotchas

- **Always gate destructive ops.** Rename and refactor require a `[y/n]` stop
  after showing the preview; never apply with `net_delta > 0` without confirmation.
- **Speculate before disk.** Use `preview_edit`/`simulate_chain` to check the
  diagnostic delta first; abort if errors are introduced.
- **`run_tests` on big repos can blow the context window.** It may write to a
  file — don't read it whole; grep for `^(FAIL|--- FAIL)` or scope tests to the
  correlated test files from `get_tests_for_file`.
- **Capability-gate optional tools.** `find_callers`, `type_hierarchy`,
  `go_to_implementation` aren't supported by every language server — check
  `get_server_capabilities` and skip (don't fail) when absent.
- **Symbol paths use dot notation** (`"codec.Encode"`, `"Buffer.Reset"`).
  `position_pattern` with `@@` is an agent-lsp extension; fall back to line/column.
