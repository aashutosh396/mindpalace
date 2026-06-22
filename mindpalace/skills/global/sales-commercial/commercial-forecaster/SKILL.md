---
name: Commercial Bookings Forecaster
description: Use when building a quarterly bookings forecast, ARR/NRR projection, or commit/best-case/pipe-only board number — decomposes pipeline into 3 tiers, projects cohort-level NRR/GRR to surface leaks, scores per-stage funnel confidence, and always names the conversion assumption.
tags: [commercial, forecasting, bookings, arr, nrr, grr, cohort, funnel, pipeline-math, pipeline-coverage]
source: alirezarezvani/claude-skills
derived_from: commercial/skills/commercial-forecaster
---

# Commercial Bookings Forecaster

Answers three forecast-moment questions and emits **three numbers + an explicit assumption block**. The CRO picks the commit number and walks the board through the variance. (Not financial close, not strategic CFO planning, not CRO hiring/territory.)

## Workflow
1. **Intake** — opportunity list (stage, amount, close-date, age, last-activity); historical stage-to-stage conversion (last 4Q and last 12Q); per-cohort ARR + retention + expansion; funnel stage names with 12Q conversion history.
2. **3-tier bookings forecast** — commit / best-case / pipe-only, each with the conversion rate applied, the data window (last-4Q vs last-12Q weighted **70/30**), and the time-to-close probability adjustment. Surface commit-vs-pipe-only variance as the pipeline-risk indicator. **The assumption block is non-optional.**
3. **Cohort ARR projection** — per-cohort NRR + GRR over the horizon. Flag any cohort whose NRR is declining vs the trailing-cohort average — leaky cohorts hide in the consolidated number for 2-3 quarters before surfacing in the topline. Output: consolidated trajectory + cohort heatmap + leaky-cohort callout.
4. **Funnel confidence** — per stage: mean conversion %, stdev, coefficient of variation (CoV = stdev/mean), confidence band (HIGH <10%, MEDIUM 10-25%, LOW 25-50%, VERY LOW >50%). Recommend treatment: extend-data-window / treat-as-soft-floor / commit-quality.
5. **Assemble the deck** — the assumption block goes ON the slide with the number. Single number + no assumption block = theatre.

## Anti-patterns
- Single-number forecast with no confidence band.
- Using last-12Q conversion blindly (hides recent slowdown — the 70/30 blend corrects this).
- Reporting NRR without cohort decomposition.
- Treating best-case as commit; best-case includes <50% time-to-close opps.
- Ignoring late-stage opp age (a "verbal" deal stalled 180 days is not a commit — downweight stalled opps; don't re-up by hand).
- No pipeline-coverage check (forecast > pipeline ÷ 3 is anti-pattern).

## Forcing questions (one at a time, recommended + canon)
1. Conversion rate — last-4Q or last-12Q? → 70/30 blend. (Tunguz: single-window misses regime change at ~3Q lag)
2. Pipeline coverage ratio — commit above pipeline ÷ 3? → 3x is the SaaS floor. (Pacific Crest/KeyBanc)
3. NRR by cohort, not just consolidated? → always decompose. (ProfitWell; Skok)
4. CoV on each stage over last 12Q? → <10% commit-grade; >50% don't forecast on it. (Hyndman & Athanasopoulos; MIT Sloan)
5. How long has each late-stage opp been late-stage? → >2x median stage-duration = stalled, exclude from commit. (Skok)
6. Best-case within 30% of pipe-only? → <50% = sandbagging; >80% = hockey-sticking. (McKinsey; OpenView)
7. What assumption block accompanies the number on the slide? → conversion rate + data window + weighting + coverage ratio. (Bain; Forrester)
