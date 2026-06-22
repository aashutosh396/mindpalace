---
name: Social Media Performance Analyzer
description: Use when analyzing social campaign performance, calculating engagement rate or ROI, comparing platforms, or benchmarking against industry standards — produces metrics, ROI, and ranked performers.
tags: [social media analytics, engagement rate, roi, campaign performance, benchmarks, instagram, tiktok, ctr]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/social-media-analyzer
---

# Social Media Performance Analyzer

Campaign analysis with engagement metrics, ROI, and platform benchmarks.

## Workflow
1. Validate input (reach > 0, valid dates, recognized platform, spend > 0 if ROI requested, non-negative counts).
2. Calculate per-post metrics → aggregate campaign-level.
3. Calculate ROI if spend provided.
4. Compare against platform benchmarks.
5. Identify top/bottom performers.
6. Generate recommendations.
7. Validate (engagement rate < 100%, ROI matches spend).

## Engagement metrics
`Engagement Rate = (Likes + Comments + Shares + Saves) / Reach × 100`

| Metric | Formula |
|---|---|
| CTR | Clicks / Impressions × 100 |
| Reach rate | Reach / Followers × 100 |
| Virality rate | Shares / Impressions × 100 |
| Save rate | Saves / Reach × 100 |

Performance: >6% excellent (scale) · 3-6% good (optimize) · 1-3% average (test) · <1% poor (pivot).

## ROI
CPE = Spend / Engagements · CPC = Spend / Clicks · CPM = (Spend / Impressions) × 1000 · ROAS = Revenue / Spend.

Engagement value estimates: like $0.50 · comment $2.00 · share $5.00 · save $3.00 · click $1.50. ROI = (Value − Spend) / Spend × 100.

ROI interpretation: >500% excellent (scale) · 200-500% good · 100-200% acceptable (optimize first) · 0-100% break-even (review) · <0% pause.

## Platform benchmarks (avg engagement rate)
Instagram 1.22% · Facebook 0.07% · Twitter/X 0.05% · LinkedIn 2.0% · TikTok 5.96%.

Avg CTR: IG 0.22% · FB 0.90% · LinkedIn 0.44% · TikTok 0.30%. Avg CPC: FB $0.97 · IG $1.20 · LinkedIn $5.26 · TikTok $1.00.

## Proactive flags
Engagement below platform avg → analyze top performers for patterns. Follower growth stalled → audit distribution/frequency. High impressions, low engagement → content quality issue. Competitor outperforming → content gap; analyze their winners.

## Output
Campaign metrics + post-by-post breakdown + benchmark comparison + ranked top performers + actionable recommendations. Tag every finding 🟢 verified / 🟡 medium / 🔴 assumed.
