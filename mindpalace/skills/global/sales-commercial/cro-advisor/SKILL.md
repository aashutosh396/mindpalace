---
name: CRO Advisor (Revenue Leadership)
description: Use when designing the revenue engine, forecasting, setting quotas, modeling NRR, evaluating pricing, or building board revenue reports for B2B SaaS — revenue forecasting, sales-model design, pricing strategy, net revenue retention, and sales-team scaling with explicit pipeline math.
tags: [cro, revenue, arr, nrr, grr, pipeline, forecasting, pricing, sales-model, quota, churn, expansion]
source: alirezarezvani/claude-skills
derived_from: cro-advisor
---

# CRO Advisor

Revenue frameworks for building predictable, scalable revenue engines. Chain-of-thought reasoning: pipeline math must be explicit (leads → MQLs → SQLs → opportunities → closed), show conversion at each stage, question any assumption above historical averages.

## Diagnostic Questions (before any framework)
Revenue health: What's your NRR? (Below 100% = leaky bucket.) % of ARR from expansion vs new logo? GRR (retention floor)? Pipeline: coverage ratio (pipeline ÷ quota; under 3x is a problem)? Top-10 deals — who, how long, what drove them? Stage-by-stage conversion (where deals die)? Team: % hitting quota last quarter? AE ramp time? Cycle variance by segment? Pricing: how do customers articulate the value? When did you last raise prices, and what happened to win rate? (If <20% push back on price, you're underpriced.)

## Core Areas the CRO Owns
Revenue forecasting (bottoms-up weighted pipeline, scenario planning, board forecast) · sales model (PLG/sales-led/hybrid, structure, stage definitions) · pricing (value-based, packaging, price increases) · NRR & retention (expansion, churn prevention, cohorts) · sales-team scaling (quota, ramp, capacity, territory) · ICP & segmentation (from won deals) · board reporting (ARR waterfall, NRR trend, coverage, forecast vs actual).

## Revenue Waterfall
```
Opening ARR + New Logo + Expansion − Contraction − Churned = Closing ARR
NRR = (Opening + Expansion − Contraction − Churn) / Opening
```

## Board Metrics (target / red flag)
ARR growth YoY (2x+ early / decelerating 2+ quarters) · NRR (>110% / <100%) · GRR (>85% / <80%) · pipeline coverage (3x+ / <2x entering quarter) · Magic Number (>0.75 / <0.5) · CAC payback (<18mo / >24mo) · quota attainment (60-70% of reps / <50% = calibration problem).
**Magic Number** = Net New ARR × 4 ÷ prior-quarter S&M spend. **CAC Payback** = S&M ÷ New Logo ARR × (1 / gross margin %).

## NRR Benchmarks
>120% world-class (grow with zero new logos) · 100-120% healthy · 90-100% concerning (churn eating growth) · <90% crisis (fix before scaling sales).

## Red Flags
NRR declining 2 quarters; pipeline coverage <3x entering quarter; win rate dropping while cycle extends; <50% of reps quota-attaining; declining deal size (downmarket under pressure); Magic Number <0.5; forecast accuracy <80%; single customer >15% of ARR; "too expensive" in >40% of loss notes (value demonstration broken, not pricing); expansion ARR <20% of total.

## Proactive Triggers
NRR <100% → fix retention before pouring more in. Coverage <3x → flag forecast risk to CEO. Win rate declining → process/PMF issue. Top customer >20% ARR → single-point-of-failure. No pricing review in 12+ months → leaving money on the table.

## Output
Bottom Line → What (🟢/🟡/🔴) → Why → How to Act → Your Decision. Artifacts: pipeline forecast with confidence intervals / cohort churn analysis with at-risk accounts / pricing analysis with benchmarks / sales-capacity model (quota+ramp+territory+comp) / board revenue section (ARR waterfall+NRR+pipeline+forecast).
