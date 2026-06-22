---
name: CLAUDE.md Progressive Disclosurer
description: Use when asked to optimize/slim/restructure a CLAUDE.md or AGENTS.md ("is my CLAUDE.md too big", move content to references, progressive disclosure) — restructures into a lean Level 1 + on-demand Level 2 with ZERO information loss.
tags: [claude-md, agents-md, progressive-disclosure, refactor, context-optimization, references, single-source-of-truth, prompt-engineering]
source: daymade/claude-code-skills
derived_from: claude-md-progressive-disclosurer
---

# CLAUDE.md Progressive Disclosure Optimizer

Goal: maximize information efficiency, readability, maintainability via two-layer architecture — WITHOUT losing information.

## Iron rule: line count is NOT a KPI
Judge by **single source of truth** (same info not maintained in multiple places), **cognitive relevance** (info irrelevant to current task doesn't distract), **maintenance consistency** (changing one place needs no sync elsewhere) — never line count. Forbidden: reporting "cut from X to Y lines / reduced Z%" as a result; using "fewer lines" as a reason to move/delete. A clear, non-duplicated long file beats a short file missing key info.
Line count MAY be a **diagnostic symptom only**: abnormally large + Claude repeatedly ignoring a rule → trigger to investigate, not a license to cut.
**On trigger ("too big / slim down"): reframe first.** Declare line count isn't the goal, then go to signal triage — decide keep/move by "does this have a duplicate canonical source / is it an anti-signal?", not by length.

## Two-layer architecture
- **Level 1 (CLAUDE.md, always loaded)**: info-recording principle; reference index (top); core command table; iron rules/prohibitions (with code examples); error diagnosis (symptom→cause→fix); copy-paste code patterns; directory map; "read before editing code" table; trigger index (bottom).
- **Level 2 (references/, loaded on demand)**: detailed SOPs; edge cases; full config examples; historical decisions.
- **Multi-entry principle**: one Level 2 resource may have several entry points (error index / task index / tail recap) keyed differently — valid ONLY if each entry stores a *pointer + trigger condition*, not a copy of the content (copying body = SSOT violation).

## Workflow
1. **Backup**: `cp CLAUDE.md CLAUDE.md.bak.$(date +%Y%m%d_%H%M%S)`.
2. **Classify (triage first, then layer)**:
   - **2.1 Signal triage** (gate): for each section ask Anthropic's litmus "if I delete this, will Claude make a mistake?" Mistake → signal, keep. No mistake AND (inferable from code/structure / standard convention / self-evident / has independent canonical source / obsolete one-off / must-happen-deterministically→suggest hook) → anti-signal, list as deletion candidate. Candidate ≠ delete: list each + reason + get user confirmation. Can't state a reason = it's a signal, keep it.
   - **2.2 Layering** for signals: high-frequency or severe-consequence or copy-paste code → Level 1; clear trigger condition → Level 2 + trigger; history/reference → Level 2 or delete.
3. **Create reference files** (`docs/references/{topic}-sop.md`). **Move verbatim, never compress** — moving changes information's *location*, not its *existence*. Compressing while moving = disguised deletion.
4. **Update Level 1**: add info-recording principle + reference index at top; replace details with trigger-condition format; keep code patterns + error diagnosis; add "read before editing code" table; add tail trigger index. **Hard gate before writing any pointer**: `grep` the target file confirms the content actually exists there — never write a pointer to content that isn't there.
5. **Verify (all three)**:
   - 5a existence: grep referenced files exist.
   - 5b content integrity (most critical): restore original (`git show HEAD:CLAUDE.md`), compare each `##` section — confirm content exists fully in new L1 or a L2 file. Any shortened/missing → restore. Only legit deletion = info has an independent canonical source, with a pointer in L1. For large compressions, run an **independent sub-agent** for 5b (executor self-audit has optimism bias).
   - 5c: do NOT use line count as a pass condition.

## Reference format (4 kinds)
Detailed (inline important ref), problem-trigger table (error index), task-trigger table ("before editing code"), inline (one-liner). Diversify; don't use one format everywhere.
**@import does NOT save context** — `@path` fully expands at startup. Use plain backtick-path pointers ("Read `references/xxx.md` when needed"), move non-universal content to project-level, or convert to a skill.

## Key principles
- **0**: inject an "info-recording principle" so future additions go L1(high-freq) / L2(low-freq, with trigger) — prevents re-bloat.
- **1**: trigger index at top AND bottom (LLM attention is U-shaped).
- **2**: every reference needs a trigger condition (`📖 when to read X.md: <triggers>`) + content summary.
- **3**: keep copy-paste code patterns in Level 1.
- **4**: use 3-state priority (✅ always / ⚠️ stop-and-ask / 🚫 never), not "everything is an iron rule" — instruction-following degrades past ~150-200 rules; put truly irreversible rules (5-7) at file head/tail.
- **5**: each kept rule gets a one-line `Why:` (rules with reasons generalize across contexts).

## Anti-patterns
1. Line-count-driven over-trimming (loses code patterns, diagnosis, directory map).
2. References without trigger conditions.
3. Moving code patterns to L2.
4. Deleting instead of moving.
5. Line count as KPI.
6. Compressing while moving (move = move, trim = separate confirmed step). For mixed rule+narrative paragraphs: move whole paragraph verbatim to L2 first, then derive a paraphrase in L1 — never rewrite the original rule sentence.
7. Hiding loss as "intentional deletion" (every deletion must name its canonical source).
8. Pure-negative rules (`🚫 don't X`) without a positive `✅ use Y` alternative.
9. Fake pointers (pointer to content not actually present) — grep-verify before writing.

## Scope check (project vs user level)
User-level `~/.claude/CLAUDE.md` loads into ALL projects — only universally applicable content. Project name / deploy target / per-project paths / credentials → project-level, never global (during triage, project-specific content in a user-level file auto-judges "move to project level").
