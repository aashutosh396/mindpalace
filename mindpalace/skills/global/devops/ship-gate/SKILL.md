---
name: Ship Gate
description: Use for "am I ready to ship", "pre-launch audit", "can I deploy", "go-live checklist", or when a deploy command is issued — pre-production audit across 8 categories that blocks until critical items pass.
tags: [pre-deploy, audit, security, deploy-checklist, go-live, preflight, production-readiness, rls, secrets, rollback]
source: alirezarezvani/claude-skills
derived_from: ship-gate
---

# Ship Gate

Pre-production audit that scans a codebase and reports pass/fail/manual across 8 categories before anything ships. Stack-agnostic. It audits; it does NOT fix. Not for CI/CD setup or infra provisioning, and pre-deploy only (never runs after deployment).

## Intercept behavior
When the user says "push to production", "deploy", "ship it", "go live": do NOT proceed. Ask "Have you run the ship gate? Want me to scan now?" If they already ran it, ask when — if >24h ago or code changed since, recommend re-running.

## How it works
**Step 1 — Detect stack.** Framework (Next/React/Vue/Svelte/Astro/Express/Fastify/Hono, Django/Flask/FastAPI, Go, Rust), database (Supabase/Prisma/Mongo/Postgres/Firebase), deploy target (Vercel/Netlify/Docker/Fly/Railway), auth (Clerk/NextAuth/Supabase/Firebase), AI/LLM (OpenAI/Claude/Gemini). Report detected stack before proceeding — stack-tagged checks are skipped if not detected.

**Step 2 — Run automated checks** in order: SEC, DB, CODE, DEP, AI, DEPLOY, FE, OBS (security + DB first — most critical findings). Report progress per category (`[1/8] Security: 3 FAIL, 12 PASS, 3 SKIP`). Each finding: PASS / FAIL (with file:line) / SKIP.

**Step 3 — Manual confirmation** for non-automatable checks (backup restore tested, rollback plan exists, staging test passed) — present as a checklist.

**Step 4 — Verdict** by severity:
- **CRITICAL** (must fix): secrets exposed, no auth on routes, no HTTPS, SQL injection, no RLS on Supabase tables.
- **HIGH** (should fix): no error boundaries, no rate limiting, console.logs in prod, no pagination.
- **ADVISORY** (recommended): no OG tags, no custom 404, no analytics, no SBOM.

Verdict: any critical → **DO NOT SHIP**. Only high remaining → **SHIP WITH CAUTION** (acknowledge risks). Zero critical → **CLEAR TO SHIP**.

## Categories (code prefixes)
SEC (Security) · DB (Database) · DEPLOY (Deployment) · CODE (Code Quality) · AI (AI/LLM Security) · DEP (Dependencies) · FE (Frontend Quality) · OBS (Observability).

## Scope
Reports issues with file locations + remediation guidance; another skill or the user does the fix. Does not set up CI/CD, provision infra, or configure monitoring tools.
