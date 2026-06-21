---
name: qdrant
description: "Use when working with Qdrant vector database — client SDKs (Python/TS/Rust/Go/.NET/Java), deployment (Docker/Cloud/local/EDGE), bad search results, low recall/precision, hybrid search, reranking, embedding model migration, performance/memory/indexing tuning, scaling/sharding, monitoring (Prometheus/Grafana), or version upgrades."
version: 1.0.0
license: Apache-2.0
tags: [qdrant, vector-database, embeddings, similarity-search, hybrid-search, reranking, hnsw, rag, deployment, scaling]
source: https://github.com/qdrant/skills
derived_from: awesomeclaude
prerequisites:
  commands: [curl]
---

# Qdrant

Vector database for similarity search. This skill is a navigation hub over Qdrant's
official agent-skill knowledge. The Qdrant team hosts a live snippet/docs API at
`https://skills.qdrant.tech` — query it for current, version-accurate code and docs
instead of guessing.

## Live lookup helpers (prefer these over memory)

- Curated code snippets per language + use case:
  `curl -X GET "https://skills.qdrant.tech/snippets/search?language=python&query=how+to+upload+points"`
  Languages: `python`, `typescript`, `rust`, `java`, `go`, `csharp`. Add `&format=json` for JSON.
- Docs search: `https://skills.qdrant.tech/search?query=your+query+here`
- REST OpenAPI reference: `https://skills.qdrant.tech/api-reference.md`

## Client SDKs

Official clients — keep SDK major.minor matched to the Qdrant server version (e.g. server 1.17.x ↔ SDK 1.17.x):

- Python — `pip install qdrant-client[fastembed]`
- JS/TS — `npm install @qdrant/js-client-rest`
- Rust — `cargo add qdrant-client`
- Go — `go get github.com/qdrant/go-client`
- .NET — `dotnet add package Qdrant.Client`
- Java — Maven Central `io.qdrant:client`

Interact via REST (recommended for first use/prototyping) or gRPC (lower overhead at scale).

## Choosing a deployment

Decide on: managed ops vs full control? network latency tolerable? prod vs prototype?

- Prototype / CI / learning → local mode (Python only, in-memory or on-disk). NOTE: local-mode
  data format is NOT server-compatible — never use for production or benchmarking.
- Self-hosted prod → Docker is the default (full OSS feature set). You own upgrades, backups,
  scaling, monitoring. Multi-node needs distributed mode set up manually.
- Zero-ops prod → Qdrant Cloud (managed upgrades, backups, resharding, alerts, `/sys_metrics`).
- Lowest latency / edge / in-process → Qdrant EDGE (no network hop, single-node only, syncs via
  shard snapshots). Do not pick EDGE if you need distributed search.
- Data residency on your own infra → Hybrid Cloud (only if residency truly required; otherwise
  Cloud avoids the K8s complexity).

## Diagnosing bad search results

Most relevance problems come from the embedding model or the data, not Qdrant. Triage in order:

1. Check chunking first — splitting mid-sentence can drop quality 30-40%.
2. Isolate the cause: run exact (brute-force) search to remove HNSW approximation from the picture.
3. Is it the model, the Qdrant config, or the query strategy?

Then improve:

- Build a labeled golden set / ground-truth dataset; measure recall@k and precision before tuning.
- Tune HNSW params (`m`, `ef_construct`, search-time `ef`) — higher = better recall, slower/more memory.
- Consider hybrid search (dense + sparse/BM25), reranking, and relevance feedback / exploration APIs.
- Re-check quality after quantization, a model swap, or large data growth — these regress recall.

## Embedding model migration (zero downtime)

Vectors from different models are incompatible — never mix old and new embeddings in one vector space.

- v1.18+: you can add/delete named vector fields on an existing collection — no new collection needed.
- v1.17 and earlier: all named vectors must be defined at collection-creation time → migrate to a new collection.
- Use collection aliases to cut over atomically: build the new collection/vector, backfill, then
  repoint the alias. Supports A/B testing two models at once via named vectors.

## Performance optimization

- Search speed: optimize for latency (single-query time) and/or throughput (QPS) per your use case.
- Indexing: HNSW build time scales with dataset size, hardware, and config; tune `indexing_threshold`,
  defer indexing during bulk loads.
- Memory: Qdrant lets you control what stays in RAM vs on disk (memmap, on-disk payload/index,
  quantization) — cut memory without losing much performance.

## Scaling

Decide what you're scaling for first: data volume, throughput, latency, or tenant count.

- Vertical (bigger node) before horizontal where possible — simpler.
- Horizontal: shard for data that won't fit one node or for higher QPS; replicate for HA + read throughput.
- Many tenants → multitenancy via payload-based partitioning rather than one collection per tenant.

## Monitoring

- Health/readiness endpoints; `/metrics` Prometheus exposition; Grafana dashboards.
- Cloud-only: `/sys_metrics`, managed resharding, pre-configured alerts.
- Watch for: optimizer stuck, unbounded memory growth, slow requests — diagnose via metrics.
- Self-hosting without monitoring + a backup strategy will eventually lose data or miss outages.

## Version upgrades

- Keep Qdrant and SDK major/minor in lockstep (1.17.x ↔ 1.17.x).
- Upgrade one minor version at a time on self-hosted; Cloud supports multi-version jumps automatically.
- For HA: rolling upgrades across replicas; snapshot/back up before upgrading.

## Gotchas

- Local-mode data format ≠ server format — incompatible, prototyping only.
- Mixing embeddings from different models in one space silently ruins relevance.
- Quantization and model changes can quietly degrade recall — re-measure against a golden set.
- EDGE and local mode are single-node only — no distributed search.

## Deeper sub-skills (in source repo under `skills/`)

`qdrant-clients-sdk`, `qdrant-deployment-options`, `qdrant-search-quality`,
`qdrant-model-migration`, `qdrant-performance-optimization`, `qdrant-scaling`,
`qdrant-monitoring`, `qdrant-version-upgrade` — each has nested SKILL.md detail at
https://github.com/qdrant/skills/tree/main/skills.
