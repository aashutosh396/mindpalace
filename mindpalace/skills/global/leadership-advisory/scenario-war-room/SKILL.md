---
name: Scenario War Room (Cascading What-If)
description: Use when facing compound multi-variable risk ("what if we lose our top customer AND miss the Q3 raise?") — models cascading adversity across all business functions with a 6-step cascade model, three severity levels, early-warning triggers, and act-now hedges. Not a single-assumption stress test.
tags: [scenario-planning, war-room, what-if, cascading-risk, compound-risk, contingency, early-warning, hedge]
source: alirezarezvani/claude-skills
derived_from: scenario-war-room
---

# Scenario War Room

Models cascading what-if scenarios across all functions — compound adversity that shows how one problem creates the next. Not single-assumption stress testing; not finance-only; not worst-case-only; not paralysis (outputs concrete hedges + triggers).

## 6-Step Cascade Model

**1. Define variables (max 3).** Each: what changes (quantified), probability, timeline. (e.g., "Top customer (28% ARR) gives 60-day termination notice — 15% — within 90 days".)

**2. Domain impact mapping.** Per variable, each role models impact: CFO (burn/runway/bridge), CRO (ARR gap/churn cascade/pipeline), CPO (roadmap/PMF), CTO (velocity/key-person), CHRO (attrition/freeze), COO (capacity/OKR), CISO (compliance), CMO (CAC/competitive).

**3. Cascade effect mapping (the core).** Show how variable A triggers consequences that trigger variable B's effects. Example: customer churn ($560K ARR) → CFO runway 14→8mo → CHRO hiring freeze + retention risk → CTO reqs frozen + roadmap slips → CPO feature delayed → CRO NRR drops + more churn → potential death spiral. Name the cascade explicitly; show where it can be interrupted.

**4. Severity matrix.** Base (one variable; manageable) / Stress (two simultaneously; significant response) / Severe (all; existential, board intervention). Per level: runway, ARR, headcount impact + timeline to unacceptable state.

**5. Trigger points (early warning).** Measurable signals that a scenario is unfolding *before* confirmed. (Churn: sponsor dark >3wk, usage −25% MoM, no Q1 QBR confirmed. Fundraise delay: <3 term sheets after 60d, lead requests >30d DD extension. Attrition: Glassdoor activity, 2+ referral interview requests.)

**6. Hedging strategies.** Per scenario, act NOW (before it materializes): hedge / cost / impact / owner / deadline. (e.g., $500K credit line — $5K/yr — buys 3mo if churn hits — CFO — 60d.)

## Output Format
```
SCENARIO + variables + most-likely path (with probability)
SEVERITY: Base / Stress / Severe (runway+ARR impact, existential y/n)
CASCADE MAP (A → impact → B trigger → impact → end state)
EARLY WARNING SIGNALS (signal → which scenario)
HEDGES (action / cost / impact / owner / deadline)
RECOMMENDED DECISION (one paragraph: what, in what order, why)
```

## Rules
Max 3 variables (more is noise). Quantify or estimate ("$420K ARR at risk over 60 days", not "revenue drops"). Don't stop at first-order effects — the damage is in the cascade. Model recovery, not just impact. Separate base case from sensitivity. 3-4 scenarios per planning cycle (more = paralysis).
