---
name: Playwright Test Reporting
description: Use when generating a Playwright test report or results summary ("test report", "results summary", "show results", "how did tests go", "test dashboard").
tags: [playwright, test-report, results, slack, testrail, ci, trend-analysis, flaky-tests]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/report
---

# Playwright Test Reporting

Generate reports that route into the user's existing workflow — zero new tools.

## Steps

1. **Run if needed** — check `test-results/`/`playwright-report/`; if stale, `npx playwright test --reporter=json,html,list`.

2. **Parse JSON** — total/passed/failed/skipped/flaky, duration per test + total, failed names + errors, flaky (passed on retry).

3. **Detect destination & route automatically:**

| Check | If found | Action |
|---|---|---|
| `TESTRAIL_URL` | TestRail configured | push results |
| `SLACK_WEBHOOK_URL` | Slack configured | post summary |
| `.github/workflows/` | GitHub Actions | results → PR comment via artifacts |
| `playwright-report/` | HTML reporter | open/serve report |
| none | default | markdown report |

4. **Generate report** — always a markdown report (summary counts, failed-tests table with error+file:line, flaky table, by-project/browser breakdown) saved to `test-reports/{date}-report.md`. Plus Slack summary (curl webhook), TestRail push, or `npx playwright show-report` per destination.

5. **Trend analysis** — if previous reports exist in `test-reports/`: compare pass rate over time, identify newly-flaky tests, distinguish new vs recurring failures.

## Output
Pass/fail/skip/flaky summary, failed details with errors, destination confirmation, trend comparison, next-action recommendation.
