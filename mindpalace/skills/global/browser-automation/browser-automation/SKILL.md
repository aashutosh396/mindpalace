---
name: Browser Automation (Playwright)
description: Use when you need to scrape websites, fill multi-step forms, capture screenshots/PDFs, or build repeatable browser data pipelines (not E2E testing) — production-grade Playwright patterns with anti-detection.
tags: [playwright, scraping, browser-automation, web-scraping, screenshots, form-filling, anti-detection, pagination, headless]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/browser-automation
---

# Browser Automation

Production-grade web automation with Playwright. For data extraction and workflow automation — NOT testing (use a test framework for E2E). Playwright wins over Selenium/Puppeteer: auto-wait, multi-browser one API, network interception, browser contexts, codegen, async-first.

## Core competencies

### 1. Selector priority (most → least reliable)
1. `data-testid`/`data-id` custom attributes (stable across redesigns)
2. `#id` selectors (unique, may change on deploy)
3. Semantic: `article`, `nav`, `main`, `section`
4. Class-based: `.product-card` (brittle if generated, e.g. CSS modules)
5. Positional: `nth-child()` (last resort)

Use XPath only when CSS can't express the relationship (ancestor traversal, text selection).

### 2. Forms & multi-step workflows
One function per step: fill fields, click Next, wait for next step (URL change OR DOM element). Key APIs: `fill()`, `select_option()`, `set_input_files()`, `expect_file_chooser()`.

### 3. Screenshots & PDF
- Full page: `page.screenshot(path=..., full_page=True)`
- Element: `page.locator("div.chart").screenshot(...)`
- PDF (Chromium): `page.pdf(format="A4", print_background=True)`
- Visual regression: store baselines `{page}_{viewport}_{state}.png` in VCS

### 4. Structured extraction
Tables→JSON (thead headers + tbody rows), listings→arrays (field-selector map, `::attr()`), nested/threaded (recursive).

### 5. Session management
Save after login: `context.storage_state(path="state.json")`; restore: `browser.new_context(storage_state="state.json")`. Check session validity before a long job (request a protected page, verify no login redirect).

### 6. Anti-detection (priority order)
1. Remove `navigator.webdriver` via init script (critical)
2. Custom/rotating real user agents (never default headless UA)
3. Realistic viewport (1920x1080; default 800x600 is a red flag)
4. Random `random.uniform()` delays
5. Per-context proxy

### 7. Dynamic content
- SPA: `wait_for_selector` (not load event)
- AJAX: `page.expect_response("**/api/data*")`
- Shadow DOM: `page.locator("custom-element >> .inner")`
- Lazy images: `scroll_into_view_if_needed()`

### 8. Error handling
Retry with exponential backoff (1s,2s,4s); fallback selectors on TimeoutError; error-state screenshots; detect HTTP 429, respect `Retry-After`.

## Workflow patterns
- **Single page:** launch headed in dev → headless prod; goto + wait content selector; extract with field mapping; validate (nulls/types); output JSON.
- **Paginated:** extract current → check Next exists & enabled → click → wait NEW content (not just nav) → repeat to max → dedup by key → write incrementally.
- **Authenticated:** check session file → login+save if absent → navigate → fill steps → `expect_download()` → save_as.

## Anti-patterns
Hardcoded `wait_for_timeout` (use wait_for_selector/url/response); no retry; ignoring robots.txt/Crawl-delay; credentials in scripts (use env/secrets); no rate limiting; fragile auto-generated class selectors; not closing browsers (use try/finally); headed in production.
