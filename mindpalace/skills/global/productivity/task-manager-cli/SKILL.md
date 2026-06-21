---
name: task-manager-cli
description: "Use when adding, listing, completing, or filtering to-do tasks — across Todoist, Things 3, or Taskwarrior. Detects which tool is installed. Handles due dates, priorities, projects, tags, overdue filtering."
version: 1.0.0
license: MIT
tags: [tasks, todo, todoist, things, taskwarrior, productivity, due-dates, projects]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-tasks
derived_from: awesomeclaude
---

# Task Manager CLI

Manage to-dos across Todoist, Things 3, or Taskwarrior. Detect with
`which todoist-cli things-cli task` and use the one available.

## When to use
Adding/listing/completing tasks, filtering by project or due date, checking
overdue items.

## Todoist — `todoist-cli`

```bash
todoist-cli list                        # Today's tasks
todoist-cli list --project "Work"
todoist-cli add "Task" --due today --priority 2
todoist-cli complete <task-id>
todoist-cli projects
todoist-cli search "query"
```

## Things 3 — `things-cli` (macOS)

```bash
things-cli today
things-cli add "Task" --when today --tag "urgent"
things-cli add "Task" --project "Project" --deadline "2026-03-01"
things-cli complete "Task name"
things-cli projects
```

## Taskwarrior — `task`

```bash
task list                               # Pending
task next                               # Top priority
task add "Task" due:tomorrow pri:H project:work
task <id> done
task <id> modify priority:H
task +OVERDUE list                      # Overdue
task summary
```

## Guidelines
- Check which tool is installed before running commands.
- If several exist, ask the user which they prefer.
- Todoist/Things parse natural-language dates; Taskwarrior uses `due:YYYY-MM-DD`.
