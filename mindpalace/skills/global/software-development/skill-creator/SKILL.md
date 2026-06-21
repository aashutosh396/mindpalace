---
name: skill-creator
description: "Use when creating a new Claude skill from scratch, editing or improving an existing skill, writing or running skill evals/test cases, benchmarking skill performance, packaging a .skill file, or optimizing a skill's frontmatter description for better triggering/auto-detection accuracy."
version: 1.0.0
license: Apache-2.0
tags: [skill, skill-creator, skills, evals, benchmark, description-optimization, claude, authoring, triggering, packaging]
source: https://github.com/anthropics/skills/tree/main/skills/skill-creator
derived_from: awesomeclaude
prerequisites:
  commands: [python]
---

# Skill Creator

Create new Claude skills and iteratively improve them. Figure out where the user is in the loop, then jump in and move them forward. Be flexible — if the user just wants to "vibe", skip the heavy eval machinery.

## When to use

- "Make a skill for X" / "turn this workflow into a skill"
- Editing or optimizing an existing skill
- Running evals / benchmarking a skill
- Optimizing a skill description so it triggers reliably

## Core loop

1. Figure out what the skill is about (capture intent).
2. Draft or edit the skill.
3. Run claude-with-the-skill on a few realistic test prompts.
4. Evaluate outputs with the user (qualitative + optional quantitative benchmark).
5. Improve, rerun, repeat until satisfied.
6. Optionally optimize the description, then package the `.skill` file.

## Communicating with the user

Users range from non-coders to experts. Read context cues. "Evaluation"/"benchmark" are borderline OK; explain "JSON"/"assertion" unless the user clearly knows them. Briefly define terms when in doubt.

## 1. Capture intent

If the conversation already shows a workflow ("turn this into a skill"), extract the tools, steps, corrections, and I/O formats from history first. Then confirm:
1. What should the skill enable Claude to do?
2. When should it trigger (what user phrases/contexts)?
3. Expected output format?
4. Set up test cases? Objectively-verifiable skills (file transforms, extraction, code gen, fixed workflows) benefit from them; subjective ones (writing style, art) often don't. Suggest a default, let the user decide.

Proactively ask about edge cases, example files, success criteria, dependencies. Use available MCPs/subagents to research in parallel before burdening the user.

## 2. Write the SKILL.md

Frontmatter needs **name** and **description** (the rest is optional, e.g. `compatibility` for required tools).

The **description is the primary trigger mechanism** — put ALL "when to use" info here, not in the body. Include both what the skill does AND specific trigger contexts. Claude tends to *undertrigger*, so make descriptions a little pushy: e.g. "...Make sure to use this whenever the user mentions dashboards, data viz, or internal metrics, even if they don't say 'dashboard'."

Skill anatomy:
```
skill-name/
├── SKILL.md              (required: YAML frontmatter + markdown)
└── (optional bundled resources)
    ├── scripts/          executable code for deterministic/repetitive tasks
    ├── references/       docs loaded into context as needed
    └── assets/           templates, icons, fonts used in output
```

**Progressive disclosure** — three loading levels:
1. Metadata (name+description) — always in context (~100 words)
2. SKILL.md body — loaded when triggered (<500 lines ideal)
3. Bundled resources — loaded/executed as needed (unlimited)

Patterns: keep SKILL.md under 500 lines (add hierarchy + pointers if approaching it); reference files clearly with read-when guidance; give large reference files (>300 lines) a table of contents. For multi-domain skills, organize references by variant (e.g. `references/aws.md`, `gcp.md`, `azure.md`) so Claude reads only the relevant one.

**Writing style**: prefer imperative form. Explain the *why* behind instructions instead of heavy-handed all-caps MUSTs — modern LLMs have good theory of mind and a rigid rule is a yellow flag. Use theory of mind, keep it general (not overfit to examples). Draft, then reread with fresh eyes and improve.

**No surprises**: no malware/exploit/exfiltration content; a skill's behavior must match its stated intent.

## 3-4. Test, benchmark, review (Claude Code with subagents)

Save test prompts to `evals/evals.json` (prompts only at first; add assertions later). Put run results in `<skill-name>-workspace/iteration-<N>/eval-<ID>/`.

- **Spawn all runs in one turn** — for each test case, one with-skill subagent + one baseline. Baseline = no skill (new skill) or a snapshot of the old skill (improving). Snapshot first: `cp -r <skill-path> <workspace>/skill-snapshot/`.
- **While runs go**, draft objectively-verifiable assertions with descriptive names; write `eval_metadata.json` per case. Don't force assertions on subjective skills.
- **Capture timing** from each task-completion notification (`total_tokens`, `duration_ms`) into `timing.json` immediately — it isn't persisted elsewhere.
- **Grade** via a grader subagent reading `agents/grader.md`; save `grading.json` (fields must be `text`/`passed`/`evidence` — the viewer depends on these). Prefer scripts for programmatic checks.
- **Aggregate**: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>` → `benchmark.json`/`.md`.
- **Launch viewer** (do NOT hand-write HTML):
  ```bash
  nohup python <skill-creator-path>/eval-viewer/generate_review.py \
    <workspace>/iteration-N --skill-name "my-skill" \
    --benchmark <workspace>/iteration-N/benchmark.json > /dev/null 2>&1 &
  ```
  Add `--previous-workspace <...iteration-(N-1)>` for iteration 2+. Headless/Cowork: use `--static <out.html>` to emit a standalone file.
- Tell the user to review the "Outputs" and "Benchmark" tabs, then read `feedback.json` when they submit. Kill the viewer when done.

## 5. Improving the skill

This is the heart of the loop.
1. **Generalize from feedback** — the skill must work across a million future prompts, not just these examples. Avoid fiddly overfit changes and oppressive MUSTs; try different metaphors/patterns for stubborn issues.
2. **Keep it lean** — read the transcripts (not just outputs); cut parts that make the model waste time.
3. **Explain the why** — terse/frustrated feedback still has real intent; transmit understanding into the instructions.
4. **Bundle repeated work** — if every run independently wrote the same helper (e.g. `create_docx.py`), write it once into `scripts/` and point the skill at it.

Iterate: apply changes → rerun into `iteration-<N+1>/` (with baselines) → launch viewer with `--previous-workspace` → read feedback → repeat. Stop when the user is happy, feedback is all empty, or progress stalls.

## Description optimization

The frontmatter description decides whether Claude invokes the skill. After building/improving, offer to optimize it.

1. Generate ~20 realistic trigger eval queries (8-10 should-trigger, 8-10 should-not), as `[{"query": "...", "should_trigger": true}]`. Make them concrete (file paths, column names, company names, casual speech, typos). The valuable negatives are near-misses that share keywords but need something else — avoid obviously-irrelevant negatives.
2. Review with the user via `assets/eval_review.html` (replace `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, `__SKILL_DESCRIPTION_PLACEHOLDER__`); they export `eval_set.json` to `~/Downloads`.
3. Run the loop in background (needs `claude` CLI — Claude Code only):
   ```bash
   python -m scripts.run_loop --eval-set <trigger-eval.json> \
     --skill-path <skill> --model <current-session-model-id> \
     --max-iterations 5 --verbose
   ```
   Splits 60/40 train/test, runs each query 3x, proposes improvements on failures, picks `best_description` by test score (avoids overfit).
4. Apply `best_description` to SKILL.md; show before/after + scores.

Note on triggering: Claude only consults skills for tasks it can't trivially do itself — simple one-step queries ("read this PDF") may not trigger even on a perfect description. Make eval queries substantive.

## Packaging

`python -m scripts.package_skill <path/to/skill-folder>` → `.skill` file. Works anywhere with Python + filesystem. Only auto-present if a `present_files` tool exists.

When **updating** an existing installed skill: preserve the original name and directory; copy to a writeable location (e.g. `/tmp/skill-name/`) before editing since the install path may be read-only.

## Environment notes

- **Claude.ai** (no subagents): run test cases yourself one at a time, skip baselines/quantitative benchmark, present outputs inline or as saved files, skip description-optimization (`claude -p` is Claude Code only) and blind comparison.
- **Cowork**: subagents work; no browser — always use `--static` for the viewer and generate it BEFORE evaluating outputs yourself.

## Helper scripts / references (in source skill dir)

Source path: `skills/skill-creator/` in the anthropics/skills repo. Key files referenced by this workflow:
- `scripts/aggregate_benchmark.py`, `scripts/run_loop.py`, `scripts/run_eval.py`, `scripts/package_skill.py`
- `eval-viewer/generate_review.py`
- `agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`
- `references/schemas.md` (evals.json / grading.json / benchmark.json schemas)
- `assets/eval_review.html`

Fetch these from the source rather than reconstructing them.
