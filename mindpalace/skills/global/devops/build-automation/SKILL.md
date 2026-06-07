---
name: build-automation
description: "Set up a scheduled/automated task at the right tier — cron one-liner, a workspace project, or a stateful long-running job with JSON/SQLite tracking."
version: 1.0.0
author: mindpalace
license: MIT
platforms: [linux, macos]
tags: [automation, cron, schedule, scraper, pipeline, background-job, sqlite, venv, django, idempotent, resumable]
related_skills: [deploy-django-app, connect-tailscale]
---

# Build Automation

Use this when the owner wants something to run **on its own** — on a schedule, repeatedly, or in the background: "scrape X every morning", "back up Y weekly", "watch Z and tell me when…", "keep this data fresh".

The whole point of this skill is to **pick the lightest tier that fits and not over-build**. Reach for the smallest thing that does the job; escalate only when the task genuinely needs state, code, or resumability.

## Decide the tier first

```
stateless one-off?            → Tier 1 (cron / queued script)
needs real code + context?    → Tier 2 (workspace project)
must resume / dedupe / track? → Tier 3 (project + JSON or SQLite state)
```

Ask yourself: *Does it need to remember anything between runs?* No → Tier 1. *Does it have real logic/deps that will evolve?* → Tier 2. *Is it long-running, accumulating data, or must survive crashes and pick up where it left off?* → Tier 3.

---

## Tier 1 — simple / stateless

A periodic command, reminder, or backup. No project, no state.

- A queued script at `~/.mindpalace/jobs/queue/<name>.sh` (the background watcher runs it and reports back), **or** a direct `crontab` entry.
- Report results to the owner with `python3 -m mindpalace.notify 'msg'`.
- Example: `0 9 * * *  /usr/bin/rsync -a ~/important/ ~/backup/ && python3 -m mindpalace.notify 'daily backup done'`

Don't create a project for this.

## Tier 2 — needs code + continuous context

Real logic, dependencies, several files, will evolve. Make it a **project** in the workspace.

1. `mkdir -p ~/.mindpalace/workspace/<slug>` (use the owner's confirmed workspace).
2. Python/Django split — keep env apart from source:
   - `<slug>/venv/` — the virtualenv (`python3 -m venv venv`)
   - `<slug>/<project>/` — the actual source (scripts, package, `manage.py`)
3. Scaffold the basics (ALWAYS): `git init`; a `.gitignore` excluding `venv/`, `.env`, `__pycache__/`, `*.pyc`, `node_modules/`, build artifacts, and any data/state files; a committed `.env.example` documenting every variable; a real `.env` with actual values (gitignored, never committed); a short `README`.
4. Schedule it (see "cron that actually runs", below).
5. Map it: pointer note at `vault/projects/<slug>.md` (where it lives, what it does, how to run/schedule it) + a line in `vault/LOG.md`.

## Tier 3 — long-lived / stateful

Scrapers, pipelines, anything that must **resume, dedupe, accumulate data, or report progress over time**. This is a Tier 2 project **plus a tracking store**.

- **Pick the store by complexity:**
  - **JSON** (`state.json`) — light state: a cursor, a small set of seen IDs, last-run timestamp, a few counters.
  - **SQLite** (`state.db`) — larger / queryable / concurrent: thousands of rows, dedup at scale, joins, or overlapping writers. Use **WAL mode** (`PRAGMA journal_mode=WAL;`).
- **Idempotent + resumable:** every run reads the store, skips what's already done, and writes progress as it goes — so a crash or re-run never duplicates work and always picks up where it left off.
- Keep `state.json` / `state.db` and any scraped data **inside the project and gitignored**.
- Report **meaningful** updates only (milestones, completion, errors) via `python3 -m mindpalace.notify` — not every row.

Sketch:
```python
# resumable scraper
import json, pathlib
STATE = pathlib.Path(__file__).with_name("state.json")
seen = set(json.loads(STATE.read_text())) if STATE.exists() else set()
for item in source():
    if item.id in seen:        # idempotent: never re-do
        continue
    handle(item)
    seen.add(item.id)
    STATE.write_text(json.dumps(sorted(seen)))   # checkpoint as you go
```

---

## cron that actually runs (the usual failure)

- Call the project's **own venv python by ABSOLUTE path** — never bare `python`/`python3` (cron's PATH is minimal and won't find the venv):
  ```
  */30 * * * *  /Users/<you>/.mindpalace/workspace/<slug>/venv/bin/python /Users/<you>/.mindpalace/workspace/<slug>/<project>/run.py >> /Users/<you>/.mindpalace/workspace/<slug>/run.log 2>&1
  ```
- **Guard overlapping runs:** a lockfile (`flock`) or a SQLite WAL + a "running" flag, so a slow run doesn't stack on the next tick.
- Long work runs in the **background** (cron/queue), never inline in chat — set it up, tell the owner it's scheduled, then let it report back.
- Redirect output to a logfile in the project so failures are diagnosable.

## Done checklist

- [ ] Chose the lowest tier that fits (didn't over-build).
- [ ] Tier 2/3: project in the workspace with venv/source split + git/.gitignore/.env/.env.example/README.
- [ ] Tier 3: state store chosen by complexity; runs are idempotent + resumable; data/state gitignored.
- [ ] cron uses the venv's absolute python path + a logfile + an overlap guard.
- [ ] Pointer note in `vault/projects/` + `LOG.md` line; meaningful updates via `notify`.
