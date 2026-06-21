---
name: skillcheck
description: "Use when asked to check skill, skillcheck, validate SKILL.md, lint a Claude Code skill, review a skill definition, or check a .claude-plugin/plugin.json manifest or MCP tools/list — validates skills against Anthropic guidelines and the agentskills spec (structure, naming, semantics, security)."
version: 1.0.0
license: MIT
tags: [skill, validation, lint, claude-code, agentskills, frontmatter, plugin-manifest, mcp, owasp]
source: https://github.com/olgasafonova/SkillCheck-Free
derived_from: awesomeclaude
prerequisites:
  commands: []
---

# SkillCheck (Free tier)

Validate a Claude Code skill's `SKILL.md` (or a `plugin.json` manifest / MCP `tools/list` JSON) against Anthropic guidelines and the agentskills.io spec. Read-only, no side effects, single pass.

## When to use

User says "check skill", "skillcheck", "validate SKILL.md", "lint this skill", "find issues in this skill", "check this plugin manifest", or "is this MCP server too big". Do NOT use for anti-slop detection, deep security scanning, token-budget analysis, WCAG, or enterprise checks — those are Pro-tier and out of scope here.

## How to check

1. Locate the target `SKILL.md` (or plugin.json / tools/list JSON).
2. Read the full content.
3. Apply each rule section below, in order.
4. Report: overall score (0-100), issue list, and strengths.

Stop after one pass. Idempotent — same input gives same result.

## 1. Frontmatter structure

Must start with YAML frontmatter between `---` markers.

Required fields:
- `name` — lowercase, hyphens only, 1-64 chars, pattern `^[a-z][a-z0-9-]*[a-z0-9]$`, no reserved/vague words (`helper`, `utils`, `tools`, `misc`, `manager`, `handler`).
- `description` — must have WHAT (action verb) + WHEN (trigger phrase), 1-1024 chars.

Security: frontmatter values must NOT contain `<` or `>` (prompt-injection risk — frontmatter is loaded into the system prompt). Critical. Markdown/XML in the body is fine.

Optional spec fields: `license`, `allowed-tools`, `compatibility`, `metadata`.
Claude Code extensions (do not flag if missing): `category`, `model`, `effort`, `maxTurns`, `disallowedTools`, `context`, `agent`, `hooks`, `user-invocable`, `disable-model-invocation`, `produces`, `consumes`.

`category` if present: lowercase/numbers/hyphens, same pattern as name. Common: development, productivity, data, automation, writing, security, devops, testing.

`allowed-tools`: space-separated or YAML list. Comma-separated is deprecated — flag it.

`produces`/`consumes`: comma-separated lowercase-hyphen types. Unknown type = Warning, not error. `consumes:` without `Read`/`Glob` in allowed-tools = Warning.

## 2. Directory structure

- File must be `SKILL.md` (case-sensitive).
- Parent directory name must exactly match the `name` field.
- Optional subdirs: `references/` (.md docs), `scripts/` (executable), `assets/`.
- No `README.md` inside the skill folder (Warning) — put README at repo root.
- Namespaced paths supported: `~/.claude/skills/{namespace}/{skill}/SKILL.md`.

## 3. Naming quality

Names are descriptive compounds, not single generic words (`generator`, `helper`). Min 3 chars, optimal 10-30, max 64.

Anti-pattern lint (2.8, Suggestion): sections titled "anti-patterns / common mistakes / avoid / pitfalls" should use tables or bullet lists, not wall-of-text prose.

## 4. Semantic checks

- Contradiction: flag instructions that both require and forbid the same action.
- Ambiguous terms: flag vague language ("multiple items", "correct settings"). Skip code blocks, examples, before/after comparisons.
- Output format: if the skill mentions output/returns/produces, it needs an `## Output` section with a concrete example (code/JSON/table).
- Wisdom/platitude (4.6, Suggestion, ~5% false-positive): flag generic advice — openers like "Remember that", "It's important to"; "[X] is essential/crucial to [Y]"; vague imperatives "ensure quality", "maintain standards". Replace with concrete directives.
- Description trigger style (4.8, Suggestion): description should read as a trigger, not a summary. Flag openers "This skill", "A tool that", "Provides", "Offers", "Handles", "Manages", "Enables" — UNLESS a "Use when" clause appears later or it starts with an action verb.
- Railroading (4.9, Suggestion): flag 5+ prescriptive phrases ("you must always", "never deviate", "follow these exact steps") in non-example content. Give context, let Claude adapt. Skip safety-critical skills.
- Misplaced routing (4.4, Warning): body headings like `## When to Use` or routing phrases ("Activate when user", "Trigger this skill when") are invisible during routing — they load only after invocation. Merge into the `description` field.

## 5. Strengths (report as positives)

Example section; error/limitation docs; trigger phrases in description; output-format examples; numbered/structured steps; prerequisites; negative triggers ("Do NOT use for…"); a Gotchas/Pitfalls section (highest-signal content per Anthropic guidance).

## 6. Design pattern classification (19.1, Strength)

Classify into one (hybrids common): Reviewer (evaluates against criteria), Generator (artifacts from templates), Inversion (asks questions first), Pipeline (chained steps), Tool Wrapper (wraps an API).

## 7. OWASP Agentic Top 10 — 8 deterministic items (Cat 26)

Activation gate: only score skills with an agent surface (tools beyond Read/Glob/Grep, external content ingestion, subagent orchestration, or consequential actions). Read-only formatting skills report `not-applicable`. Flag, with severity:

- ASI-02 Tool Misuse: `allowed-tools: *`/`all` (Critical); `Bash` with no constraint note (Warning); 5+ tools no rationale (Suggestion).
- ASI-03 Identity Abuse: identity-override params (`as_user`, `act_as_user`, `on_behalf_of`, `impersonate`, `run_as`) (Critical).
- ASI-04 Supply Chain: unpinned installs (`pip install X` no `==`, `npm install X` no `@version`, `@latest`, `npx X@latest`) (Warning).
- ASI-05 Code Execution: `eval(`, `exec(`, `os.system(`, `subprocess shell=True`, `child_process`, `pickle.loads`, or `curl … | sh` (Warning).
- ASI-08 Cascading Failure: "retry until", "loop until", uncapped fan-out (Suggestion).
- ASI-09 Trust Exploitation: destructive verb (`rm -rf`, `DROP TABLE`, `git push --force`, "send money", `merge`) with no gate token (`confirm`, `ask the user`, `approval`) within ±10 lines (Warning).
- ASI-10 Rogue Agents: `--no-verify`, `--force`, "skip validation", "bypass", `dangerouslyDisableSandbox`; or long-running marker (`loop`, `daemon`, `every N minutes`) with no kill-switch (Warning).
- ASI-11 Untraceability: consequential verb (`commit`, `push`, `publish`, `POST`, `send`) with zero traceability tokens (`log`, `audit`, `record`, `handoff`) anywhere (Warning).

## Plugin manifest checks (Cat 24)

When input is `.claude-plugin/plugin.json`. Four required fields, all Critical if missing/malformed:
- `name` — kebab-case `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`.
- `version` — canonical semver `MAJOR.MINOR.PATCH`, no `v` prefix.
- `description` — non-empty.
- `author.name` — non-empty.
- `commands/<name>.md` must not collide with bundled commands (`simplify`, `batch`, `debug`, `loop`, `claude-api`, `security-review`) (Critical).
- `.claude-plugin/` should contain only `plugin.json`; skills/commands/hooks/agents live at plugin root (Warning).

## MCP tools/list checks (Cat 23)

When input is an MCP `{"tools":[…]}` response:
- 20 tools → consider intent grouping (Warning); 40 → strong candidate for search+execute pattern (Warning).
- API-mirror: one noun with 3+ CRUD verb prefixes (`list_`/`get_`/`create_`/`update_`/`delete_`…) → rename toward intent (Warning).

## Severity & output

| Level | Meaning | Action |
|-------|---------|--------|
| Critical | May not function | Must fix |
| Warning | Best-practice violation | Should fix |
| Suggestion | Could improve | Nice to have |

Output format:
```
# SkillCheck Report: {skill-name}
## Summary  (score 0-100, issue/strength counts)
## Issues   (check_id, severity, line, message, fix per issue)
## Strengths (check_id, detail per strength)
```

## Gotchas

- Multi-line YAML descriptions trigger false positives on line-based checks — use a single-line or `|` pipe description.
- Wisdom/platitude (4.6) has ~5% false positives on advisory technical prose — if flagged wrongly, the content is fine.
- Misplaced-routing (4.4) fires on body trigger phrases — wrap example invocations in code/`<example>` blocks to avoid false positives.
- Non-standard frontmatter fields get informational notices, not errors — safe to ignore.

Pro tier (anti-slop, token budget, deep security, WCAG, enterprise, Eval Kit, auto-fix, CI binary, badge) is out of scope for this skill. Full rule source: source repo `skills/skill-check/SKILL.md` plus `references/cli.md` and `references/marketplace-checks.md`.
