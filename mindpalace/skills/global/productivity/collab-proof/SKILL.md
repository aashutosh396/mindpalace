---
name: Collab-Proof (AI Contribution Evidence)
description: Use at session end (or /collab-proof) to surface what the AI contributed vs what you drove — git-grounded signal detection, 4-frame scoring, DECISIONS.md + session-history + WORKLOG + HTML artifacts.
tags: [session-retrospective, ai-contribution, collaboration-evidence, decisions-log, worklog, git-analysis, session-history]
source: alirezarezvani/claude-skills
derived_from: engineering/collab-proof
---

# collab-proof

Surfaces AI-collaboration evidence the developer didn't consciously record. 3-layer pipeline, prompt-native, zero dependencies. Run at session end.

## Layer 01 — Signal detection
Run `git log --oneline -10` and `git diff --stat HEAD~3..HEAD` first. Classify (highest match wins):
- **HIGH** → full artifacts. New file OR 4+ files modified OR explicit option comparison ("vs", "chose X over Y") OR 15+ exchange design discussion OR bug with root-cause diagnosis (the WHY, not just "fixed X").
- **BUG_FIXING override:** even 1 file = HIGH if conversation has root-cause explanation + diagnosis process + fix rationale. A well-diagnosed single-file fix beats a 10-file feature with no discussion.
- **MEDIUM** → WORKLOG only. 1-3 files, no root-cause discussion, or minor feature with no tradeoffs.
- **LOW** → silence ("Routine session — nothing recorded."). No code changes, or trivial change with no context.
Show: `Signal: HIGH/MEDIUM/LOW — [one-line reason]`.

## Layer 02 — WorkIntentClassifier (4 frames, score 0.0-1.0)
- **A Technical:** 1.0 new module/complex logic · 0.5 modified function · 0.1 typo/comment.
- **B Uncertainty:** 1.0 rollback/explicit doubt/git revert · 0.5 advice sought mid-impl, 2+ revisions · 0.0 uninterrupted execution.
- **C Fork:** 1.0 ≥2 alternatives compared · 0.5 tradeoff mentioned no comparison · 0.0 single standard approach.
- **D AI contribution:** 1.0 Claude found a bug/edge case dev missed + proposed fix · 0.6 generated structural boilerplate that accelerated · 0.2 reformatted dev-directed code, no independent contribution.

**Pruning:** prune any frame < 0.4. **High-Speed Execution Guard:** if A≥0.8 AND D≥0.6, do NOT prune/silence even if B=C=0 → classify `FEATURE_BUILDING`/HIGH (zero uncertainty in a fast session is a feature).

**Intent map:** A+D high (B,C low) → FEATURE_BUILDING · B high + A/D high → BUG_FIXING/STUCK · C+A high → REFACTORING/EXPLORING · all <0.4 → FLOW_STATE/LOW. Record runner-up for the narrative.

## Layer 03 — Output
**HIGH:** append per-fork entry to `DECISIONS.md` (Context/Decision/Alternatives/Reasoning [prefix "inferred:" if reconstructed]/AI contribution [Identified/Suggested/Developer-driven]/Intent/Outcome). BUG_FIXING uses Root cause/Symptom/Fix/Why-this-fix/Alternatives format. Create `session-history/YYYY-MM-DD-HHMM.md` (What shipped / figured out / decisions / where it got hard / AI summary / next steps). Append `WORKLOG.md` line. Generate self-contained `*-proof.html` (dark theme `#0d1117`, monospace, fixed class names). Collect token usage from `~/.claude/projects/*.jsonl` (cache hit %, top turns).
**MEDIUM:** one WORKLOG line only.
**LOW:** tell user, write nothing.

## Honesty rules
Never invent decisions not in conversation/diff. "inferred:" when reconstructed. Frame D calibrated (no over/under-claim). All frames <0.4 → write nothing.

## PreCompact defence
On compaction: compute signal, score frames, write `session-history/.tmp-TIMESTAMP.json` snapshot (signal/frames/intent/key_moments). At session end merge all snapshots (max per frame, combine key_moments), then delete `.tmp-*.json`.
