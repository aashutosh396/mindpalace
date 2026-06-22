---
name: Scrapling CLI (web extraction)
description: Use when extracting HTML/Markdown/text from a webpage with Scrapling CLI — diagnose the install, choose static vs dynamic fetch, handle WeChat articles, and validate saved output instead of trusting exit codes.
tags: [scrapling, web-scraping, cli, wechat, static-dynamic, playwright, extraction, validation]
source: daymade/claude-code-skills
derived_from: scrapling-skill
---

# Scrapling Skill

Use Scrapling CLI as default. Start with the smallest working command, validate the saved output, escalate only when static fetch lacks real content. Don't assume the install is healthy — verify first.

## Workflow
1. **Diagnose**: `python3 scripts/diagnose_scrapling.py` — source of truth for next step.
2. **Fix install**:
   - CLI missing `click`/extras → `uv tool uninstall scrapling && uv tool install 'scrapling[shell]'` (avoid `[all]` unless needed).
   - Browser fetchers needed → `scrapling install` (Playwright runtime). Don't claim success until it reports already-installed OR diagnostic confirms Chromium + Chrome Headless Shell.
3. **Choose fetcher**: `extract get` for normal/article/most WeChat pages → `extract fetch` when static HTML lacks real content / JS-rendered → `extract stealthy-fetch` only after `fetch` fails on anti-bot (never default).
4. **Run smallest command** (always quote URLs — mandatory in zsh with `?`/`&`):
   - `scrapling extract get 'URL' page.html`
   - `scrapling extract get 'URL' article.md -s 'main'`
   - `scrapling extract fetch 'URL' page.html --timeout 20000`
   - WeChat body: `scrapling extract get 'https://mp.weixin.qq.com/s/ID?scene=1' article.md -s '#js_content'`
5. **Validate** (never trust exit code): `wc -c article.md`, `sed -n '1,40p'`, `rg -n '<title>|js_content|rich_media_title|main' page.html`. Tiny/empty/missing container → back to step 3.

## Failure modes
- TLS `curl: (60) SSL certificate problem` → local trust-store issue, retry with `--no-verify` (only after confirming the cert error pattern; not by default).
- WeChat: `get` before `fetch`, `-s '#js_content'`, validate immediately.
- `fetch` fails → re-diagnose, confirm browsers present, longer timeout, then stealthy-fetch.

## Guardrails
Verify before reinstalling. Don't default to the Python library when user means CLI. Don't jump to browser unless static lacks content. Inspect the saved file, not just exit code. No hardcoded user-specific absolute paths.
