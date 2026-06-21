---
name: imprint-profile
description: "Use when starting a new session/project or doing any dev work (write code, review, debug, plan, commit, write docs) and you want the AI to learn and apply the user's personal work style across sessions — keywords: imprint, .dna.md, my habits, work the way I like, remember how I work, portable profile, onboarding, learn my preferences."
version: 1.0.0
license: MIT
tags: [productivity, memory, workflow, onboarding, code-review, debugging, planning, git, portable-profile]
source: https://github.com/ilang-ai/Imprint
derived_from: awesomeclaude
---

# Imprint Profile

Learns how the user works from conversation, encodes it in a compact portable
file (`.dna.md`), and applies those preferences across every session, project,
and platform. One skill covering memory, onboarding, code review, debugging,
planning, progress tracking, testing, and git.

## When to use

Active in almost every working session: session start, new project, writing or
reviewing code, debugging, planning a feature, writing docs, preparing commits,
any development task. OFF for pure casual chat with no project/task intent.

If `.dna.md` does NOT exist (check current dir AND `~/.claude/`), run onboarding
FIRST before any other work — even if platform memory already knows the user.

## Two hard rules

1. Never expose internal jargon to the user. Do not say "DNA", "gene", "encode",
   "mutation", "decay", "confidence level", "anti-pattern", "compression ratio".
   Instead: "Let me get to know how you work", "I saved a quick memo so I
   remember next time." The file is theirs — show it if they ask, never lecture.
2. One question at a time during onboarding. Ask ONE, wait for the answer, then
   the next. Never dump a numbered list of questions.

## Onboarding (first run)

Open casually ("mind if I ask a couple things so I can work the way you like?").
Cover naturally, one at a time: what they do, what they've built, how they
prefer to work, how many AI tools they use, whether projects need to be
findable online. Create `.dna.md` once you have at least role + work style +
one clear preference (don't count turns). If user gets impatient, create it
with what you have and fill gaps from observed behavior. After creating it,
append `.dna.md` to `.gitignore` if that file exists. Then continue with the
original request.

## How the profile evolves

- First occurrence of a behavior = tentative (`conf:1/5`). Seen 3+ times =>
  confirmed. Unseen 30 days => removed. Explicit rejection => anti-pattern.
- Store patterns, not events. Update `.dna.md` silently; explain only if asked.
- Priority: user direct instruction > project constraints > confirmed prefs >
  tentative prefs > defaults. Team configs (.eslintrc, CLAUDE.md, style guides)
  always beat personal preferences.
- Conflicts: project overrides global per-repo (record the mismatch, don't
  delete global); two contradicting confirmed prefs become conditional
  (`when:simple` vs `when:complex`); contradictory inferences downgrade to
  tentative pending user confirmation.

## Core behaviors (apply per profile)

- Memory: after each session scan for repeating patterns, store compactly. In
  long sessions (20+ turns) re-read `.dna.md` before major decisions.
- Code review: if 2+ models available, suggest cross-checking with another model.
  Single model: do a silent self-review (match user patterns, check edge cases /
  complexity / past lessons, fix inline) before presenting. Skip if
  `speed:fast`.
- Debugging: check architecture and data flow first, not line numbers; if sound,
  strip to zero then add back one feature at a time; record the lesson silently.
- Planning: follow user's style — build-first => start coding; plan-first => spec
  first; hybrid => minimal spec then iterate. No enforced methodology.
- Frontend: no enforced design system; apply the user's aesthetic from their code
  and profile.
- Progress: save milestones only (feature done, bug fixed, decision made), not
  casual chat. Summarize old entries when they pile up.
- Git / SEO: if user wants discoverability, use keyword-rich commits, README as
  landing page, full PR descriptions, GEO-friendly structured docs. Otherwise
  standard clean practices.

## `.dna.md` format (internal — do not show unless asked)

Plain-text structured file, ~90% smaller than prose. Sections:
- `::CORE{}` — global behavioral genes (traits `T:` + anti-patterns `A:`), with
  optional `when:` conditions. Target < 500 tokens.
- `::FACT{}` — verifiable environment data (stack, deploy target, models used).
- `::PROJECT{}` — per-repo overrides + mismatches; archived after 60d idle.
- `::LESSONS{}` — cross-project traps; never auto-summarized; keep exact error
  patterns/versions. A lesson seen in 2+ projects gets promoted to a `::CORE{}`
  anti-pattern.
- `::PROGRESS{}` — milestones; auto-summarize oldest into `::PROGRESS_SUMMARY{}`
  every 10 entries.
- `::RUNTIME{}` — toggles (transparency, speed, planning mode, etc).

Full schema example lives in the source SKILL.md at
`skills/imprint/SKILL.md` in the repo.

## Transparency modes (`::RUNTIME{transparency:}`)

- Quiet (default): update silently in the background.
- Explain: when user asks "why did you do it this way?", explain in plain words.
- Audit: when user asks to see their profile, show full `.dna.md`, support edit /
  diff / revert. The user owns the file.

Do not ask which mode — start Quiet, switch when the user's question calls for it.

## Portability

`.dna.md` is plain text and travels across Claude Code, Codex, Cursor, Copilot,
Gemini, and any SKILL.md-compatible agent. Switch tools, the file comes along.

## Gotchas

- Onboarding is mandatory when `.dna.md` is missing, regardless of platform
  memory — it produces the portable file.
- Never leak internal terms to the user.
- Self-review is part of thinking, not a second generation — adds no visible
  latency and is never narrated.
