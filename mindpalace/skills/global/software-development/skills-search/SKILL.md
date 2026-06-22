---
name: Claude Code Skills Search (CCPM registry)
description: Use when the user wants to search, discover, install, update, or manage Claude Code skills/plugins from the CCPM registry — runs ccpm commands directly rather than asking the user to copy-paste.
tags: [skills, search, install, ccpm, registry, discover, manage, plugins, claude-code]
source: daymade/claude-code-skills
derived_from: skills-search
---

Search, discover, install, and manage Claude Code skills from the CCPM registry. **Execute ccpm commands directly via Bash — never show a command and ask the user to copy-paste.**

## Auto-bootstrap (run first)
```bash
which ccpm || npx @daymade/ccpm setup
```
If `ccpm` isn't globally installed, use `npx @daymade/ccpm` as a drop-in for all commands.

## Intent mapping
| User intent | Action |
|-------------|--------|
| "find skills for X" / "search X" | `ccpm search <query>` |
| "popular skills" | `ccpm popular` |
| "what's new" | `ccpm recent` |
| "install X" | `ccpm install <name>` |
| "what does X do" | `ccpm info <name>` |
| "list my skills" | `ccpm list` |
| "remove X" | `ccpm uninstall <name>` |
| "update X / all" | `ccpm update [name] [--all]` |
| "I need help with PDF/Excel/…" | `ccpm search <topic>` then offer best match |

## Command reference
```bash
ccpm search <query> [--limit n] [--tags t1,t2] [--author name] [--smart]
ccpm popular [--limit n]
ccpm recent [--limit n]
ccpm install <name>           # user-level default
ccpm install <name> --project # project-level only
ccpm install <name> --force   # force reinstall
ccpm list | info <name> | update [name] | update --all | uninstall <name>
```
Supports namespaced skills: `ccpm install @org/skill-name`.

## Execution rules
Execute directly; summarize results clearly; suggest next steps (after search → offer install; after install → remind to restart Claude Code); handle errors gracefully (fall back to `npx`; say so if registry unreachable).

## Post-install reminder
Always tell the user: "Skill installed. Restart Claude Code (or start a new conversation) for it to become available."

## Troubleshooting
"ccpm: command not found" → `npx @daymade/ccpm` or `npm install -g @daymade/ccpm`. Not available after install → restart (skills load at startup). Permission errors → check write perms to `~/.claude/skills/` or use `--project`.
