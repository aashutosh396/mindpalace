---
name: Playwright Init
description: Use when setting up Playwright in a project ("set up playwright", "add e2e tests", "configure playwright", "init playwright", "add test infrastructure").
tags: [playwright, setup, e2e, configuration, ci, test-infrastructure, scaffolding, nextjs, vite, github-actions]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/init
---

# Playwright Init

Set up a production-ready Playwright environment: detect framework, generate config, structure, example test, and CI.

## Steps

1. **Analyze project** — `package.json` framework (React/Next/Vue/Angular/Svelte), `tsconfig.json` → TS else JS, whether `@playwright/test` is installed, existing test dirs (`tests/`/`e2e/`/`__tests__/`), existing CI config.

2. **Install** (if absent): `npm init playwright@latest -- --quiet`, or manual `npm install -D @playwright/test && npx playwright install --with-deps chromium`.

3. **Generate `playwright.config.ts`** — framework-adapted. Core: `testDir: './e2e'`, `fullyParallel: true`, `forbidOnly: !!process.env.CI`, `retries: CI ? 2 : 0`, `workers: CI ? 1 : undefined`, reporters `[['html',{open:'never'}],['list']]`, `use: { baseURL, trace: 'on-first-retry', screenshot: 'only-on-failure' }`, projects chromium/firefox/webkit, `webServer: { command, url, reuseExistingServer: !CI }`. baseURL/webServer per framework: Next/Vue/Nuxt `http://localhost:3000` `npm run dev`; React-Vite `:5173` `npm run dev`; Angular `:4200` `npm run start`; none → omit webServer.

4. **Folder structure** — `e2e/{fixtures/index.ts, pages/.gitkeep, test-data/.gitkeep, example.spec.ts}`.

5. **Example test** — homepage loads (`toHaveTitle(/.+/)`), visible navigation (`getByRole('navigation')`).

6. **CI workflow** — if `.github/workflows/` exists, create `playwright.yml` (checkout, setup-node lts, `npm ci`, `npx playwright install --with-deps`, `npx playwright test`, upload `playwright-report/` artifact retention 30d). If `.gitlab-ci.yml`, add a Playwright stage instead.

7. **`.gitignore`** — append `/test-results/`, `/playwright-report/`, `/blob-report/`, `/playwright/.cache/`.

8. **npm scripts** — `test:e2e`, `test:e2e:ui` (`--ui`), `test:e2e:debug` (`--debug`).

9. **Verify** — run `npx playwright test`; if it fails, diagnose and fix before finishing.

## Output
Confirm: config path + key settings, test dir + example, CI workflow (if added), npm scripts, how to run.
