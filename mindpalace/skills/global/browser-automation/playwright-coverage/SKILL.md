---
name: Playwright Coverage Gaps
description: Use when analyzing test coverage gaps ("test coverage", "what's not tested", "coverage gaps", "missing tests", "what needs testing").
tags: [playwright, test-coverage, coverage-gaps, e2e, routes, prioritization, test-planning]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/coverage
---

# Playwright Coverage Gaps

Map all testable surfaces, identify tested vs missing, prioritize by business impact.

## Steps

1. **Map application surface** — routes/pages (scan Next `app/`, React Router, Vue Router), interactive components (forms/modals/dropdowns/tables, complex-state ones), API endpoints (route files/controllers), critical user flows (auth, checkout, onboarding, core features).

2. **Map existing tests** — scan all `*.spec.ts/.js`: which routes (`page.goto()` calls), which components (locator usage), which endpoints (mocked/hit), tests per area.

3. **Coverage matrix** — table of Area | Route | Tests | Status (✅ Covered / ⚠️ Partial / ❌ Missing).

4. **Prioritize gaps** — Critical (auth, payment, core) → test first; High (user-facing CRUD, search, nav); Medium (settings, edge cases); Low (static pages).

5. **Suggest a test plan** — per gap: number of tests, which template, effort (quick/medium/complex), grouped by priority.

6. **Optionally auto-generate** — ask "Generate tests for top N gaps?"; if yes, generate per gap with the recommended template.

## Output
Coverage matrix, coverage % estimate, prioritized gap list with effort estimates, option to auto-generate.
