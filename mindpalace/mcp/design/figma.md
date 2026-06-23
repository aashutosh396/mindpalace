---
name: Figma
slug: figma
description: Use when reading Figma designs/specs to implement them in code.
category: design
env: FIGMA_API_KEY
homepage: https://github.com/GLips/Figma-Context-MCP
transport: stdio
---
Figma MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable figma` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "figma-developer-mcp",
    "--stdio"
  ],
  "env": {
    "FIGMA_API_KEY": "${FIGMA_API_KEY}"
  }
}
```
Homepage: https://github.com/GLips/Figma-Context-MCP
