---
name: serialize-data-formats
description: "Use when choosing or implementing a data serialization format — JSON, XML, YAML, Protocol Buffers, MessagePack, or Apache Arrow/Parquet — for API wire formats, on-disk persistence, cross-language data exchange, or optimizing transfer size and parsing speed. Triggers: serialize, deserialize, wire format, JSON, protobuf, MessagePack, Parquet, Arrow, schema, encoding, data format choice."
version: 1.0.0
license: MIT
tags: [serialization, json, xml, yaml, protobuf, messagepack, parquet, arrow, data-formats]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/serialize-data-formats
derived_from: awesomeclaude
---

# Serialize Data Formats

Select and implement the right serialization format with correct encoding/decoding and performance awareness.

## When to Use

- Choosing a wire format for API communication
- Persisting structured data to disk or object storage
- Exchanging data between systems in different languages
- Optimizing transfer size or parsing speed
- Migrating from one serialization format to another

## Procedure

### Step 1 — Select the format
| Format | Human-readable | Schema | Size | Speed | Best for |
|---|---|---|---|---|---|
| JSON | Yes | optional | medium | medium | REST APIs, config, broad interop |
| XML | Yes | XSD/DTD | large | slow | enterprise/legacy, SOAP, documents |
| YAML | Yes | optional | medium | slow | config, CI/CD, Kubernetes |
| Protocol Buffers | No | required (.proto) | small | fast | gRPC, microservices, mobile |
| MessagePack | No | none | small | fast | real-time, embedded, Redis |
| Arrow/Parquet | No | built-in | very small | very fast | analytics, columnar queries, data lakes |

Decision tree: human editing → YAML/JSON; strict schema + fast RPC → Protobuf; smallest wire → MessagePack/Protobuf; columnar analytics → Parquet; in-memory interchange → Arrow; legacy enterprise → XML. Document the rationale; on conflicting requirements, prioritize the primary use case and note the trade-off.

### Step 2 — JSON
Use a custom encoder for non-standard types (datetime → ISO 8601, bytes → base64). Verify round-trip preserves types; if a type is lost (dates become strings), add explicit conversion on deserialize. In R, `jsonlite::toJSON(auto_unbox=TRUE)` / `fromJSON`.

### Step 3 — Protocol Buffers
Define a `.proto` schema, compile with `protoc`, then serialize/deserialize with the generated classes. Best when you need a strict schema, small payloads, and forward/backward-compatible evolution (add fields with new tags; never reuse tag numbers).

### Step 4 — MessagePack
Schema-less compact binary, near drop-in for JSON semantics. Good for real-time, Redis values, and embedded contexts where size and speed matter but a schema is unnecessary.

### Step 5 — Apache Parquet (columnar)
Use for analytics and data lakes — column pruning and predicate pushdown make queries fast and files tiny. Write/read via Arrow/pyarrow or pandas. Built-in schema and compression.

### Step 6 — Compare performance
Benchmark representative payload sizes for serialize time, deserialize time, and on-wire size before committing. Validate edge cases: empty collections, null/None, Unicode, large numbers.

## Validation

- [ ] Format matches requirements (documented rationale)
- [ ] Round-trip preserves all data types
- [ ] Edge cases handled (empty, null, Unicode, large numbers)
- [ ] Performance benchmarked for representative sizes
- [ ] Graceful handling of malformed input
- [ ] Schema documented (JSON Schema, .proto, or equivalent)

## Common Pitfalls

- Floating-point precision — JSON uses IEEE 754 doubles; string-encode financial decimals.
- Date/time — JSON has no native datetime; document ISO 8601 + timezone.
- Schema evolution — Protobuf handles it well; JSON needs careful versioning.
- Binary in JSON — base64 inflates ~33%; use a binary format for binary-heavy payloads.
- YAML security — parsers can execute code via tags; always use safe loaders.

## Related

- headless-web-scraping, use-graphql-api — produce data that needs serializing
