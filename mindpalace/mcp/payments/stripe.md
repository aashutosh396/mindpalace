---
name: Stripe
slug: stripe
description: Use when working with Stripe — customers, charges, invoices, products.
category: payments
env: STRIPE_SECRET_KEY
homepage: https://github.com/stripe/agent-toolkit
transport: stdio
---
Stripe MCP server. Use a restricted/test key.

Config (mcpServers entry — substitute creds via `!mcp enable stripe` or env):
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@stripe/mcp",
    "--tools=all"
  ],
  "env": {
    "STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}"
  }
}
```
Homepage: https://github.com/stripe/agent-toolkit
