---
name: Chaos Engineering
description: Use when planning, running, or learning from a chaos experiment or Game Day — design a hypothesis, bound the blast radius, set abort criteria, pick an attack and tool, and write a blameless postmortem.
tags: [chaos-engineering, resilience, fault-injection, gameday, sre, reliability, blast-radius, abort-criteria, steady-state, chaos-mesh]
source: alirezarezvani/claude-skills
derived_from: engineering/chaos-engineering
---

# Chaos Engineering

Surface real weaknesses in production without becoming an outage. Most attempts fail because they skip steady-state measurement, define no abort criteria, and have no blast-radius bound.

## Core principle: chaos without abort criteria is an outage

The 4 principles (Netflix) + a mandatory 5th:
1. Build a hypothesis around **steady-state behavior** — not "what breaks?" but "X holds; will it still hold under fault Y?"
2. **Vary real-world events** — kill nodes, slow networks, lose cache, throttle dependencies.
3. **Run in production** — staging lacks prod failure modes. Start small.
4. **Automate to run continuously** — one-off chaos is a press release.
5. **Define abort criteria up front** — non-negotiable.

## When NOT to use
General incident response, threat hunting/red-team, performance load testing (capacity, not failure modes), or after-the-fact production debugging.

## Design an experiment (one at a time)
1. State a hypothesis: "When [fault], steady-state metric X stays within Y."
2. Identify the steady-state metric — measurable BEFORE the experiment.
3. Calculate blast radius (traffic share × user pop × duration → expected affected users + error-budget burn). Risk score: GREEN <1% budget, YELLOW 1-10%, RED >10%. Proceed only on GREEN.
4. Produce a plan with: hypothesis, steady-state, attack, magnitude, duration, blast radius, abort criteria, rollback, monitoring dashboards, learning question.
5. Peer-review; confirm abort criteria are concrete.
6. Notify on-call. Run with monitoring open.
7. If abort criteria hit, abort immediately; record what happened.
8. Write a blameless postmortem: hypothesis confirmed/refuted, what we learned, what surprised us, follow-up actions with owners, link to next experiment.

## The 7 attack types
| Attack | Tests |
|---|---|
| Latency | Timeouts, retries, circuit breakers |
| Error | Error handling, fallback paths |
| Resource (CPU/mem/disk) | Saturation handling, autoscaling |
| Network partition | Split-brain, consensus, failover |
| Dependency failure | Graceful degradation |
| Time | Clock skew, NTP |
| Infrastructure (kill instance) | Auto-recovery, failover |

Match attack to hypothesis: "what if X is slow?" → latency; "what if X loses network?" → partition.

## Tooling
k8s-only + OSS → Chaos Mesh or Litmus (Litmus = bigger library) · multi-cloud + OSS → Chaos Toolkit · AWS-heavy + simple → AWS FIS · enterprise + audit → Gremlin.

## Game Day → continuous
Weekly Game Day in staging → weekly in prod with limited blast radius → continuous scheduled experiments → wire a baseline chaos sweep to every prod deploy. Track: experiments/week, weaknesses found, MTTR trend.

## Anti-patterns
No hypothesis · no steady-state metric · no blast-radius bound · no abort criteria · no on-call coverage · staging-only or dev-only chaos · one-off chaos · blame-laden postmortem.

## Verifiable success
100% of experiments have a written hypothesis, abort criteria, and blast-radius calc; any single experiment ≤10% error budget; <14 days between experiments; each yields ≥1 shipped follow-up; zero chaos-caused customer incidents in trailing 90 days.
