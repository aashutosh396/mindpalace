---
name: Exa Search
slug: exa
description: Use when you need high-quality semantic/neural web search + content retrieval.
category: web
env: EXA_API_KEY
homepage: https://github.com/exa-labs/exa-mcp-server
transport: stdio
---
Exa Search MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable exa` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "exa-mcp-server"
  ],
  "env": {
    "EXA_API_KEY": "${EXA_API_KEY}"
  }
}
```
Homepage: https://github.com/exa-labs/exa-mcp-server
