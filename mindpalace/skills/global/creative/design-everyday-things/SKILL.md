---
name: design-everyday-things
description: "Use when diagnosing why a design confuses users or causes mistakes — triggers: 'why is this confusing', 'affordance', 'error prevention', 'discoverability', 'human-centered design', 'fault tolerance', 'mental model', 'mapping', 'seven stages of action', reducing product complexity, improving error messages and feedback."
version: 1.0.0
license: MIT
tags: [ux, affordances, signifiers, mental-models, feedback, error-prevention, human-centered-design, discoverability]
source: https://github.com/wondelai/skills/tree/main/design-everyday-things
derived_from: awesomeclaude
---

# Design of Everyday Things Framework

Don Norman's foundational design principles for intuitive, discoverable, understandable products. Good design is invisible; when something fails users blame themselves, but the fault is almost always the design.

## Core Principle

Great design bridges what people want to do and what the product allows. It is **discoverable** (you can figure out what to do) and **understandable** (you can figure out what happened).

## Scoring

Rate any design 0-10 on discoverability, understandability, and error tolerance. State current score and fixes to reach 10/10.

## The Two Gulfs
- **Gulf of Execution** — "How do I do what I want?" Bridge with: signifiers, natural mappings, constraints, familiar conceptual models.
- **Gulf of Evaluation** — "What happened? Did it work?" Bridge with: immediate visible feedback, clear state indicators, meaningful error messages, progress indicators.

Make both gulfs as narrow as possible.

## Seven Principles
1. **Discoverability** — a new user should know what to do within 10 seconds. If they need a manual, the design failed.
2. **Affordances** — what an object lets you do. Design for *perceived* affordance. Failures: flat design erasing button cues, tiny touch targets, interactive vs decorative looking identical.
3. **Signifiers** — show WHERE/HOW to act (affordance = what you CAN do). Cursor/hover changes, icons + labels, color + position. When in doubt, add a signifier.
4. **Mappings** — control layout should match what it controls (volume up = louder). Use proximity, spatial layout, cultural convention (red=stop), sequential order.
5. **Constraints** — limit actions to prevent errors: input validation (date picker vs free text), disabled states, forced sequence + undo. Make wrong actions impossible rather than punishing them.
6. **Feedback** — communicate results. Must be immediate (0.1s for direct manipulation), informative, dosed, non-intrusive. Response times: 0.1s instant; 1s noticeable (change cursor); 10s loses attention (progress bar); >10s users leave.
7. **Conceptual Models** — design model, user's model, system image (the only bridge). Goal: user's model matches design model. Build with familiar metaphors, visible state, consistent behavior, progressive disclosure.

## Human Error = Bad Design
There is no "human error," only bad design. Look for the design flaw, not the person.
- **Slips** (right intention, wrong action): action slip, memory lapse, mode error, capture error. Fixes: separate destructive actions, attachment reminders, show mode state, interrupt at decision points.
- **Mistakes** (wrong intention): rule-based, knowledge-based, memory lapse. Fixes: provide context, better conceptual model, reminders/history.

**Design for error:** Prevent with constraints, undo/redo, confirmation for destructive actions, sensible defaults, forgiving input. Recover with clear messages, never erasing user work, partial saves, easy reset.

**Error-message checklist:** what went wrong (human language) · how to fix · doesn't blame user · preserves work · offers an alternative path.

## Seven Stages of Action
Goal → Plan → Specify → Perform — (Gulf of Execution) — Perceive → Interpret → Compare (Gulf of Evaluation). Support stages 1-3 with signifiers/mappings/constraints, stage 4 with affordances, stages 5-7 with feedback and visible state. Walk any interaction through each stage to find where users stall.

## Human-Centered Design Process
Observation → Idea Generation → Prototyping → Testing → iterate. Watch real users in context (don't ask what they want); generate many ideas; build cheap disposable prototypes; test with 5 real users (reveals ~85% of problems), observe behavior not opinions.

## Quick Diagnostic
Can users figure out what to do? (else add signifiers/affordances) · Do they understand what happened? (else add feedback/state) · Can they recover from errors? (else add undo/clear messages) · Does control layout match output? (else fix mapping) · Are invalid options hidden/disabled? (else add constraints).
