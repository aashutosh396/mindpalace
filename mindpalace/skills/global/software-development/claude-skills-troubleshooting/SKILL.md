---
name: Claude Skills Troubleshooting
description: Use when a Claude Code plugin is installed but not showing in skills, a skill won't activate, or enabledPlugins/settings.json seems off — diagnoses and fixes plugin installation, enablement, and marketplace-cache issues.
tags: [claude-code, plugins, skills, enabledPlugins, settings-json, marketplace, troubleshooting, plugin-not-working]
source: daymade/claude-code-skills
derived_from: claude-skills-troubleshooting
---

# Claude Skills Troubleshooting

Systematic debugging for Claude Code plugin/skill installation, enablement, and activation.

## Quick diagnosis
`python3 scripts/diagnose_plugins.py` — checks installed-vs-enabled mismatch, missing enabledPlugins entries, stale marketplace cache, invalid configs.

## Common issues

**1. Installed but not in available skills**
Symptoms: `/plugin` shows installed, skill missing from list, metadata in `installed_plugins.json`.
Root cause: known bug ([#17832](https://github.com/anthropics/claude-code/issues/17832)) — added to `installed_plugins.json` but NOT to `enabledPlugins` in `settings.json`.
Diagnose: `grep` plugin name in both files.
Fix: `claude plugin enable plugin-name@marketplace-name`, OR add `"plugin-name@marketplace-name": true` to `enabledPlugins` in settings.json.

**2. Plugin state architecture**
| File | Purpose |
|---|---|
| `~/.claude/plugins/installed_plugins.json` | registry of ALL plugins |
| `settings.json → enabledPlugins` | which are ACTIVE |
| `~/.claude/plugins/known_marketplaces.json` | marketplace sources |
| `~/.claude/plugins/cache/` | actual plugin files |
A plugin is active ONLY when registered in installed_plugins.json AND listed `true` in enabledPlugins.

**3. Stale marketplace cache**
Symptoms: GitHub has latest, install gets old version, new plugins invisible.
Fix: `claude plugin marketplace update marketplace-name`, or `rm -rf ~/.claude/plugins/cache/marketplace-name` then update.

**4. Plugin not found in marketplace** (by likelihood)
1. Local changes not pushed — `git status && git push && claude plugin marketplace update <name>`.
2. marketplace.json error — `python3 -m json.tool .claude-plugin/marketplace.json`.
3. Skill dir missing — `ls -la skill-name/SKILL.md`.

## Diagnostic command reference
`claude plugin marketplace list|update {name}`; `claude plugin install|enable|disable|uninstall {plugin}@{marketplace}`; `cat installed_plugins.json | jq '.plugins | keys'`; `cat settings.json | jq '.enabledPlugins'`.
Batch-enable all disabled from a marketplace: `python3 scripts/enable_all_plugins.py marketplace-name`.

## Skills vs commands
- **Skills** (`skills/`): auto-activated by description matching.
- **Commands** (`commands/`): explicitly invoked via `/command-name`, appear in the Skill tool list, need a command file. To make a skill explicitly invocable, add a corresponding command file.

**Quick fix for most issues**: commit → push → `claude plugin marketplace update <name>` → retry install.
