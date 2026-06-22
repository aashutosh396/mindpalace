---
name: Spec to Repo
description: Use when someone provides a natural-language project spec and wants a complete runnable repo ("build me an app", "scaffold a project", "turn this idea into code") — stack-agnostic spec interpreter that generates real working code, not stubs.
tags: [scaffold, spec, bootstrap, starter-repo, code-generation, project-generator, fastapi, nextjs, cli, repo]
source: alirezarezvani/claude-skills
derived_from: product-team/spec-to-repo
---

# Spec to Repo

Turn a natural-language project spec into a complete, runnable starter repo. A spec interpreter, not a template filler. Stack-agnostic (Next.js, FastAPI, Rails, Go, Rust, Flutter…). *Not this skill* for a Stripe+Auth SaaS specifically — use saas-scaffolder.

## Phase 1 — Parse & Interpret

Extract silently: app name, description, features, tech stack, auth, database, API surface, deploy target.

**Stack inference** (when unspecified): "web app/dashboard/SaaS" → Next.js+TS; "API/backend/microservice" → FastAPI or Express; "mobile" → Flutter/React Native; "CLI" → Go/Python; "data pipeline" → Python; "high performance/systems" → Rust/Go.

Present interpretation back (App / Stack / Features / Database / Auth / Deploy) and ask: "Does this match? Corrections before I generate?" Flag ambiguities; ask **at most 3** clarifying questions. If "just build it", proceed with best-guess defaults. **Honor explicit tech preferences — non-negotiable.**

## Phase 2 — Architecture

Before writing files: (1) select stack template; (2) define full file tree; (3) map each feature to ≥1 file; (4) design DB schema (tables/fields/types); (5) list every dependency with version constraints; (6) plan API routes (method, path, request/response shape). Present the file tree to the user before generating.

## Phase 3 — Generate

Rules:
- **Real code, not stubs** — every function has a real implementation; no `// TODO` / `pass`.
- **Syntactically valid** — every file parses.
- **Imports match dependencies** — every import in the manifest.
- **Types included** — TS types, Python hints, Go structs.
- **`.env.example`** — every required var, commented with purpose.
- **README.md** — description, prerequisites, setup (clone/install/configure/run), scripts.
- **CI** — `.github/workflows/ci.yml`: install, lint (if linter present), test, build.
- **.gitignore** — stack-appropriate (node_modules, __pycache__, .env, build artifacts).

Generation order: manifest → config files → DB schema/migrations → core logic → API routes → UI → tests → README.

## Phase 4 — Validate

- [ ] Every imported package in the manifest
- [ ] Every import-referenced file exists
- [ ] `.env.example` lists every env var used in code
- [ ] `.gitignore` covers build artifacts + secrets
- [ ] README setup actually works
- [ ] No hardcoded secrets/keys/passwords
- [ ] ≥1 test file exists
- [ ] Build/start command documented and works

## Progressive Enhancement (complex specs)

MVP (core only, working end-to-end) → Auth → Polish (error handling, validation, loading states) → Deploy (Docker, CI, deploy config). After MVP ask: "Core works. Add auth/polish/deploy, or iterate?"

## Anti-Patterns

Placeholder code; stack override (don't pick Next.js when user said Flask); missing .gitignore; phantom imports (cross-check before finishing); over-engineering MVP (no Redis/rate-limiting/WebSockets in v1); ignoring stated DB/preference; missing env vars; no tests; hallucinated library APIs (stick to stable, documented methods).
