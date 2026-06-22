---
name: Senior Backend Engineer
description: Use when designing REST/GraphQL APIs, optimizing database queries, implementing auth, building microservices, or load-testing — Node/Express/Fastify, Postgres optimization, API security, eval-gated decisions.
tags: [backend, rest-api, graphql, database-optimization, authentication, microservices, postgres, load-testing, api-security, indexing]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-backend
---

# Senior Backend Engineer

Backend patterns, API design, DB optimization, security.

## Core Tools
- **API scaffolder**: routes + validation middleware + TS types from OpenAPI spec or DB schema (Express/Fastify/Koa); reverse-generate spec from routes.
- **DB migration tool**: analyze schema, detect changes, generate migrations w/ rollback, suggest indexes, dry-run.
- **Load tester**: configurable concurrency → latency percentiles, throughput, error rates, scaling recommendations.

## API Design Workflow
Define resources/operations (OpenAPI) → scaffold routes → implement business logic → add validation middleware (auto from schema) → regenerate spec.

## Database Optimization Workflow
Analyze performance → identify slow queries (`EXPLAIN ANALYZE`, look for Seq Scan = bad, Index Scan = good) → generate index migrations → dry-run → apply → verify improvement.

## Security Hardening Workflow
JWT config (secret from env, short-lived 1h, RS256 asymmetric) → rate limiting (`express-rate-limit`, 100/15min) → validate all inputs (zod schema) → load test with attack patterns (rate limit, bad input expect 400) → security headers (helmet: CSP, HSTS, cross-origin policies).

## Surface 4 Assumptions Before Recommending
1. **Read/write ratio + 1-yr p99 QPS** — drives DB/cache/queue/partitioning (Kleppmann DDIA).
2. **Tenancy model** — single / shared multi-tenant / isolated multi-tenant.
3. **Data sensitivity tier** — public/internal/PII/PHI/PCI → compliance floor.
4. **SLO + named error-budget consumer** (Google SRE Workbook).

Every recommendation must include latency targets (p50/p95/p99), uptime/SLO, RPO+RTO. Missing any → incomplete.

## Profiles
node-express (TS, <15 eng, customer SaaS, p99 600ms) · fastapi-python (Python, <20 eng, ML-adjacent, async, 500ms) · django-monolith (content CRUD + admin, <25 eng, 800ms) · go-or-rust-microservice (extracted service, ≥30 eng, QPS ≥1000, 200ms).

## Quick Reference
REST response: `{data, meta:{requestId}}`. Error: `{error:{code,message,details}, meta}`. Status: 200/201/204/400/401/403/404/429/500. Index strategy: single-column (equality), composite (multi-column), partial (`WHERE status='active'`), covering (`INCLUDE`). Common issues: N+1 → DataLoader/eager load; slow builds → bundle/lazy; auth → Auth.js/Clerk.
