# _skillforge — skill harvesting & training workspace

Temporary staging area for importing high-value Claude skills from
[awesomeclaude.ai](https://awesomeclaude.ai/awesome-claude-skills) into mindpalace's
auto-detected global skill library. Once a batch is installed + verified, this folder
can be deleted — installed skills live in `mindpalace/skills/global/<category>/<slug>/SKILL.md`.

## Pipeline
1. **P1 (this):** `MANIFEST.json` — the curated list (individual skills + collections to mine).
2. **P2:** harvest each skill's `SKILL.md` (+ scripts) → convert to mindpalace format → `staging/<category>/<slug>/SKILL.md`.
3. **P3:** validate frontmatter + auto-detection (`skills.match()`), dedup vs existing globals, install.
4. **P4:** ralph-wiggum goal-loop.

## Target format (every installed skill)
`mindpalace/skills/global/<category>/<slug>/SKILL.md`:

```markdown
---
name: <slug>                 # kebab-case, unique
description: "<ONE line, 'use when …' phrasing — this drives skills.match() auto-detection>"
version: 1.0.0
license: <source license or MIT>
tags: [<5-10 keywords the owner might say>]
source: <source repo URL>
derived_from: awesomeclaude
platforms: [<macos|linux>]   # only if OS-specific
prerequisites:
  commands: [<cli deps>]     # only if any
---

# <Human Title>

<Adapted instructions: what it does, WHEN to use it, how to use it (commands/steps),
key gotchas. Trim vendor fluff/marketing. Keep scripts under scripts/ if essential.>
```

## Rules for conversion
- The **description** is the most important field — it's what auto-detection matches.
  Write it as "use when the owner wants to …" with the real trigger words.
- **Skip** vendor-locked / niche skills (crypto wallets, single-SaaS connectors, blockchain).
- **Dedup** against existing globals (don't re-add TDD, systematic-debugging, llm-wiki,
  deep-research, google-workspace, etc. — see `skills/global/`).
- Keep bodies lean; pull only essential `scripts/` (no node_modules, no large assets).
- Preserve attribution via `source:` + `license:`.

## Categories (existing + new)
existing: apple, research, social-media, devops, data-science, software-development,
mlops, github, note-taking, creative, email, smart-home, autonomous-ai-agents,
productivity, media
new: documents, writing, security, project-management
