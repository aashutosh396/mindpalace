---
name: Write a Skill
description: Use when creating, writing, or authoring a new agent skill — gather requirements, draft SKILL.md with progressive disclosure, write a trigger-rich description, and decide when to add scripts or split files.
tags: [skill-authoring, write-a-skill, skill-md, progressive-disclosure, description, agent-skills, meta]
source: alirezarezvani/claude-skills
derived_from: engineering/write-a-skill (Matt Pocock, MIT)
---

# Write a Skill

Create agent skills with proper structure, progressive disclosure, and bundled resources.

## Process
1. **Gather requirements** — what task/domain it covers; what specific use cases; needs executable scripts or just instructions; any reference materials to include.
2. **Draft** — SKILL.md with concise instructions; reference files only if content exceeds ~500 lines; utility scripts only for deterministic operations.
3. **Review with user** — does it cover the use cases; anything missing/unclear; any section to expand or trim.

## Structure
```
skill-name/
├── SKILL.md          # main instructions (required)
├── REFERENCE.md      # detailed docs (if needed)
├── EXAMPLES.md       # usage examples (if needed)
└── scripts/          # utility scripts (if needed)
```

SKILL.md template: frontmatter (`name`, `description`) → `# Skill Name` → `## Quick start` (minimal working example) → `## Workflows` (step-by-step with checklists) → `## Advanced features` (link to separate files).

## Description requirements (the only thing the agent sees when choosing a skill)
Give the agent enough to know (1) what capability this provides, (2) when/why to trigger it (keywords, contexts, file types). Format: max 1024 chars, third person, first sentence = what it does, second sentence = "Use when [specific triggers]".
- Good: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- Bad: "Helps with documents." (no way to distinguish from other document skills)

## When to add scripts
Operation is deterministic (validation, formatting) · same code would be generated repeatedly · errors need explicit handling. Scripts save tokens and improve reliability over generated code.

## When to split files
SKILL.md exceeds ~100 lines · content has distinct domains (finance vs sales schemas) · advanced features rarely needed.

## Review checklist
- [ ] Description includes triggers ("Use when...")
- [ ] SKILL.md under ~100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep
