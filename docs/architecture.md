# Architecture

```
mindpalace/                        # the engine (this repo) — zero personal data
├── cli.py · config.py             # entry + path/config resolver
├── setup.py · identity.py         # onboarding + soul
├── skills.py · bots.py            # skill + bot registries
├── core/    brain · daemon · jobs · heartbeat · service · notify
├── agents/  analyst (+ base, registry)
├── gateways/ terminal · discord
├── memory/  store · session_store (SQLite FTS)
├── plugins/ base · loader · contrib
└── skills/global/*.md
```

## Core ↔ data separation
The engine is stateless about *you*. Your instance lives in `~/.mindpalace` (`MINDPALACE_HOME`).
`git pull` the engine → your data is untouched. Point a fresh data home at the same engine → a
brand-new agent that learns from zero.

## Flow
Message → gateway → `core.brain` runs Claude (your Max plan) with full context (identity, memory,
recall, skills, vault) → streams steps → replies. In parallel, the **Analyst** files + skillifies.
Long work is queued as a **job** (`core.jobs`) and reported back. A **heartbeat** drives the
Analyst's autonomous review on a timer. The **daemon** (`core.daemon`) hosts the bot + watchers.
