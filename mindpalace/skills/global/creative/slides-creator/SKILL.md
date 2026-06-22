---
name: Slides Creator (narrative-first)
description: Use when creating a slide deck / presentation from a user's content — runs narrative co-design (ABCDEFG model) first, then delegates visual generation, enforcing that the user's own words drive every claim.
tags: [slides, presentation, deck, narrative, abcdefg, ppt, storytelling, content-first]
source: daymade/claude-code-skills
derived_from: slides-creator
---

# Slides Creator

Narrative-first deck creation. Do the human part (narrative co-design); delegate visual generation to a slide-deck generator.

## First Law (overrides everything)
AI cannot write high-quality content FOR the user — only help express THEIR content. **Step 1 is ALWAYS collect the user's original words** (transcripts, articles, notes, prior decks). Weight: user's words > user-approved external > AI synthesis > AI invention. Output must sound like the user at their best. No source material = STOP and interview, never fabricate.

## Phases
**Phase 0 — Source collection** (do NOT proceed without it): request transcripts/articles/notes/decks. Gather external refs only if user explicitly approves each. Save to `00-上游/source-materials/`.

**Phase 1 — Narrative discussion** (NO files, only discuss). Align on arc before any visuals. ABCDEFG model:
- A Attention (hook in 30s), B Benefit (promised takeaway), C Credibility, D Difference (contrarian angle), E Evidence (proof/demo/story), F Framework (mental model left behind), G Go (Monday-morning action).
Gather: topic, audience, duration, ≤3 key messages, tone, existing content, constraints. Flag anti-patterns (too many slides, no emotional arc, no clear takeaway). Validate: summarize arc in 3-5 bullets, get explicit confirmation.

**Phase 2 — Content structuring**: write `narrative-brief.md` (topic/audience/duration/tone/key messages + ABCDEFG arc + slide-count recommendation: 10-15min→8-12, 20-30→12-18, 30-45→15-25, 45-60→20-30) and `content.md` (generator input). Optional `style-instructions.md` SSOT. **Content integrity**: every claim/quote/example traceable to user words / approved refs / Phase-1 statements — else `[TODO: user to provide]`.

**Phase 3 — Delegate (prompts)**: call the slide-deck generator `--prompts-only`. Inject narrative-brief + a "CONFIRMED CHOICES" metadata block (style/audience/slide-count/language) to prevent re-asking and style drift. Map user style description → generator preset. Post-process: copy prompts to `03-prompts/`, embed FULL style-instructions into every prompt, append `// NARRATIVE GOAL` + `// SPEAKER NOTES`.

**Phase 4 — Prompt review** (recommended): display summary, confirm before image gen.

**Phase 5 — Delegate (images)**: `--images-only`. Visual verify: read first slide PNG, check style consistency + text legibility (test Chinese text). Regenerate single slides as needed.

**Phase 6 — Post-process**: reorganize into `00-上游/ 01-成品/ 02-slides/ 03-prompts/`, extract speaker notes, archive prior versions, final checklist (PDF/PPTX open, numbering, notes coverage, no garbled text).

## Failure log
AI-wrote-content (First Law violation) → collect words first. Too many slides → duration÷2 max. Style drift → full style in every prompt. Flat arc → always Phase 1 first. Unhappy first draft → generate ONE test slide, get approval. Redundant work → delegate visuals, own only narrative.
