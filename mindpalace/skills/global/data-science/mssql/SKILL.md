---
name: mssql
description: "Use when querying Microsoft SQL Server / MSSQL databases, exploring schemas/tables, or running read-only SELECT queries for data analysis across multiple configured DB connections (pymssql, TDS, Azure SQL) — blocks all writes (INSERT/UPDATE/DELETE/DROP)."
version: 1.0.0
license: Apache-2.0
tags: [mssql, sql-server, database, sql, pymssql, read-only, azure-sql, data-analysis]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/mssql
derived_from: awesomeclaude
prerequisites:
  commands: [python3, pip]
---

# MSSQL Read-Only Query

Run safe, read-only SQL against one or more configured Microsoft SQL Server databases via a Python helper using `pymssql`.

## When to use

- Querying an MSSQL / SQL Server database.
- Exploring schema, listing tables, inspecting columns.
- Running SELECT queries for data analysis or content checks.
- Choosing among several DB connections by matching user intent to each connection's description.

## Requirements

- Python 3.8+
- `pip install pymssql` (the source skill ships a `requirements.txt`).

## Setup

Create `connections.json` in the skill dir or at `~/.config/claude/mssql-connections.json`. It holds credentials, so lock it down:

```bash
chmod 600 connections.json
```

```json
{
  "databases": [
    {
      "name": "production",
      "description": "Main app database - users, orders, transactions",
      "host": "db.example.com",
      "port": 1433,
      "database": "app_prod",
      "user": "readonly_user",
      "password": "your-password",
      "encrypt": true,
      "tds_version": "7.3"
    }
  ]
}
```

Required fields: `name`, `description`, `host`, `database`, `user`, `password`.
Optional: `port` (default 1433), `encrypt` (default false; set `true` for Azure SQL/TLS), `tds_version` (7.0–7.4, default auto).

`description` matters — it drives database auto-selection.

## Usage

The helper script lives at the source repo: `scripts/query.py` (under the skill dir).

```bash
# List configured databases
python3 scripts/query.py --list

# Run a query
python3 scripts/query.py --db production --query "SELECT TOP 10 * FROM users"

# List tables
python3 scripts/query.py --db production --tables

# Show schema
python3 scripts/query.py --db production --schema

# Limit results (auto-converts to TOP N)
python3 scripts/query.py --db production --query "SELECT * FROM orders" --limit 100
```

Note: MSSQL uses `TOP N`, not `LIMIT`. The `--limit` flag inserts `TOP N` after SELECT automatically.

## Database selection

Match user intent to each connection's `description`:

| User asks about | Look for description containing |
|---|---|
| users, accounts | users, accounts, customers |
| orders, sales | orders, transactions, sales |
| analytics, metrics | analytics, metrics, reports |
| logs, events | logs, events, audit |

If unclear, run `--list` and ask which database to use.

## Workflow

1. `--list` to show available databases.
2. Match intent to a database description.
3. `--tables` or `--schema` to explore structure.
4. Run the query with an appropriate `--limit`.

## Safety

- Read-only enforced: only SELECT, SHOW, EXPLAIN, WITH, SP_HELP allowed; writes (INSERT/UPDATE/DELETE/DROP/etc.) blocked.
- Single statement only — multi-statement queries rejected.
- 30s query timeout, 10s login timeout.
- Max 10,000 rows per query (OOM guard); 100-char column width cap for readable output.
- Error messages sanitize credentials.
- Defense in depth: also use a `db_datareader`-role DB user for server-side read-only enforcement.

## Troubleshooting

| Error | Fix |
|---|---|
| Config not found | Create `connections.json` in skill dir or `~/.config/claude/`. |
| Authentication failed | Check user/password in config. |
| Connection timeout | Verify host/port; check firewall/VPN. |
| TDS version error | Try `"tds_version": "7.3"` or `"7.4"`. |
| Encryption error | Set `"encrypt": true` (needed for Azure SQL). |
| Permission warning | `chmod 600 connections.json`. |

Exit codes: 0 = success, 1 = error (config missing, auth failed, invalid query, DB error).
