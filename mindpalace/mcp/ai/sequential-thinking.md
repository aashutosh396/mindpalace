---
name: Sequential Thinking
slug: sequential-thinking
description: Use when a hard problem needs explicit step-by-step structured reasoning scaffolding.
category: ai
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Sequential Thinking MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable sequential-thinking` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-sequential-thinking"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
