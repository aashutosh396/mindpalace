---
name: plugin-authoring
description: "Use when creating, modifying, validating, or debugging a Claude Code plugin — triggers on .claude-plugin/, plugin.json, marketplace.json, commands/, agents/, skills/, hooks/, scaffolding a plugin, adding a slash command/skill/agent/hook, or 'plugin not loading'."
version: 1.0.0
license: MIT
tags: [claude-code, plugin, plugin-json, marketplace, slash-commands, skills, hooks, agents, scaffolding, validation]
source: https://github.com/ivan-magda/claude-code-plugin-template/tree/main/plugins/plugin-development/skills/plugin-authoring
derived_from: awesomeclaude
---

# Plugin Authoring

Canonical guide for building Claude Code plugins. Default to read-only: diagnose
the repo layout, then propose vetted commands or PR-style diffs rather than
writing files directly. Ask before edits.

Official best-practices reference:
https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

## When to use

Activate whenever context includes any of: `.claude-plugin/`, `plugin.json`,
`marketplace.json`, `commands/`, `agents/`, `skills/`, or `hooks/` — or when the
user wants to scaffold a plugin, add a component, validate, or troubleshoot one
that won't load.

## Flow

1. **Diagnose** current repo layout (read-only).
2. **Propose** the minimal safe action (scaffold, validate, or review).
3. **Execute** via `/plugin-development:...` commands once the user agrees.
4. **Escalate** to the `plugin-reviewer` agent for deep audits.

## Plugin structure rules (the part everyone gets wrong)

- `.claude-plugin/plugin.json` is **required** and is the ONLY thing inside
  `.claude-plugin/`.
- Component dirs (`commands/`, `agents/`, `skills/`, `hooks/`) live at the
  **plugin root**, NOT inside `.claude-plugin/`.
- These standard directories are **auto-discovered**. Do NOT add
  `"commands": "./commands/"` (or agents/skills/hooks) fields to plugin.json —
  declaring standard paths breaks discovery.
- Hooks must reference scripts via `${CLAUDE_PLUGIN_ROOT}/scripts/foo.sh`, never
  relative paths like `./scripts/foo.sh` (works in dev, breaks on install).
- All hook scripts must be `chmod +x` (otherwise they silently fail).

## Component checklist

```
□ .claude-plugin/plugin.json exists (required: name, version, keywords)
□ Component dirs at plugin root (not inside .claude-plugin/)
□ No standard-dir fields in plugin.json (auto-discovered)
□ Commands use kebab-case naming
□ Hooks use ${CLAUDE_PLUGIN_ROOT}; scripts are chmod +x
□ Skills have valid frontmatter (see below)
```

## Skill frontmatter requirements

- `name` (required): lowercase letters, numbers, hyphens only; max 64 chars;
  must match the directory name; no reserved words `anthropic`/`claude`; no XML
  tags.
- `description` (required): include BOTH what the skill does AND when to use it;
  max 1024 chars; no XML tags. This string drives auto-detection.
- `model` (optional): e.g. `model: claude-sonnet-4-6`; defaults to conversation
  model.
- `allowed-tools` (optional): comma-separated; tools listed skip permission
  prompts when the skill is active. Omit to leave tools unrestricted.
- Keep SKILL.md under ~500 lines; push detail into sibling files
  (reference.md, examples.md, scripts/).

## Commands

- Scaffold: `/plugin-development:init <name>`
- Add components: `/plugin-development:add-command|add-skill|add-agent|add-hook`
- Validate: `/plugin-development:validate` (schema + structure; catches ~90% of
  issues before you start debugging)
- Test locally: `/plugin-development:test-local` (dev marketplace)

## Common workflows

**New plugin**: `init <name>` → edit `.claude-plugin/plugin.json` → add
components → `validate` → `test-local`.

**Add a slash command**: `add-command <name> <desc>` → edit `commands/<name>.md`
→ add frontmatter (`description`, `argument-hint`) → `/plugin install`, then
run `/<name>`.

**Add a skill**: `add-skill <name> <when-to-use>` → edit `skills/<name>/SKILL.md`
with the frontmatter rules above.

## Troubleshooting

- **Plugin not loading** → check plugin.json; remove any standard-dir fields;
  paths relative to plugin root.
- **Commands not showing** → confirm `commands/` exists at plugin root with
  `.md` files; do NOT add a `commands` field.
- **Hooks not running** → scripts `chmod +x`; use `${CLAUDE_PLUGIN_ROOT}`.
- **Skill not triggering** → `name` matches dir, lowercase/numbers/hyphens, ≤64
  chars; `description` covers what + when, ≤1024 chars; no XML tags in either.

## Why validation matters

| Skip            | Failure mode                          |
|-----------------|---------------------------------------|
| Validate manifest        | Plugin won't load, no error  |
| chmod +x scripts         | Hooks silently fail          |
| ${CLAUDE_PLUGIN_ROOT}    | Works in dev, breaks on install |
| Standard-dir rules       | Components not discovered     |

All of these cause **silent** failures. When in doubt, validate first.

## Notes

- Prefer templates and scripts over freeform generation for deterministic tasks.
- If writes are needed, propose a command or a PR-style diff first.
- Source repo ships reference files alongside the original SKILL.md:
  `schemas/{plugin-manifest,hooks-schema,marketplace-schema}.md`, `templates/`,
  `examples/`, `best-practices/common-mistakes.md` — fetch from the source URL if
  deeper schema detail is needed.
