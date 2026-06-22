---
name: Deep Research Report Generator
description: Use when the user requests a research report, literature review, market/industry analysis, competitive landscape, or policy/technical brief — generates a format-controlled, citation-backed report via lead-agent + subagent fan-out, source governance, and multi-pass synthesis.
tags: [research, report, literature-review, citations, source-governance, multi-agent, counter-review, market-analysis, enterprise]
source: daymade/claude-code-skills
derived_from: deep-research
---

Create high-fidelity research reports with strict format control, evidence mapping, source governance, and multi-pass synthesis.

## Architecture: Lead Agent + Subagents
Lead agent coordinates; subagents do the searching (raw results stay in their context and are discarded — lead sees only distilled notes, ~60-70% context reduction). Pipeline: P0 environment/policy → P1 task board → P2 dispatch+investigate (parallel, write notes files) → P3 citation registry → P4 evidence-mapped outline → P5 draft from notes → P6 counter-review → P7 verify → polish.

## Mode selection
- **Topic mode:** Enterprise (company) — six-dimension collection + SWOT/risk-matrix/barrier-quantification; or General (industry/policy/tech) — standard P0-P7.
- **Depth:** Standard (5-6 tasks, 3000-8000 words) or Lightweight (3-4 tasks, 2000-4000 words; single entity <30 words).

## Source governance
**Accessibility classification (every source):** `public` ✅ always; `semi-public` ✅ with disclosure; `exclusive-user-provided` (user's Crunchbase Pro etc. for *third-party* research) ✅ — use as advantage; `private-user-owned` (user's own accounts researching themselves) ❌ **circular verification ban**. Never use the user's private data to "discover" what they already know about themselves.
**Source-type labels:** official / academic / secondary-industry / journalism / community / other.
**Quality gates** (Standard / Lightweight): ≥30% / ≥20% official sources; max single-source share ≤25% / ≤30%; min unique domains 5 / 3; ≥12 / ≥6 approved sources.
**AS_OF date:** set at P0; include source publication date with every citation; downgrade confidence for stale sources (studies >3yr, news >6mo for fast topics).

## Phases
- **P0:** check capabilities (web_search required; web_fetch for DEEP tasks else SCAN-only; subagent dispatch preferred; filesystem writable). Set AS_OF, MODE, source policy, counter-review plan.
- **P1 — Task board:** decompose into 4-6 (or 3-4) tasks, each with expert role, one-sentence objective, 2-3 queries, DEEP/SCAN depth, output path, parallel group (A independent / B depends on A; max 3 per group).
- **P2 — Dispatch:** subagents search, fetch, tag each source with Source-Type + As-Of + Authority(1-10); output ≤10 one-sentence findings, deep-read notes (2-3 full sources for DEEP), and a gaps section (searched-but-not-found, alternative interpretations). Discard raw results after writing notes.
- **P3 — Citation registry:** merge all task notes, dedup by URL, assign final sequential [n], apply quality gates, drop sub-threshold sources explicitly. These [n] are FINAL — P5 cites only from Approved; dropped never reappear. For info black boxes (no public footprint), state plainly "UNABLE TO VERIFY from external perspective", document failed search attempts, never fill gaps with speculation or privileged data.
- **P4 — Outline:** topic-first (not task-order), map each section to findings + source numbers, flag counter-claim candidates and recency checks.
- **P5 — Draft from notes:** every factual claim/number cited [n]; per-section confidence marker (High/Med/Low + rationale); counter-claim sentence when evidence conflicts; no new sources; `[unverified]` for unsupported. Never invent URLs or fabricate data.
- **P6 — Counter-review (mandatory, find ≥3 issues):** could the conclusion be wrong? which high-impact claims rest on a single source? which lack official/academic backing? stale sources on time-sensitive claims? Output a "Key Controversies" section.
- **P7 — Verify:** cross-check every [n] vs approved registry; spot-check 5+ claims to notes; remove non-traceable claims; confirm no dropped source resurrected.

## Anti-patterns
Single-pass drafting; splitting passes by section; ignoring the format contract; claims without citations; mixing conflicting dates without flagging; lead agent reading raw search results; inventing URLs; resurrecting dropped sources; missing AS_OF; skipping counter-review; circular verification; ignoring exclusive user-provided sources for competitor research.
