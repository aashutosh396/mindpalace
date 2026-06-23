---
name: Postman
slug: postman
description: Use when working with Postman collections, APIs, and the Postman API network.
category: dev
env: POSTMAN_API_KEY
homepage: https://github.com/postmanlabs
transport: stdio
---
Postman MCP server. Generate a Postman API key.

Config (mcpServers entry — substitute creds via `!mcp enable postman` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@postman/mcp-server"
  ],
  "env": {
    "POSTMAN_API_KEY": "${POSTMAN_API_KEY}"
  }
}
```
Homepage: https://github.com/postmanlabs
