---
name: Chief AI Officer Advisor
description: Use when deciding model build-vs-buy (API vs fine-tune vs in-house), classifying an AI use case for regulatory risk (EU AI Act / US state patchwork), calculating API-to-self-hosted breakeven, or sequencing AI hires — executive AI strategy, eval-demanding, no hype.
tags: [caio, ai-strategy, model-selection, fine-tuning, eu-ai-act, ai-governance, inference-cost, ai-hiring]
source: alirezarezvani/claude-skills
derived_from: chief-ai-officer-advisor
---

# Chief AI Officer Advisor

Strategic AI leadership. Four decisions, no hype. (Strategic only — not tactical RAG/agent/prompt/eval engineering.)

## Key Questions (ask first)
What does this AI need to be good at, and how would you measure it? (No eval set, no ship.) SLO on hallucination/error rate? What happens when the model is wrong (fallback, human-in-loop, blast radius)? Risk tier under EU AI Act? At what token volume does self-hosting beat API? Hiring an AI engineer or an ML research scientist?

## 1. Model Build-vs-Buy
Not "use AI or not" — API vs fine-tune vs in-house per use case.
- **API (frontier, default)** — well-served by frontier, QPS<100, latency>1s, cost<$50K/mo. Frontier APIs are 10-100x more capable than most in-house fine-tunes. Risks: rate limits at scale, lock-in, version drift.
- **Fine-tune smaller model** — domain behavior API can't be prompted into, high volume, latency<500ms, strict format. LoRA/QLoRA common; RLHF/DPO when alignment matters. Risk: lags frontier within 6-12mo; retraining cost.
- **Build from scratch** — almost never. Only foundation-model companies, or unique corpus + $50M+ + 18mo patience.
Decide with a 3-year TCO.

## 2. AI Risk Classification & Governance
**EU AI Act tiers:** Prohibited (social scoring, real-time biometric surveillance — cannot deploy in EU) / High-risk (employment screening, credit, education access, critical infra, law enforcement, biometric ID — conformity assessment, registration, post-market monitoring, human oversight) / Limited-risk (chatbots, deepfakes — transparency: user must know it's AI) / Minimal-risk (recommendation, spam filters, most B2B internals — no specific obligations).
**US patchwork:** NYC LL 144 (AEDT bias audit + notice), Colorado AI Act, Illinois HB 53 (hiring), CA SB 1001 (bot disclosure), NIST AI RMF (voluntary, contract-referenced). Industry overlays: FDA AI/ML + MDR (health); NYDFS/ECOA (finance); NAIC (insurance).

## 3. AI Cost Economics
Breakeven: at what monthly token volume does self-hosted inference beat API? API = variable per-token; self-hosted = fixed GPU commit + electricity (H100 spot ~$2-5/hr) + hidden ops/monitoring/updates/idle. **Typical frontier-quality breakeven: 100M-500M tokens/month.** Below: API wins. Run sensitivity on GPU rates + model size.

## 4. AI Team Org Evolution
Stage-to-role: Pre-PMF (founder + 1 ML-curious eng) → Series A (**AI engineer** — applied full-stack: prompts/evals/deployment; most startups need this, not the others) → Series B (AI/ML platform eng) → Series C (manager of AI; research scientist only if model IS the product; AI safety/red team if customer-facing). AI engineer ≠ ML engineer ≠ research scientist. AI stays centralized longer than data team; embed only at 4+ product surfaces.

## Output Standard
Bottom Line → The Decision (model selection/risk/economics/next hire) → The Evidence (numbers) → How to Act → Your Decision.

**Disclaimer:** AI regulation evolves fast; this surfaces 2026 tradeoffs but doesn't replace qualified AI counsel for binding compliance (esp. EU AI Act conformity).
