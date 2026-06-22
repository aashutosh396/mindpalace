---
name: Competitor Repository Analysis (evidence-based)
description: Use when tracking competitors, creating a competitor profile, or generating competitive analysis of a software product — all findings must come from actual cloned code with file:line citations, never assumptions or web summaries.
tags: [competitor-analysis, evidence-based, code-audit, tech-stack, profile, citations, competitive-intelligence]
source: daymade/claude-code-skills
derived_from: competitors-analysis
---

Evidence-based competitor tracking. **All analysis must be based on actual cloned code, never assumptions.**

## Pre-analysis checklist (mandatory)
- [ ] Repo cloned locally (`~/Workspace/competitors/{product}/`)
- [ ] Can `ls` the directory structure
- [ ] Can read the config file (`package.json` / `pyproject.toml` / `Cargo.toml`) for version info
- [ ] `git log -1` confirms code is current

If any unmet, STOP and clone first.

## Forbidden vs required
| Forbidden | Why |
|-----------|-----|
| "推测/可能/应该" (speculation) | No evidence |
| "架构图（推测版）" | Must be from real code |
| "未公开/未披露" | If you don't know, don't write it |
| tech detail with no source | Unverifiable |

| Required format | Example |
|-----------------|---------|
| detail + (source: file:line) | "uses better-sqlite3 (package.json:88)" |
| quote + source | `> "description" (README.md:3)` |
| version + source | "v1.3.3 (package.json:2)" |

## Workflow
1. **Clone** (`mkdir -p ~/Workspace/competitors/{product}; git clone git@github.com:org/repo.git`). CN network may need retries.
2. **Gather facts** in order: project metadata (config file: name/version/deps), structure (`ls -la`, `ls src/`, `find . -name "*.md" -maxdepth 2`), core modules (entry file, helpers/utils), README + CHANGELOG.
3. **Deep dive** key technical points — read specific implementation files; record `| file | line | finding |`.
4. **Write profile** from the template, every technical detail source-tagged.
5. **Post-analysis verification:** all version numbers sourced? all tech stack from config files? architecture based on real structure? no "推测/可能"? comparison-table competitor data sourced?

## Tech-stack source map
- Node: package.json → `version`, `dependencies`, `main`/`scripts.start`, framework deps.
- Python: pyproject.toml → `[project].version`, `dependencies`, `[project.scripts]`.
- Rust: Cargo.toml → `[package].version`, `[dependencies]`.

## Common mistakes
1. Skipping clone, analyzing from GitHub web/WebFetch → always clone + Read local files.
2. Mixing facts and speculation → tech-stack table sourced from config (`electron 36.9.5 | package.json:68`).
3. Stale info → `git pull` first, record analysis commit hash.
4. Comparison-table competitor data with no source → add a source column (`支持语言 | 25种 | modelRegistryData.json:9-35`).

Profile top must note data-source path + commit hash; every detail `(source: file:line)`; unverifiable items marked "待验证" with reason.
