---
name: Git
slug: git
description: Use when running git ops on a local repo (log, diff, blame, commit) via MCP.
category: dev
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Git MCP server. Needs uv/uvx installed.

Config (mcpServers entry — substitute creds via `!mcp enable git` or env):
```json
{
  "command": "uvx",
  "args": [
    "mcp-server-git",
    "--repository",
    "/path/to/repo"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
