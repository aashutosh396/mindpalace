---
name: Sentry
slug: sentry
description: Use when investigating Sentry errors/issues and stack traces (hosted MCP).
category: devops
env: 
homepage: https://docs.sentry.io/
transport: remote
---
Sentry MCP server. Hosted; OAuth.

Config (mcpServers entry — substitute creds via `!mcp enable sentry` or env):
```json
{
  "type": "sse",
  "url": "https://mcp.sentry.dev/sse"
}
```
Homepage: https://docs.sentry.io/
