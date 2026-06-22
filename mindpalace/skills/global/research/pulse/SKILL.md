---
name: Multi-Source Recency Pulse
description: Use when the user wants the current conversation on a topic ("pulse on X", "what's happening with X", "what are people saying about X", "trending: X") — synthesizes Reddit + Hacker News + open web (+ optional X) within a recent window into one briefing with citations, engagement signals, and cross-platform patterns.
tags: [pulse, sentiment, trends, reddit, hacker-news, recency, social-listening, buzz]
source: alirezarezvani/claude-skills
derived_from: research/pulse (Multi-Source Recency Research)
---

# Pulse — Multi-Source Recency Research

Captures the **current conversation**, not the canonical reference. Output is one coherent briefing with citations + engagement signals + cross-platform pattern analysis, within a configurable window (default 30 days).

## Phase 0: Intake (2-4 forcing questions, one at a time)
1. **Topic specificity** — refuse "AI"; push once for an angle. After one push-back, deliver with "vague topic — survey level" caveat.
2. **Angle** — trend / sentiment / problems / opportunities / comparison. Dictates which sources weight more.
3. **Time window** — 7/14/30/60/90 days (default 30).
4. **Platform scope** (only if some clearly off-target) — default all (Reddit + HN + web + X if available).

## Pre-flight
Compute window timestamps (HN `created_at_i>`, Reddit `t=`). Generate output slug + duplicate-date check. Start three-count audit log.

## Phases 1-3 (parallel platforms; sequential within each, 1 q/sec)
- **Reddit** (`reddit.com/search.json`, unauthenticated): `sort=top&t=<window>` + `sort=new&t=<window>`; fetch comments for top 3-5 posts. On 429/ratelimit: wait 3s, retry, fall back to subreddit-restricted or `?raw_json=1`.
- **Hacker News** (Algolia `hn.algolia.com/api/v1/`): stories + comments in window. If empty: broaden query, then drop timestamp filter (label "outside window"). Note HN's technical/builder bias in synthesis.
- **Web** (WebSearch + WebFetch): trusted publishers (`site:` filter + `after:`) → recent reviews → honest-opinion/problems queries. Fetch top 3-5 URLs per query; cite only fetched URLs, never snippets alone.

## Phase 4: X/Twitter (optional, last)
Try Grok → X API → browser automation → skip with documented note. If skipped: emit `## X/Twitter` header with `Skipped — [reason]`. Never fake data.

## Synthesis (cross-platform)
Consensus (3+ platforms agree = highest confidence) · controversy · pain points · excitement · emerging trends (in `sort=new` but not `sort=top`) · gaps. Cite source URLs per pattern.

## Output
Markdown file + chat paste. Sections: TL;DR → Reddit → Hacker News → Web → X (or skipped) → Cross-Platform Patterns → Key Takeaways → Content Angles → Audit (queries sent per platform / received / cited).

## Agent Integrity Rules
Cite only this-session sources; training tagged "[Background — not from search]". Three counts. Retry once after 3s; after 3 consecutive failures across sources, stop and return what was collected — never an empty file.

## Anti-Patterns
Searching before topic is committed; batching intake; hardcoded fragile URLs; tight coupling to one X interface; missing fallbacks; citing training knowledge; fabricating sources to fill a section.
