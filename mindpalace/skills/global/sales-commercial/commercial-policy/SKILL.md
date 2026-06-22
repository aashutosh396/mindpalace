---
name: Commercial Policy Design
description: Use when designing or revising a company's discount policy — building a data-backed discount matrix (ARR band × term × payment terms × strategic value), an exception flow with compensating commitments, and linting the matrix for governance defects.
tags: [commercial, discount-policy, discount-matrix, exception-flow, governance, deal-framework, approval-thresholds]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/commercial-policy
---

# Commercial Policy Design

Designs the **rules of engagement** governing discounts off list price — the artifact Deal Desk and AEs operate under. Output is the policy itself (matrix + exception flow + lint report), NOT a per-deal application. Assumes list price already exists.

## Workflow
1. **Audit current discount distribution** — pull last 4 quarters of closed-won + closed-lost. Per deal capture: arr, discount_pct, term_months, payment_terms_days, strategic_value, win/lost, nrr_12mo.
2. **Design the data-backed matrix** — 4 dimensions (ARR band × term length × payment terms × strategic value tier). Each cell carries: approved discount band, approver tier (AE/Manager/Director/VP/CFO), margin floor, observed win-rate + NRR. Cells with n<5 deals flagged THIN. Profile by saas/enterprise-software/api/marketplace/services.
3. **Design the exception flow** — per severity band (0-5 pts over, 5-10, 10-20, 20+), enforce required compensating commitments (multi-year prepay + named expansion path + reference commitment + MSA tightening). Produce machine-readable audit-trail metadata. Flag precedent risk if 3+ similar exceptions landed in the trailing quarter.
4. **Lint the matrix** — BLOCKER/MAJOR/MINOR across ~10 rules: approver inversion, band inversion, margin-floor violation, coverage gaps, cliff edges, undefined strategic tiers, thin data backing. Resolve every BLOCKER before publishing.
5. **Publish + quarterly review** — versioned artifact; re-run builder + linter every quarter on the rolling 4Q corpus. Cells where observed NRR < target are flagged for review.

## Key principle
The matrix is **data-backed, not data-driven**: bands are set by constraints + profile; observed data is annotation. If observed NRR < target, that's a signal to REVIEW the band, not to discount deeper.

## Anti-patterns
- Setting bands without data backing ("VP argued for it in Slack" is not backing).
- Letting precedent set policy (3+ similar exceptions = the matrix is wrong, not the deal).
- Approving exceptions without compensating commitments (discount-for-nothing is a leak).
- Cliff edges at round-number ARR thresholds (causes deal-size gaming — smooth the gradient).
- "Strategic value" as an undefined catch-all (define with concrete tests).
- No quarterly review; skipping the lint pass before publishing.
- **Mixing CFO and CRO accountabilities** — CFO owns the margin floor; CRO/Head of Deal Desk owns the band cap. Same owner = predictable drift.

## Forcing questions (one at a time, recommended + canon)
1. Observed discount distribution last 4Q — median inside or outside the matrix? → pull the corpus first. (OpenView; RevOps Co-op)
2. Win-rate AND 12mo NRR at the current max band? → both; high win-rate + low NRR = buying logos with leaky retention. (Tunguz; Bessemer)
3. Who owns the margin floor vs the band cap — same person? → separate them. (Bain *Pricing Power*)
4. Is "strategic value" defined with concrete tests? → "top-20 named account in 2026 list" is a test; "important customer" is not. (SaaStr; Forrester)
5. Exceptions above max — what compensating commitments, in writing before sign-off? → min multi-year prepay + named expansion path. (Winning by Design; McKinsey)
6. Same exception approved 3+ times this quarter — is the matrix wrong? → rebuild, don't keep approving. (OpenView)
7. When did you last re-run the matrix against the last 4Q? → quarterly. (OpenView; RevOps Co-op)
8. Machine-readable audit trail for every exception, or Slack/email? → structured record. (Salesforce CPQ; Forrester)
