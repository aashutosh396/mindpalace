---
name: Douban Collection Export
description: Use when exporting or syncing a Douban (豆瓣) book/movie/music/game collection to local CSV — full export via the reverse-engineered Frodo API plus RSS incremental sync, no login/cookies/browser.
tags: [douban, 豆瓣, frodo-api, csv-export, rss-sync, books, movies, collection-backup]
source: daymade/claude-code-skills
derived_from: douban-skill
---

# Douban Collection Export

Export Douban collections (books/movies/music/games) to CSV. No official export exists.

## Why Frodo API (do NOT web-scrape)
Douban web pages use PoW (Proof of Work) challenges blocking all HTTP scraping. 7 approaches tested — only the Frodo API works. Do NOT attempt web scraping, `browser_cookie3`+requests, curl+cookies, or Jina Reader. The API key + HMAC secret are Douban's **public mobile-app credentials** (from the APK) — shared by all users, identify no one.

## Full export (primary)
```bash
DOUBAN_USER=<user_id> python3 scripts/douban-frodo-export.py
```
User ID is the part after `/people/` in `douban.com/people/<ID>/` (full URL auto-extracted). Env: `DOUBAN_USER` (required), `DOUBAN_OUTPUT_DIR` (optional). Python 3.6+ stdlib only. Output: `~/Downloads/douban-sync/<user_id>/`.

## RSS incremental sync (complementary)
```bash
DOUBAN_USER=<user_id> node scripts/douban-rss-sync.mjs
```
Returns only latest ~10 items (no pagination). Use full export first, RSS for daily updates.

## Output
Four UTF-8-BOM (Excel-compatible) CSVs: `书.csv`, `影视.csv`, `音乐.csv`, `游戏.csv`. Columns: `title, url, date, rating, status, comment`. Rating ★-★★★★★ (empty if unrated). Safe to re-run (overwrites).

## Limits
Cannot export reviews/notes/broadcasts; can't filter by single category in one run; private profiles return 0 silently.

## Workflow
Ask for user ID → run full export → verify counts (`wc -l <dir>/*.csv`) → optional RSS sync. Errors: code 996 = signature error; rate limits; row counts may be slightly below displayed due to delisted items.
