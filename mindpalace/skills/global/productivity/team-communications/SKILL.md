---
name: Internal Team Communications
description: Use when drafting or formatting internal company comms — 3P updates, newsletters, FAQ roundups, incident reports, status/leadership updates ("write my update", "summarize what my team did this week").
tags: [internal-comms, 3p-update, newsletter, status-report, faq, weekly-update, leadership, team-update, incident-report]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/team-communications
---

# Internal Team Communications

Write polished internal comms by matching the company's exact format, gathering real context, and outputting tightly.

## Routing — identify the type first

| Type | Trigger phrases | Format to follow |
|---|---|---|
| 3P Update | "3P", "progress plans problems", "weekly team update", "what did we ship" | Progress / Plans / Problems, per team, time-boxed |
| Newsletter | "newsletter", "company update", "weekly/monthly roundup", "all-hands summary" | Headline + sectioned roundup with links/metrics |
| FAQ | "FAQ", "common questions", "what people are asking", "confusion around" | Q → concise A, grouped by theme |
| General | anything internal not matching above | Headline-first, scannable bullets |

If type is ambiguous, ask one clarifying question — don't guess.

## Workflow

1. Match the type and its format above. Follow it exactly — do not invent a new format.
2. Gather inputs. Pull real data from connected tools (Slack, Gmail, Drive, Calendar). If none connected, ask the user for bullet points / raw context.
3. Clarify scope: team name (for 3Ps), time period, audience, must-include/exclude items.
4. Draft to the format, tone, and length constraints.
5. Present the draft; ask what to add, remove, or reword.

## Tone & style (all types)

- Use "we" — you are part of the company.
- Active voice. Present tense for progress, future tense for plans.
- Concise — every sentence carries information. Cut filler.
- Include metrics and links wherever possible.
- Professional but approachable. Most important info first.

## When tools are unavailable

Don't stall. Ask the user to paste/describe what to cover — formatting and sharpening is still valuable. Mention which tools would improve future drafts.

## Anti-patterns

- Writing before matching the format → output needs reformatting. Lock the format first.
- Inventing metrics or accomplishments → fabrication destroys trust. Only use provided/retrieved data.
- Passive voice for accomplishments ("the feature was shipped" hides who did it) → "Team X shipped Y".
- Walls of text → leadership scans. Lead with the headline, then 3-5 bullets.
- Sending without confirming audience → team update reads differently than company-wide. Always confirm who reads this.
