---
name: linear-cli
description: "Use when the user mentions Linear or wants to list, view, create, update, comment on, assign, prioritize, or delete Linear issues, or check issue/team/project/user status from the command line (ENG-123, sprint, backlog, ticket)."
version: 1.0.0
license: MIT
tags: [linear, issue-tracking, project-management, cli, tickets, sprint, backlog, kanban]
source: https://github.com/Valian/linear-cli-skill
derived_from: awesomeclaude
prerequisites:
  commands: [node]
---

# Linear Issue Management

Lightweight Node CLI to drive Linear's issue tracker. Use whenever the user
mentions Linear or asks to work with issues, teams, projects, or users.

## When to use

- "create a Linear issue for X", "comment on ENG-123", "what's the status of ENG-45"
- "list my in-progress issues", "assign this ticket to Sam", "bump priority to urgent"
- "show open issues for the backend team", "delete that ticket"

## Setup

- Requires `node`. Dependencies (`@linear/sdk`, `dotenv`) auto-install on first run.
- Needs a Linear personal API key in env: `LINEAR_API_KEY`.
  Get one at https://linear.app/settings/api (Settings > API > Personal API keys > Create key).
- The CLI entrypoint is the `linear` script in the skill dir; the implementation
  lives at `scripts/linear-cli.js` in the source repo
  (https://github.com/Valian/linear-cli-skill/tree/main/linear). Run it as `./linear`
  from the skill directory.

## Command pattern

```bash
./linear <resource> <action> [arguments] [options]
```

Resources: `issue`, `user`, `team`, `project`. Add `--json` to any command for
machine-readable output; `--help` on any command for details.

## Lookups (get the UUIDs you need)

```bash
./linear user list      # -> #<user-id>  <name>  <email>
./linear team list      # -> #<team-id>  <name>  <key>
./linear project list   # -> #<project-id>  <name>  <state>
```

User/team/project IDs are UUIDs; grab them from these list commands before
creating or filtering.

## Issues

List (filterable):
```bash
./linear issue list [--team <id>] [--assignee <id>] [--status <name>] [--limit <n>]
# default limit 50; returns: #<identifier>  <title>  <status>  <assignee>
./linear issue list --assignee def456 --status "In Progress"
```

View full detail (title, status, assignee, team, priority, labels, dates,
description, comments):
```bash
./linear issue view ENG-123      # or a UUID
```

Create (`--team` required):
```bash
./linear issue create "Fix login bug" --team abc123 --priority 2 \
  [--description <text>] [--assignee <id>] [--status <name>]
```

Comment (multi-word text auto-combined, no quotes needed):
```bash
./linear issue comment ENG-123 needs another reviewer before merge
```

Update (one or many fields at once):
```bash
./linear issue update ENG-123 --status "In Progress" --assignee abc123 \
  [--priority <n>] [--title <text>] [--description <text>]
```

Delete (soft delete -> trash, recoverable):
```bash
./linear issue delete ENG-123
```

## Priority values

`0`=None, `1`=Urgent, `2`=High, `3`=Medium, `4`=Low.

## Gotchas

- Issue identifiers are case-insensitive (`ENG-123` == `eng-123`).
- Status names are case-SENSITIVE: `"In Progress"` != `"in progress"`.
- User/team/project IDs are UUIDs — always fetch via the `list` commands, never guess.
- Issue key format is `<TEAM_KEY>-<NUMBER>` (e.g. `ENG-123`).
- API-key errors are self-explanatory; fix `LINEAR_API_KEY` and re-run.
