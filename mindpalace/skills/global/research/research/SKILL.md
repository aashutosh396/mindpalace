---
name: Research Router + Fallback
description: Use when the user makes a general research request that doesn't obviously match a specialist ("research X", "look into X", "investigate X", "what do we know about X") — classifies the question deterministically, routes to a specialist or runs a plan-decompose-search-synthesize-cite fallback, always surfacing the routing decision.
tags: [research, router, web-search, synthesis, citations, literature, briefing, investigate]
source: alirezarezvani/claude-skills
derived_from: research/research (Hybrid Router + Fallback)
---

# Research — Hybrid Router + Fallback

Deterministic classification → specialist delegation OR own plan-search-synthesize workflow. Every invocation ends in one of three outcomes: delegation, fallback execution, or one clarifying question. **Never delegate silently** — always state the routing decision and accept override.

## Phase 1: Minimal Intake (route fast, one question per turn)
- **Q1 (always) — Research question.** "State it in 1-2 sentences. Specific beats broad." Refuse mush: push back once if the user says "research AI".
- **Q2 (always) — Output.** Quick chat briefing (markdown) OR standalone document (.docx with citations). Document mode triggers deeper search budgets + full audit log.
- **Q3 (only if classification ambiguous, ≤1 signal) — Domain disambiguation.** Academic / industry-trends / specific-entity / patents / grant-funding / course-material / none.
- **Q4 (only if Q3 → "none") — Scope.** Quick scan (5 searches) or thorough (15). Most invocations exit after Q1+Q2.

## Phase 2: Deterministic Classification (keyword, not LLM-reasoned)
Score each specialist by counting matched signal phrases (case-insensitive substring):
- **pulse** — reddit, hn, x/twitter, buzz, sentiment, trending, "what are people saying", "pulse on", "current conversation"
- **grants** — nih, grant, r01, k-award, reporter, nosi, funding, study section, principal investigator
- **litreview** — literature review, pico, spider, systematic review, "review papers on", meta-analysis
- **syllabus** — syllabus, course outline, curriculum, reading list, "for my class/students"
- **patent** — prior art, fto, freedom to operate, patent, "patent landscape", invention, novelty search, "ip landscape"
- **dossier** — "dossier on", due diligence, background check, "prep me for", competitor research, investor diligence, interview prep, "background on"

Rules: `max(score) ≥ 2` → route to argmax (high confidence). `max == 1` and only one specialist scored → route there (weak match). Else → fallback (ask Q3). Generic "research [topic]" does NOT auto-route — the verb must be paired with a specialist noun ("dossier on X", not "research X").

## Phase 3a: Specialist Delegation
Pass the question verbatim + output preference. Let the specialist run its own intake. Tag result `[Delegated to: research → {specialist}]`. If a specialist is missing from the environment, skip it in scoring and route to fallback/next-best.

## Phase 3b: Fallback Workflow (8 steps)
1. **Decompose** — 3-5 sub-questions (what/why/how/who/what's next). Show before searching.
2. **Source selection** — recency → web search+fetch (+reddit/hn if signal); academic → scholar filter; entity → offer dossier.
3. **Search** — sequential, 1 q/sec, 2-4 queries per sub-question (broad→narrow).
4. **Read + extract** — WebFetch high-signal results; note source URLs.
5. **Synthesize** — 2-4 paragraphs per sub-question with inline citations; surface disagreement.
6. **Cross-cutting patterns** — consensus, controversy, gaps.
7. **Output** — markdown brief (default) or DOCX.
8. **Audit log** — three counts (sent/received/cited) + per-source reliability tier.

## Agent Integrity Rules
- Cite only sources from this session's tool calls. Training knowledge tagged `[Background — not from search]`, excluded from counts.
- Three-count tracking: queries sent / sources received / sources cited.
- Retry: fail → wait 3s → retry once → log. After 3 consecutive failures, stop and alert.
- When fallback search is thin, surface it explicitly. Never fabricate sources.

## Routing Transparency (mandatory)
State the decision in one sentence ("Routing to litreview — you mentioned PICO + meta-analysis, 2 signals"), offer override, accept and re-route + log if the user overrides.

## Anti-Patterns
LLM-reasoned classification; silent delegation; refusing to route at ≥2 signals; routing on ambiguous (≤1 signal) input; pre-answering the specialist's intake; fabricating thin-result sources; skipping the audit log.
