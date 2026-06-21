---
name: daily-briefing
description: "Use when the user asks for a daily briefing, morning summary, or 'what's on my plate today' — aggregates email, calendar, tasks, weather, GitHub, and packages from whatever skills are installed into one concise digest. Can run on a schedule."
version: 1.0.0
license: MIT
tags: [briefing, daily, morning, summary, digest, agenda, schedule, productivity]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-briefing
derived_from: awesomeclaude
---

# Daily Briefing

Compile a concise morning digest by pulling from whatever assistant skills are
installed. Adapt sections to what is actually available.

## When to use
"Daily briefing", "morning summary", "what's on my plate today", or a scheduled
automated digest.

## What to include (only if the source skill/tool exists)

| Source | Include |
|---|---|
| Email | Unread count + top 5 subjects + flagged |
| Calendar | Today's events + tomorrow preview |
| Tasks | Due today + overdue |
| Notes | Recently modified |
| GitHub | Open PRs, review requests, CI failures |
| Slack | Unread DMs + mentions |
| Tracking | Package delivery updates |

## Format

```
Good morning, {name}! Briefing for {date}:

📧 Email: 12 unread — 3 flagged
  → "Q4 Budget Review" from Sarah
📅 Calendar:
  → 9:00 AM  Team standup (30 min)
✅ Tasks: 3 due today, 1 overdue
  → [overdue] Fix login bug
🔔 Other: 2 PRs need review · package arriving today
```

## Scheduled briefing

```bash
cat > ~/.claude/briefing.sh << 'SCRIPT'
#!/bin/bash
claude --print "Run my daily briefing. Be concise."
SCRIPT
chmod +x ~/.claude/briefing.sh
(crontab -l 2>/dev/null; echo "0 8 * * 1-5 ~/.claude/briefing.sh") | crontab -
```

## Guidelines
- Read the user's name/city from memory.
- Only include sections for tools that exist; keep each to ≤5 items.
- Flag urgent items at the top; include the date and day of week.
