---
name: featured-snippet-optimizer
description: "Use when you want to win a featured snippet (position zero) for a keyword you already rank for in positions 1-5. Checks the current snippet format, analyzes your page, and rewrites the relevant section to match the format Google wants. Triggers: featured snippet, position zero, win the snippet, snippet optimization, answer box, rich answer, capture the snippet."
version: 1.0.0
license: MIT
tags: [featured-snippet, position-zero, seo, on-page, answer-box, serp, content-optimization]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/featured-snippet-optimizer
derived_from: awesomeclaude
---

# Featured Snippet Optimizer

Featured snippets earn roughly 42.9% CTR vs 39.8% for organic #1 without one. If you rank positions 1–5 and don't hold the snippet, you're leaving clicks on the table. This finds the gap and fixes it.

## When to use

You already rank top 5 for a keyword and want the snippet. From position 6+, fix the ranking first (use `improve-content` or `keyword-deep-dive`).

## Input

Target keyword (required) and your page URL that already ranks for it (required).

## Steps

1. **Check the current snippet** — Google the keyword. Is there a snippet? Who holds it (you or a competitor)? Format (paragraph / ordered list / unordered list / table)? Exact text? No snippet at all = the slot is up for grabs.

2. **Classify the query format** — Google matches format to query type:

| Query type | Snippet format |
|---|---|
| "What is X" | Paragraph (40–60 words) |
| "How to X" | Ordered list |
| "X list" / "types of X" | Unordered list |
| "X vs Y" | Table or paragraph |
| "Best X" / "top X" | Unordered list with brief |
| "When did X" / "who is X" | Short paragraph (<50 words) |
| Numeric answer | Short phrase or table |

3. **Fetch and read your page** — where do you answer the query? Right format? Clean and self-contained? Right length (40–60 words for paragraph; 3–8 items for list)?

4. **Identify the gap** — common failures: wrong format; answer too long (truncated ~60 words / 8–10 items); too short; buried mid-article instead of directly under a matching H2; not self-contained; not in a heading→answer structure.

5. **Rewrite** — new answer optimized for the snippet: start with an H2/H3 that restates the query verbatim; answer directly and completely in the first 40–60 words (no preamble, no "it depends"); use the correct format; be self-contained; include the keyword naturally in the first 20 words. Provide two versions — the snippet answer block, and a longer follow-up paragraph after it.

6. **Supporting structure** — H2 with the exact query phrasing immediately above the answer; optional 1–2 sentence intro; the 40–60 word answer or 3–8 step list; deeper explanation AFTER. The answer block must be the FIRST substantial thing under the matching H2.

7. **Format-specific rules** — Paragraph: complete sentence, direct, keyword in first 20 words, no "in this guide" fluff. Ordered list: 3–8 steps, each = one action verb + one sentence, self-contained, "1. 2. 3." numbering. Table: clear headers, 3–6 rows, cells 1–10 words.

## Output

Current state (holder, format, text); your page analysis (position if known, where answer appears, format gap); the rewrite (new H2, answer block, follow-up); implementation notes (where to place it, keep the rest intact, the FIRST instance is what Google extracts); realistic timeline (picks up in 1–4 weeks; don't re-edit for 2 weeks after).

## What to ignore

- Targeting snippets from position 6+ — fix ranking first.
- AI-Overview-heavy queries — AIO has largely replaced snippets for informational intent; check a snippet actually shows.
- Schema tricks (help rich results, not snippets) and keyword stuffing.
