# Configuration

Everything about *you* lives in the **data home** (default `~/.mindpalace`, override with
`MINDPALACE_HOME`). The repo (engine) holds none of it.

```
~/.mindpalace/
├── config.json   # gateway, admins, webhooks, heartbeat_minutes, bots
├── secrets/      # tokens (chmod 600, never in git)
├── identity/     # USER.md (you) + AGENT.md (its soul)
├── memory/       # MEMORY.md + sessions.db (FTS recall)
├── vault/        # projects/ infra/ accounts/ runbooks/ docs/ notes/ LOG.md
├── skills/       # derived user skills
└── state/        # history, daemon pid
```

- **Admins** (Discord access): `mindpalace admins` / `add-admin <id>` / `remove-admin <id>`, or
  `!add-admin @user` in the home channel. First messager auto-bootstraps as admin.
- **Webhooks:** `mindpalace add-webhook <name> <url>` (used to post updates, incl. from cron).
- **Heartbeat:** `mindpalace heartbeat <minutes>` (0 = off; default 30) — the autonomous self-tick.
