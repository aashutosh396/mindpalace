---
name: Playwright on BrowserStack
description: Use when running Playwright tests on BrowserStack cloud grid for cross-browser/cross-device testing ("browserstack", "cross-browser", "cloud testing", "test on safari", "browser compatibility").
tags: [playwright, browserstack, cross-browser, cloud-testing, safari, firefox, webkit, compatibility, mcp]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/browserstack
---

# Playwright on BrowserStack

Run Playwright on BrowserStack's cloud grid for cross-browser/device coverage.

## Prerequisites
Env vars `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY` (from browserstack.com/accounts/settings). If unset, tell the user and stop.

## Capabilities

**Configure** — add BrowserStack projects to `playwright.config.ts` gated on `process.env.BROWSERSTACK_USERNAME`. Each project uses `connectOptions.wsEndpoint` = `wss://cdp.browserstack.com/playwright?caps=<encoded JSON>` where caps include browser, browser_version, os, os_version, and the username/accessKey. Provide chrome/firefox(playwright-firefox)/webkit(playwright-webkit) on Windows-11 / OS X Ventura. Add a local-projects fallback for when the env vars are absent. Add npm script `test:e2e:cloud`.

**Run** — verify credentials, then `npx playwright test --project='chrome@*' --project='firefox@*'` with the env vars exported; monitor and report per browser.

**Get build results** — `browserstack_get_builds` → latest build's sessions; per session report status, browser+OS, duration, video URL, log URLs; format as a table.

**Check browsers** — `browserstack_get_browsers`, filter Playwright-compatible, display combinations.

**Local testing** (localhost/staging behind firewall) — `npm install -D browserstack-local`, add the local tunnel to config.

## MCP tools
`browserstack_get_plan/browsers/builds/sessions/session/logs`, `browserstack_update_session`.

## Output
Cross-browser results table, per-browser pass/fail, dashboard links for video/screenshots, browser-specific failures highlighted.
