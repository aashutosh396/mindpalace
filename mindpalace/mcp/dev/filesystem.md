---
name: Filesystem
slug: filesystem
description: Use when reading/writing files in a specific directory tree — sandboxed local file access.
category: dev
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Filesystem MCP server. Set the allowed dir(s) in args.

Config (mcpServers entry — substitute creds via `!mcp enable filesystem` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/path/to/allowed/dir"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
