---
name: Database Designer
description: Use when designing database schemas, planning data migrations, optimizing queries, choosing SQL vs NoSQL, or modeling data relationships — schema analysis, index optimization, and migration generation.
tags: [database, schema, normalization, index, migration, sql, nosql, sharding, replication, explain, connection-pooling]
source: alirezarezvani/claude-skills
derived_from: database-designer
---

# Database Designer

Architecture-level database design: normalization analysis, index optimization, zero-downtime migrations, and SQL-vs-NoSQL decisions. (Pair with sql-database-assistant for day-to-day queries; database-schema-designer for ERD modeling.)

## Tool workflow (don't analyze schemas by hand)
1. **Analyze schema** (SQL DDL or JSON) → normalization findings (1NF–BCNF), missing constraints, naming issues, Mermaid ERD. Fix flagged issues before optimizing.
2. **Optimize indexes** against real hot-query patterns → priority-ordered CREATE INDEX recommendations + redundant-index removals.
3. **Generate migration** current→target; `--zero-downtime` emits expand-contract plan; `--validate-only` checks feasibility.
4. **Verify**: re-run analysis on the target schema, assert first-pass issues gone; `--validate-only` before handing over.

## Migration patterns
- Up/down scripts, timestamp-prefixed for ordering; every migration reversible.
- Zero-downtime expand-contract: add nullable column → backfill in batches + dual-write → read new/stop writing old → drop old.
- Backfill in batches (`LIMIT 5000` loops) to avoid long locks.
- Test `down.sql` in staging first; after contract step, rollback needs a new forward migration; backup before irreversible changes.

## Index strategies
B-tree (equality/range/ORDER BY), GIN (full-text/JSONB/arrays), GiST (geometry/range/NN), Partial (row subset), Covering (`INCLUDE` for index-only scans). Read `EXPLAIN (ANALYZE, BUFFERS)`: Seq Scan on large tables = missing index; high-estimate Nested Loop = wrong join; shared read >> hit = working set exceeds memory.

## Connection pooling
PgBouncer (PG transaction pooling), ProxySQL (MySQL read/write split), built-in (HikariCP/SQLAlchemy). Pool size ≈ `2 * vCPUs` for cloud SSDs, tune from there. Route SELECT to read replicas (account for replication lag; `pg_last_wal_replay_lsn()` to detect).

## SQL vs NoSQL
Default to SQL. PostgreSQL = default for new projects (JSONB, extensions, standards). MySQL = read-heavy web. SQLite = embedded/edge/test. SQL Server = .NET/Azure enterprise. NoSQL only when access pattern clearly benefits: MongoDB (document flexibility), Redis (cache/session/leaderboard/pub-sub), DynamoDB (serverless AWS, single-digit-ms at scale).

## Sharding & replication
Vertical partition (split columns) vs horizontal (shard rows). Shard strategies: Hash (even, costly resharding), Range (simple, hot-spots latest), Geographic (locality/compliance, hard cross-region queries). Replication: Synchronous (strong, higher write latency, financial), Asynchronous (eventual, low latency, read-heavy), Semi-sync (balance).

## Best practices
Meaningful names, right-sized types, proper constraints, plan for growth, document relationships, index strategically without over-indexing, partition large tables, least-privilege grants, encrypt sensitive data, validate inputs.
