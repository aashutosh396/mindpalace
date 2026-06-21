---
name: headless-web-scraping
description: "Use when simple HTTP/WebFetch is insufficient — JS-rendered SPAs, Cloudflare/anti-bot-protected sites, or structured multi-element extraction needing DOM traversal. Picks the right scrapling fetcher tier (HTTP, stealth Chromium, or full browser), extracts with CSS selectors, and scrapes ethically. Triggers: web scraping, headless browser, scrapling, Cloudflare, JS-rendered, extract data, parse HTML, CSS selector, anti-bot."
version: 1.0.0
license: MIT
tags: [web-scraping, headless, scrapling, automation, data-extraction, css-selectors, anti-bot, python]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/headless-web-scraping
prerequisites: ["python", "pip install scrapling", "python -m playwright install chromium (for stealth/dynamic tiers)"]
derived_from: awesomeclaude
---

# Headless Web Scraping

Extract data from pages that resist simple HTTP requests, using scrapling's three-tier fetcher architecture and CSS-based extraction.

## When to Use

- Page requires JS rendering (SPA, React, Vue)
- Site has anti-bot protections (Cloudflare Turnstile, TLS fingerprinting)
- You need structured extraction of multiple elements via CSS selectors
- Simple WebFetch or requests.get() returns empty or blocked responses

## Procedure

### Step 1 — Select fetcher tier
Try `Fetcher` first and escalate on failure:
- `Fetcher` — static HTML, no protection (fastest)
- `StealthyFetcher` — 403/503, Cloudflare challenge, TLS fingerprint checks (best default for modern sites)
- `DynamicFetcher` — page loads but content area empty, or needs click/scroll; use `wait_selector`
- altcha proof-of-work CAPTCHA → cannot be automated; document and fall back to manual.

### Step 2 — Configure the fetcher
Use the `configure()` method (constructor kwargs are deprecated in v0.4.x). Set `timeout`, `retries`, `follow_redirects` for Fetcher; add `headless=True`, `network_idle=True`, and `wait_selector` for the browser tiers. If the browser binary is missing, run `python -m playwright install chromium`.

### Step 3 — Fetch and extract
API: `response.find("selector")` (first match), `response.find_all("selector")` (all), `element.get("attr")`, `element.get_all_text()` (recursive text), `element.html_content` (raw inner HTML). Do NOT use `.css_first()` — it is not part of scrapling. If `find()` returns None, inspect `response.html_content` to verify the selector; if text is empty, content may be in shadow DOM/iframe (use DynamicFetcher + wait_selector).

### Step 4 — Handle failures and edge cases
Implement tier fallback (Fetcher → Stealthy → Dynamic) with CAPTCHA detection (scan text for "altcha"/"proof of work" and stop, don't retry). On 403/503 escalate; on persistent 403 across all tiers the site blocks automation — document for manual access. Increase timeout to 120s for slow CDNs; add cookies/auth for session-gated sites.

### Step 5 — Rate limiting and ethics
Check `robots.txt` (urllib.robotparser) before bulk runs and respect Disallow. Minimum 1s delay between requests; descriptive User-Agent; cache responses; do not scrape personal data without legal basis; stop immediately on 429 (raise delay to 3-5s) or IP ban.

## Validation

- [ ] Correct fetcher tier (not over/under-powered)
- [ ] `configure()` used, not deprecated constructor kwargs
- [ ] Selectors verified against actual page source
- [ ] `.find()` / `.find_all()` used (not `.css_first()`)
- [ ] CAPTCHA detection in place (altcha reported, not retried)
- [ ] Rate limiting + robots.txt checked for bulk
- [ ] Extracted data non-empty and structurally correct

## Common Pitfalls

- Using `.css_first()` (AttributeError) instead of `.find()`.
- Starting with DynamicFetcher (10-50x slower) — escalate, don't start there.
- Constructor kwargs instead of `configure()`.
- Ignoring altcha CAPTCHA.
- No rate limiting (IP ban / service degradation).
- Assuming stable selectors — validate before each campaign.

## Related

- use-graphql-api — prefer a GraphQL endpoint over scraping when available
- serialize-data-formats — convert extracted data to JSON/CSV
