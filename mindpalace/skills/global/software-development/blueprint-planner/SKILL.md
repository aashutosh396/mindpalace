---
name: blueprint-planner
description: "Use when starting a new feature/change and you want a written implementation plan or spec before coding — triggers: 'plan this feature', 'write a spec', 'blueprint', 'ask me clarifying questions first', 'don't code yet, plan it', 'one-shot plan for the agent'."
version: 1.0.0
license: MIT
tags: [planning, spec, implementation-plan, clarifying-questions, codebase-exploration, qa, software-design, blueprint]
source: https://github.com/imbue-ai/blueprint
derived_from: awesomeclaude
---

# Blueprint Planner

Planning copilot. Before writing any code, explore the codebase, ask the user
multiple-choice clarifying questions in rounds, then generate a markdown
implementation plan the agent can execute in one shot. You enumerate the choices;
the user makes the decisions and decides when planning is done.

## When to use

- User wants a plan/spec written before implementation.
- A change has real design choices that should be settled up front.
- User says "plan it first", "don't code yet", "ask me questions", "blueprint".

## Hard rules

- Do NOT write or modify code during planning — you are only gathering info.
- Do NOT decide when Q&A is done. ONLY the user ends it (by asking to generate the plan).
- Gather facts before asking — if code/docs/APIs answer a question, find it yourself.
- Ground every question in what you actually read in the codebase. Never ask what's obvious from the code.

## Phase 1 — Q&A session (explore + plan)

1. Parse the feature description from the user's message.
2. Pick a template. Two built-in shapes:
   - **Default**: Overview, Expected behavior, Implementation plan, Implementation phases, Testing strategy, Open questions.
   - **Concise**: Overview, Expected behavior, Changes.
   Offer these plus an "Other" (custom) option. Ask this template question ONCE only.
3. Explore the project for real — structure, key modules, architecture, existing
   patterns/conventions, and the files relevant to the request. Read actual source.
4. Ask 3-5 clarifying questions (multiple-choice, labelled `1a/1b/...`). Match the
   template's level/perspective: if it asks about external behavior, ask about
   external behavior; only ask about implementation details if the template calls
   for them. Assume the user wants to extend existing patterns — only question a
   pattern when the change clearly conflicts with it.
   - Before the questions, add:
     `> Answer with shorthand like \`1a, 2b, 3e, 4a, 5b\` or write freely.`
   - After the questions, remind the user that more rounds follow and that they
     end the Q&A by asking to generate the plan.
5. Continue in rounds. Accept shorthand, prose, or mixed answers. If the user
   replies with their own question, answer it first. Each round:
   - Acknowledge briefly.
   - Show the **refined prompt** in a blockquote — the original feature
     description plus `*` bullets capturing every clarification so far.
   - Ask 3-5 more questions (follow-ups or new topics) in the same format.
   - Keep looping until the user says to generate.

Progress line — append to EVERY message once a feature + template are set
(not during template selection):
```
✓ Explore  ● Plan  ○ Write  ○ Refine
```

## Phase 2 — Generate plan (write + refine)

Triggered only when the user explicitly asks to generate / finish planning.

1. Recall the chosen template.
2. Make a slug: 2-5 word kebab-case, lowercase, alphanumeric + hyphens, max 50
   chars, no leading/trailing hyphens. If `blueprint/<slug>` exists, append
   `-2`, `-3`, etc.
3. `mkdir -p blueprint/<slug>`
4. Use the latest refined prompt (generate one now if it was never shown).
5. Write the plan markdown into `blueprint/<slug>/` following the template's
   section structure and the level/detail it implies.
6. Offer refinement — let the user iterate on the written plan.

Progress line during write phase:
```
✓ Explore  ✓ Plan  ● Write  ○ Refine
```

## Notes / gotchas

- Keep inter-question text to a sentence or two of context — not a full analysis.
- Questions should make the user think and surface choices they wouldn't have
  asked about; start broad, get more specific as the plan firms up.
- Source repo ships reference files used by the original skill (templates,
  question format, refine-prompt rules, write-plan/refinement guides) under
  `skills/blueprint/references/` and `skills/blueprint-generate/references/` at
  https://github.com/imbue-ai/blueprint — consult them for exact phrasing if needed.
- Agent-agnostic (skills.sh format); works across Claude Code, Codex, Gemini CLI, etc.
