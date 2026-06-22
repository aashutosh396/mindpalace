---
name: Multi-Model Consensus (cross-eval)
description: Use when a high-stakes, irreversible memo needs an independent sanity check before a decision — M&A, major fundraise, layoff, pivot, regulatory commitment — runs the memo through multiple model providers and reconciles divergences.
tags: [consensus, multi-model, sanity-check, irreversible, m&a, fundraise, adversarial-review, decision]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/cross-eval
---

# Multi-Model Consensus

Runs the same memo through multiple model providers and reconciles divergences. For high-stakes, irreversible decisions where single-model bias is too costly.

## When to run
Before signing a term sheet, announcing a layoff, committing to a regulated market, any decision whose reversal costs >6 months, or when a board vote was split / had a critical dissent.

## Models (graceful degradation)
Try each available in order: Claude (always), then Codex/OpenAI (if key/CLI present), then Gemini (if key/CLI present). If only one model is available, run **adversarial mode** — same model, different prompt seeds — and clearly label output as single-model.

## Workflow
1. Read the memo.
2. Probe environment for available model CLIs / API keys.
3. Send each model the memo with this reviewer prompt:
   > "You are an independent C-suite reviewer. Identify the top 3 concerns, top 3 supports, and your vote (APPROVE / REJECT / DEFER). Do not deferentially agree — assume the reasoning is flawed until proven otherwise."
4. Collect independent reviews.
5. Reconcile: where do they agree, where diverge?
6. Surface divergences as questions for the founder.

## Output
```markdown
# Cross-Eval: <memo title>  (Models: Claude / Codex / Gemini or fallbacks)
## Vote Tally — | model | vote | confidence |
## Consensus Concerns (≥2 models flagged)
## Divergent Concerns (1 model flagged)
## Consensus Supports (≥2 models endorsed)
## Recommendation
- 🟢 GO if 2+ APPROVE and no critical concern from any model
- 🟡 PAUSE if any DEFER or any concern critical
- 🔴 STOP if 2+ REJECT
## Open Questions for Founder
```

## Why it matters
Single-model recommendations carry systematic biases. Disagreement is signal, not noise. This is the safety net before irreversibility — not a substitute for outside counsel or a real board.

## Adversarial fallback (Claude-only)
Run 3 independent passes: (1) standard reviewer, (2) devil's advocate (must find 3 critical concerns), (3) steelman (must find 3 strongest reasons to approve). Treat as suggestive, not conclusive.
