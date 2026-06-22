---
name: SLO Architect
description: Use when defining/reviewing/operating SLOs, SLIs, error budgets, or burn-rate alerts — enforces Google SRE Workbook discipline and catches the four cardinal SLO mistakes.
tags: [slo, sli, sla, error-budget, burn-rate, sre, reliability, observability, google-sre-workbook]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/slo-architect
---

# SLO Architect

Define SLOs that mean something. Most "SLOs" are arbitrary numbers nobody believes (99.9% on every endpoint, no SLI definition, no error budget, no policy). This enforces SRE Workbook discipline: right SLI → target users care about → error budget → multi-window burn-rate alerts → written policy for when budget runs out.

## Vocabulary
```
SLI = measurable signal of user-perceived health (e.g., HTTP 2xx rate)
SLO = target for the SLI over a window (e.g., 99.9% over 30 days)
SLA = customer-facing commitment with consequences (separate concern)
EB  = error budget = 100% − SLO target = how much "bad" you can spend
BR  = burn rate = how fast you consume the error budget
```

## The four cardinal mistakes (catch each)
1. **Target too high** (99.99%+ on services that can't support it) → every blip violates SLO, alerts become noise.
2. **Wrong SLI** (CPU as proxy for UX) → system "green" while users suffer.
3. **No error budget policy** → burning budget means nothing without an agreed action.
4. **Single-window burn-rate alert** → too noisy (5-min) or too slow (notice after the fact).

## SLI selection cheatsheet
| User experience | SLI type | Measure |
|---|---|---|
| Did request succeed? | request-success-rate | `2xx / total` |
| Was response fast? | request-latency | `count(p99 < threshold) / total` |
| Was service up? | availability-time | `(window − downtime) / window` |
| Is data current? | data-freshness | `count(age < threshold) / total` |
| Was answer correct? | correctness | `count(correct) / total` |

## SLO review checks
target ≥99.99% (too high) · target ≤99.0% (too low/wrong SLI) · window <7d (statistical noise) · window >90d (slow feedback) · missing/vague SLI definition · no error budget policy · CPU/memory as SLI.

## Error budget math (99.9% over 30 days)
- Allowed unavailability: `0.1% × 30 × 24 × 60 = 43.2 min`
- Multi-window burn-rate (SRE Workbook ch.5): Fast burn = page if 2% of monthly budget in 1h; Slow burn = page if 10% in 6h, ticket if 10% in 3 days.

## Workflows
**Define new SLO:** pick user journey → choose SLI type → define numerator/denominator with concrete labels → set target from 30d historical (`floor(p50 × 100)/100`, avoids never-sustained targets) → pick window (28d recommended) → render definition → compute burn-rate alerts → write error budget policy → review (must pass before "live").

**Quarterly review:** run review on every active SLO; too easy (never burned) → tighten; too hard → loosen or fix system; check alerts fired usefully; audit whether budget policies were followed; commit revisions, archive old with date stamps.

**SLO-driven rollback:** deploy burns budget faster than baseline → burn-rate alert fires → auto-rollback via feature flag → postmortem → next SLO revision.

## Anti-patterns
99.99% copy-pasted everywhere · CPU as SLI · single-window alerts · no budget policy · SLOs without owners · annual-only reviews · SLAs in the SLO doc · SLO target = SLA target (SLO must be tighter).
