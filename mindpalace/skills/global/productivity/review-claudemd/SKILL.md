---
name: review-claudemd
description: "Use when the user wants to review, improve, audit, or update CLAUDE.md files based on recent sessions — phrases like 'review my CLAUDE.md', 'improve CLAUDE.md', 'what should I add to CLAUDE.md', 'find violated instructions', or 'mine conversation history for memory rules'."
version: 1.0.0
license: Proprietary (YK Sugi, All Rights Reserved)
tags: [claudemd, memory, conversation-history, audit, self-improvement, productivity, jsonl, subagents]
source: https://github.com/ykdojo/claude-code-tips/tree/main/skills/review-claudemd
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [jq]
---

# Review CLAUDE.md from conversation history

Mine recent Claude Code conversations to find concrete improvements for both the
global (`~/.claude/CLAUDE.md`) and local (project `./CLAUDE.md`) memory files.

## When to use

- User asks to "review", "audit", "improve", or "update" their CLAUDE.md.
- After a stretch of work where the agent repeatedly missed or violated standing
  instructions, and the user wants the memory file tightened.
- User wants to discover recurring project patterns worth promoting into memory.

Do NOT auto-edit the CLAUDE.md files — produce findings, then ask before drafting edits.

## How it works

### Step 1 — Locate conversation history

Conversation logs live in `~/.claude/projects/`. The folder name is the absolute
project path with every `/` replaced by `-`.

```bash
PROJECT_PATH=$(pwd | sed 's|/|-|g')      # leading slash becomes a leading dash
CONVO_DIR=~/.claude/projects/${PROJECT_PATH}
ls -lt "$CONVO_DIR"/*.jsonl | head -20
```

### Step 2 — Extract recent conversations to plain text

Pull the 15-20 most recent `.jsonl` logs (skip the current session) into a scratch
dir, flattening each into readable USER/ASSISTANT turns:

```bash
SCRATCH=/tmp/claudemd-review-$(date +%s)
mkdir -p "$SCRATCH"

for f in $(ls -t "$CONVO_DIR"/*.jsonl | head -20); do
  base=$(basename "$f" .jsonl)
  jq -r '
    if .type == "user" then
      "USER: " + (.message.content // "")
    elif .type == "assistant" then
      "ASSISTANT: " + ((.message.content // []) | map(select(.type=="text") | .text) | join("\n"))
    else empty end
  ' "$f" 2>/dev/null | grep -v "^ASSISTANT: $" > "$SCRATCH/${base}.txt"
done

ls -lhS "$SCRATCH"
```

### Step 3 — Analyze with parallel subagents

Launch Sonnet subagents (batched by file size) to compare the conversations
against both CLAUDE.md files. Batching guide:
- Large files (>100KB): 1-2 per agent
- Medium (10-100KB): 3-5 per agent
- Small (<10KB): 5-10 per agent

Per-agent prompt:

```
Read:
1. Global CLAUDE.md: ~/.claude/CLAUDE.md
2. Local CLAUDE.md: <project>/CLAUDE.md (if it exists)
3. Conversations: <list of files>

Compare the conversations against BOTH CLAUDE.md files. Find:
1. Instructions that exist but were VIOLATED (need reinforcement or rewording)
2. Patterns to ADD to LOCAL CLAUDE.md (project-specific)
3. Patterns to ADD to GLOBAL CLAUDE.md (applies everywhere)
4. Anything in either file that is OUTDATED or unnecessary

Be specific. Output bullet points only.
```

### Step 4 — Aggregate and present

Combine agent outputs into four sections:

1. **Instructions violated** — existing rules that weren't followed (need stronger wording)
2. **Suggested additions — LOCAL** — project-specific patterns
3. **Suggested additions — GLOBAL** — patterns that apply everywhere
4. **Potentially outdated** — items that may no longer be relevant

Present as tables or bullets. Then ask the user whether to draft the edits.

## Gotchas

- The project folder name uses the FULL absolute path with `/` → `-`; macOS paths
  keep a leading dash. Verify the dir resolves before looping.
- Exclude the current conversation so the review doesn't recurse on itself.
- Requires `jq`; the extraction silently drops malformed lines (`2>/dev/null`).
- Local `./CLAUDE.md` may not exist — agents should treat it as optional.
- Clean up the `/tmp/claudemd-review-*` scratch dir when done.
