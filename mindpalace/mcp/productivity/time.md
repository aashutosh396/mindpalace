---
name: Time
slug: time
description: Use when you need current time/timezone conversions reliably.
category: productivity
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Time MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable time` or env):
```json
{
  "command": "uvx",
  "args": [
    "mcp-server-time"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
