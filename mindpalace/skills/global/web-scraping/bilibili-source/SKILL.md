---
name: Bilibili Video Data Fetcher
description: Use when working with a Bilibili (B站) video and you need real, citable numbers or metadata — stats, UP follower count, tags, per-part cids, full danmaku — instead of hand-typing or estimating. Accepts BVID/av/b23.tv/URL.
tags: [bilibili, b站, video, danmaku, stats, scraping, metadata, api, citable, login-free]
source: daymade/claude-code-skills
derived_from: bilibili-source
---

Fetch **real, verifiable** Bilibili video data so you can cite it instead of guessing. Hand-typed/estimated engagement numbers are how a knowledge base rots — these scripts make the numbers cheap to fetch.

## Quick start
```bash
scripts/bili-fetch.sh BV1xxxxxxxxx
```
Returns one JSON object from a single `view/detail` call: bvid, aid, `fetched_at`, url, title, up (name/mid/fans), pubdate, tname (partition), tags, duration_s, stat (view/like/coin/favorite/share/reply/danmaku), and pages[] (per-part cid/page/part/duration). Accepts BVID, av number, b23.tv short link, or full URL — normalizes all.

## Scripts
| Script | Does | Login |
|--------|------|-------|
| `bili-fetch.sh <ref>` | Core: metadata + live stats (run first) | No |
| `bili-danmaku.sh <ref> [P]` | Danmaku (time-synced bullet comments) full text for a part | No |
| `bili-subs.sh <ref> [browser]` | Subtitle/transcript track | **Yes** |
| `bili-selftest.sh` | Health-check every capability vs live API | No |

All execute (don't read as reference). `bili-danmaku.sh` reuses `bili-fetch.sh` to resolve the part's cid — keep them siblings. Danmaku are a Bilibili-specific signal of *where/how* viewers reacted, richer than a flat reply count.

## Rules that keep data honest
- **Live metrics → always cite `fetched_at`.** Re-fetched minutes later it drifts — that's proof it's live; a bare "12,000 views" with no timestamp silently goes stale.
- **No fabrication.** If a number can't be fetched, write "未获取/未核实" — never estimate.
- **Network quirks handled by the scripts:** they strip the local proxy (Bilibili is a CN service a 127.0.0.1 proxy breaks), send browser UA + Referer (avoids HTTP 412), retry with backoff. Do the same if calling by hand.
- **CJK collation trap:** when grepping/sorting fetched Chinese text, `sort`/`comm` mishandle CJK and report false "missing". Verify with `find -name` or `grep -F`, not `comm`.

## Subtitles require login (no bypass)
Stats/danmaku are login-free; subtitles are NOT — the public API returns an empty list for anonymous requests. `bili-subs.sh` needs the user's browser cookies — ask before running. The `ai-zh` track is AI-generated; treat as a draft transcript, mark it AI-ASR, don't claim verbatim.

## Maintenance
Third-party API drifts (field renames, WBI signing, anti-bot). Run `scripts/bili-selftest.sh` after a gap or when output looks wrong — one PASS/FAIL row per capability surfaces drift instead of a silent wrong answer.
