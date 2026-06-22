---
name: Playwright TestRail Sync
description: Use when syncing Playwright tests with TestRail ("testrail", "test management", "sync test cases", "push results to testrail", "import from testrail").
tags: [playwright, testrail, test-management, sync, test-cases, test-run, annotations, mcp]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/testrail
---

# Playwright TestRail Sync

Bidirectional sync between Playwright tests and TestRail.

## Prerequisites
Env vars `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`. If unset, tell the user how to configure and stop.

## The bridge: test annotations
Every linked test carries its TestRail case ID:
```typescript
test.info().annotations.push({ type: 'testrail', description: 'C12345' });
```

## Capabilities

**Import cases → tests** — fetch cases (`testrail_get_cases`); per case read title/preconditions/steps/expected, map to a Playwright test with the right template, add the case-ID annotation; group files by section.

**Push results → TestRail** — run `npx playwright test --reporter=json`; parse, map each test to its case ID via annotations; `testrail_add_result` per test: Pass→status_id 1, Fail→5 (+ error message), Skip→2.

**Create run** — `testrail_add_run` including all case IDs found in annotations; return the run ID.

**Sync status** — fetch TestRail cases, scan local tests for annotations; report TestRail cases / linked tests / unlinked cases / tests without IDs.

**Update cases** — read the test for a case ID, extract steps/expected from code, `testrail_update_case`.

## MCP tools
`testrail_get_projects/suites/cases/results`, `testrail_add_case/update_case/add_run/add_result`.

## Output
Operation summary with counts, errors/unmatched cases, link to the TestRail run/results.
