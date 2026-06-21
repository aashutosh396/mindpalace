---
name: expert-interview
description: "Use when extracting first-party expertise from a subject-matter expert before writing content, a case study, a talk, or training material. A pure conversation skill — targeted questions that pull out contrarian takes, specific examples, and surprising outcomes an AI can't fabricate. Produces a reusable knowledge document. Triggers: interview me, extract my expertise, knowledge extraction, capture what I know, source material for an article, subject-matter expert interview."
version: 1.0.0
license: MIT
tags: [interview, knowledge-extraction, content, expertise, eeat, writing, research, first-party]
source: https://github.com/inhouseseo/superseo-skills/tree/main/skills/expert-interview
derived_from: awesomeclaude
---

# Expert Interview

Extracts unique expertise through targeted questions and produces a structured knowledge document. Feed it into `write-content` or `improve-content`, or use it standalone for presentations, case studies, or training. No data, no research, no URL fetching — just good questions and active listening.

## When to use

You (or a client/expert) know things from experience that no web search would surface, and you want them captured before writing.

## Input

Topic to discuss (required — ask if not given). Optionally what the knowledge is for (blog article, case study, thought leadership, training).

## How to conduct it

Ask 2–4 questions, ONE at a time. Pick and adapt — don't ask all of them. Quality is depth, not breadth: 2–3 excellent answers beat 8 shallow ones.

**Core questions (pick 2–3):**
1. "What do most people get wrong about [topic]?" — forces a contrarian/non-obvious take.
2. "Can you give me a specific example — a client, a project, a number?" — extracts unfabricatable first-party data.
3. "What surprised you when you actually did this?" — gets unexpected results and failure stories.
4. "Who should NOT follow this advice, and why?" — forces nuance via scope limits.

**Adapt to topic type:**
- Technical/how-to → "What error do people hit first?" / "What step do beginners always skip?"
- Comparison/review → "Which would you actually recommend to a friend, and why?" (the real answer, not the official one)
- Thought leadership → lean on the contrarian question; add "Where is this heading in 2 years?"
- Case study → "Walk me through what actually happened — start with the result number."

**Follow up on interesting answers:** "You mentioned X — what happened exactly?" / "How did that compare to what you expected?" / "Can you put a number on that?"

Ask one question, wait for the answer, then proceed. Adapt style: newer/less-experienced user → explain why each question matters; experienced user → fast and direct.

## Output

Organize answers into a structured knowledge document:

**Expert Knowledge: [topic]**
- **Key insight / contrarian take** — what they know that others don't.
- **Specific examples and data points** — real numbers, the actual client, the exact project.
- **Experience details** — what worked, what failed, what surprised.
- **Scope and limitations** — who this applies to, who it doesn't, when it breaks down.

Pass this document directly to `write-content` or `improve-content` as context; the writing skills weave the first-person material in.

## Language

Conduct the interview in whatever language the user responds in.
