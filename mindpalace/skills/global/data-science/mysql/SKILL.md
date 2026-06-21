---
name: mysql
description: "Use when querying MySQL/MariaDB databases, exploring schemas/tables, running SELECT queries for data analysis, or checking DB contents — read-only, multi-database connection support, blocks all writes (INSERT/UPDATE/DELETE/DROP)"
version: 1.0.0
license: Apache-2.0
tags: [mysql, mariadb, sql, database, query, read-only, schema, data-analysis]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/mysql
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# MySQL Read-Only Query Skill

Execute safe, read-only SQL against one or more configured MySQL/MariaDB databases.
All write operations are blocked. Supports multiple connections, auto-selected by
matching user intent against each connection's `description`.

## When to use

- User wants to query a MySQL/MariaDB database (SELECT, SHOW, DESCRIBE, EXPLAIN, WITH)
- Exploring schema: list tables, show columns/types
- Pulling data for analysis or sanity-checking DB contents
- Across several known databases — the skill picks the right one from descriptions

Do NOT use for writes — INSERT/UPDATE/DELETE/DROP/etc. are rejected by design.

## Requirements

- Python 3.8+
- `mysql-connector-python` (install via the skill's `requirements.txt`)

## Setup

Create `connections.json` in the skill dir, or `~/.config/claude/mysql-connections.json`.
It holds credentials — lock it down:

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
      "port": 3306,
      "database": "app_prod",
      "user": "readonly_user",
      "password": "your-password",
      "ssl_disabled": false
    }
  ]
}
```

Config fields: `name`, `description`, `host`, `database`, `user`, `password` are required.
Optional: `port` (default 3306), `ssl_disabled` (default false), `ssl_ca`, `ssl_cert`, `ssl_key`.

## Usage

Helper script lives at the skill's `scripts/query.py` (in the source repo).

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

Match user intent to a connection's `description`:

| User asks about    | Match description containing       |
|--------------------|------------------------------------|
| users, accounts    | users, accounts, customers         |
| orders, sales      | orders, transactions, sales        |
| analytics, metrics | analytics, metrics, reports        |
| logs, events       | logs, events, audit                |

If ambiguous, run `--list` and ask the user which DB.

## Workflow

1. `--list` to see available databases
2. Match user intent to a database description
3. `--tables` or `--schema` to explore structure
4. Run the query with a sensible `--limit`

## Safety features

- Read-only session: `SET SESSION TRANSACTION READ ONLY` (primary protection)
- Query validation: only SELECT / SHOW / DESCRIBE / EXPLAIN / WITH allowed
- Single statement per query (multi-statement rejected)
- 30s `max_execution_time` cap (MySQL 5.7.8+ / MariaDB 10.1.1+)
- Max 10,000 rows per query (OOM protection)
- Column width capped at 100 chars for readable output
- Error messages sanitize credentials (no password leaks)
- SSL configurable via CA / client cert / key

## Troubleshooting

| Error                          | Fix                                              |
|--------------------------------|--------------------------------------------------|
| Config not found               | Create `connections.json` in skill dir           |
| Authentication failed          | Check username/password in config                |
| Connection timeout             | Verify host/port; check firewall/VPN             |
| SSL error                      | Try `"ssl_disabled": true` for local databases   |
| Permission warning             | `chmod 600 connections.json`                     |
| max_execution_time unsupported | Upgrade to MySQL 5.7.8+ or MariaDB 10.1.1+       |

Exit codes: `0` success, `1` error (config missing, auth failed, invalid query, DB error).
