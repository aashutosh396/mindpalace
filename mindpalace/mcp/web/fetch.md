---
name: Fetch
slug: fetch
description: Use when fetching a web page/URL and converting it to clean markdown for the model.
category: web
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Fetch MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable fetch` or env):
```json
{
  "command": "uvx",
  "args": [
    "mcp-server-fetch"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
