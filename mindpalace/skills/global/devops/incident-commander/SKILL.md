---
name: Incident Commander (Availability/Reliability)
description: Use when declaring an incident, coordinating multi-team response during an outage, leading a post-mortem, or setting up on-call — severity classification, timeline reconstruction, PIR generation, comms templates.
tags: [incident-commander, outage, sre, severity, post-mortem, pir, runbook, on-call, war-room, rca]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/incident-commander
---

# Incident Commander (Availability/Reliability)

Response framework for outages, degradations, failed deploys: severity classification, timeline reconstruction, post-incident review. (For security incidents — ransomware, intrusion, forensics — use the security incident-response skill. Both use SEV labels; this scores operational impact: users/revenue/SLA.)

## Severity Classification
- **SEV1 Critical**: complete failure, all users / data loss / revenue systems down. IC in 5 min, exec notify 15 min, status page 15 min, war room. Updates every 15 min.
- **SEV2 Major**: >25% users degraded / non-critical features down. On-call 15 min, IC 30 min, status page 30 min. Updates every 30 min.
- **SEV3 Minor**: single feature, <25% users, workarounds exist. 2h business hours.
- **SEV4 Low**: cosmetic, docs, monitoring gaps. 1-2 business days.

## IC Role
Command & control (own the process, resource allocation, situational awareness) · communication hub (updates, external comms, shield responders) · process mgmt (tracking, drive resolution, rollback strategy) · post-incident leadership (PIR, preventive measures). SEV1/2: full authority, bias to action, document decisions, consult SMEs without getting blocked. Prefer rollbacks to risky fixes under pressure; validate before declaring resolved.

## Comms Templates
- **Initial notification (SEV1/2)**: severity, start time, impact, status, affected services, symptoms, response team, next update, status page, war room link.
- **Exec summary (SEV1)**: 2-3 sentence customer/business impact, key metrics (TTD, TTE, impact %, ETA), leadership actions needed.
- **Customer comms**: brief issue + scope, what we know (factual), what we're doing, workaround if any, next update + status page.

## Comms Cadence by Stakeholder
| | SEV1 | SEV2 | SEV3 |
|---|---|---|---|
| Eng Leadership | real-time | 30m | 4h |
| Exec | 15m | 1h | EOD |
| Customers | 15m | 1h | optional |

## Timeline Reconstruction + PIR
Process timestamped events from multiple sources → chronological narrative, identify gaps, duration analysis. PIR with RCA framework (5 Whys / Fishbone / Timeline) + actionable follow-ups with owners + due dates.

## Runbook Structure
Quick reference (severity indicators, contacts, critical commands) → Detection (alerts, manual signs) → Initial Response 0-15m (assess severity, establish command, investigate recent deploys/logs/deps) → Mitigation strategies (with rollback plans) → Recovery + validation → Common pitfalls.

## Post-Incident Discipline
Blameless culture (system failures not individuals) · action items with owners + dates, tracked publicly · share PIRs broadly · look for patterns across incidents.
