---
name: Slack
slug: slack
description: Use when reading or posting Slack messages / managing channels.
category: productivity
env: SLACK_BOT_TOKEN, SLACK_TEAM_ID
homepage: https://github.com/modelcontextprotocol/servers
transport: stdio
---
Slack MCP server.

Config (mcpServers entry — substitute creds via `!mcp enable slack` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-slack"
  ],
  "env": {
    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
    "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
  }
}
```
Homepage: https://github.com/modelcontextprotocol/servers
