---
name: Feature Flags Architect
description: Use when adding, ramping, retiring, or auditing feature flags — classify the flag, plan a progressive rollout, document a kill switch, choose a provider, or clean up flag debt before a release freeze.
tags: [feature-flags, progressive-delivery, rollout, kill-switch, flag-debt, launchdarkly, growthbook, statsig, unleash, release-engineering]
source: alirezarezvani/claude-skills
derived_from: engineering/feature-flags-architect
---

# Feature Flags Architect

Treat flags as a controlled lifecycle, not throwaway `if`-statements: **request → design → ship → ramp → cleanup → archive**. Flags that skip cleanup become debt (dead branches, stale defaults, untested paths, unbounded blast radius).

## The 4 flag types (misclassifying creates debt)

| Type | Purpose | Lifespan | Owner | Cleanup trigger |
|---|---|---|---|---|
| **Release** | Hide unfinished features in prod | days–weeks | Eng | 100% rollout reached |
| **Experiment** | A/B test variants | weeks | Product | Test concluded, winner picked |
| **Operational** | Circuit breakers, kill switches, perf toggles | months–years | Eng/SRE | Feature retired |
| **Permission** | Entitlements per user/account/plan | years (permanent) | Product | Plan/role removed |

Only Release and Experiment flags belong on a debt watchlist. Operational and Permission are long-lived by design.

## Rollout strategies
- **ring** — 1% → 5% → 25% → 50% → 100%. Default for risky launches.
- **linear** — constant rate/day. Medium-risk.
- **log** — rapid early, slow tail. Low-risk with confidence.
- **cohort** — internal → beta → free → paid → all.

Each phase needs a date, percent, expected user count, abort criteria, and a verification step.

## Provider chooser
- <50 flags + no targeting → **DIY** (config file / env vars)
- Need analytics + experimentation → **Statsig** or **GrowthBook**
- Compliance / SOC2 audit logs → **LaunchDarkly**
- Self-hosting / data residency / air-gapped → **Unleash** or **Flipt**
- Build a 30-day POC before signing.

## Workflows

**Ship behind a flag:** classify type (usually Release) → plan the ramp → add a flag-doc entry BEFORE code (name, owner, type, kill-switch trigger, dashboard URL) → write code → kill-switch audit must pass before merge → deploy at 0%, verify the kill switch → execute rollout, abort if criteria hit → at 100% for 7+ days remove flag, delete dead branch, archive doc.

**Quarterly cleanup:** scan for debt (flags older than N days with low usage) → for each, confirm it reached 100% or was killed, verify owner agrees, delete dead branches + config → note "Removed N stale flags" in CHANGELOG.

**Design a kill switch:** identify failure modes (latency, error-rate, business-metric thresholds) → wire each to an abort (manual dashboard link + on-call playbook, or automated alert that flips flag to 0%) → test in staging before prod → document and pass the audit.

## Anti-patterns
Permanent `if(FLAG)` in 50 places (should be a Permission flag) · flag with no owner · no kill switch documented · A/B test that ran 6 months · flags for cosmetic changes (ship via deploy).

## Verifiable success
100% of new flags pass a kill-switch audit at merge; ≤5 stale flags repo-wide at 90 days; every flag has owner/type/kill-switch; mean time to retire a Release flag <60 days from 100%.
