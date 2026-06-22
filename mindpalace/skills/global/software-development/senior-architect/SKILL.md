---
name: Senior Software Architect
description: Use when designing system architecture, evaluating microservices vs monolith, choosing a database, planning scalability, writing ADRs, or reviewing system design — diagrams, dependency analysis, decision matrices.
tags: [architecture, system-design, microservices, monolith, database-selection, adr, dependency-analysis, cqrs, event-sourcing, scalability]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-architect
---

# Senior Software Architect

Architecture design and analysis for informed technical decisions.

## Analysis Capabilities
- **Architecture diagrams** from project structure: component (modules + relationships), layer (presentation/business/data), deployment (topology). Output Mermaid / PlantUML / ASCII.
- **Dependency analysis**: tree (direct + transitive), circular dependencies, coupling score 0-100, outdated packages. Supports npm/yarn, Python, Go, Rust.
- **Project assessment**: detect pattern (MVC/layered/hexagonal/microservices), code smells (god classes, mixed concerns), layer violations, missing components.

## Database Selection
1. **Data characteristics**: structured + relationships + ACID → SQL; flexible schema / document / time-series → NoSQL.
2. **Scale**: <1M single region → Postgres/MySQL; 1-100M read-heavy → Postgres + read replicas; >100M global → CockroachDB/Spanner/DynamoDB; >10K writes/sec → Cassandra/ScyllaDB.
3. **Consistency**: strong → SQL/CockroachDB; eventual → DynamoDB/Cassandra/Mongo.
4. **Document in an ADR**: context, options, decision, trade-offs.

Quick map: Postgres = default · MongoDB = flexible schema · Redis = cache/sessions · DynamoDB = serverless AWS · TimescaleDB = time-series.

## Architecture Pattern Selection
- Team size: 1-3 → modular monolith; 4-10 → modular/service-oriented; 10+ → consider microservices.
- Deployment: single unit → monolith; independent scaling → microservices; mixed → hybrid.
- Data boundaries: shared DB ok → monolith; strict isolation → microservices w/ separate DBs; event-driven fits → event-sourcing/CQRS.

Pattern by requirement: rapid MVP → modular monolith · independent team deploy → microservices · complex domain → DDD · read/write ratio difference → CQRS · audit trail → event sourcing · third-party integrations → hexagonal/ports-and-adapters.

## Monolith vs Microservices
**Monolith when**: <10 devs, unclear boundaries, rapid iteration, minimize ops complexity, shared DB ok.
**Microservices when**: teams own services end-to-end, independent deploy critical, different scaling per component, tech diversity needed, boundaries well understood.
**Hybrid (recommended start)**: modular monolith; extract a service only when a module has different scaling needs, a team needs independent deploy, or tech constraints require separation.
