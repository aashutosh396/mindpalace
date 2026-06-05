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
