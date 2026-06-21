---
name: manage-memory
description: "Use when an agent's persistent memory (MEMORY.md / memory directory) is approaching the ~200-line truncation limit, after a session produces durable insights worth keeping, when a topic section grew beyond ~10-15 lines and should be extracted to its own file, or when project state changed and memory entries may be stale. Triggers: MEMORY.md, persistent memory, memory file, stale memory, extract topic, prune memory, 200-line limit, remember this."
version: 1.0.0
license: MIT
tags: [memory, persistence, organization, maintenance, claude-code, staleness, knowledge-management]
source: https://github.com/pjt222/agent-almanac/tree/main/skills/manage-memory
derived_from: awesomeclaude
---

# Manage Memory

Keep an agent's persistent memory accurate, concise, and useful across sessions. MEMORY.md is loaded into the system prompt every conversation — lines after ~200 are truncated, so it must be a lean index pointing to topic files.

## When to Use

- MEMORY.md approaching the 200-line truncation threshold
- A session produced durable insights (patterns, decisions, debugging fixes)
- A topic section grew beyond ~10-15 lines and should be extracted
- Project state changed (renamed files, new counts) and entries may be stale
- Starting new work; checking whether relevant memory already exists

## Procedure

### Step 1 — Assess current state
Read MEMORY.md, check its line count against the 200-line limit, and inventory existing topic files. Create a minimal MEMORY.md (`# Project Memory` + `## Topic Files`) if none exists.

### Step 2 — Identify stale entries
Compare claims against current state. Watch for count drift, renamed paths, superseded workarounds, and contradictions. Spot-check with grep/ls. If a claim can't be verified, add `(unverified)` rather than silently keeping it.

### Step 3 — Decide what to add
Apply four filters: Durable (true next session, not session-specific), Non-duplicating (not already in CLAUDE.md/docs), Verified (confirmed across interactions or checked against docs), Actionable (knowing it changes behavior). Exception: if the user says "remember this", save immediately.

### Step 4 — Extract oversize topics
When a section exceeds ~10-15 lines, move detail to `<memory-dir>/<topic>.md` (lowercase kebab-case, named by topic not date) and leave a 1-2 line summary + link in MEMORY.md. Don't extract sections under ~5 lines.

### Step 5 — Update MEMORY.md
Remove stale entries, add filtered new ones, fix counts, and keep the Topic Files section complete and last. Each bullet 1-2 lines; most-needed context first; use inline `code`/**bold** for scannability.

### Step 6 — Verify integrity
Confirm under 200 lines, every referenced topic file exists (no broken links), no orphan files, and 2-3 spot-checked claims are accurate.

## Validation

- [ ] MEMORY.md under 200 lines
- [ ] All referenced topic files exist; no orphans
- [ ] No stale counts or renamed paths
- [ ] New entries meet durable/non-duplicate/verified/actionable
- [ ] Topic files have descriptive headers and are self-contained
- [ ] Reads as a quick-reference, not a changelog

## Common Pitfalls

- Memory pollution — writing every session observation; apply the four filters.
- Stale counts — verify against the source of truth.
- Chronological organization — organize by topic, not date.
- Duplicating CLAUDE.md — memory captures what CLAUDE.md doesn't.
- Over-extraction — only extract sections over ~10-15 lines.
- Forgetting the 200-line limit — content past it is silently truncated.

## Related

- coordinate-reasoning, manage-token-budget — companion agent-hygiene skills
