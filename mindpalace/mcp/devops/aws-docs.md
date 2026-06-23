---
name: AWS Documentation
slug: aws-docs
description: Use when you need authoritative AWS service docs/answers (read-only docs MCP).
category: devops
env: 
homepage: https://github.com/awslabs/mcp
transport: stdio
---
AWS Documentation MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable aws-docs` or env):
```json
{
  "command": "uvx",
  "args": [
    "awslabs.aws-documentation-mcp-server@latest"
  ]
}
```
Homepage: https://github.com/awslabs/mcp
