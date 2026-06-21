---
name: rag-architect
description: "Use when building RAG systems, vector databases, or knowledge-grounded AI apps needing semantic search, document retrieval, context augmentation, or embedding-based indexing. Covers chunking, embeddings, vector stores, hybrid search, reranking, and retrieval evaluation. Triggers: RAG, retrieval-augmented generation, vector search, embeddings, semantic search, vector database, document retrieval, knowledge base, similarity search."
version: 1.0.0
license: MIT
tags: [rag, embeddings, vector-database, semantic-search, hybrid-search, reranking, chunking, retrieval-evaluation]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/rag-architect
derived_from: awesomeclaude
---

# RAG Architect

Design and implement production-grade RAG systems.

## When to use

Building RAG pipelines, vector DBs, semantic search, or knowledge-grounded AI applications.

## Core workflow

1. **Requirements** — retrieval needs, latency, accuracy, scale.
2. **Vector store design** — database, schema, indexing, sharding.
3. **Chunking strategy** — splitting, overlap, semantic boundaries, metadata enrichment.
4. **Retrieval pipeline** — embedding selection, query transformation, hybrid search, reranking.
5. **Evaluation & iteration** — metrics tracking, retrieval debugging, optimization.

## Implementation examples

```python
# Chunk with metadata — evaluate chunk_size on your domain, never 512 blindly
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100,
    separators=["\n\n","\n",". "," "])
chunks = splitter.create_documents(texts=[d.page_content for d in raw_docs],
    metadatas=[{"source": d.metadata["source"]} for d in raw_docs])
# Checkpoint: assert all(c.metadata.get("source") for c in chunks)
```
```python
# Idempotent upsert with deterministic IDs (dedup)
doc_id = str(uuid.UUID(hashlib.md5(chunk.page_content.encode()).hexdigest()))
qdrant.upsert("knowledge_base", points=[PointStruct(id=doc_id, vector=emb, payload=meta)])
```
```python
# Hybrid search: dense + BM25 fused via reciprocal rank fusion
ranked = sorted(zip(dense_results, bm25_scores),
                key=lambda x: 0.6*x[0].score + 0.4*x[1], reverse=True)
# Then rerank top-k with a cross-encoder (e.g. Cohere rerank-english-v3.0) before LLM
```
```python
# Evaluate with ragas — gate before LLM integration
results = evaluate(eval_dataset, metrics=[context_precision, context_recall, faithfulness, answer_relevancy])
# Target: context_precision >= 0.7, context_recall >= 0.6
```

## Constraints

MUST: evaluate multiple embedding models on your domain data first; hybrid search (vector + keyword) for production; metadata filters for multi-tenant/domain retrieval; measure precision@k, recall@k, MRR, NDCG; rerank top-k before LLM; idempotent ingestion with dedup; monitor latency + quality; version embeddings and plan migration.
MUST NOT: use default chunk size (512) without evaluation; skip metadata enrichment; judge only on LLM output (ignore retrieval metrics); store raw docs without cleaning; rely on cosine alone for complex multi-domain retrieval; deploy without production-like volume tests; ignore edge cases (empty results, malformed docs); tightly couple the embedding model to app code.

## Output

1. Architecture diagram (ingestion + retrieval pipelines)
2. Vector DB selection + trade-offs
3. Chunking strategy with examples
4. Retrieval pipeline design (query → results)
5. Evaluation plan with metrics + pass/fail thresholds
