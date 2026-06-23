---
name: Everything (test)
slug: everything
description: Use to test/demo MCP — a reference server exercising every MCP feature.
category: dev
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Everything (test) MCP server. For testing the MCP wiring.

Config (mcpServers entry — substitute creds via `!mcp enable everything` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-everything"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
