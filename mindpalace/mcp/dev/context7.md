---
name: Context7 Docs
slug: context7
description: Use when you need up-to-date, version-correct library/framework docs injected into context.
category: dev
env: 
homepage: https://github.com/upstash/context7
transport: stdio
---
Context7 Docs MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable context7` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@upstash/context7-mcp"
  ]
}
```
Homepage: https://github.com/upstash/context7
