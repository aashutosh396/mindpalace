---
name: google-calendar
description: Use when the user wants to check their calendar, schedule or create an event, find available/free time, list upcoming events, update or delete an event, or respond to a meeting invite — a lightweight Google Calendar connector with standalone OAuth (no MCP server). Trigger keywords: google calendar, schedule meeting, create event, find free time, calendar event, RSVP.
version: 1.0.0
license: Apache-2.0
tags: [google-calendar, calendar, scheduling, google, oauth, connector, productivity, events]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/google-calendar
derived_from: awesomeclaude
prerequisites: Google Workspace account (personal Gmail not supported)
---

# Google Calendar

Lightweight Google Calendar integration with standalone OAuth. No MCP server required.

> Requires a Google Workspace account. Personal Gmail accounts are not supported.

## Setup / Auth

```bash
python scripts/auth.py login
python scripts/auth.py status
python scripts/auth.py logout
```

All operations run via `scripts/gcal.py`, auto-authenticating on first use.

## List

```bash
python scripts/gcal.py list-calendars
python scripts/gcal.py list-events                          # primary, next 30 days
python scripts/gcal.py list-events --time-min 2024-01-15T00:00:00Z --time-max 2024-01-31T23:59:59Z
python scripts/gcal.py list-events --calendar "work@example.com" --max-results 10
python scripts/gcal.py get-event EVENT_ID [--calendar "work@example.com"]
```

## Create

```bash
python scripts/gcal.py create-event "Team Meeting" "2024-01-15T10:00:00Z" "2024-01-15T11:00:00Z"
python scripts/gcal.py create-event "Team Meeting" START END --description "Sync" --location "Room A"
python scripts/gcal.py create-event "Team Meeting" START END --attendees a@x.com b@x.com
python scripts/gcal.py create-event "Meeting" START END --calendar "work@example.com"
```

## Update / Delete

```bash
python scripts/gcal.py update-event EVENT_ID --summary "New Title"
python scripts/gcal.py update-event EVENT_ID --start START --end END
python scripts/gcal.py update-event EVENT_ID --summary S --description D --location L
python scripts/gcal.py update-event EVENT_ID --attendees a@x.com c@x.com
python scripts/gcal.py delete-event EVENT_ID [--calendar "work@example.com"]
```

## Find free time

```bash
python scripts/gcal.py find-free-time --attendees me \
    --time-min "2024-01-15T09:00:00Z" --time-max "2024-01-15T17:00:00Z" --duration 30
python scripts/gcal.py find-free-time --attendees me a@x.com b@x.com \
    --time-min START --time-max END --duration 60
```

## Respond to invite

```bash
python scripts/gcal.py respond-to-event EVENT_ID accepted   # or declined / tentative
python scripts/gcal.py respond-to-event EVENT_ID accepted --no-notify
```

## Formats

Times use ISO 8601 with timezone: `2024-01-15T10:30:00Z` (UTC) or `...-05:00` (offset).
Calendar ID: use `primary` (or omit `--calendar`) for the main calendar, else the email-like ID from `list-calendars`.

## Tokens

System keyring (Keychain / Credential Locker / Secret Service). Service name `google-calendar-skill-oauth`. Auto-refresh on expiry.
