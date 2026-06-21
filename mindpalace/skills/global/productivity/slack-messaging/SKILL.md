---
name: slack-messaging
description: "Use when sending Slack messages, DMs, thread replies, or uploading files to channels — via the slack CLI. Post to #channels, DM @users, share reports/images, reply in threads with markdown."
version: 1.0.0
license: MIT
tags: [slack, messaging, communication, channels, dm, files, notifications, productivity]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-slack
derived_from: awesomeclaude
prerequisites: ["slack CLI installed and authenticated (slack auth); bot token with chat:write and files:write scopes"]
---

# Slack Messaging

Send messages and upload files to Slack channels and users with the `slack` CLI.

## When to use
Posting to a channel, DMing a user, replying in a thread, or sharing a file to
Slack.

## Commands

```bash
slack chat send --channel "#general" --text "Hello team"
slack chat send --channel "@username" --text "Hey!"          # DM
slack chat send --channel "#dev" --text "*Bold* and _italic_"  # Markdown
slack chat send --channel "#general" --thread-ts "1234567890.123456" --text "Reply"
slack files upload --channel "#general" --file ./report.pdf --title "Weekly Report"
slack channels list
```

## Guidelines
- Confirm the target channel/user before sending.
- Use `#channel-name` for channels, `@username` for DMs.
- Use threads for follow-ups; keep messages concise.
- Avoid bulk sending in tight loops — rate limits apply.
