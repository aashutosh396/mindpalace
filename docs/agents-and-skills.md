# Agents & Skills

## The Analyst agent
A dedicated background agent that makes mindpalace smarter:
- **reflect** — after each real task, it reasons, then files durable facts into the vault and
  **skillifies** first-time reusable procedures.
- **review** — on each heartbeat, it proactively reviews the vault + service health and reports.

More agents can be added under `mindpalace/agents/` (see `agents/base.py`).

## Skills: global → user
- **Global skills** (`mindpalace/skills/global/*.md`) ship read-only — reference recipes.
- When the agent does real work, it **derives a user skill** (`~/.mindpalace/skills/`) tailored to
  your setup, with `derived_from:` linking back. Globals are never edited.

## Memory
Durable facts go to `memory/MEMORY.md`; every turn is saved to a SQLite FTS index and the top
matching past turns are recalled on each new message.
