---
name: cron-scheduling
description: "Use when scheduling recurring tasks or managing background services — crontab jobs, cron syntax, macOS launchd/launchctl services via lunchy-go, start/stop/restart services, recurring scripts."
version: 1.0.0
license: MIT
tags: [cron, scheduling, launchctl, launchd, automation, services, lunchy-go, recurring]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-cron
derived_from: awesomeclaude
---

# Cron & Service Scheduling

Schedule recurring commands with `crontab` and manage macOS launchd services
with `lunchy-go`.

## When to use
Setting up recurring jobs, running scripts on a schedule, starting/stopping/
restarting background services (redis, custom daemons).

## crontab (cross-platform)

```bash
crontab -l    # List jobs
crontab -e    # Edit jobs

# Syntax: MIN HOUR DOM MON DOW command
# 0 9 * * *        daily at 9am
# */5 * * * *      every 5 minutes
# 30 8 * * 1-5     weekdays at 8:30am
```

## lunchy-go (macOS launchctl wrapper)

```bash
lunchy-go ls [pattern]            # List services
lunchy-go start redis            # Start (pattern match ok)
lunchy-go stop redis             # Stop
lunchy-go restart redis          # Restart
lunchy-go status redis           # Status
```

## Guidelines
- Prefer lunchy-go for managing macOS launchd plists; crontab for simple jobs.
- Always use full absolute paths inside cron jobs.
- Redirect output to a log: `command >> /tmp/job.log 2>&1`.
- Test the command manually before scheduling it.
