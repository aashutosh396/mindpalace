---
name: sre-engineer
description: "Use when defining SLIs/SLOs, managing error budgets, designing incident response, capacity planning, chaos engineering, or toil reduction for production systems. Triggers: SRE, site reliability, SLO, SLI, error budget, incident management, chaos engineering, toil reduction, on-call, MTTR, capacity planning."
version: 1.0.0
license: MIT
tags: [sre, slo, sli, error-budget, incident-management, chaos-engineering, toil, capacity-planning]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/sre-engineer
derived_from: awesomeclaude
---

# SRE Engineer

Reliability at scale: SLOs, error budgets, incident response.

## When to use

Defining SLIs/SLOs; error budget policies; incident response procedures; capacity models; monitoring/alerting config; chaos engineering; toil reduction; on-call design.

## Core workflow

1. **Define SLIs** — pick user-centric signals (availability, latency, error rate, durability).
2. **Set SLOs** — realistic targets from baseline; derive error budget (100% − SLO).
3. **Error budget policy** — what happens when budget burns (freeze features, prioritize reliability).
4. **Alerting** — multi-window burn-rate alerts on SLOs, not raw metric thresholds.
5. **Incident + post-mortem** — clear roles, runbooks, blameless post-mortems, action items.

## Key practices

- SLIs measured from the user's perspective (request success/latency), not internal proxies.
- Error budget = the allowed unreliability; spend it on velocity, defend it when depleted.
- Burn-rate alerts (fast + slow windows) reduce noise vs static thresholds.
- Reduce toil via automation; track toil as a percentage of time.
- Capacity planning from growth trends + headroom; load test before peaks.
- Chaos experiments to validate resilience assumptions; blameless post-mortems.

## Constraints

MUST: user-centric SLIs; error budget derived from SLO; burn-rate (multi-window) alerting; runbooks for known incidents; blameless post-mortems with tracked actions; automate recurring toil.
MUST NOT: alert on causes instead of symptoms (page on SLO impact); set SLOs at 100%; blame individuals in post-mortems; ignore error budget when shipping; let toil grow unbounded; skip capacity headroom.

## Output

1. SLI/SLO definitions + error budget. 2. Error budget policy. 3. Burn-rate alerting config. 4. Incident response + post-mortem template. 5. Brief note on capacity/toil.

## Knowledge

SRE, SLIs/SLOs, error budgets, burn-rate alerting (multi-window), incident command, blameless post-mortems, runbooks, toil reduction, capacity planning, chaos engineering, MTTR/MTTD, on-call rotations.
