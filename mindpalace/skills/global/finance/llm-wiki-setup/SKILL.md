---
name: LLM Wiki Setup (investment-research second brain)
description: Use when building a personal investment-research LLM Wiki (Karpathy's pattern) — pure markdown + wikilinks, NO RAG; co-create the user's OWN analysis framework into a living CLAUDE.md by interviewing them, never imposing a template.
tags: [llm-wiki, investment-research, second-brain, karpathy, markdown, wikilinks, no-rag, claude-md, interview]
source: daymade/claude-code-skills
derived_from: llm-wiki-setup
---

# LLM Wiki Setup (投研第二大脑)

Build a finance-research LLM Wiki (Karpathy pattern): pure markdown files + `[[wikilink]]` + LLM maintenance, knowledge compounds with use.

## The soul of this skill
Everyone builds THEIR OWN CLAUDE.md in THEIR language and investment preferences. Two investors looking at one company care about different things (next-quarter orders beating consensus vs. management tone on the call). **Giving them the same template erases the thing that makes the wiki useful.**
- ✅ Your job: interview the user → distill their dimensions → write them into CLAUDE.md **in their words**.
- ❌ Failure: hand a "standard research schema" to fill in, or have them copy `examples/`.
`examples/investment-research-CLAUDE.md` shows possibility only — copying it = the skill failed.

## Red lines (Karpathy's intent — don't over-engineer)
Pure markdown + wikilink + grep. **No RAG / vector DB / embeddings.** Knowledge compounds by pre-compiling into structured pages, not re-retrieving raw docs each query — this is the core idea. Don't add a knowledge graph or auto health-check.

## Mechanism layer vs rule layer
- **Mechanism** (3-level dirs + wikilink + lint + git hook): generic engineering hygiene — `scripts/init_vault.py` installs it, copying is fine.
- **Rule layer** (which dimensions to watch, how to record opinions, analyst attribution, review method, long report vs three lines): the user's investing brain — **grown through interview**, never templated. Copying it betrays the methodology.

## Workflow
- **Phase 0**: new vault → Phase 1; existing + ingest source → `references/ingest_sop.md`; existing + post-earnings review → `references/fulfillment_sop.md`; query → read vault `index.md` + pages, answer with citations, backfill good answers as synthesis.
- **Phase 1 — scaffold mechanism**: `python scripts/init_vault.py <dir>` (empty skeleton, no schema).
- **Phase 2 — interview to co-create CLAUDE.md** (CORE): read `references/interview.md`, ask its 8 dimensions one at a time, write answers in the user's words into the rule-layer placeholders. Cut dimensions they don't care about (minimal > comprehensive). Use examples only for inspiration when stuck ("don't copy, pick what resonates"). Self-check: does the CLAUDE.md read like THIS person? Generic template → redo.
- **Phase 3 — enable anti-rot**: `git init`, `git config core.hooksPath .githooks`, run `lint-vault.py` until green.
- **Phase 4 — first ingest demo**: with the user's REAL source (report/call/notes), walk the HITL 5 checkpoints from `references/ingest_sop.md` so they see the wiki grow from a source. Use their material, not examples.

## Why inline (no context: fork)
It calls other skills (analyst-track-record), runs Bash (scaffold/lint), may spawn Tasks — subagents can't call skills or spawn subagents.
