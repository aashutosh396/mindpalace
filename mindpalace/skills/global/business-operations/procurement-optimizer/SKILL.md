---
name: Procurement Optimizer
description: Use when running an annual SaaS/spend audit, doing category-level spend review, or rationalizing the supplier base — UNSPSC-aligned spend categorization with Pareto, purchasing-cycle bottleneck analysis, and risk-balanced supplier consolidation that refuses single-source for tier-1 without a break-glass plan.
tags: [procurement, spend-audit, saas-audit, spend-categorization, supplier-consolidation, unspsc, pareto, renewal-cluster, category-strategy]
source: alirezarezvani/claude-skills
derived_from: business-operations/procurement-optimizer
---

# Procurement Optimizer

Head of Procurement / BizOps / VP Finance running the annual category review. Decides **what to buy, from whom, on what cadence** — not how a chosen vendor performs (that's vendor-management). Categorize spend (UNSPSC-aligned), find the Pareto 20% driving 80% of cost, surface purchasing-cycle bottlenecks, produce a risk-balanced consolidation plan.

## When NOT to use

Scoring a vendor you've decided to keep → vendor-management · financial close/P&L → finance · contract terms → legal · outbound proposals → sales.

## Workflow

1. **Intake spend** — line items `{supplier, description, category_hint, annual_spend, frequency, currency}`; include prior-year for YoY.
2. **Categorize + find Pareto** — map each line to a UNSPSC-aligned Class→Family→Segment (≈30 tech-startup categories, not the 100k DB). Output: categorized items, which 20% of categories drive 80% of spend, top-10 YoY growth categories. Profiles re-prioritize the map (tech-startup / scaleup / enterprise / services / manufacturing).
3. **Analyze purchasing cycle** — per category, T-request→T-PO and T-PO→T-pay (median, P90), approver-hop count. Flag categories with cycle time > 2× cross-category median as **bottleneck** (Goldratt TOC applied to procurement: throughput = slowest step, usually legal review on services or security review on tier-1 SaaS).
4. **Plan consolidation with risk balancing** — find duplicate-function clusters (3 monitoring tools, 2 expense platforms). Per cluster: pick a winner; **refuse to collapse any tier-1 category to single-source without a documented break-glass plan** ("DO NOT CONSOLIDATE — tier-1, no break-glass; add a 72-hour contingency first"); estimate savings = cluster spend − winner spend − migration cost; flag renewal-date clusters (≥3 contracts same month = no leverage).
5. **Synthesize** — top 5 YoY-growth categories, top 3 bottlenecks, top 5 consolidation opportunities (savings + risk flags), renewal clusters, tier-1 single-source exposure needing break-glass.

## Key Rule

Supplier criticality (tier-1/2/3) is a **user judgment call** (tier-1 = revenue-blocking if it disappears), not inferred from spend. Output artifacts are inputs to a human decision, not the decision.

## Anti-Patterns

Consolidate tier-1 to single-source without break-glass · categorize by vendor name not by what's purchased (Workday = HR *or* Finance depending on modules) · ignore renewal clustering · approve-by-default sub-$5k (death-by-a-thousand-SaaS) · no quarterly renewal review · rationalize without measuring switching cost (save $50k when migration costs $200k isn't savings) · consolidate on price ignoring integration debt · treat shadow IT as marketing's problem (it's procurement's — #1 SaaS-spend driver in scaleups).

## Forcing Questions (one at a time, recommended + canon)

1. **UNSPSC taxonomy or categorizing by vendor name?** → by what's purchased. (UNSPSC; A.T. Kearney.)
2. **Of your top-10 categories, which 3 grew most YoY — and why?** → name them before opening the tool; if you can't, that's the diagnosis. (BCG; Hackett.)
3. **Per duplicate cluster, what's the switching cost vs the savings?** → estimate explicitly; refuse consolidation without it. (BCG; Spend Matters.)
4. **For any tier-1 consolidation, what's the 72-hour break-glass plan?** → documented + tested contingency; if absent, don't consolidate. (NotPetya/M.E.Doc; NIST SP 800-161.)
5. **What % goes through PO vs expense vs shadow IT — where's the maverick spend?** → measure it (A.T. Kearney: 10-40% maverick in unmonitored cos).
6. **How many top-20 contracts renew the same month? Do you have a renewal calendar?** → build it, spread renewals. (IACCM/WorldCC.)
7. **Approval threshold for net-new SaaS under $5k — who owns the sprawl?** → tightened threshold + single owner (Productiv/Zylo: 50%+ of sprawl is sub-$5k).
