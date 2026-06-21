---
name: postgres
description: "Use when querying a PostgreSQL database, exploring db schemas/tables, running read-only SELECT queries against postgres, or checking database contents across multiple configured connections — keywords: postgres, postgresql, psql, SQL query, SELECT, database schema, list tables, psycopg2."
version: 1.0.0
license: Apache-2.0
tags: [postgres, postgresql, sql, database, query, read-only, schema, psycopg2]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# PostgreSQL Read-Only Query

Run safe, read-only SQL against one or more configured PostgreSQL databases. All
write operations (INSERT, UPDATE, DELETE, DROP, etc.) are blocked. Helper script
lives in the source repo at `skills/postgres/scripts/query.py` (needs
`psycopg2-binary`, installable via the repo's `requirements.txt`).

## When to use

- User wants to query a Postgres database or inspect its data.
- Exploring schemas/tables of a Postgres instance.
- Running SELECT queries for data analysis.
- Multiple databases configured — the skill auto-selects by matching intent to each db's description.

## Setup

Create `connections.json` in the skill dir OR `~/.config/claude/postgres-connections.json`.
It holds credentials, so lock it down:

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
      "port": 5432,
      "database": "app_prod",
      "user": "readonly_user",
      "password": "your-password",
      "sslmode": "require"
    }
  ]
}
```

Config fields: `name` (required, case-insensitive id), `description` (required,
drives auto-selection), `host` (required), `port` (default 5432), `database`
(required), `user` (required), `password` (required), `sslmode` (default
`prefer`; options: disable, allow, prefer, require, verify-ca, verify-full).

## Usage

```bash
# List configured databases
python3 scripts/query.py --list

# Run a query
python3 scripts/query.py --db production --query "SELECT * FROM users LIMIT 10"

# List tables
python3 scripts/query.py --db production --tables

# Show schema
python3 scripts/query.py --db production --schema

# Cap result rows
python3 scripts/query.py --db production --query "SELECT * FROM orders" --limit 100
```

## Database selection

Match user intent to a db `description`:

| User asks about | description containing |
|---|---|
| users, accounts | users, accounts, customers |
| orders, sales | orders, transactions, sales |
| analytics, metrics | analytics, metrics, reports |
| logs, events | logs, events, audit |

If unclear, run `--list` and ask the user which database.

## Workflow

1. `--list` to show available databases.
2. Match user intent to a db description.
3. `--tables` / `--schema` to explore structure.
4. Execute the query with an appropriate LIMIT.

## Safety features

- Read-only session (`readonly=True` connection — primary protection).
- Only SELECT / SHOW / EXPLAIN / WITH queries allowed; multi-statement queries rejected.
- 30-second statement timeout.
- Max 10,000 rows per query (OOM guard); 100-char column-width cap for output.
- Error messages sanitize credentials.
- SSL mode configurable.

## Troubleshooting

| Error | Fix |
|---|---|
| Config not found | Create `connections.json` in skill dir |
| Authentication failed | Check user/password in config |
| Connection timeout | Verify host/port; check firewall/VPN |
| SSL error | Try `"sslmode": "disable"` for local dbs |
| Permission warning | `chmod 600 connections.json` |

Exit codes: 0 success, 1 error (config missing, auth fail, invalid query, db error).
