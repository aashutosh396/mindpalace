---
name: Playwright Pro
description: Use when working with Playwright tests, end-to-end testing, browser automation, flaky tests, test migration, or CI test suites — the golden rules and locator priority that govern all Playwright work.
tags: [playwright, e2e, browser-automation, testing, flaky-tests, locators, web-first-assertions, ci, getbyrole, fixtures]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/pw
---

# Playwright Pro

Production-grade Playwright testing. These golden rules and locator priorities govern all Playwright work (generation, review, fixing, migration).

## Golden rules (non-negotiable)
1. `getByRole()` over CSS/XPath — resilient to markup changes.
2. Never `page.waitForTimeout()` — use web-first assertions (`expect(locator).toBeVisible()`, `page.waitForURL()`).
3. `expect(locator)` auto-retries; `expect(await locator.textContent())` does not.
4. Isolate every test — no shared state, no execution-order dependencies.
5. `baseURL` in config — zero hardcoded URLs.
6. Retries: `2` in CI, `0` locally.
7. Traces: `'on-first-retry'` — rich debugging without CI slowdown.
8. Fixtures over globals — `test.extend()` for shared state.
9. One behavior per test — multiple related assertions are fine.
10. Mock external services only — never mock your own app.

## Locator priority (use the first that works)
```
1. getByRole()        — buttons, links, headings, form elements
2. getByLabel()       — form fields with labels
3. getByText()        — non-interactive text
4. getByPlaceholder() — inputs with placeholder
5. getByAltText()     — images
6. getByTitle()       — title attribute
7. getByTestId()      — when no semantic option exists
8. page.locator()     — CSS/XPath as last resort
```

## Recommended sequence
1. Init — scaffold config, CI pipeline, first smoke test.
2. Generate — tests from a spec or URL.
3. Review — validate quality, flag anti-patterns. Always after generate, before commit.
4. Fix — diagnose and repair failing/flaky tests when CI turns red.

Validation checkpoints: run review after generate (catches locator anti-patterns + missing assertions); re-run full suite locally after a fix; run coverage after a migration to confirm parity before decommissioning the old suite.

## Flaky-test categories (see the fix method for full taxonomy)
Timing/Async (fails intermittently everywhere) · Test Isolation (fails in suite, passes alone) · Environment (fails in CI, passes locally) · Infrastructure (random, references browser internals).

## File conventions
Tests `*.spec.ts`/`.js` · page objects `*.page.ts` in `pages/` · fixtures `fixtures.ts` or `fixtures/` · test data in `test-data/`.

## Optional integrations (env vars)
TestRail: `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY`. BrowserStack: `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`. Both optional — the toolkit works fully without them.
