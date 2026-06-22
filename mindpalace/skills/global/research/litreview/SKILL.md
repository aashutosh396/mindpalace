---
name: Academic Literature Orientation
description: Use when the user is starting literature-oriented research ("litreview on X", "literature review on X", "I'm writing a paper on X", "help me research X") — builds a PICO/SPIDER/Decomposition search plan, searches academic papers, and produces a launching-pad orientation guide. Not for one-off paper lookups.
tags: [litreview, literature-review, pico, spider, systematic-review, academic, consensus, papers]
source: alirezarezvani/claude-skills
derived_from: research/litreview (Academic Literature Orientation)
---

# Litreview — Academic Literature Orientation

Produces a **launching pad** — what a generous colleague who knows the field would tell you over coffee — not a finished review. Uses Consensus academic search + DOCX output.

## Phase 0: Intake (3 forcing questions, one at a time)
1. **Research question specificity** — refuse vague; deliver "broad-scope orientation" caveat if still vague.
2. **Framework hint** — PICO (clinical default, ~70%) / SPIDER (qualitative) / Decomposition (technology: Problem/Solution/Evaluation/Limitations) / Hybrid / "you pick".
3. **Tentative depth** — quick scan (5) / standard (10) / deep dive (20). Re-confirmed at the post-Phase-2 checkpoint.

## Phase 1: Reconnaissance
One broad Consensus search to map themes, terminology variants, methodological distinctions, coverage gaps. **Detect plan tier** from first response ("Showing top 10"/upgrade → free 10/search; 20 returned → Pro).

## Phase 2: Framework + Sub-areas
Choose framework (Q2 or override from recon). Generate 4-5 sub-area questions mapped to framework components.

## Checkpoint (forcing moment — wait for user)
Present: 3-4 sentence recon summary + framework breakdown table + depth re-confirmation (showing detected tier + theoretical ceiling) + sub-area options (proceed / merge / replace / restart). **Refuse Phase 3 without explicit choice** — this is the last cheap moment to correct course.

## Phase 3: Targeted Searches (sequential, 1 q/sec)
- **Quick (5):** 5 sub-area searches.
- **Standard (10):** 5 sub-area + 2 review-article + 2 era-gated (`year_max:2015` / `year_min:2021`) + 1 follow-up on highest-cited.
- **Deep (20):** 5 sub-area + 5 review + 4 era-gated + 3 follow-ups on top-cited + 3 spare for emerging threads.

## Cross-Search Intelligence (after Phase 3)
Repeat-hit papers (3+ searches = foundational) · recurring authors (dominant groups) · citation-per-year heuristic (seminal-work ID). Feeds "Start Here" + "Key Research Groups" + Bibliography.

## DOCX (8 sections)
Topic Overview → Start Here (5-7 papers: best review → foundational → frontier → gap) → How the Field Got Here (narrative + timeline + terminology evolution) → Sub-area Guides (each: synthesis + key papers + search terms + Boolean strings) → Key Research Groups → Open Questions & Gaps (methodological/population/conceptual, each with "why it matters") → Bibliography (alphabetical, clickable Consensus links) → Audit Log.

## Agent Integrity Rules
Only cite Consensus-returned papers from this session; training tagged + excluded. Three counts (searches / unique papers / cited). 1 q/sec sequential. Retry once after 3s; stop after 3 consecutive failures. State sparse results explicitly, never fill.

## Anti-Patterns
Parallelizing Consensus; skipping the checkpoint; padding thin results; defaulting off PICO without justification; hardcoding plan tier; skipping era-gated searches in standard/deep; truncating Consensus URLs.
