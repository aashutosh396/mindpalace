---
name: SQL Database Assistant
description: Use when writing SQL queries, optimizing database performance, generating migrations, exploring schemas, or working with ORMs (Prisma, Drizzle, TypeORM, SQLAlchemy).
tags: [sql, query, optimization, explain, index, migration, orm, prisma, postgres, mysql, n+1]
source: alirezarezvani/claude-skills
derived_from: sql-database-assistant
---

# SQL Database Assistant

Day-to-day operational SQL: writing queries, optimizing performance, generating migrations, bridging app code and DB engines. Dialect-aware across PostgreSQL, MySQL, SQLite, SQL Server.

## NL → SQL translation
1. Nouns → tables. 2. Verbs → JOINs/subqueries. 3. Conditions → WHERE. 4. "total/average/count" → GROUP BY. 5. "top/latest/highest" → ORDER BY + LIMIT.

Key templates: Top-N per group (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`), running totals (`SUM() OVER (ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`), gap detection (self LEFT JOIN on seq-1), UPSERT (`ON CONFLICT DO UPDATE` PG / `ON DUPLICATE KEY UPDATE` MySQL).

## Query optimization (EXPLAIN workflow)
1. Run `EXPLAIN ANALYZE` (PG) / `EXPLAIN FORMAT=JSON` (MySQL).
2. Find costliest node — Seq Scan on large tables, Nested Loop with high estimates.
3. Check missing indexes on filtered columns.
4. Planned vs actual row divergence = stale statistics.
5. Ensure smallest result set drives the join.

**Index when**: high-selectivity WHERE columns, JOIN/FK columns, ORDER BY + LIMIT, composite for multi-column predicates (most selective first), partial for constant filters, covering for read-heavy.

**Rewrites**: `SELECT *` → explicit columns; `WHERE YEAR(col)=2025` → sargable range; correlated subquery → LEFT JOIN + agg; `NOT IN`+NULLs → `NOT EXISTS`; `UNION` → `UNION ALL` when dedup not needed; `LIKE '%x%'` → full-text index; `ORDER BY RAND()` → app-side sampling/TABLESAMPLE.

**N+1**: symptom is one query per parent row in a loop. Fix with eager loading (`include`/`joinedload`), `WHERE id IN (...)` batching, or DataLoader for GraphQL.

## Migrations (zero-downtime)
- Add column: nullable add (safe).
- Rename: expand-contract (add new → backfill → read both → write new → drop old).
- Add NOT NULL: add nullable → backfill default → set NOT NULL + DEFAULT.
- Index: `CREATE INDEX CONCURRENTLY` (PG, non-blocking).
- Backfill: batch 1k–10k rows, background jobs, dual-write, validate counts per batch.
- Every migration needs a reversible down script; for irreversible changes: backup, feature flags, shadow tables.

## Dialect differences (key)
UPSERT, BOOLEAN type, auto-increment, JSON (JSONB indexed in PG), arrays (PG only), CTE/window support, LIMIT/OFFSET syntax all vary. Always parameterize queries; wrap dialect-specific functions in an adapter; use ISO dates; quote identifiers per dialect.

## ORM cheats
- **Prisma**: `prisma.user.findMany({ include })`, `$queryRaw` escape hatch, `migrate dev`.
- **Drizzle**: `db.select().from().where(eq())`, `drizzle-kit generate/push`.
- **TypeORM**: repository `find({ where, relations })`, `migration:generate`.
- **SQLAlchemy**: always `with Session() as session:`, `alembic revision --autogenerate`.

## Data integrity
Every table has a PK (surrogate UUID/serial). FKs with explicit ON DELETE. UNIQUE for business uniqueness. CHECK for ranges/enums. Default to NOT NULL. Money as DECIMAL(19,4) or integer cents, never FLOAT.

Isolation levels: READ COMMITTED (default OLTP), REPEATABLE READ (financial), SERIALIZABLE (billing/inventory). Deadlock prevention: consistent lock ordering, short transactions, advisory locks, retry with backoff.

## Backup
PG `pg_dump -Fc` / `pg_restore --clean`; MySQL `mysqldump --single-transaction --routines --triggers`; SQLite `.backup`. Automate, test restores, offsite copies, retention policy, monitor size/duration.

## Anti-patterns
`SELECT *`, missing FK indexes, N+1, implicit type coercion, no connection pooling, unbounded queries, money as FLOAT, god tables, soft-deletes everywhere, raw string concatenation (SQL injection).
