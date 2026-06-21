---
name: meeting-insights
description: "Use when analyzing meeting transcripts/recordings to surface communication patterns, speaking ratios, filler words, interruptions, conflict avoidance, active listening, or facilitation feedback — triggers: 'analyze my meetings', 'meeting transcript', 'when did I avoid conflict', 'speaking ratio', 'filler words', 'facilitation style', 'communication patterns', 'Granola/Zoom/Otter/Fireflies transcript'."
version: 1.0.0
license: MIT
tags: [meetings, transcripts, communication, feedback, leadership, facilitation, coaching, analysis]
source: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/meeting-insights-analyzer
derived_from: awesomeclaude
---

# Meeting Insights

Turn meeting transcripts into actionable feedback on the user's communication and
leadership patterns: conflict avoidance, speaking ratios, filler words,
interruptions, active listening, and facilitation.

## When to use

- User points to a folder of transcripts and asks what patterns show up
- Requests like: "when did I avoid conflict", "what's my speaking vs listening
  ratio", "how often do I interrupt", "do I use too many filler words", "analyze
  my facilitation style", "compare Q1 vs Q2 meetings"
- Prepping performance reviews with concrete, timestamped examples
- Coaching a report on their communication style

## Workflow

1. **Discover data** — scan the folder for transcript files (`.txt`, `.md`,
   `.vtt`, `.srt`, `.docx`). Check for speaker labels + timestamps, confirm the
   date range, and identify the user's own name/identifier in the transcripts.

2. **Clarify goal** — if unspecified, ask which to focus on: specific behaviors
   (conflict avoidance, interruptions, filler words), communication effectiveness
   (clarity, directness, listening), facilitation skills, or speaking patterns.
   One behavior at a time gives deeper analysis.

3. **Analyze patterns** — for each requested insight:
   - **Conflict avoidance**: hedging ("maybe", "kind of", "I think"), indirect
     phrasing, subject changes when tension rises, agreement without commitment
     ("yeah, but…"), not naming obvious problems.
   - **Speaking ratios**: % of meeting the user speaks, interruptions given vs
     received, average turn length, question-vs-statement ratio.
   - **Filler words**: count "um", "uh", "like", "you know", "actually"; note
     frequency and when it spikes (nervous/uncertain).
   - **Active listening**: references to others' prior points, paraphrasing,
     building on contributions, clarifying questions.
   - **Leadership/facilitation**: directive vs collaborative decisions, how
     disagreement is handled, inclusion of quiet participants, agenda/time
     control, action-item clarity.

4. **Give specific examples** — per pattern: a one-line finding, frequency
   ("X times across Y meetings"), then 2-3 strongest examples each with:
   meeting/date + timestamp, the actual quote, why it matters, and a better
   approach (concrete alternative phrasing).

5. **Synthesize** — close with a summary: analysis period, # meetings, key
   patterns (observed / impact / recommendation), communication strengths,
   growth opportunities, speaking statistics (avg speaking time, questions/mtg,
   filler/min, interruptions given/received), and 3-5 concrete next steps.

6. **Offer follow-up** — track the same metrics over time, deep-dive a single
   meeting, build a development plan, or generate performance-review material.

## Output template (per pattern)

```markdown
### [Pattern Name]
**Finding**: [one sentence]
**Frequency**: [X times across Y meetings]
**Examples**:
1. **[Meeting / Date]** — [Timestamp]
   **What Happened**: > [quote]
   **Why This Matters**: [impact / missed opportunity]
   **Better Approach**: [alternative phrasing or behavior]
```

## Getting transcripts (setup tips)

- **Granola** — auto-transcribes; export to a folder, point here.
- **Zoom** — enable cloud recording + transcription, download VTT/SRT.
- **Google Meet** — Docs auto-transcription, save as `.txt`.
- **Fireflies.ai / Otter.ai** — bulk-export transcripts to a local folder.
- Name files `YYYY-MM-DD - Meeting Name.txt`; review monthly/quarterly for trends.
- Keep sensitive meeting data local.

## Gotchas

- Reliable speaking ratios and interruption counts need speaker labels +
  timestamps. If the transcript lacks them, say so and give qualitative findings
  instead of fabricated stats.
- Always quote real lines from the transcripts — never invent examples or
  numbers. If a metric can't be derived, state that.
- Ask one behavior at a time when the user wants depth rather than a broad sweep.
