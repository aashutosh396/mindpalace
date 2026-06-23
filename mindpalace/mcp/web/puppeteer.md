---
name: Puppeteer
slug: puppeteer
description: Use when you need to drive a headless Chrome browser (navigate, click, screenshot).
category: web
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Puppeteer MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable puppeteer` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-puppeteer"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
