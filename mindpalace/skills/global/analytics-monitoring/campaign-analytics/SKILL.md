---
name: Campaign Analytics
description: Use when analyzing marketing campaigns, ad performance, attribution, conversion funnels, or computing ROI/ROAS/CPA/CAC — runs multi-touch attribution, funnel drop-off, and ROI math.
tags: [campaign-analytics, attribution, roas, roi, cpa, cac, funnel, marketing-metrics, conversion-rate, ad-performance]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/campaign-analytics
---

Deterministic campaign performance analysis: multi-touch attribution, funnel conversion, ROI. Three analysis modules, no ML, no API calls — feed JSON snapshots in, get repeatable metrics out.

## Typical workflow (run in sequence)
1. **Attribution** — understand which channels drive conversions.
2. **Funnel** — find where prospects drop off on the path to conversion.
3. **ROI** — calculate profitability and benchmark, then reallocate budget.

## 1. Attribution models
Allocate conversion credit across channels. Compare ≥3 models — no single model tells the full story.

| Model | Credit rule | Best for |
|---|---|---|
| First-Touch | 100% to first interaction | Brand awareness |
| Last-Touch | 100% to last interaction | Direct response |
| Linear | Equal across all touchpoints | Balanced multi-channel |
| Time-Decay | More credit to recent touchpoints (configurable half-life ≈ sales cycle) | Short sales cycles |
| Position-Based | 40/20/40 first/middle/last | Full-funnel |

Input shape: `journeys[]` each with `touchpoints[]` (channel, timestamp, interaction), `converted`, `revenue`.

## 2. Funnel analysis
Input: `funnel.stages[]` + `funnel.counts[]` (equal length). Computes:
- Stage-to-stage conversion rate and drop-off %
- Biggest bottleneck (largest absolute and relative drop) — focus here first
- Overall funnel conversion rate
- Segment comparison when multiple segments supplied

## 3. ROI metrics + benchmarking
Input: `campaigns[]` (name, channel, spend, revenue, impressions, clicks, leads, customers). Outputs:
- **ROI** % · **ROAS** ratio · **CPA** · **CPL** · **CAC** · **CTR** · **CVR**
- Flags campaigns below industry benchmark by channel/vertical

## Best practices
1. Triangulate with ≥3 attribution models.
2. Match time-decay half-life to your average sales-cycle length.
3. Segment funnels (channel, cohort, geo) to find drivers.
4. Benchmark against your own history first; industry benchmarks are context.
5. Run ROI weekly for active campaigns, monthly for strategic review.
6. Include creative/tooling/labor cost in ROI, not just media spend.

## Limits
Descriptive only — no statistical significance testing. Single-currency. Offline static snapshots (no real-time/API). Attribution operates on supplied journeys as-is (no cross-device identity resolution).
