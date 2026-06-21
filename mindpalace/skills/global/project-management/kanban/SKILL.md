---
name: kanban
description: "Use when the user asks to create, move, view, list, search, or manage tasks/cards on a kanban board, or track work items across statuses (backlog, todo, doing, done, archive) — board is Markdown files in a kanban/ directory."
version: 1.0.0
license: Apache-2.0
tags: [kanban, board, tasks, cards, markdown, project-management, backlog, todo, workflow, tracking]
source: https://github.com/mattjoyce/kanban-skill
derived_from: awesomeclaude
---

# Kanban (Markdown board)

Manage a Kanban board as Markdown files in a `kanban/` directory. Each `.md` file
is one card. Board state is derived by reading all card files and grouping by their
`status` frontmatter field. Completed cards may be filed under `kanban/archived/`.

## When to use

User says: create/add a card or task, move a card, "show the board", list cards,
search by tag/content, find blocked cards, archive done cards, or any work-tracking
across backlog → todo → doing → done.

## Card fields (frontmatter)

- `id` — unique numeric id. Scan all cards in `kanban/` (incl. `kanban/archived/`),
  use max + 1. Start at `1` if empty. Reference cards by this number.
- `status` — `backlog`, `todo`, `doing`, `done`, or `archive`.
- `priority` — `High` or `Normal` (defaults to `Normal`).
- `blocked_by` — list of card IDs that must be `done` before this moves to `doing`,
  e.g. `[3, 7]`. Omit or `[]` if unblocked.
- `assignee` — (optional) owner.
- `due_date` — (optional) target date (ISO).
- `tags` — (optional) list of labels.

## Creating a card

New kebab-case `.md` file in `kanban/`. Optionally include a Job Story
("When [situation], I want to [motivation], so I can [expected outcome]") only when
it fits naturally — confirm it with the requester if added.

```markdown
---
id: 1
status: todo
priority: Normal
blocked_by: []
assignee: "@claude"
due_date: 2026-02-28
tags: [auth, backend]
---

# Implement User Authentication

Set up user authentication using JWTs.

## Acceptance Criteria
- Users can register for a new account.
- Users can log in with their credentials.
- Authenticated users receive a JWT.
```

## Moving a card

Edit the `status` field. Before moving to `doing`, verify every id in `blocked_by`
has `status: done`; if any are not done, the card stays put.

Cards with `status: done` may be moved into `kanban/archived/` to keep the main
board tidy — this is a file-location move only; keep `status: done` unless told
otherwise. Create `kanban/archived/` if it does not exist.

## Narrative record (required)

Treat cards as durable source material. Do not rewrite or delete prior narrative
unless asked. When updating a card, append a brief note to a `## Narrative` section
at the end of the file — focus on reasons, discoveries, decisions; skip transactional
status-change logs. Use ISO dates. Add the section if missing. Skip the note for
trivial edits (typos). When moving to `done`, write enough that a future reader
understands the card's story and outcome.

```markdown
## Narrative
- 2026-02-05: Discovered the auth flow must support device-based MFA; shifted to WebAuthn. (by @assistant)
```

## Viewing / searching the board

Helper scripts ship with the source skill under `skills/kanban-ai/scripts/`
(in the repo above). Each takes the kanban directory as its first arg (defaults to
current dir). If installed locally, locate via glob `**/kanban-ai/scripts/<name>.sh`.

| Script | Purpose |
|---|---|
| `view_board.sh kanban/` | Cards grouped by status, with priority + blocked_by inline |
| `search_by_tag.sh kanban/ <tag>` | Cards with that tag (id, status, title) |
| `search_content.sh kanban/ "<term>"` | Cards matching term, with context lines |
| `show_blocked.sh kanban/` | Cards with non-empty `blocked_by` and what blocks them |
| `list_tags.sh kanban/` | All tags by usage count |
| `list_all_cards.sh kanban/` | All cards as `id|status|blocked_by|title`, sorted by id |

If the scripts are not present, derive the same views directly: read all `.md`
files in `kanban/` (+ `kanban/archived/`), parse frontmatter, and group/filter.

## Gotchas

- ID collisions: always scan including `kanban/archived/` before assigning a new id.
- Never auto-move a blocked card into `doing`.
- Archiving changes file location, not `status`.
