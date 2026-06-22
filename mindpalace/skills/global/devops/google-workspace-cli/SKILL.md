---
name: Google Workspace CLI (gws)
description: Use for Google Workspace admin via the gws CLI — install/auth, automating Gmail/Drive/Sheets/Calendar/Docs/Tasks, and running security audits.
tags: [google-workspace, gws, gmail, drive, sheets, calendar, cli, automation, oauth, security-audit]
source: alirezarezvani/claude-skills
derived_from: engineering-team/google-workspace-cli
---

# Google Workspace CLI (gws)

Automate Google Workspace with the open-source `gws` CLI (github.com/googleworkspace/cli, Apache-2.0). It builds its command surface dynamically from Google's Discovery Service.

> **Verify before scripting:** `gws` is pre-v1.0 and generates commands at runtime. Always confirm exact surface with `gws --help`, `gws <service> --help`, or `gws schema <service>.<resource>.<method>` before automating.

## Command shapes
- **Helper commands** (`+`-prefixed): single optimized calls, e.g. `gws gmail +send --to ... --subject ... --body ...`, `gws drive +upload`, `gws calendar +agenda`, `gws workflow +standup-report`.
- **Discovery commands** (`gws <service> <resource> <method>`): take `--params` (query/path params, JSON) and `--json` (request body). Inspect schema first: `gws schema gmail.users.messages.list`.

## Install & auth
Install via npm (`npm install -g @googleworkspace/cli`, Node 18+), Homebrew, Cargo, or prebuilt binaries. Auth: `gws auth setup` then `gws auth login -s drive,gmail,sheets` (request only needed scopes). Headless/CI: `gws auth export --unmasked > credentials.json` then `export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=...`. Key env vars: `GOOGLE_WORKSPACE_CLI_CLIENT_ID/CLIENT_SECRET/CREDENTIALS_FILE/TOKEN/CONFIG_DIR`.

## Workflows
- **Gmail** — send/reply/forward via `+` helpers; search via `gws gmail users messages list --params '{"userId":"me","q":"from:x after:2025/01/01"}'`; bulk ops with `--dry-run` first and `--page-all` to paginate (NDJSON, one line per page).
- **Drive & Sheets** — `gws drive files list`, `gws drive +upload`, `gws sheets spreadsheets create --json '{"properties":{"title":"..."}}'`; sharing via `gws drive permissions create` (inspect `gws schema drive.permissions.create` first).
- **Calendar** — events via `gws calendar +insert`/`events list`; free/busy via `gws calendar freebusy query`.

## Security audit
Checks: Drive external sharing (exfiltration), Gmail auto-forwarding (exfiltration), DMARC/SPF/DKIM (spoofing), Calendar default visibility (leak), OAuth third-party grants (unauthorized access), super-admin count (privilege escalation), 2-Step enforcement (account takeover). Review FAIL findings and follow the emitted remediation commands (verify each against `gws --help`).

## Best practices
Minimal OAuth scopes; store tokens in system keyring not plain text; rotate service-account keys every 90 days; audit OAuth grants quarterly; `--dry-run` before destructive bulk ops; request only needed `fields` to cut payload; `--page-all` only when you need complete datasets.

## Limitations
OAuth tokens expire after 1h (re-auth for long scripts); per-user/service rate limits (429 on bulk); scopes vary by service; pre-v1.0 breaking changes possible; Google Cloud project required; Admin API checks need Workspace Admin role.
