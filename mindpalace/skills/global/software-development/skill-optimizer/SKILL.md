---
name: skill-optimizer
description: "Use when creating, auditing, tuning, personalizing, mining, generalizing, or publishing Agent Skills / SKILL.md files — when a skill won't trigger, over-triggers, is too generic/noisy, needs to fit your tools and paths, needs private context stripped for public release, or when you want to mine coding-agent history for repeated workflows worth turning into skills."
version: 1.0.0
license: MIT
tags: [skills, skill-md, agent-skills, authoring, trigger-tuning, personalization, publishing, session-mining, claude-code, codex]
source: https://github.com/hqhq1025/skill-optimizer
derived_from: awesomeclaude
---

# Skill Optimizer

Three complementary jobs for turning coding-agent work into better `SKILL.md`
files. Pick the direction that matches the request:

| Goal | Use this mode | Direction |
| --- | --- | --- |
| Find repeated workflows worth packaging | **miner** | scan real usage -> draft candidates |
| Make a skill fit YOUR setup | **personalizer** | tune inward (triggers, tools, paths) |
| Make a skill safe to SHARE | **generalizer** | strip private context -> publishable |

## When to use

- "This skill never triggers when I phrase it naturally" -> personalizer
- "Audit my installed skills; which under/over-trigger or are too generic?" -> personalizer
- "I downloaded/forked this skill, tune it to my machine" -> personalizer
- "Turn this local/private skill into a public GitHub-ready skill" -> generalizer
- "Mine my agent history for repeated work that should become skills" -> miner

Do NOT use for ordinary coding help, or for project-specific instructions that
belong in `AGENTS.md`/`CLAUDE.md` rather than a reusable skill.

## skill-miner — discover candidates

1. Locate real evidence: session JSONL, memory summaries, repo notes, repeated
   scripts, recent project folders.
2. Run the deterministic first-pass scanner (sanitized cluster report):
   `python3 scripts/scan_sessions.py --days 30 --limit 300 --min-count 3`
   - `--export <file.json>` for non-native agents, `--patterns <file.json>` for
     custom workflow definitions, `--help` for all flags.
   - Treat its output as evidence for review, NOT an auto-decision to create skills.
3. Cluster by intent, trigger phrasing, tools used, files touched, verification pattern.
4. Filter out one-offs, ordinary coding knowledge, and project-only instructions.
5. Score candidates: recurrence, friction, risk, portability, future value.
6. For strong candidates draft: name, trigger description, workflow outline,
   bundled-resource needs, validation prompts.
7. Recommend: keep personal / generalize for publication / skip.
8. Only create skill folders if the user asks; then verify frontmatter + layout.

Evidence rules: quote enough to justify each candidate; never expose sensitive
transcript content unless asked; check sampled positives AND near-misses before
trusting a regex match; label findings partial if session access is incomplete.

## skill-personalizer — tune inward

1. Inspect target skill, installed copies, local memories, real session evidence.
2. Identify the user's recurring phrasing, autonomy level, tools, dirs, verify habits.
3. Compare trigger conditions against real requests that SHOULD and SHOULD NOT load it.
4. Edit only the target skill + the bundled resources needed.
5. Add concrete local defaults, preferred commands, safety bounds, verification steps.
6. Preserve useful upstream behavior; document intentional local divergence.
7. Validate with realistic prompts + a frontmatter/layout check.

Audit dimensions (the original optimizer's checks): trigger fit, user reaction,
workflow completion, static quality, conflicts, environment consistency, token
economics, and P0/P1/P2 fix priority.

Rules: personal details only if they improve future execution; don't add brittle
fallbacks that mask broken setup; keep trigger descriptions broad enough to catch
natural phrasing; don't alter upstream attribution/license on third-party skills.

## skill-generalizer — publish outward

1. Inspect the source skill and nearby repo files before judging.
2. If quality is unclear, run the personalizer audit first.
3. Separate the reusable capability from personal implementation details.
4. Redact/replace private names, paths, hosts, credentials, account IDs,
   transcripts, one-off project facts.
5. Rewrite around general triggers, portable workflows, bounded assumptions.
6. Keep `SKILL.md` concise; move long rubrics/examples/scripts into bundled resources.
7. Check target-agent compatibility before writing install/support claims.
8. Produce packaging + honest promo copy only when requested.
9. Verify frontmatter, layout, install path, and one realistic usage prompt.

Rules: `description` says WHEN to use, not what the workflow is; public examples
must be generic or explicitly sanitized; README/marketplace claims must match
files that actually exist; prefer path placeholders over the author's home dir;
turn essential personal details into configurable variables with setup guidance.

## Reference material (in the source repo)

Each mode ships rubrics under `skills/<mode>/references/` and agent helpers under
`skills/<mode>/agents/`. Notable files to pull when doing a deep pass:
- `skills/skill-miner/references/discovery-rubric.md` + `scripts/scan_sessions.py`
- `skills/skill-personalizer/references/audit-rubric.md`, `personalization-rubric.md`
- `skills/skill-generalizer/references/publication-rubric.md`, `platform-compatibility.md`

## Gotchas

- The repo has NO root SKILL.md — it is three skills under `skills/<name>/`.
  Frontmatter `description` is what drives auto-detection; keep it trigger-rich.
- Don't mistake a one-off task for a skill; package only workflows where guidance
  changes future behavior.
- Personalizer = inward (private OK); generalizer = outward (private removed).
  Don't mix the two in one pass.
