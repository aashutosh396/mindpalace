# Getting Started

## Install
```bash
git clone https://github.com/aashutosh396/mindpalace
cd mindpalace
./install.sh            # add `discord` for the bot extra:  ./install.sh discord
```
Requirements: Python 3.9+, the [Claude CLI](https://claude.com/claude-code) logged in to a Max
plan, and (for Discord) a bot token with the **Message Content** intent.

## First run
```bash
mindpalace
```
It walks you through: pick a **gateway** (terminal or discord), confirm Claude auth, and create
the agent's **identity & soul** (a short interview → `USER.md` + `AGENT.md`).

## Talk to it
- **Terminal:** just type. `/help`, `/status`, `/exit`.
- **Discord:** message the home channel (you become the first admin); the bot reads every message
  there. In other channels, `@mention` it.

Ask it to do real work ("ssh into my VPS and check pm2", "back up the DB"). It streams its steps,
replies, and quietly files what it learned into your vault.
