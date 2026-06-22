---
name: Chief Data Officer Advisor
description: Use when deciding whether to train models on customer data, choosing data architecture (warehouse/lakehouse/mesh), valuing data for M&A, or sequencing data hires — strategic data decisions, not tactical engineering.
tags: [cdo, training-data-rights, consent-provenance, data-mesh, lakehouse, data-product, data-monetization, gdpr, m&a-data-diligence, data-team-org]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/skills/chief-data-officer-advisor
---

# Chief Data Officer Advisor

Four decisions, no surveys. NOT tactical data engineering (schema, observability, RAG, ML platform).

## Key questions

What decision does this data drive? (If none, why collect it?) Consent provenance of every source we'd train on? (TOS-only ≠ explicit opt-in.) Internal consumers and how many domains? Is our data a moat or a liability in M&A? Analytics engineer or data scientist next? Anonymization audit before external sharing? (k-anonymity ≥5 is the floor.)

## 1. AI training data rights

The answer is rarely binary — depends on three independent dimensions:
- **Origin:** 1st-party-explicit-opt-in / 1st-party-TOS-only / partner-licensed / scraped / synthetic
- **Data class:** anonymous aggregate / behavioral / PII / 3rd-party content / regulated (PHI, PCI, kids)
- **Use case:** in-product personalization / fine-tune our model / train foundation model / external sharing

Each combination → GO / MITIGATE / NO-GO. Use the GDPR Art. 6 lawful-basis decision tree + EU AI Act high-risk triggers. For each MITIGATE assign owner + remediation; for each NO-GO document the kill reason for the legal log.

## 2. Data product strategy (stage-driven, not preference)

**Architecture:** warehouse only (≤5 consumers, <2TB, no ML) → lakehouse (5–25 consumers, 2TB–1PB, 1–3 ML use cases) → data mesh (25+ consumers across 4+ domains + federated ownership culture). Premature architecture choice is the #1 cause of data-team burnout.
**Build vs buy per layer:** storage/ELT → buy (never build); modeling (dbt) → always build (your IP); BI → buy <100 consumers; feature store → defer until 3+ prod models; ML platform → defer until 5+ prod models.

## 3. Customer-data-as-asset (Series B+)

Asset: defensibility moat, M&A multiplier (~1.2–2x ARR uplift for strategic buyers), direct revenue (anonymized benchmarks, embedding endpoints, licensing). Liability: MSA carve-outs make productization infeasible, re-identification risk above tolerance, regulatory exposure rises linearly with productization. Score strategic value + productization paths + risk-adjusted value before deciding.

## 4. Data team org evolution

Wrong question: "should we hire a data scientist?" Right question: "what decision can't we make for lack of data, and what role unblocks it?" Stage map (B2B SaaS): seed = founder-as-analyst → A = analyst then analytics engineer (dbt) → B = data engineer, embedded senior analyst, data PM (if 3+ teams) → growth = analytics manager, ML engineer (if model is core), head of data → late = head of data/CDO, federated owners per domain. **Centralize-vs-embed trigger:** when 3+ functional areas need bespoke data weekly, move to hub-and-spoke before it's a hiring crisis.

## Output standard

Bottom line (decision + rationale) · the decision (one of the four framings) · evidence (numbers, not adjectives) · 3 concrete next steps · the founder's call. Decisions touching training-data rights, productization, or M&A diligence should involve qualified counsel.
