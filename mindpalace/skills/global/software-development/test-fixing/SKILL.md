---
name: test-fixing
description: "Use when tests are failing, the test suite is broken, CI/CD test jobs fail, or the user says 'fix these tests', 'make tests pass', 'tests are failing after my refactor' — run the suite and systematically fix all failures via smart error grouping."
version: 1.0.0
license: Apache-2.0
tags: [testing, pytest, ci, debugging, refactor, test-failures, fix-tests, regression]
source: https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/test-fixing
derived_from: awesomeclaude
---

# Test Fixing

Systematically identify and fix all failing tests by grouping similar failures and fixing them in dependency order.

## When to use

- User explicitly asks to fix tests ("fix these tests", "make tests pass").
- User reports failures ("tests are failing", "test suite is broken", "failing after my refactor").
- After finishing an implementation and wanting the suite green.
- CI/CD pipeline fails on the test stage.

## Approach

### 1. Run the suite
Run the project's test command (e.g. `make test`, `uv run pytest`, `npm test`). Capture:
- Total failure count
- Error types / patterns
- Affected modules and files

### 2. Group failures
Cluster failures by:
- **Error type** — ImportError, AttributeError, AssertionError, TypeError, etc.
- **Module/file** — one file causing many failures
- **Root cause** — missing deps, API/signature changes, refactor fallout

Prioritize groups by impact (most affected tests first) and dependency order (infrastructure before logic).

### 3. Fix one group at a time
For each group, highest impact first:
1. **Find root cause** — read the code, check `git diff` for recent changes, understand the pattern.
2. **Fix** — minimal, focused edits that follow project conventions (check CLAUDE.md).
3. **Verify the group** — run just those tests before moving on:
   ```bash
   uv run pytest tests/path/to/test_file.py -v
   uv run pytest -k "pattern" -v
   ```
4. Only advance once the current group passes.

### 4. Fix order strategy
1. **Infrastructure first** — import errors, missing dependencies, config issues.
2. **Then API changes** — signature changes, module reorg, renames.
3. **Finally logic** — assertion failures, business-logic bugs, edge cases.

### 5. Final verification
- Re-run the full suite (`make test`).
- Confirm no regressions and coverage stays intact.

## Best practices / gotchas
- Fix one group at a time; never jump ahead while a group is still red.
- Use `git diff` to understand what recently changed — most post-refactor failures are renames/signature drifts.
- Keep changes minimal and focused; don't refactor unrelated code.
- Run focused tests after each fix to catch new breakage early.

## Example
User: "The tests are failing after my refactor."
1. `make test` → 15 failures.
2. Group: 8 ImportErrors (module renamed), 5 AttributeErrors (signature changed), 2 AssertionErrors (logic).
3. Fix ImportErrors → run subset → verify.
4. Fix AttributeErrors → run subset → verify.
5. Fix AssertionErrors → run subset → verify.
6. Run full suite → all pass.
