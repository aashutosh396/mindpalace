---
name: LLM Cost Optimizer
description: Use whenever LLM API costs come up or an AI feature is being built — cut LLM spend 40-80% via model routing, prompt caching, output-length control, prompt compression, and cost observability, without degrading quality.
tags: [llm-cost, token-optimization, model-routing, prompt-caching, ai-spend, max-tokens, semantic-cache, cost-observability, mlops]
source: alirezarezvani/claude-skills
derived_from: engineering/llm-cost-optimizer
---

# LLM Cost Optimizer

Cut LLM API spend 40-80% without degrading user-facing quality. AI API costs are engineering costs: measure first, optimize second, monitor always. **NOT** for RAG pipeline design or prompt quality.

## Step 0 — Classify the Mode

| Mode | When |
|---|---|
| Cost Audit | spend exists, no clear breakdown |
| Optimize Existing | cost drivers known, apply targeted fixes |
| Design Cost-Efficient Architecture | building new AI feature, wire controls before launch |

Pull answers from the conversation first. If logging doesn't exist, **logging is deliverable #1** — you cannot optimize what you cannot see.

## Mode 1 — Cost Audit

1. **Instrument every request** — log model, input/output tokens, latency, endpoint/feature, user segment, calculated cost.
2. **Find the 20% causing 80%** — sort by feature × model × token count; usually 2-3 endpoints dominate.
3. **Classify by complexity** — Simple (classification/extraction/short → small model: Haiku/4o-mini/Flash); Medium (summarization/structured → mid: Sonnet/4o); Complex (multi-step reasoning/codegen/long context → large: Opus/o3).

## Mode 2 — Optimize (apply in ROI order, measure at each step)

1. **Model routing (60-80% on routed traffic)** — route by task complexity, not default. Even routing 20% of traffic to a cheaper model is meaningful. Start there.
2. **Prompt caching (40-90% on cacheable)** — cache system prompts, static context, document chunks, few-shot examples. Targets: >60% hit for doc Q&A, >40% for chatbots. Flag if a system prompt >~2,000 tokens is sent every request.
3. **Output length control (20-40%)** — explicit length instructions, schema-constrained output, per-endpoint `max_tokens` (never global), stop sequences. Flag any uncapped endpoint as a leak.
4. **Prompt compression (15-30% input)** — strip filler ("Please carefully analyze…" → "Analyze:"), remove context duplicated from system prompt, strip HTML/markdown. **Caution:** over-compression causes hallucination → retries that erase savings. Compress filler, preserve task-critical instructions.
5. **Semantic caching (30-60% hit)** — cache by embedding similarity (cosine >0.95 = safe to serve), not exact match.
6. **Request batching (10-25%)** — batch non-latency-sensitive requests off-peak.

## Mode 3 — Design Cost-Efficient Architecture

Budget envelopes (per feature/tier/day, hard limits + 80% soft alert) · routing layer (classify→route→call, never large model by default) · tier model access by user tier · cost observability dashboard (spend by feature/model, cost per active user, WoW trend, anomaly alerts) · graceful degradation (over budget: smaller model → cached → async queue).

## Proactive Flags (surface unprompted)

No per-feature breakdown → instrument first · all requests on one model → model monoculture is the #1 overspend, design routing · system prompt >2,000 tokens every request → caching target · `max_tokens` unset per endpoint → active leak · no cost alerts → set p95 cost-per-request alerts · free-tier users on the expensive model → tier access.

## Handoff Triggers

Prompt quality degrades → prompt engineering · retrieval pipeline → RAG · broader monitoring → observability · latency primary → performance profiling.

## Communication

Bottom line first (cost impact before explanation) · What + Why + How · actions have owners + deadlines · confidence tag (verified/medium/assumed).
