---
name: sql-pro
description: "Use when a query is slow, you need complex joins/aggregations/window functions, or you're designing or migrating a schema. Covers CTEs, window functions, indexing, EXPLAIN/ANALYZE interpretation, before/after benchmarking, and dialect migration (PostgreSQL, MySQL, SQL Server, Oracle). Triggers: SQL optimization, query performance, database design, window functions, CTEs, query tuning, EXPLAIN plan, indexing."
version: 1.0.0
license: MIT
tags: [sql, query-optimization, ctes, window-functions, indexing, schema-design, explain, dialects]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/sql-pro
derived_from: awesomeclaude
---

# SQL Pro

Write, optimize, and troubleshoot SQL; design and migrate schemas across dialects.

## When to use

Slow queries, complex joins/aggregations, window functions, indexing strategy, query-plan analysis, schema design/migration.

## Core workflow

1. **Schema analysis** — structure, indexes, query patterns, bottlenecks.
2. **Design** — set-based operations with CTEs, window functions, appropriate joins.
3. **Optimize** — analyze plans, add covering indexes, eliminate table scans.
4. **Verify** — run `EXPLAIN ANALYZE`; confirm no seq scans on large tables; iterate until target met.
5. **Document** — explanations, index rationale, performance metrics.

## Quick-reference patterns

```sql
-- CTE: latest completed order per customer
WITH ranked AS (
  SELECT customer_id, order_id, total_amount,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
  FROM orders WHERE status='completed')   -- filter early
SELECT customer_id, order_id, total_amount FROM ranked WHERE rn = 1;

-- Window: running total + rank, no self-join
SELECT department_id, employee_id, salary,
  SUM(salary) OVER (PARTITION BY department_id ORDER BY hire_date) AS running_payroll,
  RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
FROM employees;

-- Correlated subquery (slow) -> aggregation join (fast)
-- BEFORE: one subquery per row
-- AFTER:
SELECT o.order_id, COALESCE(agg.item_count,0) AS item_count
FROM orders o
LEFT JOIN (SELECT order_id, SUM(quantity) AS item_count FROM order_items GROUP BY order_id) agg
  ON agg.order_id = o.id;
```

EXPLAIN ANALYZE — check: Seq Scan on large table → add/fix index; actual rows ≫ estimated → `ANALYZE`; high Buffers `read` vs `hit` → missing cache/index.

## Constraints

MUST: analyze plans before optimizing; use set-based over row-by-row; filter early (before joins); use EXISTS over COUNT for existence; handle NULLs explicitly; create covering indexes for frequent queries; test at production-scale volumes.
MUST NOT: `SELECT *` in production; cursors where set-based works; ignore dialect-specific optimizations; ignore data volume/cardinality.

## Output

1. Optimized query with inline comments
2. Required indexes + rationale
3. Execution-plan analysis
4. Before/after metrics
5. Platform-specific notes if relevant
