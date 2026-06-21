---
name: agnix-config-linter
description: "Use when asked to lint, validate, or fix agent config files — CLAUDE.md, SKILL.md, AGENTS.md, hooks, MCP configs, .cursor rules, or copilot-instructions — e.g. 'lint my agent configs', 'validate my skills', 'check CLAUDE.md', 'why doesn't my skill trigger', 'validate hooks', 'lint MCP'."
version: 1.0.0
license: MIT
tags: [agnix, linter, agent-config, skill-md, claude-md, mcp, hooks, cursor, copilot, validation]
source: https://github.com/avifenesh/agnix
derived_from: awesomeclaude
prerequisites:
  commands: [agnix]
---

# agnix config linter

`agnix` validates agent configuration files against 425 rules sourced from
official specs and real breakage patterns. Catches the silent failures where a
skill never triggers, a hook is ignored, or a config works in one tool but
breaks in another. Includes auto-fix.

Covers Claude Code, Codex CLI, OpenCode, Cursor, GitHub Copilot, and more.

## When to use

- "Lint my agent configs" / "validate my skills" / "check my CLAUDE.md"
- "Validate hooks" / "lint MCP configs"
- "My skill isn't triggering" — likely a malformed `name`/`description`
- "Fix agent configuration issues"
- Before committing changes to any agent config file (CI gate)

## Files it validates

| Type   | Examples |
|--------|----------|
| Skills | `SKILL.md` |
| Memory | `CLAUDE.md`, `AGENTS.md` |
| Hooks  | `.claude/settings.json` |
| MCP    | `*.mcp.json` |
| Cursor | `.cursor/rules/*.mdc` |
| Copilot| `.github/copilot-instructions.md` |

## How to run

1. Check install: `agnix --version`.
   If missing, install one of:
   - `npm install -g agnix`  (recommended, all platforms)
   - `brew tap agent-sh/agnix && brew install agnix`
   - `cargo install agnix-cli`

2. Validate: `agnix .`

3. Auto-fix if requested: `agnix --fix .`
   (`--fix-safe` for only safe fixes, `--fix-unsafe` to include risky ones.)

4. Re-validate to confirm: `agnix .`

## CLI reference

| Command | Description |
|---------|-------------|
| `agnix .` | Validate current project |
| `agnix --fix .` | Auto-fix issues |
| `agnix --strict .` | Treat warnings as errors |
| `agnix --target claude-code .` | Only Claude Code rules |
| `agnix --target cursor .` | Only Cursor rules |
| `agnix --watch .` | Watch mode |
| `agnix --format json .` | JSON output (for CI parsing) |

## Output format

```
CLAUDE.md:15:1 warning: Generic instruction 'Be helpful' [fixable]
  help: Remove generic instructions. Claude already knows this.

skills/review/SKILL.md:3:1 error: Invalid name [fixable]
  help: Use lowercase letters and hyphens only

Found 1 error, 1 warning (2 fixable)
```

## Common issues and fixes

| Issue | Fix |
|-------|-----|
| Invalid skill name | Use lowercase with hyphens: `my-skill` |
| Generic instructions | Remove "be helpful", "be accurate" — the model already knows |
| Missing trigger phrase | Add a "Use when…" line to the `description` (drives auto-detection) |
| Directory/name mismatch | Rename the directory to match the `name:` field |

## Gotchas

- A wrong/missing trigger phrase makes a skill effectively invisible — agnix
  flags this directly, which is the most common reason "my skill doesn't fire."
- `--fix-unsafe` can change semantics; review the diff before committing.
- Use `--strict` in CI so warnings fail the build.

## Links

- Rules reference: https://agent-sh.github.io/agnix/docs/rules/
- Playground (paste a config, see diagnostics): https://agent-sh.github.io/agnix/playground
