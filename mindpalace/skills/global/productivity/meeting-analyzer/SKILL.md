---
name: Meeting Transcript Analyzer
description: Use when given meeting transcripts (.txt/.md/.vtt/.srt/.docx from Zoom/Otter/Granola/Fireflies) or asked for feedback on communication habits, speaking ratios, filler words, or how you come across in meetings.
tags: [meetings, transcript, communication-coaching, speaking-ratio, filler-words, facilitation, listening, conflict-avoidance, zoom, otter]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/meeting-analyzer
---

# Meeting Transcript Analyzer

Turn meeting transcripts into evidence-backed feedback on communication patterns, leadership behaviors, and dynamics.

## Workflow

### 1. Ingest & inventory
Scan for transcript files (`.txt .md .vtt .srt .docx .json`). Per file extract: date (filename `YYYY-MM-DD` or timestamps), speaker labels (`Speaker 1:`, `[John]:`, VTT `<v Name>`), the user's identity (ask if ambiguous; don't guess), duration, participant count, word count. Print an inventory table; confirm scope before heavy analysis.

### 2. Normalize
Convert every format into `{ speaker, timestamp_sec|null, text }[]`. VTT/SRT → parse cues. Plain/markdown → `Name:`/`[Name]` prefixes. DOCX/JSON → extract then treat as plain. If no timestamps, skip timing metrics but keep text analysis. If no speaker labels, warn and skip per-speaker metrics.

### 3. Analyze (run only applicable modules)

**Speaking dynamics** — per speaker: word count & %, turn count, avg turn length, longest monologue (flag >60s or >200 words), interruptions (turn starting within 2s of prior speaker / mid-sentence). Red flags: user >60% in 1:many (dominating); user <15% when facilitating; a participant who never speaks; interruption ratio >2:1.

**Conflict & directness** — scan user's speech for hedging (maybe, sort of, I guess), permission-seeking (if that's okay), deflection (whatever you think), pre-disagreement softeners. Flag conflict-avoidance patterns (topic change after tension, agreement-without-commitment, minimizing others' concerns, absent feedback in 1:1s). Per instance: full quote with ±2 turns context, severity (low/medium/high), and a more-direct rewrite.

**Filler words** — count um/uh/like/you know/actually/basically/literally/right?/I mean. Report total, rate per 100 words, by type, contextual spikes. Only flag if rate >3 per 100 words.

**Question quality & listening** — classify questions: closed / leading / open-genuine / clarifying / building. Good listening: clarifying+building questions, paraphrasing, referencing earlier points, drawing in quiet people. Poor: re-asking answered questions, restating without acknowledging, off-topic replies. Report open/clarifying/building vs closed/leading ratio.

**Facilitation** (only if user is organizer) — agenda adherence, time per topic, inclusion of quiet voices, explicit decisions, action items with owners+deadlines, parking-lot discipline.

**Sentiment & energy** — track positive/negative/flat markers; flag energy drops (shorter, less substantive turns) which often signal discomfort or avoidance.

### 4. Report
Markdown with: header (period, count, total words, avg speaking share), Top 3 Findings (each with quote + timestamp), Detailed Analysis (one section per run module), Strengths (3 with evidence), Growth Opportunities (3 ranked, each with what to change / why / "try this next time"), and Comparison to Previous Period if prior data exists.

### 5. Follow-up
Offer: deep dive on one meeting/pattern, a 1-page cheat sheet of top 3 habits, baseline-tracking setup, export to markdown/JSON.

## Edge cases & guards
- No speaker labels → warn upfront, text-level only, suggest re-export with diarization.
- Short meetings (<5 min / <500 words) → analyze but caveat representativeness.
- Non-English → filler/hedging dictionaries are English-centric; focus on structure.
- Single meeting → no trend language; findings about that meeting only. Require 3+ for coaching trends.
- Weight speaking-ratio targets by role: facilitators SHOULD talk less, presenters more — equal time is not the goal.
- Distinguish decision meetings (hedges bad) from ideation (hedges fine).
