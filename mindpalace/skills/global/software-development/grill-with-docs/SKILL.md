---
name: Grill with Docs
description: Use when stress-testing a plan against a project's documented domain language (CONTEXT.md) and recorded decisions (docs/adr/) — relentless one-question-at-a-time interview that sharpens terminology and writes glossary/ADR entries inline as they crystallize.
tags: [grilling, ddd, ubiquitous-language, context-md, adr, glossary, plan-review, domain-modeling, interview]
source: alirezarezvani/claude-skills
derived_from: engineering/grill-with-docs (Matt Pocock, MIT)
---

# Grill with Docs

Interview the user relentlessly about every aspect of the plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies one by one. For each question, provide your recommended answer. **Ask one question at a time, waiting for feedback before continuing.** If a question can be answered by exploring the codebase, explore the codebase instead.

## Domain awareness (file structure)
Most repos have a single context: root `CONTEXT.md` + `docs/adr/NNNN-slug.md`. If `CONTEXT-MAP.md` exists at root, the repo has multiple contexts; the map points to where each lives (per-context `CONTEXT.md` + `docs/adr/`). Create files lazily — only when you have something to write.

## During the session
- **Challenge against the glossary** — term conflicts with `CONTEXT.md`? Call it out: "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"
- **Sharpen fuzzy language** — propose a precise canonical term: "You say 'account' — Customer or User? Those are different things."
- **Discuss concrete scenarios** — invent edge cases that force precision about boundaries between concepts.
- **Cross-reference with code** — when the user states how something works, check whether code agrees; surface contradictions.
- **Update CONTEXT.md inline** — when a term resolves, edit it right there (don't batch). `CONTEXT.md` is a **glossary and nothing else** — totally devoid of implementation details, not a spec or scratch pad.

## Offer ADRs sparingly
Only when ALL three are true:
1. **Hard to reverse** — changing your mind later is costly.
2. **Surprising without context** — a future reader will wonder "why this way?"
3. **Result of a real trade-off** — genuine alternatives existed and you picked one for specific reasons.

If any is missing, skip the ADR.

## Pre-flight (optional validators)
If `CONTEXT.md` exists, lint it before grilling. If `docs/adr/` exists, scan for numbering gaps / malformed ADRs / status inconsistencies. Cross-reference glossary bold-terms against codebase usage to flag dead glossary (defined-but-unused) and code-only common nouns that may need definitions — use these as opening grill questions. Closing: re-run the consistency check, then summarize terms added/refined, ADRs written, scenarios discussed, open items.
