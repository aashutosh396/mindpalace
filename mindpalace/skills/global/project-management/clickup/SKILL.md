---
name: clickup
description: 'Use when managing ClickUp tasks, sprints, comments, time tracking, docs, or goals via the `cup` CLI. Triggers: ClickUp task queries, status updates, sprint tracking, creating subtasks, posting/threaded comments, standup summaries, searching tasks, overdue items, assigning tasks/groups, listing spaces/lists/folders, custom fields, tags, checklists, time entries, attachments, bulk operations, goals & key results, docs, saved filters, chat channels.'
version: 1.0.0
license: MIT
tags: [clickup, tasks, sprints, project-management, cli, time-tracking, agile, standup]
source: https://github.com/krodak/clickup-cli
derived_from: awesomeclaude
prerequisites:
  - Node.js 22+
  - ClickUp personal API token (pk_...)
---

# ClickUp CLI (`cup`)

Drive ClickUp from the terminal: tasks, sprints, comments, time, custom fields, goals, docs, chat. Built for agents — piped output is Markdown (context-friendly); add `--json` for structured parsing.

## Install & configure

```bash
npm install -g @krodak/clickup-cli        # or: brew tap krodak/tap && brew install clickup-cli
```

Get a token at https://app.clickup.com/settings/apps (starts with `pk_`). Team/workspace ID is in the URL: `https://app.clickup.com/TEAM_ID/...`.

```bash
cup init --token pk_USER_TOKEN --team TEAM_ID   # non-interactive (best for agents)
# or env vars, no config file:
export CU_API_TOKEN="pk_..."; export CU_TEAM_ID="12345678"
cup auth                                          # verify — prints user + workspace
```

Config lives at `~/.config/cup/config.json`. Multiple profiles via `cup profile add/use <name>` or `-p <name>` per command. `CU_PROFILE` env selects a profile.

## When to use

- Listing / searching / inspecting tasks, sprints, subtasks, comments
- Creating and updating tasks, statuses, assignees, due dates, custom fields, tags
- Standup summaries, overdue reports, recently-updated inbox
- Time tracking, checklists, dependencies, links, attachments
- Goals & key results, docs, workspace structure (spaces/folders/lists), chat

At session start, run `cup filter list` to discover workspace saved shortcuts. Run them with `cup filter run <name>`.

## Read commands

```bash
cup tasks [--status s] [--name q] [--list id] [--space id] [--all] [--assignee me] [--tag t] [--due-before d] [--field "Name" val]
cup assigned [--status s]                 # my tasks grouped by status
cup sprint [--space n] [--folder id]      # active sprint (auto-detected)
cup sprints [--space n]                   # all sprints (* marks active)
cup search <query> [--all] [--status s]   # search tasks by name
cup task <id>                             # single task detail (fields, checklists, deps)
cup subtasks <id>                         # child tasks (add --include-closed for all)
cup comments <id> | cup activity <id>     # discussion / task+comments combined
cup inbox [--days n]                      # tasks updated in last n days (default 30)
cup summary [--hours n]                   # standup: done / in-progress / overdue
cup overdue [--all]                       # past due, most overdue first
cup spaces | cup folders <spaceId> | cup lists <spaceId>
cup members | cup groups | cup fields <listId> | cup tags <spaceId>
cup goals | cup key-results <goalId>
cup docs [query] | cup doc <docId> [pageId]
```

By default `tasks`, `search`, `overdue`, `assigned` show only YOUR tasks — add `--all` for team-wide (e.g. finding parent initiatives).

## Write commands

```bash
cup create -n name [-l listId|sprint:current] [-p parentId] [-s status] [--priority p] \
  [--due-date d] [--assignee me] [--group-assignee @handle] [--tags "a,b"] [--field "Name" val]
cup update <id> [-n name] [-s status] [--priority p] [--due-date d|none] [--assignee me] \
  [--remove-assignee id] [--parent id] [--archive] [--field "Name" val]
cup comment <id> -m text [--notify-all] [--mention user]   # markdown → rich text
cup reply <commentId> -m text [--mention user]             # threaded reply
cup assign <id> [--to ids|me] [--remove ids] [--group @handle]
cup depend <id> [--on taskId] [--blocks taskId] [--remove]
cup move <id> [--to listId|sprint:current] [--remove listId]   # see note below
cup field <id> [--set "Name" value] [--remove "Name"]
cup tag <id> [--add tags] [--remove tags] | cup link <id> <linksTo> | cup attach <id> <file>
cup duplicate <id> | cup merge <src> <into> --confirm
cup bulk status <status> <ids...> | cup bulk assign <ids...> --to me | cup bulk move <ids...> --to <list>
cup checklist create <id> <name> | cup checklist add-item <clId> <name> [--parent itemId]
cup time start <id> [-d desc] | cup time stop | cup time log <id> 2h | cup time list
cup goal-create <name> | cup key-result-create <goalId> <name> --type percentage --target 80
cup doc-create <title> -c "# Draft" | cup doc-page-create <docId> <name> -c content
cup chat send <channelId> -m text | cup chat reply <messageId> -m text
```

`cup move`: `--to` + `--remove` together changes the task's HOME list (v3 endpoint, auto status mapping). `--to` alone adds multi-list membership.

## Conventions

- **Task IDs**: native (`abc123def`), custom (`PROJ-123`, auto-detected), or full ClickUp URLs (ID auto-extracted).
- **`--status`**: fuzzy match (exact > starts-with > contains).
- **`--priority`**: `urgent|high|normal|low` or `1-4`.
- **`--due-date`**: `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM`, or ISO 8601 with offset; `none` clears.
- **`--time-estimate` / `time log`**: `"2h"`, `"30m"`, `"1h30m"`, or raw ms.
- **`--field --set`**: text, number, checkbox, dropdown, labels (comma list), date, url, email, rating, progress, tasks/users (comma IDs). Names resolve case-insensitively.
- **`--mention <user>`**: real @mention (notifies). Accepts ID/email/username/`me`, repeatable. Bare `@Name` in text is NOT parsed.
- **Description quoting**: use `$'...'` for `-d`/`-m` values with backticks or newlines (heredocs/double quotes strip backticks).
- **Global flags**: `-p/--profile <n>`, `--json` (all commands). `CU_OUTPUT=json` forces JSON when piped.
- **Rate limiting**: client auto-retries 429/5xx with backoff — no action needed.

## Sprints & favorites

`cup sprint` auto-detects the active sprint by folder name (sprint/iteration/cycle/scrum). Override with `--folder <id>`, `cup config set sprintFolderId <id>`, or favorite a sprint folder. Favorites are local-only: `cup favorite add sprint-folder <id> --name "Team Sprint"`, then `cup sprint` auto-uses it.

## DELETE SAFETY

ALWAYS confirm with the user before `cup delete`, `cup list-delete`, `cup folder-delete`, `cup space-delete`, `cup merge`, or `cup webhook delete`. These are destructive and irreversible. Even with `--confirm`, verify the ID with the user first. Non-interactive destructive commands require `--confirm`.
