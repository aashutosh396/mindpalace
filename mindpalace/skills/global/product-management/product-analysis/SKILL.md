---
name: Product Analysis (Multi-Path Parallel Audit)
description: Use when running a product audit, pre-launch self-review, UX/API/architecture audit, or competitive benchmark — spawns parallel exploration agents across dimensions and synthesizes a prioritized optimization report.
tags: [product-audit, ux-audit, api-review, architecture, self-review, optimization, parallel-agents, prioritization]
source: daymade/claude-code-skills
derived_from: product-analysis
---

# Product Analysis

Multi-path parallel product analysis. Same task, multiple AI perspectives, deep synthesis.

## Step 0: Detect tools & project type
- `which codex` — if present, run cross-model analysis too; if absent, proceed silently with Claude agents only (do NOT ask user to install).
- Detect project type: `ls package.json / pyproject.toml / Cargo.toml / go.mod`.

## Scope modes (parse from args)
| Scope | Covers | Agents |
|-------|--------|--------|
| `full` (default) | UX + API + Architecture + Docs | 5 explore + codex |
| `ux` | navigation, info density, journey, empty state, onboarding | 3 |
| `api` | endpoint coverage, health, error handling, consistency | 2 |
| `arch` | module structure, dependency graph, duplication, separation | 2 |
| `compare X Y` | self-audit + competitive benchmarking | 3 + competitors-analysis |

## Phase 1: Parallel exploration (launch all background simultaneously)
Spawn one Explore agent per dimension. Each must return file paths, line numbers, element counts:
- **A — Frontend nav & info density**: top-level components mounted, sidebar/tab/panel counts, first-screen interactive element count, duplicate entry points (same feature reachable 2+ places).
- **B — User journey & empty state**: empty-state clickable count, onboarding steps, input-area controls (high vs low freq), mobile vs desktop, can a new user finish first task in 3 min?
- **C — Backend API & health**: list all endpoints (method+path+purpose), unused/no-consumer endpoints, error-handling consistency, auth patterns, duplicate functionality.
- **D — Architecture** (full/arch): dependency graph, circular/tight coupling, duplication in 3+ places, single-responsibility check, dead code.
- **E — Docs & config** (full): README claims vs reality, config consistency, outdated docs, test coverage gaps.

If codex detected, run 2-3 codex commands in parallel (`--full-auto`) with the same dimensional prompts for a second model's view.

## Phase 2: Competitive benchmarking (compare scope)
Invoke a competitor-analysis flow per competitor: clone repo, evidence-based code analysis with file:line citations, generate profile.

## Phase 3: Synthesis (main context)
- **Cross-validate**: agreement = high confidence; disagreement = investigate deeper; single-model finding = validate manually.
- **Quantify**: first-screen interactive elements, feature entry-point duplication, endpoints w/o consumer, onboarding steps to first value, module coupling score.
- **Report** with Executive Summary → Quantified Findings table → P0 (block launch) → P1 (launch week) → P2 (next sprint) → Cross-Model Insights → Competitive Position.

## Checklist
Parse scope → detect codex+project → launch 3-5 explore agents → launch codex → run compare if needed → collect → cross-validate → quantify → P0/P1/P2 report.
