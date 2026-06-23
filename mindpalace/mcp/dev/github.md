---
name: GitHub
slug: github
description: Use when working with GitHub repos, issues, PRs, code search — official GitHub MCP.
category: dev
env: GITHUB_PERSONAL_ACCESS_TOKEN
homepage: https://github.com/github/github-mcp-server
transport: stdio
---
GitHub MCP server. Create a fine-grained PAT.

Config (mcpServers entry — substitute creds via `!mcp enable github` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}
```
Homepage: https://github.com/github/github-mcp-server
