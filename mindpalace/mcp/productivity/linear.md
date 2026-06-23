---
name: Linear
slug: linear
description: Use when managing Linear issues/projects (hosted MCP, OAuth).
category: productivity
env: 
homepage: https://linear.app/docs
transport: remote
---
Linear MCP server. Hosted; authorize via OAuth.

Config (mcpServers entry — substitute creds via `!mcp enable linear` or env):
```json
{
  "type": "sse",
  "url": "https://mcp.linear.app/sse"
}
```
Homepage: https://linear.app/docs
