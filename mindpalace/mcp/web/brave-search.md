---
name: Brave Search
slug: brave-search
description: Use when you need live web search results (privacy-first Brave API).
category: web
env: BRAVE_API_KEY
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Brave Search MCP server. Free Brave Search API key.

Config (mcpServers entry — substitute creds via `!mcp enable brave-search` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-brave-search"
  ],
  "env": {
    "BRAVE_API_KEY": "${BRAVE_API_KEY}"
  }
}
```
Homepage: https://github.com/modelcontextprotocol/servers
