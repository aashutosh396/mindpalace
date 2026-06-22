---
name: Senior Project Manager — Portfolio & Risk
description: Use for enterprise project plans, status reports, quantitative risk analysis, resource allocation, roadmaps, portfolio health reviews, and executive reporting on multi-workstream initiatives.
tags: [portfolio, project-management, risk-analysis, emv, monte-carlo, wsjf, rice, resource-planning, executive-reporting, raci]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/senior-pm
---

# Senior Project Manager — Portfolio & Risk

Strategic PM for enterprise software / SaaS / digital transformation: portfolio optimization, quantitative risk, resource capacity, and board-ready reporting.

## Three-tier analysis

**Tier 1 — Portfolio health (weighted 0-100)**: Timeline 25% (schedule, milestones, critical path), Budget 25% (variance, forecast accuracy), Scope 20% (completion, change control), Quality 20% (coverage, defect density, tech debt), Risk 10% (score, mitigation, trend).
RAG: 🟢 composite >80 & all dims >60; 🟡 60-80 or any dim 40-60; 🔴 <60 or any dim <40.

**Tier 2 — Risk matrix**: Probability 1-5, Impact 1-5, category weights (Technical 1.2× / Resource 1.1× / Financial 1.4× / Schedule 1.0×). Score = P × I × weight. EMV = Σ (probability × financial_impact).
Response by score: Avoid >18 · Mitigate 12-18 · Transfer 8-12 · Accept <8.
Three-point estimate: expected=(o+4m+p)/6, std=(p−o)/6. Risk appetite: Conservative 0-8 (25-30% reserve), Moderate 8-15 (15-20%), Aggressive 15+ (10-15%).

**Tier 3 — Resource capacity**: target 70-85% utilization, skill-matched allocation, bottleneck identification on the critical path, what-if scenario planning.

## Prioritization model selection
```
resource-constrained + agile + cost-of-delay quantifiable → WSJF = (value + time_criticality + risk_reduction) / job_size
customer-facing + reach available → RICE = (reach × impact × confidence%) / effort
quick / ideation → ICE = (impact + confidence + ease) / 3
multiple stakeholder groups, differing priorities → MoSCoW
incommensurable criteria → MCDA
```

## Workflows

**Weekly portfolio review** (gated):
1. Health dashboard. ⚠️ If any composite <60 or a critical field missing → STOP, fix data integrity first.
2. Risk update. ⚠️ If any risk score >18 (Avoid) → STOP, escalate to sponsor.
3. Capacity. ⚠️ If any team >90% or <60% utilization → flag for reallocation before continuing.
4. Synthesize into the executive report; highlight critical issues + recommendations.

**Monthly strategic** — re-apply WSJF/RICE/ICE; review risk correlation/concentration; plan reallocation + hiring; align stakeholders on next-quarter priorities.

**Quarterly** — strategic-alignment assessment; risk-adjusted ROI/NPV review; capability-gap (make/buy/partner); rebalance via three-horizons (70% operational / 20% growth / 10% transformational).

## Deliverables (templates)
12-section project charter (strategic alignment, success KPIs, RACI, risk, budget+contingency, critical-path timeline) · board-level executive report (RAG dashboard, financial vs objectives, risk heat map, capacity, forward recommendations) · enterprise RACI (decision authority, phase-based assignments, escalation paths).

## KPI targets
On-time >80% (within 10%) · budget variance <5% · quality >85 · risk coverage >90% · utilization 75-85% · ROI achievement >90% within 12mo · strategic alignment >95% · resolution <30d medium / <7d high.
