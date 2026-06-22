---
name: Capacity Planner
description: Use when an ops leader (Support/CX/CS/BizOps/IT/Finance ops) is sizing team capacity, building a headcount plan, modeling utilization risk, or sequencing quarterly hiring — Erlang-C queueing math, P90 demand sizing, shrinkage-adjusted FTE, and manager-trigger thresholds.
tags: [capacity-planning, headcount, utilization, erlang-c, queueing-theory, workforce, hiring-plan, ops-planning, littles-law]
source: alirezarezvani/claude-skills
derived_from: business-operations/capacity-planner
---

# Capacity Planner

Sizing tool for **ops teams that handle queued work** (Support, CX, Customer Success, BizOps, IT/Finance ops). Built on Erlang-C, Little's Law, and ops-leadership canon (Fournier, Larson, Cleveland, Reinertsen). Deterministic, arithmetic — not vibes. Apply when sustained utilization >80% or team growing >50% in 12 months. **Not** engineering capacity (that's DORA/cycle-time) and not strategic 3-5yr workforce planning.

## Three Artifacts

1. **Capacity sizing** at 70/80/90% utilization against P50/P90/P99 demand, with P(SLA breach) at each point and a SAFE/WATCH/AT_RISK/CRITICAL band.
2. **Utilization health** — per-member traffic-light + team verdict (HEALTHY/SQUEEZED/OVERLOADED/UNBALANCED).
3. **12-month quarterly hiring plan** accounting for ramp curves, attrition, QoQ demand growth, and span-of-control manager triggers.

## Workflow

1. **Intake demand** — pull P50/P90/P99 daily volume from the work system. If you only have averages, **stop and pull the distribution** — single-point demand is the most expensive ops anti-pattern.
2. **Model throughput** — Erlang-C with demand, AHT, SLA target, current FTE, shrinkage. Read the **80%-utilization row** — that's the sizing point.
3. **Flag utilization risk** — anyone >85% sustained is a throughput-collapse risk (Reinertsen). Spread >30 percentage points = UNBALANCED — fix before hiring.
4. **Sequence hiring** — front-load (Q1 ~35%, Q4 ~15%), apply ramp curves, trigger a manager hire at >7 ICs/manager.
5. **Walk the forcing questions** (below), one at a time, write the answers down.

## Assumptions

Work is queued (tickets/cases/items) not project-style · demand distribution is stationary-enough within a quarter (step-changes need re-running mid-quarter) · ≥90 days of historical demand to compute percentiles · single service class per queue (model hard priority tiers as separate queues and sum) · multi-channel teams use the right profile with built-in shrinkage premium.

## Top Anti-Patterns

Plan-to-100%-utilization (Reinertsen P12) · treat-ramp-as-instant · ignore-attrition · hire-ICs-forever-with-no-manager-trigger · size-to-P50-only · no-shrinkage-adjustment · single-channel-model-for-multi-channel · no-surge-plan-for-P99.

## Forcing Questions (one at a time, recommended answer + canon)

1. **What's your bottleneck, and have you confirmed it empirically?** → a named, measured stage with queue-time data. If unknown, run process-mapping first. (Goldratt, *The Goal*; Reinertsen.)
2. **What service trade-off are you accepting?** → a written explicit choice (fast vs empathetic, broad vs deep, low-cost vs high-quality — you can't win all four). AHT/SLA/shrinkage inputs must agree with it. (Frei & Morriss, *Uncommon Service*.)
3. **What's your P90, and the gap to P99?** → two numbers from the last 90 days with calendar context. P50-sized misses SLA half the time; P99-sized overstaffs 30-50%; P90 is the operating point. (Cleveland; Erlang 1909.)
4. **At planned utilization, what's P(SLA breach) at P90 and P99?** → two computed probabilities. >10% at P90 = understaffed; >50% at P99 = no surge plan, CEO-visible peak. (Erlang; Hopp & Spearman.)
5. **Have you budgeted replacement hires for attrition?** → yes, a specific number. At 30% attrition a 20-FTE team loses ~6; "add 5 net" is really "hire 11". (Bersin; Lawler.)
6. **When does span of control trigger a manager hire, and who's the candidate?** → a specific quarter + an identified candidate. Past 7 ICs/manager 1:1s degrade; past 10 = coverage crisis. (Fournier, *The Manager's Path* Ch.5; Grove.)
7. **What's your surge plan for the P99 day?** → explicit documented plan (overflow tier / BPO / on-call / escalation tree) OR a written degradation contract. "We'll figure it out" = board-visible fire. (Hopp & Spearman; Reinertsen.)
