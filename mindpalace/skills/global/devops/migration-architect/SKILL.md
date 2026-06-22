---
name: Migration Architect
description: Use when planning a database migration, infrastructure cutover, system replacement, or any high-risk transition — produces a phased plan, compatibility check, and explicit rollback path with zero-downtime patterns.
tags: [migration, zero-downtime, rollback, cutover, database, infrastructure, strangler-fig, blue-green, cdc, expand-contract]
source: alirezarezvani/claude-skills
derived_from: migration-architect
---

# Migration Architect

Plan, execute, and validate complex migrations with minimal business impact. Every phase needs a tested rollback. The migration is NOT approved until (a) compatibility is verified or every breaking change is accepted in writing by the owner, and (b) a rollback runbook exists for every phase.

## Flow: plan → check compatibility → generate rollback
1. Generate a phased migration plan from a spec (`phases`, `risks`, `estimated_duration_hours`).
2. Check schema/API compatibility before vs after — gate CI on it (exit non-zero unless `compatible`). Surface `breaking_changes_count` / `potentially_breaking_count`.
3. Generate the rollback runbook from the plan.
4. Re-run both checks after any schema revision.

## Database migration patterns
- **Expand-Contract**: add new alongside old → dual-write → backfill → drop old after validation.
- **Parallel schema**: run new alongside existing, feature-flag traffic, validate consistency, cut over.
- **Event sourcing**: capture changes as events during the window; replay for rollback.
- **Data movement**: bulk snapshot (maintenance window), incremental sync (change tracking), or CDC streaming for zero-downtime on large datasets.

## Service migration patterns
- **Strangler Fig**: route through gateway → replace incrementally → retire legacy → monitor error/latency throughout.
- **Parallel run / shadow traffic**: run both, compare outputs, gradual cutover by confidence.
- **Canary**: small % rollout → monitor latency/errors/business KPIs → increase → full rollout.

## Infrastructure migration
- Cloud-to-cloud: assess + map services → pilot non-critical workloads → IaC-driven production migration with cross-cloud networking + DR.
- On-prem to cloud: lift-and-shift (fast) / re-architecture (cloud-native) / hybrid (sensitive data stays).

## Safety mechanisms
- **Feature flags** for progressive rollout (hash-based % per user).
- **Circuit breaker** with CLOSED/OPEN/HALF_OPEN states, automatic fallback to legacy on degraded new-service performance.

## Data validation & reconciliation
- Row-count validation (account for soft deletes), checksums/hashing on critical subsets, business-logic validation (compare aggregates on both systems), delta-detection queries (missing/extra rows), idempotent auto-correction with audit logging.

## Rollback strategies
- DB: schema version control + per-step rollback scripts; point-in-time recovery; checkpoint snapshots.
- Service: blue-green (keep previous running, switch back); rolling rollback with automated triggers.
- Infra: versioned IaC + tested rollback templates; preserve data in original location during migration.

## Runbook checklists
**Pre:** plan approved, rollback tested, monitoring/alerting configured, roles defined, comms plan active, backups verified, staging validated, benchmarks established, security + compliance reviewed.
**During:** execute phases in order, monitor KPIs continuously, validate at each checkpoint, communicate progress, document deviations, roll back if success criteria fail, keep execution logs.
**Post:** validate success criteria, health checks, run reconciliation, monitor 72h, update docs/runbooks, decommission legacy, retrospective, archive artifacts, update DR procedures.

## Risk framework
Technical (data loss, downtime, integration failures, scale), business (revenue, CX, compliance, brand), operational (knowledge gaps, test coverage, monitoring, comms). Mitigate with comprehensive testing (unit/integration/load/chaos), gradual rollout with auto-rollback triggers, and stakeholder comms.
