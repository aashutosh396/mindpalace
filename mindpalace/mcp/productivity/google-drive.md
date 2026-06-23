---
name: Google Drive
slug: google-drive
description: Use when searching/reading files in Google Drive.
category: productivity
env: 
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Google Drive MCP server. OAuth setup required.

Config (mcpServers entry — substitute creds via `!mcp enable google-drive` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-gdrive"
  ]
}
```
Homepage: https://github.com/modelcontextprotocol/servers
