---
name: Org Health Diagnostic
description: Use when assessing overall company health, preparing a board review, or identifying at-risk functions — scores 8 cross-functional dimensions on a traffic-light scale with real benchmarks, surfaces dimension-cascade risks, and produces a prioritized dashboard.
tags: [org-health, health-check, dashboard, traffic-light, benchmarks, cross-functional, risk-dashboard, board-review]
source: alirezarezvani/claude-skills
derived_from: org-health-diagnostic
---

# Org Health Diagnostic

Eight dimensions, traffic lights, real benchmarks. Surfaces the problems you don't know you have. Handles partial data gracefully (missing metric → excluded + flagged "[data needed]").

## The 8 Dimensions (key metrics + green/red thresholds)
1. **Financial (CFO)** — runway (>12mo / <6mo), burn multiple (<1.5x / >2.5x), gross margin (>70% / <55%), revenue concentration top customer (<15% / >25%).
2. **Revenue (CRO)** — NRR (>110% / <100%), logo churn (<5% / >10%), pipeline coverage (>3x / <2x), CAC payback (<12mo / >18mo).
3. **Product (CPO)** — NPS (>40 / <20), DAU/MAU (>40% / <20%), core feature adoption (>60%), time-to-value, CSAT (>4.2 / <3.5).
4. **Engineering (CTO)** — deployment frequency (daily / monthly+), change failure rate (<5% / >15%), MTTR (<1hr / >4hr), tech-debt ratio (<20% / >35%), P0/P1 per month (<2 / >5).
5. **People (CHRO)** — regrettable attrition (<10% / >20%), engagement/eNPS (>30 / <0), time-to-fill (<45d / >90d), manager:IC ratio (1:5-1:8), internal promotion rate (25-30%+).
6. **Operations (COO)** — OKR completion (>70% / <50%), decision cycle time (<48h), process maturity (1-5), cross-functional initiative completion.
7. **Security (CISO)** — incidents last 90d (0 / 1+ major), compliance status, critical-CVE remediation SLA (100%), training completion (>95%), pen-test recency (<12mo / >24mo).
8. **Market (CMO)** — CAC trend, organic vs paid lead mix, win rate (>25% / <15%), competitive win rate, brand NPS in ICP.

## Scoring
Each dimension 1-10 with traffic light: 🟢 7-10 (healthy, optimize) / 🟡 4-6 (watch — is it improving or declining?) / 🔴 1-3 (action within 30 days). Overall = weighted average by stage.

## Dimension Interactions (why one problem creates another)
Financial red → People (hiring freeze) → Engineering (infra freeze) → Product (cut scope). Revenue red → Financial (cash gap) → People (attrition) → Market. People red → Engineering (velocity drops) → Product (quality) → Revenue (churn). Operational red → all degrade (execution failure cascades).

## Dashboard Output
Header (company / date / stage / overall + trend) → per-dimension line (icon + score + one-line state) → TOP PRIORITIES (ranked red/yellow with specific owner + action + timeframe) → WATCH (cascade risks). Always tie to a concrete action with owner and deadline, not just a score.
