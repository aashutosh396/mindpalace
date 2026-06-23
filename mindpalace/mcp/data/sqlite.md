---
name: SQLite
slug: sqlite
description: Use when querying a local SQLite database file.
category: data
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
SQLite MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable sqlite` or env):
```json
{
  "command": "uvx",
  "args": [
    "mcp-server-sqlite",
    "--db-path",
    "/path/to/db.sqlite"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
