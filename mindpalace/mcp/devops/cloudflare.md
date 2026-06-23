---
name: Cloudflare
slug: cloudflare
description: Use when managing Cloudflare Workers, DNS, KV, R2, and analytics.
category: devops
env: 
homepage: https://github.com/cloudflare/mcp-server-cloudflare
transport: stdio
---
Cloudflare MCP server. OAuth/wrangler auth.

Config (mcpServers entry — substitute creds via `!mcp enable cloudflare` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@cloudflare/mcp-server-cloudflare"
  ]
}
```
Homepage: https://github.com/cloudflare/mcp-server-cloudflare
