---
name: receiving-code-review
description: "Use when receiving code review feedback and before implementing suggestions — especially if feedback seems unclear or technically questionable. Verify against the codebase first, push back with technical reasoning when wrong, clarify unclear items before touching anything, and never give performative agreement. Triggers: 'address review comments', PR feedback, reviewer suggestions, 'reviewer says', responding to a code review."
version: 1.0.0
license: MIT
tags: [code-review, feedback, pull-request, verification, yagni, technical-rigor, pushback, collaboration]
source: https://github.com/obra/superpowers/tree/main/skills/receiving-code-review
derived_from: awesomeclaude
---

# Code Review Reception

## Overview

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving code review feedback:
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!" (performative)
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)

**INSTEAD:** Restate the technical requirement, ask clarifying questions, push back with technical reasoning if wrong, or just start working (actions > words).

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on unclear items
WHY: Items may be related. Partial understanding = wrong implementation.
```

Example: Asked to "fix 1-6", you understand 1,2,3,6 but not 4,5. Right response: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding." Don't implement the clear ones and ask about the rest later.

## Source-Specific Handling

**From your human partner:** Trusted — implement after understanding. Still ask if scope unclear. No performative agreement. Skip to action or technical acknowledgment.

**From external reviewers** — before implementing, check:
1. Technically correct for THIS codebase?
2. Breaks existing functionality?
3. Reason for the current implementation?
4. Works on all platforms/versions?
5. Does the reviewer understand full context?

If it seems wrong, push back with technical reasoning. If you can't verify, say so: "I can't verify this without [X]. Should I investigate/ask/proceed?" If it conflicts with prior architectural decisions, stop and discuss first. Be skeptical of external feedback, but check carefully.

## YAGNI Check for "Professional" Features

If a reviewer suggests "implementing properly", grep the codebase for actual usage. If unused: "This endpoint isn't called. Remove it (YAGNI)?" If used: implement properly.

## Implementation Order

For multi-item feedback: clarify unclear items FIRST, then implement blocking issues (breaks, security) → simple fixes (typos, imports) → complex fixes (refactoring, logic). Test each fix individually; verify no regressions.

## When To Push Back

Push back when the suggestion breaks existing functionality, the reviewer lacks full context, it violates YAGNI, it's technically incorrect for this stack, legacy/compatibility reasons exist, or it conflicts with architectural decisions.

**How:** technical reasoning not defensiveness, specific questions, reference working tests/code, involve your partner if architectural. If you're uncomfortable pushing back, name the tension and report the issue honestly.

## Acknowledging Correct Feedback

When feedback IS correct:
- "Fixed. [Brief description of what changed]"
- "Good catch — [specific issue]. Fixed in [location]."
- Just fix it and show it in the code

No gratitude expressions ("Thanks for catching that!"). Actions speak — the code shows you heard the feedback. If you catch yourself about to write "Thanks", delete it and state the fix instead.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong: "You were right — I checked [X] and it does [Y]. Implementing now." State the correction factually and move on. No long apology, no defending why you pushed back.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if it breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## GitHub Thread Replies

When replying to inline review comments on GitHub, reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

## The Bottom Line

External feedback = suggestions to evaluate, not orders to follow. Verify. Question. Then implement. No performative agreement. Technical rigor always.
