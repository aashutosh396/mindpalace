---
name: CAIO Review (Forcing Questions)
description: Use when shipping an AI feature without an eval set, choosing between API / fine-tune / self-hosted, or classifying a use case under the EU AI Act — six eval-demanding CAIO questions before any AI ships.
tags: [caio-review, ai-evals, hallucination-slo, eu-ai-act, model-build-vs-buy, ai-cost-economics, ai-hiring, forcing-questions]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/caio-review
---

# CAIO Review — Six Forcing Questions

Eval-demanding pressure test for any AI plan. Run before: shipping any AI feature, signing a multi-year AI vendor contract, EU launch of an AI feature, a major AI hire, a fine-tuning commitment, or adopting AI in a regulated domain — and whenever someone says "AI" near "competitive advantage" or "moat."

## The six questions

1. **What does this AI need to be good at, and how would you measure it?** No eval set = no ship. Define ≥50–100 representative inputs, expected outputs or grading rubric, edge cases (ambiguous, adversarial, format-edge). If you can't write down what "good" looks like, you have a vibe, not a feature.
2. **SLO on hallucination/error rate, and the fallback?** Quantified SLO ("<5% hallucination on factual queries"), detection (monitoring/sampling/feedback loop), fallback (human-in-loop, lower-risk default, refuse-to-answer), blast radius if breached.
3. **EU AI Act risk tier — conformity assessment required?** PROHIBITED → can't launch in EU, re-scope. HIGH → conformity assessment + EU DB registration + obligations (3–12 months, $50–200K). LIMITED → transparency (chatbot disclosure, AI-content marking). MINIMAL → none; NIST AI RMF voluntary. Classify if any EU residents affected OR domain is regulated.
4. **API, fine-tune, or build?** ~80% of B2B SaaS use cases → API; ~15% → fine-tune (domain-specific behavior + labeled data + ML team + high volume); <1% → build. Decide on economic breakeven AND practical feasibility (data, team, compliance).
5. **12-month cost trajectory at expected scale?** API scales linearly; self-hosted is mostly fixed (breakeven ~1–10B tokens/month for 70B-class). Hidden self-hosted costs: ops, monitoring, updates, failover, security. Hidden API costs: lock-in, capability drift, rate limits, data residency. Prompt caching is the most underrated lever.
6. **What role unblocks this — prerequisites hired first?** AI engineer (applied: prompts, evals, deployment — most startups need this) vs ML engineer (fine-tuning/retraining infra — needs platform engineer + labeled data first) vs research scientist (model invention — only if model IS the product). Don't hire a research scientist first.

## Output

Verdict 🟢 SHIP / 🟡 SHARPEN / 🔴 BLOCK. State the decision (model selection | risk classification | economics | next hire), eval discipline (set committed? SLO? fallback), and 3 concrete next steps. Route training-data implications to CDO, vendor contracts/output liability to legal, prompt-injection/poisoning threat model to CISO, multi-year TCO to CFO.
