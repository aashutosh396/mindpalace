---
name: Founder Interview / Company Onboarding
description: Use when setting up a virtual C-suite or advisor system for a company, or when advisors lack company context (e.g. before a first board meeting or after a fundraise) — a 12-question founder interview that populates a durable company-context file.
tags: [onboarding, founder-interview, company-context, stage, icp, runway, priorities, risks, advisory]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/onboard
---

# Founder Interview

A structured interview producing a single `company-context.md` — the file every advisor reads before responding. Without it, advice is guesswork.

## The interview (12 questions)
**Company basics**
1. Company name + one-sentence pitch.
2. Stage: pre-seed / seed / A / B / C+ / public.
3. Headcount: total + by function (eng/product/GTM/ops/G&A).
4. Geographic distribution: HQ + remote split, key countries.

**Business model**
5. Revenue model: subscription / usage / transaction / marketplace / hardware / services.
6. ICP: name one real customer; what do they share with others?
7. ACV: median + range; deal count last 12 months.
8. Growth rate: ARR YoY; if pre-revenue, the leading metric.

**Financial posture**
9. Runway: months of cash at current burn; bear-case months.
10. Last raise: amount, valuation, lead, date.

**Strategic context**
11. Top 3 priorities for the current quarter (plain language).
12. Top 3 risks the founder loses sleep over (be specific).

## Output (company-context.md)
Sections: Identity, Business, Financial, Team, Quarter (priorities + risks), Routing Hints. Quote the founder's own words wherever possible (especially the ICP) — don't paraphrase. Write `[not captured]` for anything the quick intake doesn't reach.

## Workflow
1. Walk all 12 questions. 2. Save to `company-context.md`. 3. Read it back and ask "anything missing?"

## When to re-run
After a fundraise (numbers change), a major pivot/launch, every 6+ months (facts drift), or before any high-stakes board deliberation.
