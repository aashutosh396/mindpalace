---
name: Notion
slug: notion
description: Use when reading/updating Notion pages and databases (hosted MCP, OAuth).
category: productivity
env: 
homepage: https://developers.notion.com/
transport: remote
---
Notion MCP server. Hosted; authorize via OAuth.

Config (mcpServers entry — substitute creds via `!mcp enable notion` or env):
```json
{
  "type": "http",
  "url": "https://mcp.notion.com/mcp"
}
```
Homepage: https://developers.notion.com/
