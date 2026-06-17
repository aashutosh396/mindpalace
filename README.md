<div align="center">

# 🧠 mindpalace

**A self-learning, always-on personal AI agent that runs on your Claude Max subscription.**

Ships generic — sharpens into *your* world with every conversation. Lives in your terminal
and on Discord at the same time. Remembers, learns your conventions, writes its own skills,
and runs real work in the background.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Runs on Claude Max](https://img.shields.io/badge/runs%20on-Claude%20Max-8A2BE2.svg)](https://claude.com/claude-code)

[Quick start](#-quick-start) · [Features](#-why-mindpalace) · [Docs](docs/) · [Contributing](CONTRIBUTING.md)

</div>

---

> One command. Talk to it like a person. It replies fast, runs real work in the background —
> backups, reminders, schedules, code, cron, deploys — files everything it learns into a
> structured knowledge vault, and gets more precise for *you* over time. No metered API: it
> runs on the **Claude Max** subscription you already have.

## ✨ Why mindpalace

- 🗣️ **Two interfaces, at once** — a Claude-Code-style **terminal** chat *and* an always-on
  **Discord** bot, sharing one brain, memory, and vault.
- 🧩 **Self-learning** — it writes durable facts to memory, and an **Analyst agent** turns
  first-time procedures into reusable **skills** automatically.
- 🗄️ **Knowledge vault** — every server, login, project, and decision is filed into a
  structured, resource-first vault (your **second brain**), not lost in chat.
- ⚡ **Async + alive** — long tasks run as background **jobs** and stream their steps live;
  the chat never blocks.
- 💓 **Proactive** — an autonomous **heartbeat** reviews your world on a timer and reports.
- 🤖 **Multi-bot** — spin up scoped Discord bots, each with its own persona + a real
  permission fence (read-only / full / custom tools).
- 🔌 **Extensible** — a clean `core / agents / gateways / plugins` architecture.
- 🔐 **Yours** — self-hosted, admin-locked, secrets stay on your machines. Core ↔ data fully
  separated, so updates never touch your private data.

## 🚀 Quick start

```bash
git clone https://github.com/aashutosh396/mindpalace
cd mindpalace
./install.sh            # add `discord` for the always-on bot:  ./install.sh discord
mindpalace              # first run: pick a gateway, create its identity, start talking
```

**Requirements:** Python 3.9+ · the [Claude CLI](https://claude.com/claude-code) logged in to a
Max plan · (Discord) a bot token with the *Message Content* intent.

## 🗣️ Terminal + Discord — both, at once

- **Terminal is always there:** `mindpalace` opens a polished shell chat (boxed input,
  live step streaming, markdown replies).
- **Discord runs as a background service** once configured — it never blocks your terminal.
  You're reachable from both at once; the first person to message the home channel becomes the
  first admin.

```bash
mindpalace gateway discord     # token + home channel
sudo mindpalace service install # background systemd/launchd service, survives reboot
```

## 🧠 How it learns (the compounding loop)

1. You ask it to do something. It does it — streaming each step live.
2. The **Analyst agent** reflects in the background: files facts into the **vault**
   (`infra/`, `accounts/`, `projects/`, `runbooks/`, `LOG.md`) and **skillifies** any reusable
   procedure into `skills/`.
3. Next time, it reuses the skill + recalls relevant history (SQLite FTS). It gets sharper.

Global skills (shipped, read-only references) → the agent **derives** private user skills
tailored to your exact setup. Your world compounds into a superb, personal assistant.

## 🤖 Scoped bots

```
mindpalace add-bot
> What should this bot do?  "summarize deploy-log errors, nothing else"
  …Claude drafts a scoped system prompt → you pick a permission tier → paste a token
```
`@mention` it anywhere. A `readonly` bot literally *cannot* run commands — the fence is the
Claude CLI tool allowlist, not just a polite prompt.

## 🖥️ Run on a server (headless, always-on)

```bash
mindpalace setup
sudo mindpalace service install   # systemd (Linux) / launchd (macOS), reboot-persistent
# close SSH — work entirely from Discord.  logs: journalctl -u mindpalace -f
```

## ⚙️ Commands

Everything is the single `mindpalace` command. Args in `<>` are required, `[]` optional;
settings persist to `~/.mindpalace/config.json` and most apply on the next daemon **restart**.

| Command | What it does |
|---|---|
| `mindpalace` | First run → setup; afterwards opens the terminal chat (and auto-starts the Discord daemon if configured) |
| `mindpalace setup` | Re-run onboarding (gateway choice + identity) |
| `mindpalace status` *(`-s`)* | Show data home, identity, Discord/daemon state, heartbeat, concurrency |
| `mindpalace version` *(`-v`)* | Print the version |
| `mindpalace help` *(`-h`)* | Show command help |
| **Interface** | |
| `mindpalace gateway <terminal\|discord>` | Configure/switch the interface (`mindpalace discord` / `mindpalace terminal` are shortcuts) |
| **Daemon / service** | |
| `mindpalace start` | Start the background daemon (detached, no terminal) |
| `mindpalace stop` | Stop the background daemon |
| `mindpalace restart` | Restart the daemon (applies config changes) |
| `mindpalace daemon` | Run the daemon in the **foreground** (for systemd/launchd) |
| `mindpalace service <install\|uninstall\|status>` | Install/remove a reboot-persistent OS service |
| `mindpalace halt` *(`stop-task`, `abort`)* | 🛑 Emergency-stop running work; daemon stays up |
| **Tuning** *(restart to apply)* | |
| `mindpalace concurrency [<n>]` | Get/set max parallel Claude agents (**default 8**) |
| `mindpalace model [sonnet\|opus\|haiku\|<id>\|default]` | Get/set the main reasoning model |
| `mindpalace heartbeat [<minutes>]` | Get/set the autonomous heartbeat interval (`0` = off) |
| `mindpalace voice [lean\|full]` | Switch reply style — **lean** (brief, to-the-point) vs **full** (chatty); applies on the next message, no restart |
| `mindpalace usage [N]` | Session-continuity + token/cache stats for the last N turns (the soak dashboard) |
| `mindpalace update-interval [<minutes>]` | Get/set the git auto-update check interval (`0` = off) |
| `mindpalace workspace [<path>]` | Get/set the permanent folder where project code is created |
| **Updates** | |
| `mindpalace update` | Pull the latest from GitHub now + restart |
| **Bots & access** | |
| `mindpalace add-bot` | Create a scoped Discord bot (drafts its system prompt + permission fence) |
| `mindpalace bots` | List configured bots |
| `mindpalace admins` | List admins (Discord access) |
| `mindpalace add-admin <discord-id>` | Grant Discord access |
| `mindpalace remove-admin <discord-id>` | Revoke Discord access |
| `mindpalace add-webhook <name> <url>` | Save a notify webhook |
| `mindpalace notify "message"` | Post a message to the home channel |

### In Discord (home channel, admins only)

Type these as messages prefixed with `!`; anything else goes straight to the brain.

| Command | What it does |
|---|---|
| `!help` | List the in-chat commands |
| `!stop` | 🛑 Emergency-stop the current running task (bot stays online) |
| `!update` | Pull the latest from GitHub + reload live |
| `!bots` | List running bots |
| `!admins` · `!add-admin @user` · `!remove-admin @user` | Manage who can talk to the bot |
| `!add-webhook <name> <url>` | Add a notify webhook |
| `!model [sonnet\|opus\|haiku]` | Show/switch the model |
| `!heartbeat [scan-now \| <minutes>]` | Run a health check now, or set the interval (`0` = off) |
| `!curate [now \| pause \| resume]` | Tidy the skill library now, or pause/resume auto-curation; `!curate` shows status |
| `!voice [lean \| full]` | Switch reply style — brief vs chatty (live from your next message) |

> Full reference: [`docs/commands.md`](docs/commands.md).

## 🧱 Architecture

```
mindpalace/
├── cli.py · config.py · setup.py · identity.py · skills.py · bots.py   # spine
├── core/      brain · daemon · jobs · heartbeat · service · notify     # engine
├── agents/    analyst (+ base, registry)                              # cognitive agents
├── gateways/  terminal · discord                                       # interfaces
├── memory/    store · session_store (FTS)                              # recall
├── plugins/   base · loader · contrib                                  # extensibility
└── skills/global/*.md                                                  # shipped skills
```
Your private instance lives **outside** the repo in `~/.mindpalace/` (config, secrets,
identity, memory, vault, skills, state). Update the engine → your data is untouched.

## 📚 Documentation

Full docs in [`docs/`](docs/):
[Getting Started](docs/getting-started.md) ·
[Configuration](docs/configuration.md) ·
[Gateways](docs/gateways.md) ·
[Agents & Skills](docs/agents-and-skills.md) ·
[Plugins](docs/plugins.md) ·
[Commands Reference](docs/commands.md) ·
[Architecture](docs/architecture.md)

## 🤝 Contributing

mindpalace is open source and built to grow with its community. Issues, ideas, skills, and PRs
are all welcome — start with [CONTRIBUTING.md](CONTRIBUTING.md).
**If it's useful, please ⭐ star the repo** — it genuinely helps others find it.

## 📄 License

MIT — see [LICENSE](LICENSE).

<div align="center">
<sub>Built on always-on agent patterns (self-learning soul + self-learning memory), packaged so
anyone can run their own. Keywords: AI agent · personal assistant · Claude · Claude Code ·
Claude Max · autonomous agent · self-learning · Discord bot · second brain · self-hosted.</sub>
</div>
