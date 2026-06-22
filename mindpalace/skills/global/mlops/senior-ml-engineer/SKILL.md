---
name: Senior ML Engineer
description: Use when deploying ML models to production, building MLOps pipelines, monitoring drift, building RAG, or integrating LLM APIs with retries/cost controls — production and operational concerns, not research.
tags: [mlops, model-deployment, drift-detection, feature-store, rag, llm-integration, model-serving, mlflow, vector-database, retraining]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/senior-ml-engineer
---

# Senior ML Engineer

Production ML: deployment, MLOps, LLM integration. Focused on operations, not model research.

## Model Deployment
Export (ONNX/TorchScript/SavedModel) → Docker package → staging → integration tests → canary (5% traffic) → monitor latency + errors 1h → promote. **Validation: p95 < 100ms, error rate < 0.1%.** Container: HEALTHCHECK + uvicorn server. Serving: FastAPI (REST, small) · Triton (GPU batching, very high throughput) · TF Serving / TorchServe · Ray Serve (multi-model pipelines).

## MLOps Pipeline
Feature store (Feast/Tecton) → experiment tracking (MLflow/W&B) → training w/ hyperparameter logging → model registry w/ version metadata → staging deploy on registry events → A/B testing → drift monitoring + alerts. New models auto-evaluated against baseline. **Retraining triggers**: scheduled (cron) full retrain · accuracy < threshold → immediate · PSI > 0.2 → evaluate then retrain · new data volume → incremental.

## LLM Integration
Provider abstraction layer (vendor flexibility) → retry w/ exponential backoff (tenacity, 3 attempts) → fallback to secondary provider → token counting + context truncation → response caching → cost tracking per request → structured output validation (Pydantic). **Validation: parses correctly, cost in budget.** Look up current provider pricing — don't trust cached tables.

## RAG Implementation
Vector DB → embedding model (quality/cost) → chunking → ingestion w/ metadata → retrieval (query embedding) → reranking → format context → LLM. **Validation: response references retrieved context, no hallucinations.**
- Vector DBs: Pinecone (managed prod) · Qdrant (perf-critical, very low latency) · Weaviate (hybrid search) · Chroma (prototyping) · pgvector (existing Postgres).
- Chunking: fixed 500-1000 tokens / 50-100 overlap (general) · sentence (structured) · semantic (papers) · recursive parent-child (long docs).

## Monitoring
Latency (p50/p95/p99) · error rate alerting · input data drift · prediction distribution shift · log ground truth · A/B compare versions. **Drift**: KS test (`ks_2samp`, p < 0.05). Alert thresholds: p95 latency warn >100ms / crit >200ms; error rate warn >0.1% / crit >1%; PSI warn >0.1 / crit >0.2; accuracy drop warn >2% / crit >5%. Alerts fire before user-visible degradation.
