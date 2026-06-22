---
name: Codebase Onboarding
description: Use when onboarding a new engineer, writing architecture-overview docs for an unfamiliar repo, or producing tech-lead briefings — analyzes a codebase and generates audience-aware onboarding documentation.
tags: [onboarding, documentation, architecture, codebase-analysis, developer-experience, handoff, tech-lead-briefing, setup-guide]
source: alirezarezvani/claude-skills
derived_from: codebase-onboarding
---

# Codebase Onboarding

Analyze a codebase and generate onboarding documentation for engineers, tech leads, and contractors. Optimized for fast fact-gathering and repeatable outputs.

## When to use
Onboarding a new team member/contractor · rebuilding stale docs after large refactors · preparing internal handoff documentation · creating a standardized onboarding packet for services.

## Workflow
1. Run the codebase analyzer against the target repo (gather facts; JSON output available).
2. Capture key signals: file counts, detected languages, config files, top-level structure.
3. Fill the onboarding template (architecture/stack discovery, key-file inventory, local setup, common-task guidance, debugging + contribution checklist).
4. Tailor depth by audience:
   - **Junior**: setup + guardrails
   - **Senior**: architecture + operational concerns
   - **Contractor**: scoped ownership + integration boundaries

## Common pitfalls
Writing docs without validating setup commands on a clean environment · mixing architecture deep-dives into contractor-oriented docs · omitting troubleshooting + verification steps · letting onboarding docs drift from current repo state.

## Best practices
1. Keep setup instructions executable and time-bounded. 2. Document the "why" for key architectural decisions. 3. Update docs in the same PR as behavior changes. 4. Treat onboarding docs as living operational assets, not one-time deliverables.
