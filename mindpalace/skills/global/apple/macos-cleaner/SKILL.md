---
name: macOS Disk Cleanup (safety-first)
description: Use when a Mac is low on disk space or the user wants to understand and reclaim storage — analyzes usage, categorizes findings by risk, explains impact-if-deleted, and requires explicit confirmation (never auto-deletes).
tags: [macos, disk-space, cleanup, cache, docker, mole, storage, safety, analysis]
source: daymade/claude-code-skills
derived_from: macos-cleaner
---

Analyze macOS disk usage and recommend cleanup. **Safety-first: analyze thoroughly, present clearly, require explicit confirmation before any deletion. The user executes cleanup — never auto-execute.**

## Core principles
1. Never run dangerous commands (`rm -rf`, `mo clean`) without confirmation.
2. Precision deletion only — by exact object ID/name, never batch prune.
3. List every object (each image/volume/container), not "12 GB of unused images".
4. **Value over vanity** — goal is identifying *truly useless* vs *valuable cache*, not maximizing the cleaned number.
5. Network awareness — slow internet makes re-downloading caches costly; a cache that saves 30min download is worth keeping.
6. Every recommendation includes "what happens if deleted".
7. Conservative default — when in doubt, don't delete.

**Absolute prohibitions:** NEVER `docker image/volume/system/container prune` (exception: `docker builder prune` is safe). Never `rm -rf` user dirs or `mo clean` without `--dry-run` first.

## Workflow
1. **Quick diagnosis with Mole.** Verify/upgrade: `which mo && mo --version`; install `brew install tw93/tap/mole`. Mole needs a TTY — run via tmux: `tmux new-session -d -s mole -x 120 -y 40; tmux send-keys -t mole 'mo analyze' Enter`. Use `mo analyze` (interactive tree, read-only) as PRIMARY; `mo clean --dry-run` (preview, no deletion) as secondary. Home scans take 5-10 min — be patient, report progress.
2. **Deep analysis categories:** (1) caches `~/Library/Caches`, logs (🟢 generally safe; preserve running-browser/IDE/package-manager caches); (2) app remnants — cross-ref `/Applications` vs `~/Library/Application Support` for orphans (🟡); (3) large files & duplicates (🟡 user judgment); (4) dev env — Docker/Homebrew/npm/pip/git (🟢 brew/npm cleanup; 🔴 Docker volumes per-project confirm).
3. **Present findings** with classification + impact:

| Symbol | Meaning |
|--------|---------|
| 🟢 | Absolutely safe — no negative impact |
| 🟡 | Trade-off — useful cache, deletion has cost |
| 🔴 | Do not delete — valuable data / actively used |

Every item gets an "Impact If Deleted" column.
4. **Execute with confirmation** — provide the command for the user to run (don't auto-run); per-item or batch confirmation.
5. **Verify** with `df -h /` before/after, report space recovered + maintenance tips.

## What to KEEP (anti-patterns — don't delete to inflate numbers)
Xcode DerivedData (saves 10-30min rebuilds), npm `_cacache`, `~/.cache/uv`, Playwright browsers, iOS DeviceSupport, Docker stopped containers, `~/.cache/huggingface|modelscope` (model cache), JetBrains caches. The vanity trap: "Cleaned 50GB!" → user spends 2 hours redownloading.

## Actually safe to delete
Trash, Homebrew old versions, npm `_npx` (temp), orphaned app remnants, confirmed-abandoned Docker volumes.

## Docker handling
List + inspect every volume; identify which project each belongs to; ask per-project; delete specific volumes only after confirmation. Never prune-family.

## Sudo / SIP
System-wide caches (`/Library/Caches`, `/var/log`) need sudo — ask the user to run manually. Don't fight SIP "Operation not permitted" — those protections are intentional. Recommend a Time Machine backup before any cleanup >10GB.
