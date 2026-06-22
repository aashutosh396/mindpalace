---
name: Transcript Fixer
description: Use when working with ASR/STT output containing recognition errors, homophones, garbled technical terms, or mixed CJK/English — or when asked to "fix this transcript" / "clean up these meeting notes" — corrects errors via dictionary rules + AI judgment and learns reusable patterns.
tags: [asr, stt, transcript, speech-to-text, homophones, correction, meeting-notes, dictionary, cjk, false-positives]
source: daymade/claude-code-skills
derived_from: transcript-fixer
---

# Transcript Fixer

Two-phase pipeline: deterministic dictionary rules (instant, free) → AI error detection. Corrections accumulate in `~/.transcript-fixer/corrections.db`, improving over time. The dictionary shines on *recurring* errors (product names, known homophones); on a fresh DB or high-quality ASR, the AI pass does almost all the real work — don't be alarmed when Stage 1 changes only a few lines.

## Quick start
```bash
uv run scripts/fix_transcription.py --init                       # first time
uv run scripts/fix_transcription.py --input meeting.md --stage 1 # dictionary pass
```
After Stage 1, Claude reads the output and fixes remaining errors natively (no API key). Alt API batch: `export GLM_API_KEY=...; uv run scripts/fix_transcript_enhanced.py input.md --output ./corrected`.

## Core workflow
1. Init (once). 2. Add domain corrections (`--add "错误词" "正确词" --domain <d>`). 3. Stage 1 dictionary. 4. AI correction (native, or `--stage 3` with GLM_API_KEY). 5. Save stable patterns. 6. Review learned (`--review-learned`, `--approve`).
Domains: `general`, `embodied_ai`, `finance`, `medical`, custom. Patterns appearing ≥3× at ≥80% confidence auto-promote to the dictionary.

## Native AI correction (default; scale effort to the transcript)
A short clean memo just needs steps 1-3 + one obvious-fix pass. For long/multi-speaker/domain-heavy/high-stakes, do the full method:
1. Run Stage 1 on all files (parallel if many).
2. Verify Stage 1 vs original; if it introduced false positives, work from the **original** instead.
3. Read the **entire** transcript before proposing fixes — later context disambiguates earlier errors.
4. **Triage each candidate into 3 buckets**:
   - **Confident fix**: non-words, obvious garbling, recognized product-name variants, unambiguous homophones → apply.
   - **Needs verification**: a proper noun you can't confirm from context (person/company/ticker/product/place) → **search it, don't guess** (WebSearch, or local grep for project entities). Batch the unknowns. Confirmed → confident; unconfirmable → uncertain.
   - **Uncertain**: suspect an error but can't confirm even after searching → **leave original as-is**, log in the needs-checking list. A fluent-but-wrong fix is worse than an obvious garble.
5. Apply confident fixes: global non-word replacements via one `sed -i '' -e ...`; context-dependent via longer phrase or Edit. Re-grep each changed term.
6. **Second pass** — one read always leaves residue. Re-scan; for long/high-stakes, spawn an independent subagent (Task) to re-read cold and report residuals with line numbers, then re-triage. If Task unavailable (already in a subagent), do another thorough re-read.
7. **Emit a needs-checking list** in chat (not the file): line number, original text left in place, what you suspect, why unconfirmed.
8. Verify with `diff` against the file you actually edited.
9. Finalize: rename `*_stage1.md` → `*.md`, delete original `.txt`.
10. Save stable patterns to the dictionary.

## Dictionary addition (after fixing — the core value)
| Pattern | Example | Action |
|---|---|---|
| non-word → correct term | cloucode→Claude Code | ✅ add |
| rare word → correct term | 拉行链→LangChain | ✅ add (verify not a real word) |
| person/company name error | 卡帕西→Karpathy | ✅ add |
| common word → context word | affect→effect | ❌ skip (false-positive risk) |
| real brand → other brand | Xcode→Claude Code | ❌ skip |
**Read the false-positive guide before adding any rule**, especially short (≤2 char) or common CJK words — a bad global rule silently corrupts every future transcript.

## Parallel batch (10+ files) — four hard-earned rules
1. Hardcode the file list into the script (`const FILES=[...]`), don't pass paths through `args` (non-ASCII/brackets can silently arrive empty).
2. Scope each agent to exactly one file; forbid cross-file `grep -r`/`sed` in its prompt.
3. After the batch, `git diff --name-only` vs your intended list (revert strays); grep deleted lines for invariants — **speaker-label lines must never change**.
4. Run aggregated dictionary suggestions through the false-positive filter (parallel agents over-propose; keep only unambiguous non-word→term).

## Common ASR garbles
Claude (cloud, 克劳锐, Clover), Claude Code (Xcode, cloucode), Opus (Opaas), GitHub (get Hub), prototype (Pre top). Always add confirmed name corrections to the dictionary.

## DB ops
Real columns are `from_text` / `to_text` (not wrong_term/correct_term). `sqlite3 ~/.transcript-fixer/corrections.db "SELECT from_text, to_text, domain FROM active_corrections;"`

## Utilities
Timestamp repair (`fix_transcript_timestamps.py --in-place`), section split (`split_transcript_sections.py`), word-level diff HTML (`generate_word_diff.py`). Health check: `--validate`.
