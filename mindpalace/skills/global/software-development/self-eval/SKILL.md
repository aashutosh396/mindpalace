---
name: Self-Eval (Honest Work Evaluation)
description: Use after completing a task, code review, or work session to get a calibrated, un-inflated quality score — two-axis matrix + mandatory devil's advocate + cross-session anti-inflation.
tags: [self-evaluation, code-review, quality, scoring, retrospective, calibration, devils-advocate, anti-inflation]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/self-eval
---

# Self-Eval

Honest, calibrated work evaluation. Replaces the AI "everything is a 4" tendency with a two-axis matrix the model cannot override. Core insight: a single-axis score conflates task difficulty with execution quality — separate them, then combine via fixed matrix.

## Step 1 — Identify what to evaluate
If given context, evaluate that. Otherwise review the full session and summarize the work in ONE sentence before scoring.

## Step 2 — Score two axes independently (do NOT pick a number first)

**Axis 1 — Task Ambition (what was attempted, not how well):**
- Low (1): safe, routine, no real risk of failure (config tweaks, simple refactors, copy-paste-with-edits). If you were confident of success before starting → Low/Medium, not High.
- Medium (2): meaningful work with novelty; partial failure possible (new feature, unfamiliar API, tricky debug).
- High (3): ambitious/unfamiliar/high-stakes; real risk of total failure (from-scratch in new domain, system redesign, perf-critical, prod under pressure).

**Axis 2 — Execution Quality (output quality, independent of ambition):**
- Poor (1): major failures, incomplete, wrong, abandoned — doesn't meet own criteria.
- Adequate (2): completed but with gaps/shortcuts/missing rigor.
- Strong (3): thorough, quality, no obvious improvements left undone given scope.

## Step 3 — Composite matrix (read it, don't override)
|  | Poor (1) | Adequate (2) | Strong (3) |
|---|:--:|:--:|:--:|
| **Low (1)** | 1 | 2 | 2 |
| **Medium (2)** | 2 | 3 | 4 |
| **High (3)** | 2 | 4 | 5 |

Properties: Low ambition caps at 2 (safe work done perfectly is still safe). A 5 needs BOTH High ambition AND Strong execution (rare). High+Poor = 2 (bold failure hurts). Most common honest score for solid work is 3.

## Step 4 — Devil's advocate (MANDATORY, ≥3 sentences total)
1. **Case for LOWER** — what was easy/avoided/less ambitious than it looks?
2. **Case for HIGHER** — what was genuinely hard or exceeded plan?
3. **Resolution** — if either reveals a mis-rated axis, re-rate and recompute. The devil's advocate can re-rate an axis but cannot directly override the matrix.

## Step 5 — Anti-inflation check
Read `.self-eval-scores.jsonl` (cwd). If 4+ of last 5 scores are identical: flag "Score clustering detected — consider whether you're anchoring to a default." If no file: ask "Would an outside observer rate this the same?"

## Step 6 — Persist
Append one line to `.self-eval-scores.jsonl`:
`{"date":"YYYY-MM-DD","score":N,"ambition":"...","execution":"...","task":"1-sentence"}`

## Output format
**Task / Ambition (+justify) / Execution (+justify) / Devil's Advocate (Lower, Higher, Resolution) / Score: N — final justification.**
