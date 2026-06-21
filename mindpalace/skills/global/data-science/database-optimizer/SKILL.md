---
name: database-optimizer
description: "Use when investigating slow queries, analyzing execution plans, or optimizing database performance on PostgreSQL or MySQL. Covers index design, query rewrites, config tuning, partitioning, and lock contention. Triggers: database optimization, slow query, query performance, database tuning, index optimization, execution plan, EXPLAIN ANALYZE."
version: 1.0.0
license: MIT
tags: [database, performance, postgresql, mysql, indexes, explain-analyze, tuning, query-optimization]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/database-optimizer
derived_from: awesomeclaude
---

# Database Optimizer

Performance tuning, query optimization, and scalability across PostgreSQL and MySQL.

## When to use

Slow queries, execution-plan analysis, index strategy, config tuning, schema/partitioning, lock contention, cache-hit improvement.

## Core workflow

1. **Analyze** — capture baseline metrics; run `EXPLAIN ANALYZE` before any change.
2. **Identify bottlenecks** — inefficient queries, missing indexes, config issues.
3. **Design solutions** — index strategies, query rewrites, schema improvements.
4. **Implement** — apply incrementally with monitoring; validate each change before the next.
5. **Validate** — re-run `EXPLAIN ANALYZE`, compare cost + wall-clock, document.

Always test in non-production first. Revert if write performance or replication lag worsens.

## Common operations

```sql
-- Top slow queries (needs pg_stat_statements)
SELECT query, calls, round(mean_exec_time::numeric,2) AS mean_ms, rows
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;

-- Capture plan with buffer cache ratio
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, c.name FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending' AND o.created_at > now() - interval '7 days';

-- Covering index (eliminates heap fetch)
CREATE INDEX CONCURRENTLY idx_orders_status_created_covering
  ON orders (status, created_at) INCLUDE (customer_id, total_amount);
```

Reading EXPLAIN — patterns:
| Pattern | Symptom | Remedy |
|---|---|---|
| Seq Scan on large table | no filter selectivity | add B-tree index |
| Nested Loop, large outer | exponential inner growth | Hash Join; index inner key |
| est rows=1, actual=50000 | stale stats | `ANALYZE <table>` |
| Buffers hit=10 read=90000 | low cache hit | bump `shared_buffers`; covering index |
| Sort Method: external merge | sort spills to disk | bump `work_mem` for session |

```sql
-- MySQL slow queries + plan
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 20;
EXPLAIN FORMAT=JSON SELECT * FROM orders WHERE status='pending';
```

## Constraints

MUST: capture `EXPLAIN (ANALYZE, BUFFERS)` baseline first; measure before/after every change; create indexes `CONCURRENTLY` (PostgreSQL); test in non-prod and roll back on regression; document with before/after metrics; `ANALYZE` after bulk changes.
MUST NOT: optimize without a baseline; create redundant/unused indexes; make multiple changes at once; ignore write amplification from new indexes; neglect VACUUM/stats maintenance.

## Output

1. Analysis with baseline metrics (time, cost, buffer hit ratio)
2. Bottlenecks + root causes (with EXPLAIN evidence)
3. Optimization strategy
4. SQL/config changes
5. Validation queries
6. Monitoring recommendations
