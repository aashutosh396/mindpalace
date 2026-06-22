---
name: R&D Program Finance
description: Use when managing money for an internal R&D program/portfolio — building a multi-period budget with the F&A (indirect) split, tracking burn rate and runway against milestones, and routing R&D costs to a capitalize-vs-expense determination (decision-support only, never books the entry).
tags: [research-finance, rd-budget, burn-rate, runway, fa-rate, indirect-rate, capitalize-vs-expense, ias-38, asc-730, portfolio]
source: alirezarezvani/claude-skills
derived_from: research-ops/skills/research-finance
---

# R&D Program Finance

Financial management of internal R&D programs (money already allocated/raised — NOT corporate close/valuation, NOT the next round, NOT grant discovery). Every number ships with its **assumptions block**; accounting-treatment calls **route to a named finance owner** — this skill never books an entry.

## Workflow
1. **Lay out the program** — work-package line items, categories, per-period amounts.
2. **Build the budget** — apply the F&A (indirect) rate to an MTDC-style eligible base; roll up direct / F&A / fully-loaded cost per period with an explicit assumptions block. Profile by pharma-rd/biotech/medtech/deep-tech/software-rd/university-lab. Capital equipment, large subaward portions, and certain categories are MTDC-exempt — exclude them from the F&A base.
3. **Track burn & runway** — average + trailing (recent-weighted) burn as the forward run-rate; runway in months; per-milestone reachability before cash runs out. Flag accelerating burn and below-threshold runway.
4. **Route accounting treatment** — score each cost item against IAS 38 development-phase criteria (or ASC 730 expense-as-incurred for US GAAP) → CAPITALIZE-CANDIDATE / EXPENSE / FINANCE-OWNER-REVIEW with a named owner. Never auto-decides.
5. **Assemble the review** — every number carries assumptions; treatment calls carry a named owner.

## Anti-patterns
- Stating a budget number without its assumptions (F&A rate, escalation, base must travel with it).
- Auto-deciding capitalize-vs-expense — the tool routes; the controller (and auditor) decides.
- Using lifetime-average burn for runway — recent burn is the honest forward run-rate.
- Applying F&A to the full base — respect MTDC exemptions.
- Confusing this with corporate finance (valuation/close/fundraise live elsewhere).

## Forcing questions (one at a time, recommended + canon)
1. Research phase or development phase — can you evidence technical feasibility? → research = expense; development = capitalize-candidate only with evidence, routed to a named owner. (IAS 38.54-57; ASC 730)
2. What F&A/indirect rate — negotiated NICRA, de minimis 10%, or assumption? → use the negotiated rate; flag if assumed. (2 CFR 200)
3. Runway in months at current burn — clears the next value-inflection milestone? → must cover milestone + buffer; surface the gap. (Cooper stage-gate; a16z/Bessemer)
4. Portfolio ROI risk-adjusted (rNPV / PoS-weighted) or raw NPV? → risk-adjusted; raw overstates R&D value. (rNPV; real-options)
5. Who is the named finance/controller owner signing the treatment? → name them — recommends, never books. (ASC 730 / IAS 38 governance)

The F&A rate is the most error-prone input — confirm it is a negotiated NICRA, not a guess.
