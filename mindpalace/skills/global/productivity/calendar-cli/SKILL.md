---
name: calendar-cli
description: "Use when viewing, creating, updating, or checking availability for calendar events — Google Calendar via gog or Apple Calendar via icalBuddy. List upcoming events, create meetings with attendees, freebusy checks, manage multiple calendars."
version: 1.0.0
license: MIT
tags: [calendar, events, scheduling, google-calendar, apple-calendar, gog, icalbuddy, freebusy, meetings]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-calendar
derived_from: awesomeclaude
---

# Calendar CLI

Manage calendars via `gog` (Google Calendar) or `icalBuddy` (Apple Calendar).
Check availability first with `which gog icalBuddy`.

## When to use
Listing today's/upcoming events, creating or updating events, inviting
attendees, checking free/busy before scheduling.

## Google Calendar — `gog cal`

```bash
gog cal list                          # Upcoming events
gog cal list --days 7                 # Next 7 days
gog cal list --calendar "Work"
gog cal create --title "Meeting" --start "tomorrow 2pm" --duration 1h
gog cal create --attendees "alice@x.com,bob@x.com" --title "Sync"
gog cal update <event-id> --title "New Title"
gog cal delete <event-id>
gog cal calendars                     # List calendars
gog cal freebusy --start "tomorrow" --end "tomorrow 5pm"   # Availability
```

## Apple Calendar — `icalBuddy` (read-only)

```bash
icalBuddy eventsToday
icalBuddy eventsToday+3                # Today through next 3 days
icalBuddy eventsFrom:"2026-03-01" to:"2026-03-07"
icalBuddy -ic "Work" eventsToday      # Specific calendar
icalBuddy calendars
```

## Guidelines
- Use `gog cal freebusy` to check availability before scheduling.
- `icalBuddy` is read-only — for creating Apple events use `gog` or AppleScript.
- `gog` accepts natural-language dates ("tomorrow 2pm", "next Monday 9am").
- `gog` needs OAuth (`gog auth`); multi-account via `--account work`.
