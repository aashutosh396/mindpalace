---
name: Playwright
slug: playwright
description: Use when you need robust browser automation/testing across browsers (Playwright MCP).
category: web
env: 
homepage: https://github.com/microsoft/playwright-mcp
transport: stdio
---
Playwright MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable playwright` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@playwright/mcp@latest"
  ]
}
```
Homepage: https://github.com/microsoft/playwright-mcp
