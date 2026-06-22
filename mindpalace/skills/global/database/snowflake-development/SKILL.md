---
name: Snowflake Development
description: Use when writing Snowflake SQL, building pipelines with Dynamic Tables or Streams/Tasks, using Cortex AI functions/agents, writing Snowpark Python, configuring dbt for Snowflake, or troubleshooting Snowflake errors.
tags: [snowflake, sql, dynamic-tables, streams-tasks, cortex-ai, snowpark, dbt, data-pipeline, merge, rbac]
source: alirezarezvani/claude-skills
derived_from: engineering-team/snowflake-development
---

# Snowflake Development

Snowflake SQL, pipelines, Cortex AI, Snowpark Python, dbt.

## SQL best practices
- `snake_case` identifiers; avoid double-quoted (forces case-sensitivity). CTEs over nested subqueries. `CREATE OR REPLACE` for idempotent DDL. Explicit column lists — never `SELECT *` in production (columnar storage scans only referenced columns).
- **Colon-prefix rule (stored procedures):** inside BEGIN...END SQL statements, variables/parameters MUST use `:` prefix or Snowflake treats them as column identifiers ("invalid identifier"). `SELECT name INTO :result FROM users WHERE id = :p_id;` — applies to DECLARE/LET vars and params in SELECT/INSERT/UPDATE/DELETE/MERGE.
- **Semi-structured:** VARIANT/OBJECT/ARRAY; access `src:customer.name::STRING` (always cast `::TYPE`); JSON `null` stored as string `"null"` → use `STRIP_NULL_VALUE = TRUE` on load; flatten via `LATERAL FLATTEN(input => src:items)`.
- **MERGE upsert:** `MERGE INTO target t USING source s ON t.id=s.id WHEN MATCHED THEN UPDATE SET ... WHEN NOT MATCHED THEN INSERT (...) VALUES (...);`

## Pipelines
| Approach | When |
|---|---|
| Dynamic Tables | Declarative transforms — **default**. Define query, Snowflake refreshes. |
| Streams + Tasks | Imperative CDC, procedural logic, branching. |
| Snowpipe | Continuous file loading from S3/GCS/Azure. |

**Dynamic Tables:** `CREATE OR REPLACE DYNAMIC TABLE x TARGET_LAG='5 minutes' WAREHOUSE=wh AS SELECT ...`. Set TARGET_LAG tighter at top of DAG, looser downstream. Incremental DTs can't depend on full-refresh DTs. Explicit columns (SELECT * breaks on schema change). No views between two DTs.
**Streams+Tasks:** `CREATE STREAM s ON TABLE t;` then a TASK with `WHEN SYSTEM$STREAM_HAS_DATA('s')`. **Tasks start SUSPENDED — `ALTER TASK x RESUME;`**

## Cortex AI
Functions (current names): `AI_COMPLETE`, `AI_CLASSIFY` (≤500 labels), `AI_FILTER`, `AI_EXTRACT`, `AI_SENTIMENT` (-1..1), `AI_PARSE_DOCUMENT`, `AI_REDACT`. **Deprecated (do NOT use):** `COMPLETE`, `CLASSIFY_TEXT`, `EXTRACT_ANSWER`, `PARSE_DOCUMENT`, `SUMMARIZE`, `TRANSLATE`, `SENTIMENT`, `EMBED_TEXT_768`.
`TO_FILE` takes stage path and filename as **two** args: `TO_FILE('@db.schema.mystage','invoice.pdf')`.
Cortex Agents: JSON spec with top-level `models`/`instructions`/`tools`/`tool_resources`; use `$spec$` delimiter (not `$$`); `models` is an object not array; `tool_resources` is top-level; tool descriptions drive agent quality most.

## Snowpark Python
`Session.builder.configs({...}).create()` — never hardcode credentials (env vars / key-pair). DataFrames lazy (execute on `collect()`/`show()`); don't `collect()` large DataFrames (process server-side); use vectorized UDFs (10-100×) for batch/ML.

## dbt
`materialized='dynamic_table'` (streaming marts, with snowflake_warehouse+target_lag), `'incremental'` (large facts, unique_key). Snowflake configs: `transient`, `copy_grants`, `query_tag`. Don't use `{{ this }}` without `{% if is_incremental() %}` guard.

## Performance & security
Cluster keys only multi-TB on WHERE/JOIN/GROUP BY cols; search optimization `ADD SEARCH OPTIMIZATION ON EQUALITY(col)`; start X-Small warehouses, `AUTO_SUSPEND=60`, `AUTO_RESUME=TRUE`; separate warehouses per workload (load/transform/query). Least-privilege RBAC via database roles; audit `SHOW GRANTS OF ROLE ACCOUNTADMIN`; network policies for IP allowlisting; masking + row-access policies for PII/multi-tenant.

## Proactive triggers (flag unprompted)
Missing colon prefix in procedures · `SELECT *` in Dynamic Tables · deprecated Cortex names · task not resumed · hardcoded credentials in Snowpark.

## Common errors
"Object does not exist" → fully-qualify names, check grants. "Invalid identifier" in proc → add `:`. "Numeric value not recognized" → cast VARIANT `::NUMBER`. Task not running → `ALTER TASK ... RESUME`. DT refresh failing → explicit columns, verify change tracking. TO_FILE error → split into two args.

## Debug a failing pipeline
Task history: `INFORMATION_SCHEMA.TASK_HISTORY()` WHERE STATE='FAILED'. DT refresh: `DYNAMIC_TABLE_REFRESH_HISTORY('my_dt')`. Stream staleness: `SHOW STREAMS` (stale_after column).
