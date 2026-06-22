---
name: Research Operations Orchestrator
description: Use when an enterprise research request could span clinical study design, R&D finance, market sizing, or product/user research and you need to route it to the right discipline — deterministic two-signal routing with grill-first discipline.
tags: [research-ops, orchestrator, routing, clinical-research, research-finance, market-research, product-research, rd]
source: alirezarezvani/claude-skills
derived_from: research-ops/skills/research-ops-skills
---

# Research Operations Orchestrator

Routes an enterprise research inquiry to one of four disciplines, then returns a digest. This is the counterpart to academic research (finding literature/grants/patents): this domain **plans, funds, scopes, and synthesizes** research.

## Signal table (deterministic routing)
| Signal | Keywords | Route to |
|---|---|---|
| CLINICAL | clinical trial, protocol, endpoint, sample size, power, phase 1/2/3, biostatistics, estimand | clinical study design |
| RD_FINANCE | R&D budget, burn, runway, F&A, indirect rate, capitalize vs expense, rNPV, portfolio ROI | research finance |
| MARKET | TAM, SAM, SOM, market sizing, survey, sampling, MoE, segmentation, competitive intelligence | market research |
| PRODUCT | user interview, JTBD, usability test, concept test, research repository, insight synthesis, saturation | product research |

## Routing logic
1. **Explore before asking.** Check the workspace: a `protocol.json` → clinical; `program-budget.json` → finance; `tam-model.json` → market; `interview-guide.md` → product. If the artifact resolves the lane, route silently.
2. **Two-signal threshold.** Single weak signal → ask ONE clarifying question with a recommended answer (name the two candidate lanes + signal-table rationale). Never bundle questions.
3. **Multi-lane inquiry** (e.g., "design this trial AND budget it" = CLINICAL + RD_FINANCE): walk depth-first — highest-confidence lane first → digest → ask "now run [second]? recommended yes because [dependency]". **Never silently chain.**
4. **Digest** ≤200 words: analyzed, top-3 findings (each anchored to a canon citation), top-3 next actions (named human owner where applicable), artifact path, and ONE grill challenge.

## Lane-defining forcing questions (lock before invoking)
- CLINICAL: primary endpoint clinical or surrogate — if surrogate, validated for this indication? (FDA Surrogate Endpoint Table; BEST)
- RD_FINANCE: research phase or development phase, and can you evidence technical feasibility? (IAS 38; ASC 730)
- MARKET: TAM top-down or bottoms-up — computed both ways to triangulate? (Bessemer/a16z; Fermi)
- PRODUCT: study generative (discover) or evaluative (test)? — method follows the goal. (Rohrer, NN/g)

## Hard rules
- Clinical output = estimate + named clinical owner (never fact).
- Capitalize-vs-expense routes to a named finance owner (never auto-decide).
- Market size shows method + both-ways triangulation + assumptions (never one unsourced number).
- Product insight requires recurrence across independent participants (singletons = anecdotes).
- Don't run all four "to be thorough" — pick one, digest, chain if needed.
