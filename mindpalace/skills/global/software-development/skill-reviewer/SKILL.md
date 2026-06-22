---
name: Claude Code Skill Reviewer
description: Use when checking skill quality, reviewing a skill repository, or contributing improvements to an open-source skill — validates against official best practices in three modes (self-review, external review, auto-PR), additive-only.
tags: [skill, review, claude-code, best-practices, validation, frontmatter, pr, additive, quality-gate]
source: daymade/claude-code-skills
derived_from: skill-reviewer
---

Review and improve Claude Code skills against official best practices.

## Three modes
- **Self-review** — check your own skill before publishing: run automated validation (quick_validate + security_scan from skill-creator) then the manual checklist.
- **External review** — clone to /tmp/, read ALL docs first, identify the author's intent, run the checklist, generate an improvement report.
- **Auto-PR** — `gh repo fork` → feature branch → apply additive improvements only → self-review respect-check → PR with detailed explanation.

## Evaluation checklist
| Category | Check |
|----------|-------|
| Frontmatter | name present? description present? description in third-person? includes trigger conditions? |
| Instructions | imperative form? under 500 lines? has a workflow pattern? |
| Resources | no hardcoded paths? scripts have error handling? |

## Core principle: ADDITIVE ONLY (for external skills)
NEVER delete files, remove functionality, change primary language, or rename components. ALWAYS add new capabilities, preserve original content, explain every change.
```
❌ "Removed metadata.json (non-standard)"   ✅ "Added marketplace.json (metadata.json preserved)"
❌ "Rewrote README in English"              ✅ "Added README.en.md (Chinese preserved as default)"
```

## Common issues & fixes
- **Description not third-person:** "Browse YouTube videos and summarize" → "Browses YouTube videos and generates summaries. Use when...".
- **Missing trigger conditions:** "Processes PDF files" → "Extracts text from PDFs. Use when working with PDFs, forms, or document extraction".
- **No workflow pattern:** add a copy-the-checklist block for complex tasks.

## PR guidelines
Tone: frame as alignment with best practices, never "your skill doesn't follow best practices". Required sections: Summary / What's NOT Changed (show respect) / Rationale (why each change helps) / Test Plan.

## Self-review respect check (before any PR)
No files deleted? No functionality removed? Original language preserved? Author's design decisions respected? All changes additive? PR explains the "why"?
