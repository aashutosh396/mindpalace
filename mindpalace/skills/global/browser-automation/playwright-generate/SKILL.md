---
name: Playwright Generate Tests
description: Use when writing or generating Playwright tests from a user story, URL, component, or feature ("write tests", "add tests for", "test this component", "e2e test for").
tags: [playwright, test-generation, e2e, locators, web-first-assertions, page-objects, fixtures, templates]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/generate
---

# Playwright Generate Tests

Generate production-ready Playwright tests from a user story, URL, component path, or feature description.

## Steps

1. **Understand the target** — user story → behavior to verify; component path → read source for props/states/interactions; page/URL → route + elements; feature → app areas.

2. **Explore the codebase** — read `playwright.config.ts` (testDir/baseURL/projects), existing tests for patterns/fixtures/conventions, the component source, existing page objects (`pages/`), fixtures (`fixtures/`), auth setup (`auth.setup.ts`/`storageState`).

3. **Select a template** matching the surface (auth, CRUD, checkout, search, forms, dashboard, settings, onboarding, API, accessibility); replace placeholders with real selectors/URLs/data.

4. **Generate the test** — Arrange/Act/Assert in `test.describe` blocks.
   - Locator priority: getByRole → getByLabel → getByText → getByPlaceholder → getByTestId.
   - Web-first assertions only: `await expect(locator).toBeVisible()` / `.toHaveText()` — never `const t = await page.textContent(); expect(t).toBe()`.
   - Never use `waitForTimeout()`, `page.$()/$$()`, bare CSS unless necessary, or `page.evaluate()` for locator-doable work.
   - Always: descriptive names explaining behavior, error/edge tests alongside happy path, `await` on every Playwright call, baseURL-relative navigation (`page.goto('/')`).

5. **Match conventions** — TS → `.spec.ts`, JS → `.spec.js` with `require()`; reuse project page objects, custom fixtures, and test-data dir.

6. **Supporting files when warranted** — page object if a test touches 5+ unique locators on one page; fixture for shared setup (auth/data); JSON in `test-data/` for structured data.

7. **Verify** — run `npx playwright test <file> --reporter=list`; on failure fix the test (not the app), re-run; if it's a genuine app issue, report it.

## Output
Generated file(s) + path, any supporting files, run result, coverage note (what behaviors are now tested).
