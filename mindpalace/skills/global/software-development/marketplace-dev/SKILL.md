---
name: Claude Code Marketplace Dev
description: Use when turning a Claude Code skills repo into an installable plugin marketplace — generate spec-conforming .claude-plugin/marketplace.json, validate with `claude plugin validate`, test real install, and PR upstream, encoding hard-won schema anti-patterns.
tags: [claude-code, marketplace, plugin, marketplace-json, plugin-validate, skills, install-test, distribution]
source: daymade/claude-code-skills
derived_from: marketplace-dev
---

# Marketplace Dev

Convert a skills repo into an official plugin marketplace so users install via `claude plugin marketplace add` with auto-updates. Input: repo with skill dirs containing SKILL.md. Output: validated, install-tested, PR-ready `.claude-plugin/marketplace.json`.

## Phase 0 — Evidence intake
Read current marketplace.json, repo rules (CLAUDE.md/README/changelog), official docs for path semantics. If refining from failures, mine session history (`~/.claude/projects/<escaped-cwd>/*.jsonl` + `*/subagents/*.jsonl`) with grep for `Unrecognized key|Plugin not found|No manifest found|Duplicate plugin`. Encode lessons as evidence-backed rules, not memory guesses.

## Phase 1 — Analyze repo
`find <repo>/skills -name SKILL.md`. Per skill extract `name` + `description` (ORIGINAL text, never rewrite/translate). Read VERSION (→ `metadata.version`), README, LICENSE, git remotes (upstream vs fork). Group into freeform categories (confirm if ambiguous). Choose plugin boundaries: single-skill plugin (independent install/update/rollback) vs suite plugin (shared namespace `/suite:skill`).

## Phase 2 — Create marketplace.json
**Non-obvious schema rules:**
1. `$schema` field is REJECTED by validate — omit it.
2. `metadata` has ONLY 3 valid fields: `description`, `version`, `pluginRoot`. (`metadata.homepage` does NOT exist — silently ignored.)
3. `metadata.version` = marketplace catalog version (matches VERSION file), NOT plugin versions.
4. Plugin entry `version` independent; new = `"1.0.0"`.
5. `strict: false` required when no `plugin.json` (entry IS the whole plugin def). BOTH strict:false AND a plugin.json with components = load failure.
6. `source` = installed plugin root. Single-skill: point `source` at the skill dir (`"./tunnel-doctor"`), OMIT `skills` (official pattern, 167/168 plugins). Suite: `source: "./<suite>"` + explicit `skills` array. Avoid `source: "./"` (installs full repo) and `skills: ["./"]` (rejected by 2.1.x path validator).
7. Reserved names that CANNOT be used: claude-code-marketplace, claude-code-plugins, claude-plugins-official, anthropic-marketplace, anthropic-plugins, agent-skills, knowledge-work-plugins, life-sciences.
8. `tags`/`keywords` don't affect discovery (Discover searches name+description+marketplaceName only); include keywords for future-proofing, don't over-invest.

Template:
```json
{ "name": "<kebab-case>", "owner": {"name": "<gh-user>"},
  "metadata": {"description": "...", "version": "<VERSION>"},
  "plugins": [{"name":"<skill>","description":"<EXACT SKILL.md text>","source":"./<skill>","strict":false,"version":"1.0.0","category":"<cat>","keywords":[]}] }
```
Description rules: use ORIGINAL SKILL.md frontmatter text (no translate/embellish; keep Chinese if source is Chinese).

## Maintaining existing
Adding a plugin: bump `metadata.version` (semver), update `metadata.description`, new plugin `version: "1.0.0"`, bump existing plugin `version` when its SKILL.md OR source/skills change (same version = update skipped), audit for invalid `metadata.homepage`.

## Phase 3 — Validate
`bash scripts/check_marketplace.sh [path]` runs: (1) JSON syntax, (2) `claude plugin validate .`, (3) source+skills resolution per entry, (4) reverse-sync WARN (disk SKILL.md not registered). Common: `Unrecognized key "$schema"` → remove; `Duplicate plugin name`; `Path contains ".."` → use `./`.
Install test: `claude plugin marketplace add .` → `install <plugin>@<market>` → `list | grep` → `update` (says latest) → cleanup. Cache footprint: inspect `installPath` from `installed_plugins.json` — single-skill cache = SKILL.md + own resources; if unrelated dirs appear, `source` too broad.

## Pre-flight checklist (before PR)
check_marketplace.sh must print `RESULT: PASSED`. Verify: metadata.version bumped, description covers categories, no homepage/`$schema`; per plugin: description EXACT, version correct, source at skill dir, single-skill omits skills, suite lists skills, strict:false, name kebab-case+unique.

## Phase 4 — PR
Pure incremental (don't modify existing files); squash commits (avoid binary bloat); add only marketplace.json + optional scripts/README. README: add marketplace install above existing instructions. PR body: what added, install commands, design decisions, validation evidence, test plan.

Optional bundled PostToolUse hooks validate marketplace.json on edit + warn on missing version bump. They're editor-time guardrails, NOT a replacement for check_marketplace.sh.
