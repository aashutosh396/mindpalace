# mindpalace v3 — Projects GUI

v3 turns mindpalace from a chat-gateway bot into a **project workspace**: a web GUI
where each project has assets, git repos, a kanban board, and a chat that turns
instructions into agent tickets.

## The one big architecture decision

**A browser cannot touch the local machine.** No git, no spawning Claude sessions,
no free filesystem access — the File System Access API is sandboxed and can't
execute anything. So:

> The daemon does the work. The browser is only the screen.

```
┌─────────────────────────── user's machine ───────────────────────────┐
│                                                                      │
│  Browser (localhost:7777)          mindpalace daemon (Python)        │
│  ┌──────────────────────┐   HTTP   ┌───────────────────────────────┐ │
│  │  Nuxt SPA (static)   │◄────────►│  web gateway (FastAPI)        │ │
│  │  - project list      │    WS    │   ├─ REST: projects/tasks/    │ │
│  │  - kanban board      │◄────────►│   │        assets/repos       │ │
│  │  - project chat      │  events  │   ├─ WS: live task/chat events│ │
│  │  - asset uploads     │          │   └─ serves the Nuxt bundle   │ │
│  └──────────────────────┘          │                               │ │
│                                    │  brain (existing v2 engine)   │ │
│                                    │   ├─ per-project job routing  │ │
│                                    │   ├─ Claude Code sessions     │ │
│                                    │   └─ skills / MCP / goals     │ │
│                                    │                               │ │
│                                    │  storage                      │ │
│                                    │   ├─ SQLite (projects, tasks, │ │
│                                    │   │   repos, chat log)        │ │
│                                    │   └─ ~/.mindpalace/projects/  │ │
│                                    │       <slug>/assets/…        │ │
│                                    └───────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

The web gateway sits **beside** the Discord and WhatsApp gateways — third gateway,
same brain. A project in the GUI is the same concept as an activated channel today.

## Distribution — "how do I give this to everyone?"

**Hard requirement: install stays `./install.sh` and done.** No Node, no npm, no
build step on the user's machine — ever.

- The Nuxt app is pre-built (`npm run generate`) by developers/CI and the static
  output is committed into the repo (e.g. `mindpalace/web/dist/`) and declared as
  package data in `pyproject.toml`. pip ships the UI inside the package like any
  other file.
- **v3.0 user flow**: `./install.sh` (unchanged) → `mindpalace` → daemon starts the
  web gateway and auto-opens `http://localhost:7777`. The browser is the GUI —
  nothing extra to install.
- Updating = `git pull && ./install.sh`, same as today.
- Only new runtime deps: FastAPI + uvicorn, pulled in silently by pip.
- **Later (optional)**: wrap the same UI in Tauri for a desktop-app feel. Zero rework —
  Tauri just embeds the localhost page.
- **Not this**: a hosted web app. Then the agent would act on the server's files, not
  the user's machine — a different product.

## Data model (SQLite)

```
project        id, slug, name, created_at
repo           id, project_id, path, url, is_primary
repo_link      project_id, repo_id          -- referenced repo from ANOTHER project
asset          id, project_id, filename, path, uploaded_at
task           id, project_id, title, body, status(todo|in_progress|review|done),
               created_by(user|agent), session_id, created_at, closed_at
chat_message   id, project_id, role, text, task_id?, created_at
```

Assets land in `~/.mindpalace/projects/<slug>/assets/` — DB stores metadata,
filesystem stores bytes. Same philosophy as the vault.

## Core flows

**Chat → ticket.** User types an instruction in the project chat. The gateway
creates a `task` in **todo**, the brain picks it up (existing per-room job queue),
moves it to **in progress**, works in a Claude Code session whose cwd/allowed
paths = the project's repos + linked repos, then moves it to **review** with a
short report. The user closes it, or tells the agent "close task 42" — the brain
gets a `close_task(id)` tool.

**Kanban.** The board is just a view over `task` grouped by status, updated live
over the WebSocket. Drag-and-drop = status PATCH.

**Repos & linked repos.** A project owns one or many repos (local paths, optionally
with remotes). It can also *link* a repo owned by another project — read/write
access from this project's chat, but ownership (and where it shows as primary)
stays with the original project. The agent's sandbox allowlist per task =
`own repos ∪ linked repos ∪ project asset folder`.

## Build order

1. **P1 — web gateway skeleton**: FastAPI in the daemon, serves static dir, REST
   for projects CRUD, WS event bus. `mindpalace serve` command.
2. **P2 — Nuxt app**: project list + create, project screen shell (chat / kanban /
   assets tabs). Static build wired into packaging.
3. **P3 — chat→ticket loop**: chat input → task row → brain queue → status
   transitions streamed to the board. `close_task` tool.
4. **P4 — repos**: attach repos, linked repos, per-task path allowlist.
5. **P5 — assets**: upload endpoint + browser, agent can read assets in-session.
6. **P6 — polish**: auth token for the local port, multi-repo status chips,
   Tauri wrapper (optional).

## What carries over from v2 untouched

Brain, session continuity, skills library, MCP registry, goal loops, per-room
routing (rooms become projects), telemetry. Discord and WhatsApp gateways keep
working — v3 adds a surface, it does not replace one.
