---
name: alpha-insights
description: "Use when the user wants decision-grade business analysis or strategy research — industry research, competitive analysis, product analysis, business model analysis, opportunity discovery, market entry strategy, investment decision support, strategic planning, or due diligence — and wants an in-depth, evidence-backed HTML research report rather than a quick search answer."
version: 1.0.0
license: MIT
tags: [business-analysis, market-research, competitive-analysis, due-diligence, strategy, investment, consulting, report-generation, research]
source: https://github.com/Ericyoung-183/alpha-insights
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# Alpha Insights — Business Analyst Skill

Acts as a senior business analyst. Discusses the business problem with the user, then runs a disciplined seven-stage research workflow and delivers a decision-grade HTML report (with ECharts charts). Not an "AI search engine" — every conclusion is tied to graded evidence.

## When to use
User asks about any of the ten research scenarios:
- Foundational: industry research, competitive analysis, product analysis, business model analysis
- Opportunity: business opportunity discovery
- Strategic: market entry strategy, investment decision support
- Planning: strategic planning, due diligence
- Specialized: special topics / custom consulting

Triggers on vague directions too ("I'm thinking of entering X space") — use questioning to focus.

## Language rule
Detect the language of the user's first message; use it for all interaction and deliverables.

## The seven stages
Each stage produces a deliverable file under a workspace dir (`{cwd}/workspace/{slug}/`). Each deliverable feeds the next — never skip a node.

1. **Briefing** → `user_brief.md`. 2-3 quick background searches (broadcast a one-sentence conclusion only, never raw results). Identify scenario + user context. Confirm **report tier** via AskUserQuestion. Ask 2-4 clarifying questions at once. Do NOT ask "which dimensions to focus on" — those come from Stage 2.
2. **Framing** → `research_definition.md`. Match 1 primary + 2-4 enhanced frameworks (PESTEL, Five Forces, BMC, TAM/SAM/SOM, etc.). User confirms frameworks. MECE-decompose core question into 3-5 sub-questions, assign an analysis lens to each. Mark irrelevant framework dimensions N/A. Add context anchoring ("who we are, where we stand, what we need").
3. **Planning** → `research_plan.md`. Generate opinionated, falsifiable hypotheses mapped Q→H→Lens. Plan research tracks + data sources. Fill a **chapter blueprint** per sub-question (Tier 2: 2-3 items; Tier 3: 4-6). For due diligence/M&A/target screening, include a **primary-source plan**. Record interview decision (cannot be skipped).
   - **3.5 Interview (optional)** → `interview_guides.md` if user wants expert interviews.
4. **Research** → `evidence_base.md`. Three layers: overview scan → directed deep dive (per track) → evidence integration with triangulation. Tracks: A public data / B directed sources / C interviews / D knowledge base / E social / F internal DB / G user voice. Grade every key fact A/B/C/D confidence; log headline numbers/entity facts in an Evidence Claim Ledger. Trace to original sources, not second-hand citations.
5. **Insights** → `insights.md`. Apply 8 judgment rules (So What chain ≥3 layers, key-variable ID, contrarian test, SMART, pre-mortem, priority ranking). Broadcast one line per rule. User confirms insight direction, THEN run Red Team (adversarial) + Blue Team (blind-spot) review; fix conclusions/scores on the spot, supplement fatal gaps immediately.
6. **Report** → `report.html`. Organize chapters by **insight theme** (titles are findings, not questions). Conclusion-first (pyramid principle). Back-link headline numbers/charts to the Evidence Claim Ledger. Anti-pattern self-check.
7. **Iteration & wrap-up**. Apply changes via the cascade rule (below); output wrap-up summary.

## Report tiers (confirm in Stage 1)
- **Tier 1 Quick Scan** — 1-2 pages, Layer-1 research only, exec summary only.
- **Tier 2 Topical Brief** — 5-8 pages, Layers 1-2, condensed seven-section, ≥3 charts.
- **Tier 3 Deep Report** (default) — 20-35 pages, all layers, full seven-section, ≥6 charts.

## Change cascade rule (Stage 7 iterations)
The chain is directional: research_definition → research_plan → evidence_base → insights → report. When editing an upstream deliverable, ALL downstream nodes must be incrementally updated — never skip intermediates. Classify the request and start from the right stage:
| Request | Start | Cascade |
|---|---|---|
| Wording/layout/chart-style only (data unchanged) | S6 | S6 only |
| "Search more" / add evidence / depth | S4 | S4→S5→S6 |
| "This conclusion is wrong" / add a point | S5 | S5→S6 |
| Change angle / add sub-question | S2 | S2→S3→S4→S5→S6 |
| User provides interview notes | S4 | S4→S5→S6 |

When uncertain, classify upward (over-cascade rather than skip). During cascade, do NOT advance the state machine — only re-run the affected stages' logic.

## Quality gates
Each stage has a structure-validation gate (deliverable exists with required content) plus risk-based checks: independent quality review (IQR subagent) at S2/S4/S6, Red/Blue Team at S5, anti-pattern + self-check at S6. A FAIL blocks transition; fix or roll back. Translate any script JSON output into plain language for the user — never show raw JSON.

## Evidence standards
- Confidence A/B = trustworthy; C = "needs further validation"; D = never a key argument.
- High-certainty recommendations ("must enter", "acquire now") require A/B evidence + any needed primary sources; otherwise downgrade to conditional and record why.
- Aggregators/media = leads only, not primary sources. Multiple secondary sources tracing to one origin do NOT count as independent cross-validation.

## Gotchas
- **HTML report must be written via Python, not the Write tool.** The model output layer randomly filters the `data` keyword in ECharts configs (breaking charts), and the Write tool truncates large HTML. Generate step by step (1-2 chapters per call) using the repo's `scripts/report_helper.py` `ReportBuilder` (init → add_chapter/add_chart → save_state → build). Fallback: `build_report()`; last resort: manual concat with `dk = "dat"+"a"` workaround.
- All charts use ECharts (no CSS charts); layout components (cards, boxes) use CSS.
- Self-contained: do NOT invoke other skills — other users may not have them installed.
- Never write to the skill install dir; all deliverables go to the workspace dir.
- Workspace path + tier are stored in `_state.json` (created by `scripts/harness/state_manager.py init`); recover the path at every stage start.
- If Bash/Python unavailable, harness checks degrade to manual self-verification against the gate-conditions table; report falls back to Write-tool output (accept the data-filtering risk).

## Helper scripts (in source repo, not copied here)
`scripts/harness/` holds `state_manager.py`, `stage_gate.py`/`stage_gate_hook.py`, `resume_check.py`, `dashboard.py`, hook scripts; `scripts/report_helper.py` holds `ReportBuilder`. Knowledge/framework/methodology files live under `frameworks/`, `methodology/`, `resources/`, `references/` in the repo. Clone the repo to use the full harness: https://github.com/Ericyoung-183/alpha-insights
