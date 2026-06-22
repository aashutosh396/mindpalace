---
name: Customer Success Manager Analytics
description: Use when analyzing customer accounts, reviewing retention, scoring at-risk customers, or finding upsell opportunities — three deterministic models for multi-dimensional health scoring, churn risk tiering, and expansion opportunity ranking across Enterprise/Mid-Market/SMB.
tags: [customer-success, health-score, churn-risk, expansion, upsell, retention, segmentation, qbr, saas]
source: alirezarezvani/claude-skills
derived_from: business-growth/skills/customer-success-manager
---

# Customer Success Manager

Deterministic, repeatable CS analytics: health scoring, churn-risk prediction, and expansion identification. Point-in-time analysis of exported CRM/CS data (no real-time, no ML). Calibrate thresholds to your product/industry. Combine all three for a full picture and act on trends, not snapshots — a declining Green is more urgent than a stable Yellow.

## 1. Health Score (weighted, segment-aware)
| Dimension | Weight | Metrics |
|---|---|---|
| Usage | 30% | login frequency, feature adoption, DAU/MAU |
| Engagement | 25% | support ticket volume, meeting attendance, NPS/CSAT |
| Support | 20% | open tickets, escalation rate, avg resolution time |
| Relationship | 25% | exec sponsor engagement, multi-threading, renewal sentiment |

Classification: Green 75-100 (healthy) · Yellow 50-74 (monitor) · Red 0-49 (intervene now). Compare current vs previous period for trend.

## 2. Churn Risk (weighted signals → tiers)
| Signal category | Weight |
|---|---|
| Usage decline | 30% |
| Engagement drop | 25% |
| Support issues | 20% |
| Relationship signals (champion left, sponsor change, competitor mentions) | 15% |
| Commercial factors (pricing complaints, budget cuts) | 10% |

Tiers: Critical 80-100 (exec escalation) · High 60-79 (urgent CSM) · Medium 40-59 (proactive outreach) · Low 0-39 (standard monitoring). Each tier maps to an intervention playbook.

## 3. Expansion Opportunity
Types: **Upsell** (higher tier / more of existing), **Cross-sell** (new modules), **Expansion** (seats / departments). Analyze adoption depth, whitespace (unused features), estimate revenue, and rank by effort × impact.

## Workflow
1. Score health across portfolio. 2. Identify at-risk accounts. 3. Find expansion in healthy accounts. 4. Prep QBR/EBR with the combined data. Verify each step's output is non-empty before piping into the next.
