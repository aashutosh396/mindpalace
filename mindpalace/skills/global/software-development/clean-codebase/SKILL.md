---
name: clean-codebase
description: "Use when a codebase has accumulated hygiene debt — piled-up lint warnings, unused imports/variables, dead code paths, inconsistent formatting — and you want to clean it WITHOUT changing business logic or architecture. Triggers: clean up code, remove dead code, unused imports, fix lint, lint warnings, format codebase, code hygiene, tidy code, autoflake/eslint/black/clippy."
version: 1.0.0
license: MIT
tags: [cleanup, lint, dead-code, formatting, maintenance, hygiene, refactor, static-analysis]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/clean-codebase
derived_from: awesomeclaude
---

# Clean Codebase

Remove dead code, unused imports, fix lint warnings, and normalize formatting — purely hygiene, no logic or architecture changes.

## When to Use

- Lint warnings piled up during rapid development
- Unused imports and variables clutter files
- Dead code paths were never removed
- Formatting is inconsistent across files
- Static analysis reports fixable hygiene issues

Do NOT use for architectural refactoring, bug fixes, or business-logic changes.

## Procedure

### Step 1 — Pre-cleanup assessment
Capture baseline metrics: lint warnings (`lint_tool --format json`), LOC (`cloc`), and unused-symbol reports (ts-prune/depcheck for JS, vulture for Python, lintr for R). Save before/after to quantify improvement. If no lint tool, focus on manual review.

### Step 2 — Fix automated lint warnings
Apply safe auto-fixes: JS/TS `eslint --fix . && prettier --write .`; Python `black . && isort . && ruff check --fix .`; R `styler::style_dir('.')`; Rust `cargo fmt && cargo clippy --fix`. If a fix breaks tests, revert and escalate.

### Step 3 — Identify dead code paths
Static analysis for unreferenced functions/vars/orphaned files: ts-prune + depcheck (JS), vulture (Python), lintr unused linters (R). Generic approach: grep definitions vs calls, report defined-but-never-called.

### Step 4 — Remove unused imports
JS `eslint --fix --rule 'no-unused-vars: error'`; Python `autoflake --remove-all-unused-imports --in-place --recursive .`; R manual review of `library()` calls. If removing breaks the build, the import was used indirectly — restore and document.

### Step 5 — Remove dead code (mode-dependent)
Safe mode (default): only deprecated-marked code, commented-out blocks >10 lines and >6 months old, TODOs for completed issues. Aggressive mode (opt-in): all unused functions, zero-reference private methods, deprecated feature flags. For each deletion: verify zero references, check git history (skip if modified in last 30 days), log to CLEANUP_LOG.md. If uncertain, move to `archive/` instead of deleting.

### Step 6 — Normalize formatting
Line endings (LF/CRLF), single trailing newline, remove trailing whitespace, consistent indentation. Skip binary files.

### Step 7 — Run tests
Run the language's test/check command. Tests must pass (or show the same failures as before cleanup). On new failures, revert incrementally to find the breaking change, then escalate.

### Step 8 — Generate cleanup report
Document mode, language, and before/after metrics (lint warnings, LOC, removed symbols) plus the list of changes and any escalations.

## Validation

- [ ] Baseline metrics captured before changes
- [ ] Safe auto-fixes applied; formatting consistent
- [ ] Dead code identified via static analysis
- [ ] Unused imports removed without breaking build
- [ ] Deletions verified zero-reference and logged
- [ ] Tests pass (or same pre-existing failures)
- [ ] Cleanup report generated

## Common Pitfalls

- Treating cleanup as refactoring — keep logic and architecture unchanged.
- Removing "unused" imports that are used indirectly (side effects, re-exports).
- Deleting recently-modified code — check git history first.
- Skipping the test run after changes.
- Aggressive mode without zero-reference verification.

## Related

- serialize-data-formats, use-graphql-api — companion software-development skills
