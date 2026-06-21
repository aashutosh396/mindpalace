---
name: linkedin-growth
description: Use when the user wants to grow their LinkedIn network at scale — import leads from a Sales Navigator or regular search URL/filters, qualify them against an ICP, then auto-send connection invites on a schedule across one or more accounts and withdraw stale pending requests. Also for status questions (counts, conversion, pending older than N days), pausing/resuming an account, changing the ICP, or installing the recurring scheduler. Built on linkedin-cli + a local SQLite pipeline.
version: 1.0.0
license: MIT
tags: [linkedin, lead-gen, outreach, automation, sales-navigator, pipeline, scheduler, vendor-locked]
source: https://github.com/Linked-API/linkedin-skills/blob/main/linkedin-growth/SKILL.md
derived_from: awesomeclaude
platforms: [linkedapi.io]
prerequisites: [node, "@linkedapi/linkedin-cli", better-sqlite3]
---

# LinkedIn Growth Pipeline

Turns a LinkedIn / Sales Navigator search into a managed pipeline:
**search → qualify (you, via sub-agent against the user's ICP) → store → invite on schedule
→ check pending → withdraw stale**. All state is in a local SQLite DB. Every LinkedIn action
goes through `linkedin-cli`; you orchestrate via the Node scripts in `scripts/`.

**Phase A (import)** runs only when the user triggers it and includes the LLM qualification
step. **Phase B (network maintenance)** runs on a schedule and NEVER calls an LLM.

## First-run setup

1. `node --version` ≥ 20. If missing, print the OS install command and stop.
2. From the skill dir: `node scripts/doctor.mjs --json`. If it reports a missing
   `better-sqlite3`, run `npm install --omit=dev` (or `doctor.mjs --fix`) and re-run.
3. Fix each FAIL:
   - `linkedin-cli` → `npm install -g @linkedapi/linkedin-cli`
   - `cli-accounts` → get tokens from app.linkedapi.io, `linkedin setup --linked-api-token=<a> --identification-token=<b>` (per LinkedIn account)
   - `db` → auto-created, or `node scripts/db.mjs init`
   - `db-accounts` → `linkedin account list`, then register each: `node scripts/account.mjs add --name <short> --cli-account "<exact name from list>"`
4. Re-run doctor until `"ok": true`.
5. **Pace** — ask once for all accounts: "at most one invite every N minutes (default 15)?";
   apply via `--min-invite-interval N` on add or `account.mjs update`.
6. **Retry policy** — ask "if not accepted, try another account? (no / N / all)":
   `node scripts/settings.mjs set max_connect_attempts 1|N|all` (1 = no retry, default).
7. **Scheduler** (only after ≥1 account): `node scripts/schedule.mjs install`. Describe it as
   "runs in the background, sends invites during each account's active hours" — never expose
   the internal tick frequency.
8. Setup sends nothing until leads exist — end by asking for a search URL + list name and go
   straight into Phase A.

## Phase A — Import (interactive)

**Step 1 — Prepare.** ALWAYS ask the user for a limit first (`--limit` is required; `max`/`all`
= cap). Caps: Sales Nav (`nv`) 2500, standard (`st`) 1000. Auto-detect type: URL with `/sales/`
→ `nv`, else `st`.

```bash
node scripts/import.mjs prepare --searcher <db-account> --list "<name>" --limit <N|max> \
  [--type nv|st] [--search-url "<url>"] [--term ... --position ... --locations ... --industries ...]
```

It runs the search, dedupes against `leads`, writes candidates to a tmp file, creates an
`import_batches` row in `pending_qualification`, and returns the batch id, candidate path,
expected result path, qualification prompt path, plus `icp_configured` / current `icp_definition`.

**Step 2 — Qualify (you, against the user's ICP).** The ICP is user-owned, lives in the
`icp_definition` setting (DB, NOT a file), and must come from the user — never hardcode one.
- If `icp_configured` is false: interview the user (roles/seniority, industries, company
  size/stage, locations, hard exclusions). Save via stdin:
  ```bash
  node scripts/settings.mjs set icp_definition --stdin <<'ICP'
  <agreed ICP text>
  ICP
  ```
- If true: show it in plain language, ask use-as-is or tweak.

Read the candidate file + the contract at `config/qualification-prompt.md`. Judge each
candidate against the ICP. For >~25 candidates, chunk and delegate to sub-agents using a
**cheap/fast model** (e.g. `model: "haiku"` in Claude Code) — this is bounded classification,
not deep reasoning. Each sub-agent returns `[{hashed_url, suitable, reasoning}]` for EVERY lead,
preserving `hashed_url`, with `reasoning` citing the actual ICP criterion. Keep orchestration,
the ICP interview, and the final report on the main model. Concatenate results to the expected
result file.

**Step 3 — Commit.**

```bash
node scripts/import.mjs commit --batch <id> --results <result-file>
```

Round-robin assigns `owner_account` across active accounts, inserts suitable leads as
`not_connected`, returns `suitable/unsuitable/assigned/skippedExisting/skippedMissing`. Then
report transparently: how many kept vs filtered, with a few sample reasons from each side.

Other: `import.mjs list [--state ...]`, `show --batch <id>`, `abort --batch <id>`.

## Phase B — Network maintenance (scheduled)

Not a single daily batch — the scheduler does small, resumable units across each account's
active window (`active_start`–`active_end`, local time). On each wake-up, per active account
in-window:
1. **Invites** — send ONE invite if daily quota (`daily_invite_limit`) not reached AND
   `min_invite_interval_minutes` elapsed since last invite.
2. **Pending checks** — process up to `pending_batch_size` due pending leads (status check,
   withdraw if pending past `max_pending_days`). Independent of invites, not interval-throttled.

Each op is persisted immediately; an interruption loses at most one in-flight op and the next
wake-up continues from DB state — no batch to resume. Daily quota is recomputed from `runs`
against the local calendar day.

Manual one-offs (testing only):
```bash
node scripts/network-invite.mjs --account <name> --limit 1
node scripts/network-pending.mjs --account <name> --limit 1
node scripts/network-run.mjs --account <name>
```

Invite result handling: success → `pending`; `alreadyPending` → `pending`; `alreadyConnected`
→ `connected`; account-level limit (`limitExceeded`) → stay `not_connected` and back off;
`requestNotAllowed` streak → weekly limit, back off; isolated → counts against lead, `exhausted`
after 2; else → `error`. cli exit 4 (account) or 6 (rate limit) aborts the whole run.

Pending + retry: `connected` → terminal success; declined/expired or withdrawn-stale → failed
attempt → `resolveFailedAttempt`: if distinct-account attempts < `max_connect_attempts` and an
untried active account exists, reassign to least-loaded and reset to `not_connected`; else
`exhausted`.

## Status questions

```bash
node scripts/status.mjs [--account <a>] [--since 7d] --json   # paused, limits, sent_today, status counts, errors
node scripts/lead.mjs list [--account <a>] [--status pending] [--list "<name>"] [--limit N]
node scripts/lead.mjs show <hashed-url|public-url|"Full Name">   # lead + last 25 runs
node scripts/schema.mjs --examples --json                       # refresh schema
node scripts/query.mjs --sql "SELECT ... FROM leads WHERE ..." --json   # read-only, SELECT only
```

Schema: `accounts(name PK, cli_account, paused, daily_invite_limit, min_invite_interval_minutes,
active_start, active_end, max_pending_days, pending_batch_size, ...)`,
`leads(hashed_url PK, public_url, full_name, position, location, list_name, reasoning,
owner_account FK, status[not_connected|pending|connected|exhausted|error], sent_at, ...)`,
`runs(id PK, lead_hashed_url FK, account, action[invite|check_status|withdraw], success, ...)`,
`import_batches(...)`, `import_state(id=1, last_assigned_account)`, `settings(key PK, value)`.
All timestamps UTC.

## Account & scheduler management

```bash
node scripts/account.mjs add --name <a> --cli-account "<cli name>" [--daily-invite-limit 35] \
  [--min-invite-interval 15] [--active-start 09:00 --active-end 18:00] [--max-pending-days 10]
node scripts/account.mjs update --name <a> --daily-invite-limit 25   # or --min-invite-interval / --active-*
node scripts/account.mjs pause|resume --name <a>
node scripts/account.mjs rename --name <a> --new-name <b>
node scripts/account.mjs remove --name <a> [--force]   # --force orphans leads

node scripts/schedule.mjs detect|status|uninstall
node scripts/schedule.mjs install [--interval-minutes 5]   # interval is internal; default is fine
node scripts/settings.mjs list|get <key>|set max_connect_attempts 1|N|all
```

Frame controls to the user as plain behavior ("invites 9am–6pm, one every 15 min, up to 35/day")
— never in terms of the scheduler's wake-up frequency.

## Pitfalls

- Two accounts with the same `cli_account` mapping = undefined behavior; reject it.
- `nv` (hashed URL) vs `st` (public URL) → same person from both = two rows. Mention if mixed.
- `error` status is terminal until `lead.mjs reset <hashed-url>`; the pipeline never auto-retries errors.
- `connected` on invite only means already-1st-degree; real new connections surface via pending checks.
- Daily quota resets at LOCAL midnight, not UTC.
- `schedule.mjs install` before any account = harmless no-op. Order: doctor → add accounts → install.
- Idempotent: db init, doctor, schema, status, lead show/list, query, schedule status. `prepare`
  makes a new batch each call; `commit` refuses to run twice on a batch.
