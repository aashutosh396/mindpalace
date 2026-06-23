---
name: PostgreSQL
slug: postgres
description: Use when querying or inspecting a Postgres database (read-only schema + SQL).
category: data
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
PostgreSQL MCP server. Put the connection string in args.

Config (mcpServers entry — substitute creds via `!mcp enable postgres` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-postgres",
    "postgresql://USER:PASS@HOST:5432/DB"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
