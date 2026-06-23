---
name: Memory (KG)
slug: memory
description: Use when the agent needs a persistent knowledge-graph memory across turns.
category: ai
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Memory (KG) MCP server. mindpalace already has its own memory; use for graph-style facts.

Config (mcpServers entry — substitute creds via `!mcp enable memory` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-memory"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
