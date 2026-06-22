---
name: Senior Fullstack
description: Use when scaffolding a new project, choosing a stack, or auditing codebase quality across Next.js/FastAPI/MERN/Django — project boilerplate, security + complexity scoring, eval-gated stack decisions.
tags: [fullstack, scaffolding, nextjs, fastapi, mern, django, code-quality, stack-selection, security-scan, architecture]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-fullstack
---

# Senior Fullstack

Project scaffolding, code-quality analysis, stack-selection discipline.

## Scaffold Templates
- `nextjs` — Next.js 14+ App Router, TS, Tailwind.
- `fastapi-react` — FastAPI + React + Postgres.
- `mern` — Mongo/Express/React/Node TS.
- `django-react` — DRF + React.
Output: structure, package configs, TS config, Docker + compose, env templates. Verify scaffold succeeded (`package.json`/`requirements.txt` exists) before proceeding.

## Code Quality Analysis
Categories: security (hardcoded secrets, injection), complexity (cyclomatic, nesting), dependency health (outdated + CVEs), test coverage estimate, docs. Output: 0-100 score + grade, issues by severity, high-complexity files, prioritized recommendations. **Audit flow**: full analysis → fix all P0 (critical) immediately → re-run to verify → ticket P1/P2.

## Surface 4 Assumptions Before Recommending
1. **Team size today + 12-month headcount** — drives monolith/modular/services (Sam Newman: MonolithFirst).
2. **Deployment cadence** — drives CI/CD + feature-flag spend (Accelerate).
3. **User-facing vs internal vs marketing-site** — drives stack + a11y/perf budget.
4. **Monthly cloud + SaaS budget ceiling** — drives build-vs-managed split.

Every recommendation must include three machine-checkable numbers: API latency (p50/p95/p99), frontend perf (LCP/INP/CLS mobile-4G), uptime/SLO. Missing any → incomplete.

## Profiles
| Profile | When | Cloud ceiling | Pattern |
|---|---|---|---|
| saas-startup | <10 eng, customer-facing, daily+ | $8K/mo | modular monolith Next+Postgres |
| enterprise-scale | 50+ eng, regulated, per-PR gates | $250K/mo | domain-bounded services + platform team |
| internal-tool | ≤5 eng, auth-walled, <100 DAU | $500/mo | Retool-first, thin custom |
| marketing-site | SEO-dependent, near-zero write | $200/mo | static-first (Astro/11ty/Next-static) |

## Stack Decision Matrix
SEO-critical → Next.js SSR · internal dashboard → React+Vite · API-first → FastAPI/Fastify · enterprise scale → NestJS+Postgres · rapid prototype → Next.js API routes · document-heavy → MongoDB · complex queries → Postgres.

## Common Issues
N+1 → DataLoader/eager load · slow builds → bundle size/lazy load · auth complexity → Auth.js/Clerk · type errors → tsconfig strict · CORS → middleware config.
