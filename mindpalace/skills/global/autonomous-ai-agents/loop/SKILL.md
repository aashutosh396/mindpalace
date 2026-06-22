---
name: Autoresearch Loop (/ar:loop)
description: Use when running an autoresearch experiment continuously on a schedule (10m/1h/daily/weekly/monthly) — creates a recurring cron job that runs one experiment iteration per fire.
tags: [autoresearch, loop, cron, scheduler, recurring, autonomous, ar-loop, overnight-experiments]
source: alirezarezvani/claude-skills
derived_from: engineering/autoresearch-agent/skills/loop
---

# /ar:loop — Autonomous Experiment Loop

Start a recurring experiment loop at a user-selected interval using a cron scheduler.

## Steps
1. **Resolve experiment** — if none specified, list and let user pick.
2. **Select interval** — map to cron:
   | Interval | Cron | Shorthand |
   |---|---|---|
   | 10 min | `*/10 * * * *` | 10m |
   | 1 hour | `7 * * * *` | 1h |
   | Daily | `57 8 * * *` | daily |
   | Weekly | `57 8 * * 1` | weekly |
   | Monthly | `57 8 1 * *` | monthly |
3. **Create recurring job** with a prompt that does exactly ONE iteration: read config.cfg + program.md + results.tsv → checkout `autoresearch/{domain}/{name}` → review history → edit target with ONE change (strategy escalation by run count) → commit → `run_experiment.py --single` → read KEEP/DISCARD/CRASH. Job rules: one change per experiment; never modify evaluator; if 5 consecutive crashes, delete the cron job and alert; every 10 experiments update program.md Strategy.
4. **Store metadata** → `.autoresearch/{domain}/{name}/loop.json` (cron_id, interval, started, experiment).
5. **Confirm** — interval, cron ID, auto-expiry (3 days), how to check (`/ar:status`) and stop.

## Stopping (`/ar:loop stop {experiment}`)
Read loop.json for cron ID → delete the cron job → delete loop.json → confirm "{n} experiments completed."

## Limitations
3-day auto-expiry (re-run to restart; results persist) · one loop per experiment · concurrent experiments only on different git branches (default — each gets its own branch).
