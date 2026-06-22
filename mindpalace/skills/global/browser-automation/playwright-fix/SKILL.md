---
name: Playwright Fix Flaky Tests
description: Use when a Playwright test fails or passes intermittently ("fix test", "flaky test", "test failing", "passes sometimes", "fails in CI but passes locally").
tags: [playwright, flaky-tests, debugging, test-isolation, timing, trace, ci, web-first-assertions]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/fix
---

# Playwright Fix Flaky Tests

Diagnose and fix a failing/intermittent test with a systematic taxonomy.

## Steps

1. **Reproduce** — `npx playwright test <file> --reporter=list`. If it passes, it's flaky: burn-in `--repeat-each=10`; still passing → `--fully-parallel --workers=4 --repeat-each=5`.

2. **Capture trace** — `npx playwright test <file> --trace=on --retries=0`; read the trace.

3. **Categorize** — every failure is one of four:

| Category | Symptom | Diagnosis |
|---|---|---|
| Timing/Async | fails intermittently everywhere | `--repeat-each=20` reproduces locally |
| Test Isolation | fails in suite, passes alone | `--workers=1 --grep "name"` passes |
| Environment | fails in CI, passes locally | compare CI vs local screenshots/traces |
| Infrastructure | random, no pattern | error references browser internals |

4. **Apply targeted fix**:
   - **Timing/Async** — replace `waitForTimeout()` with web-first assertions; add missing `await`; wait for specific network responses; `toBeVisible()` before interacting.
   - **Isolation** — remove shared mutable state; create test data per-test via API/fixtures; unique identifiers (timestamps/random); check DB state leaks.
   - **Environment** — match viewport between local/CI; account for font rendering in screenshots; run docker locally to match CI; check timezone-dependent assertions.
   - **Infrastructure** — increase timeouts for slow runners; add `retries: 2` in CI; reduce parallel workers (browser OOM); ensure browser deps installed.

5. **Verify** — `--repeat-each=10`; all 10 must pass, else back to step 3.

6. **Prevent recurrence** — add `retries: 2` in CI, enable `trace: 'on-first-retry'`, document the fix pattern in test conventions.

## Output
Root-cause category + specific issue, the fix (diff), verification (10/10), prevention recommendation.
