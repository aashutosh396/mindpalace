---
name: Skill Tester
description: Use when authoring a new agent skill, auditing existing skills for tier promotion, setting up skill-quality pre-commit hooks, or integrating skill QA into CI — structure validation, script testing, and quality scoring.
tags: [skill-qa, validation, quality-score, tier-classification, script-testing, ci-gate, pre-commit, meta-skill, structure-check]
source: alirezarezvani/claude-skills
derived_from: skill-tester
---

# Skill Tester

Meta-skill that validates, tests, and scores agent skills. Four stdlib-only tools, run from the repo root with full paths.

## Tools
1. **skill_validator.py** — structure + documentation compliance.
2. **script_tester.py** — Python script syntax/imports/runtime/output testing.
3. **quality_scorer.py** — multi-dimensional scoring with letter grade.
4. **security_scorer.py** — security posture (also via `quality_scorer.py --include-security`).

## Flow (the verification loop)
A skill passes when, in one run from repo root: validator exits 0 · script_tester reports all scripts passing · quality_scorer meets `--minimum-score`. If any step fails, apply the top `improvement_roadmap` item and re-run all three — never report a partial pass.

## What each tool checks
- **Validator**: frontmatter parsing, required sections, minimum line counts per tier; required structure (SKILL.md, README.md, scripts/, references/, assets/, expected_outputs/); argparse present + stdlib-only imports.
- **script_tester**: AST syntax validation, import analysis (flags external deps), controlled execution with timeout, `--help` verification, sample-data runs compared to expected_outputs/.
- **quality_scorer**: four dimensions at 25% each — Documentation (depth, examples, references), Code Quality (complexity, error handling, output consistency), Completeness (required dirs, sample data, expected outputs), Usability (help text, example clarity). 0–100 + A–F grade + tier recommendation.

## Tier classification (advisory for legacy skills)
| Tier | SKILL.md | Scripts | CLI |
|---|---|---|---|
| BASIC | ≥100 lines | 1 (100–300 LOC) | basic argparse |
| STANDARD | ≥200 lines | 1–2 (300–500 LOC) | subcommands, JSON+text |
| POWERFUL | ≥300 lines | 2–3 (500–800 LOC) | multiple modes, CI integration |

> Scope note: tier line-count minimums measure *legacy* skills. For authoring *new* skills, the write-a-skill doctrine (SKILL.md under ~100 lines) is the binding standard — do not pad a new skill to hit a tier minimum.

## CI / pre-commit
Gate changed skills in CI: run validator (`--json`), script_tester, and quality_scorer (`--minimum-score 75`) per changed skill. Pre-commit hook: run the validator on the staged skill directory, block on non-zero exit.

## Troubleshooting
Timeout errors → raise `--timeout` or optimize the script · import failures → external deps detected (stdlib-only is policy) · tier misclassification → check line counts/LOC vs the table (remember the new-skill exception).
