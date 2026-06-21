---
name: define-prioritization-framework
description: "Use when ranking a list of features or initiatives — runs RICE, ICE, MoSCoW, Weighted Scoring, and Kano against the candidates and shows where rankings agree and diverge. Triggers: prioritize features, RICE, ICE, MoSCoW, weighted scoring, Kano, roadmap prioritization, what to build first, rank initiatives, backlog triage."
version: 1.0.0
license: Apache-2.0
tags: [prioritization, rice, ice, moscow, weighted-scoring, kano, roadmap, backlog, decision-making]
source: https://github.com/product-on-purpose/pm-skills/tree/main/skills/define-prioritization-framework
derived_from: awesomeclaude
---

# Prioritization Framework

Run all applicable prioritization frameworks against a candidate list of work items, then surface where they agree and disagree. Core principle: **multi-framework analysis surfaces what single-framework selection hides.** Where frameworks agree, confidence rises; where they diverge, the divergence reveals hidden assumptions worth examining.

Refuse to fabricate scores. When input data is missing, produce an explicit estimation scaffold and label assumptions.

## When to use

- Ranking Q-roadmap candidates, MVP scope cuts, or sprint hypothesis triage
- Any time you have more candidates than capacity and need a defensible ranking

## Inputs

Required: list of candidate items (name + one-sentence description each) and decision context (e.g. "Q3 roadmap candidates").
Optional (improves quality): per-item impact/effort estimates, customer signal, stakeholder criteria + weights, confidence levels, time horizon, customer-research data (unlocks Kano).

## Framework applicability filter

Evaluate each before running; run all that pass, and state which were excluded and why. ICE always runs (lowest input).

| Framework | Runs when | Excluded when |
|---|---|---|
| RICE (Reach×Impact×Confidence ÷ Effort) | quantitative reach/impact/effort available or user accepts scaffold | inputs missing and scaffold declined |
| ICE (Impact×Confidence×Ease) | always | never |
| MoSCoW (Must/Should/Could/Won't) | binary commitment or scope bounding | pure ranking with no scope constraint |
| Weighted Scoring | multiple stakeholders/criteria + weights | single criterion dominates |
| Kano (Must-have/Performance/Delighter) | customer-research input provided | **gated:** no research → exclude, explain what would unlock it |

## How / output

1. **Applicability summary** (3-5 sentences): which ran, which excluded, why.
2. **Inputs summary**: what was given; label any assumed/missing input.
3. **Per-framework scoring tables**: e.g. RICE columns (Reach, Impact 0.25-3, Confidence %, Effort eng-weeks, Score, Notes); ICE (Impact 1-10, Confidence 1-10, Ease 1-10, Score); MoSCoW (Bucket, Rationale, Risk if dropped); Weighted Scoring (criteria × weights); Kano if unlocked.
4. **Comparison table**: ranking per framework side by side; highlight agreements and divergences.
5. **Executive summary + recommendation**: the recommended order, with the divergences flagged as the key findings.
6. **What could go wrong**: risks in the prioritization itself.
