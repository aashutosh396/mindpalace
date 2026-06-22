---
name: Reflect (Mid-Conversation Reassessment)
description: Use when the user says "step back", "zoom out", "are we missing something", "sanity check", or a conversation has gone deep without strategic check-in — pauses and honestly reassesses direction, assumptions, and bias.
tags: [reflect, step-back, zoom-out, reassessment, bias-check, sanity-check, cognitive-bias, big-picture]
source: alirezarezvani/claude-skills
derived_from: productivity/reflect
---

# Reflect — Mid-Conversation Reassessment

Pause execution and produce a frank reassessment of where the conversation has been heading. Output is **flowing prose (no headers, conversational)**. Ends with a directional recommendation: continue, pivot, or pause.

## Stop directive
Halt the current thread — don't continue execution while "reflecting on the side" (you'd over-weight the current direction). Reflection is a pause, not a side-quest.

## Triggers
Explicit: "reflect", "step back", "zoom out", "are we missing something", "bigger picture", "sanity check this", "are we on track", "are we overthinking this", "forest for the trees". Implicit (10+ detail turns without strategic check-in, frustration, repeated dead-ends): don't auto-invoke — OFFER reflection.

## Low-intake clarifier (only when context too thin)
If invoked with no prior context to reassess, ask once: reassess the goal / approach / assumptions / all (default). Otherwise run the full analysis directly on existing conversation.

## 5-dimension framework (re-read full conversation from original goal, not just recent turns)
1. **Macro perspective** — original goal? drift? how does current work connect to the objective? Anchor with evidence ("at turn 3 goal was X; turn 12 we're on Y — productive narrowing or drift?").
2. **Gap analysis** — unverified assumptions, missing stakeholders/users, skipped constraints, dismissed alternatives, external factors.
3. **Reflective inquiry** — problem framed correctly? right problem vs adjacent easier one? simpler path overcomplicated? harder-but-more-valuable path avoided? fresh-eyes view?
4. **Bias check** — name + cite evidence + corrective move for each: confirmation (only supporting evidence cited), sunk cost ("we've invested X"), anchoring (stuck on first option), complexity (adding without justification), recency (over-weighting last turns).
5. **Contextual alignment** — serves the user's actual goals? best use of their time/energy now?

## Tone rules
Flowing prose, no headers/bullets. Tight but thorough. Direct critique with evidence when warranted; validation with reasoning when warranted. No vague reassurance ("looks good!"). No manufactured problems — if the path is solid, say so with specific reasons.

## Closing recommendation (mandatory, always specific)
- **Continue.** {specific reasoning}.
- **Pivot toward {X}, away from {Y}.** {specific evidence}.
- **Pause for {Q}.** Without answering, next step risks {specific cost}.
