---
name: Meeting Minutes Taker
description: Use when a meeting transcript needs structured minutes/notes/summary, multiple minute versions must merge without loss, existing minutes need a completeness review, or anonymous speakers ("Speaker 1", "发言人1") need identifying — multi-pass generation with human review.
tags: [meeting-minutes, transcript, notes, summary, speaker-identification, action-items, decisions, multi-pass, mermaid]
source: daymade/claude-code-skills
derived_from: meeting-minutes-taker
---

# Meeting Minutes Taker

Transform raw transcripts into comprehensive, evidence-based minutes through multi-pass generation + iterative human review. (For fixing ASR errors first, use transcript-fixer; this skill structures clean transcripts.)

## Workflow
```
- [ ] 1. Read & analyze transcript (topic, attendees, decisions, action items, deferred items)
- [ ] 1.5 Speaker identification (if "Speaker 1/2/3")
- [ ] 1.6 Generate filename YYYY-MM-DD-<topic>-<type>.md, confirm with user
- [ ] 1.7 Quality assessment (optional, sets depth)
- [ ] 2. Multi-pass generation (PARALLEL subagents), UNION merge
- [ ] 3. Self-review for completeness
- [ ] 4. Present draft for human line-by-line review
- [ ] 5. Cross-AI comparison (if user provides another AI's output)
- [ ] 6. Iterate on feedback (expect multiple rounds)
- [ ] 7. Human approves
```

## Step 1.5: speaker identification (when only generic labels)
**Phase A — feature analysis** per speaker: word count, segment count, avg segment length, filler-word ratio (对/嗯/啊/就是/然后), speaking style, topic focus, interaction pattern. Inference: share >70% + avg >100 chars → 主讲人; avg <50 chars → responder; filler <5% → prepared; >10% → improvised.
**Phase B — context mapping** (if user gives `context.md` team directory): match feature patterns to known members.
**Phase C — confirm before proceeding**: never silently assume identity; present mapping + confidence + evidence, get user confirmation, then apply consistently.

## Step 2: multi-pass generation (single pass WILL lose content)
**Each pass generates COMPLETE minutes (all sections) from the full transcript** — not narrow per-section passes (which waste tokens and cause bias). Different context states catch different details; UNION merge captures all.
**Preferred — Strategy B (parallel subagents)**: launch 3 Task subagents IN PARALLEL (single message, 3 calls), each writing complete minutes to `<output_dir>/intermediate/<transcript-name>/version{1,2,3}.md`. Each subagent prompt must include: transcript path, output path, context/template files, reference images, output-language requirement, quote-formatting requirement. Then main agent UNION-merges (consolidate duplicates, **aggressively include ALL diagrams from ALL versions**) → `draft_minutes.md` → compare against transcript, add omissions → `final_minutes.md`.
File-based offloading keeps conversation context clean and lets humans inspect each pass. Preserve intermediate files (add `intermediate/` to `.gitignore`); don't delete after merge.

## Output requirements
Match transcript language, preserve technical terms in English. Evidence-based: every significant decision needs a supporting verbatim quote. Sections: Executive Summary, Key Decisions, Discussion, Action Items, Parking Lot. **Mermaid diagrams strongly encouraged** — sequence (data flow/API), ER (schema), flowchart (process), state (state machines), component (architecture). Place reviewed artifacts (mockups, API docs, images) at the TOP for context. Attribute decisions to specific people, not teams. Preserve numerical values. Single source of truth — each fact in ONE location.

## Quote formatting (correct)
```markdown
* **Quote:**
  > "Exact quote" - **Speaker Name**
```
`* **Quote:**` on its own line; content indented 2 spaces then `> `; attribution `- **Name**` at end. Never inline `> "quote"`.

## Iterate (human-in-the-loop)
Minutes are not one-shot. On "deep review / anything missing": re-read section by section, compare against minutes, look for entities/field names/numerical ranges/state transitions/trade-offs/deferred items, add omissions — never claim "nothing missing" without section-by-section review. On merging another version: **UNION, never remove** — keep all existing + add all new, consolidate duplicates, prefer the more detailed version. On cross-AI comparison: add valid items missing from the draft (verify against transcript first), don't copy the other AI's errors.

## Anti-patterns
Single-pass generation; section-divided passes without overlap; narrow per-section passes; generic summaries without quotes; action items assigned to "team"; missing numerical values; incomplete state machines; removing content during merge; "nothing missing" without review; shared context between subagents; sequential (not parallel) subagents; flat intermediate dir; inline quote formatting; omitting diagrams during merge; duplicate content across sections; deleting intermediate files.
