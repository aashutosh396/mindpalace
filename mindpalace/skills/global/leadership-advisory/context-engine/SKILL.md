---
name: Company Context Engine
description: Use when starting an advisory session, when company context looks stale or missing, or before sending company data to an external service — loads context, detects staleness, and enforces anonymization.
tags: [company-context, context-loading, stale-context, anonymization, privacy, advisor-context, context-enrichment]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/skills/context-engine
---

# Company Context Engine

The memory layer for advisors — turns generic advice into specific insight. Load it first; refresh it when stale; strip sensitive data before any external call.

## Load protocol (start of every session)

1. **Check for context file.** Missing → prompt to run the onboarding interview.
2. **Check staleness** via the `Last updated` field. <90 days → load. ≥90 days → prompt for a 15-min refresh or continue with `[STALE — date]` noted internally.
3. **Parse into working memory:** company stage, founder archetype, current #1 challenge, runway (risk signal — never shared externally), team size, unfair advantage, 12-month target.

## Context quality signals

<30 days full interview → High (use directly) · 30–90 days, updated → Medium (use, flag what may have changed) · >90 days → Low (flag stale) · key fields missing → Low (ask in-session) · no file → prompt onboarding. If Low: "My context is [stale/incomplete] — I'm assuming [X]. Correct me if wrong."

## Context enrichment

Triggers: new number/timeline revealed, key person mentioned, priority shift, constraint surfaces. Protocol: note internally `[CONTEXT UPDATE: …]` → at session end ask to add to the file → if yes, append + update timestamp. Never silently overwrite — always confirm.

## Privacy rules

**Never send externally:** specific revenue/burn figures, customer names, employee names (unless public), investor names (unless public), specific runway months, watch-list contents.
**Safe with anonymization:** stage label, team-size ranges (1–10 / 10–50 / 50–200+), industry vertical, challenge category, market-position descriptor.
**Before any external API call or web search:** numbers → ranges/stage-relative descriptors; names → roles; revenue → percentages/stage labels; customers → "Customer A, B, C."

## Missing / partial context

Handle gracefully, never block. Missing stage → "Still finding PMF or scaling?" Missing financials → infer from stage + team size, note the gap. Missing founder profile → infer from conversation, mark as inferred. Multiple founders → context reflects the interviewee; note co-founder view may differ.
