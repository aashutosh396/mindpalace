---
name: task-observer
description: "Use when running any multi-step task, agentic workflow, or work session that uses tools to produce deliverables — silently capture skill-improvement opportunities, user corrections, workflow patterns, and methodology worth turning into reusable skills. Also triggers on post-task feedback, skill review, 'observation log', 'skill taxonomy', 'watch for skill opportunities', or the phrase 'one skill to rule them all'. Invoke at the START of task-oriented sessions."
version: 1.0.0
license: CC-BY-4.0
tags: [meta-skill, skill-improvement, observation-log, agentic-workflow, skill-taxonomy, continuous-improvement, self-improving-agents, weekly-review]
source: https://github.com/rebelytics/one-skill-to-rule-them-all
derived_from: awesomeclaude
---

# Task Observer — Continuous Skill Discovery & Improvement

A persistent behavioral layer that notices skill-creation and skill-improvement
opportunities during real task work, logs them silently, and surfaces them for
review. It feeds the skill-creator; it does not replace it. Created by Eoghan
Henn / rebelytics.com, CC BY 4.0.

## When to use
Invoke at the start of ANY task-oriented session (you are about to use tools and
produce deliverables). Observation stays active through active execution,
post-task feedback, meta-discussion about skills/methodology, and reflective
planning. It is NOT active during casual chat or quick factual Q&A.

## Reliable activation
Description matching alone gets missed when the agent is focused on the task.
For reliability, add to CLAUDE.md / project instructions:

> At the start of any task-oriented session (any interaction where you use tools
> and produce deliverables), invoke task-observer before beginning work. When
> loading any skill, check the observation log for OPEN observations tagged to
> that skill and apply their insights even if the skill file isn't updated yet.

On context compaction, the CLAUDE.md trigger re-fires; observations append to the
same log with continuous numbering.

## What to watch for
- NEW skill: reusable multi-step workflow, a methodology the user explains, a
  recurring task type with stable structure, "I always do it this way".
- IMPROVE skill: user correction revealing a missing rule/edge case; a skill's
  workflow proving less efficient than what emerged; a technique worth promoting
  to explicit; a wrong assumption; corrections forming a pattern; the agent
  failing to follow a documented rule (→ needs stronger enforcement, not louder
  wording).
- SIMPLIFY skill: never-relevant sections; one-off rules never validated by
  recurrence; elaborate workflows users skip; dead weight in context;
  contradictory rules; "just in case" complexity that never triggered.
- DO NOT log: one-off corrections that don't generalise; preferences already in
  a skill; tool bugs; anything needing proprietary client info for an
  open-source skill.

## How to log (silently, same turn — never batch)
Append to the log immediately when a correction/insight occurs. Writing is the
enforcement; mental notes are not observations. Flush at workflow checkpoints,
and run a hard checkpoint after every 3rd TodoWrite completion: "have unlogged
observations accumulated?"

Observation format:
```markdown
### Observation [N]: [title]
**Date:** … | **Session context:** … | **Skill:** [name | New skill candidate: working-name]
**Type:** [open-source | internal] | **Phase/Area:** …
**Issue:** what happened / what the user corrected / pattern (enough to understand weeks later)
**Suggested improvement:** concrete change; reference the specific section/rule for existing skills
**Principle:** the generalisable takeaway (most important field — turns one case into reusable insight)
```
Always use the `### Observation NNN:` format and append to the END of the file.
Never insert mid-file; never use alternative ID formats.

### Numbering without collisions (mandatory)
Always re-read the actual log before assigning a number — never trust session
memory. Get the next number, assert it's free, append, then verify post-write:
```bash
PROPOSED=$(( $(grep -oP '### Observation \K\d+' log.md | sort -n | tail -1) + 1 ))   # macOS: grep -o '### Observation [0-9]*' log.md | grep -o '[0-9]*' | sort -n | tail -1
grep -qE "^### Observation ${PROPOSED}:" log.md && { echo "COLLISION"; exit 1; }      # pre-write assertion
# ... append the observation with #${PROPOSED} ...
WRITTEN=$(grep -cE "^### Observation ${PROPOSED}:" log.md)                            # post-write verify (closes TOCTOU race)
# if WRITTEN > 1, a parallel session collided → sed-renumber my (last) line to max+1
```
Pre-write catches stale reads; post-write catches the race between parallel
sessions. Both are required.

## Skill taxonomy (drives confidentiality)
- **Open-source**: client-agnostic, methodology-driven. Needs author block,
  licence (CC BY 4.0 default), feedback pathway, tool-agnostic language,
  built-in enforcement. Default here when in doubt — strip specifics, generalise.
- **Internal**: contains client/project/proprietary info or personal habits. No
  author block or licence needed; keep lean.

The open-source/internal line is a confidentiality boundary. Scrub client names,
URLs, domains, internal terms before any open-source skill ships. Run a final
**cross-product re-identifiability sweep**: two individually-sanitised examples
can together narrow to a real client (matching counts, thin-vertical numbers,
thin-disguise placeholders). Blur counts, widen verticals, drop specific numbers
to ranges.

## Pre-flight / self-enforcement principle
Propagate to every skill you create/improve: if a skill has rules, it must have a
mechanism to enforce them (a re-read/verification step before delivery). Before
surfacing observations, verify each was logged in-session, logged silently,
follows Issue→Suggested→Principle, is correctly typed, and (for open-source)
carries no client-identifying info.

## Surfacing
Default: surface all observations at end of session, grouped by skill, new-skill
candidates listed separately, each with suggested type. Surface earlier if an
observation needs user input, reveals a skill producing wrong output now, or
multiple cluster on one skill. Hand approved items to the skill-creator.

## Acting on observations (log, don't act by default)
Apply observations only in three contexts: (1) the comprehensive review,
(2) explicit user request ("update X", "apply observation #N"), (3) in-session
when a skill is producing wrong output. Otherwise mid-task work produces
observations only.
- **Small/additive/low-risk** (new anti-pattern, clarify wording, fix a fact):
  edit the skill directly.
- **Substantial** (restructure workflows, new capabilities, change methodology):
  hand to skill-creator if available; else use observations as spec and flag for
  manual review.
- **New skills**: skill-creator preferred; decide type early (default
  open-source).

## Comprehensive review (scheduled preferred, in-session 7-day fallback)
Cross-checks all OPEN observations + cross-cutting principles against all skills.
- Interactive (user present): present grouped summary, wait for approval.
- Scheduled (user absent): apply non-escalated observations autonomously; stage
  to `skill-updates/YYYY-MM-DD/{skill}/SKILL.md` (nothing live until user
  uploads). Escalate (report only) for: new-skill creation, removing/restructuring
  content, self-flagged uncertainty, conflicting observations.

Steps: load OPEN observations + active principles → inventory skills (exclude
system skills: docx, pdf, xlsx, pptx, skill-creator, schedule) → map
observation→skill (don't trust only the "Skill" field) → check each principle
against each skill → apply updates (integrate natively, never just append) →
mark applied observations ACTIONED with a note → write today's date to
`last-review-date.txt` → present summary. Observations targeting system skills
route to a `{system-skill}-extras` complementary skill instead of being skipped.

## Cross-cutting principles
When an observation reveals a principle that applies to skills in general, log it
with `Skill: All skills`, surface it, and on approval add it to
`skill-observations/cross-cutting-principles.md`. That file is a mandatory
compliance checklist read before delivering any new/regenerated skill.

## Files & locations (workspace folder = project root in Claude Code)
- `skill-observations/log.md` — the observation log (create on first use)
- `skill-observations/cross-cutting-principles.md` — principle checklist
- `skill-observations/last-review-date.txt` — review timestamp
- `skill-observations/archive/log-YYYY-MM-DD.md` — archived ACTIONED/DECLINED
- `skill-updates/YYYY-MM-DD/{skill}/SKILL.md` — staged updates (keep 2 newest per skill)

Status key: OPEN | ACTIONED | DECLINED. Archival is event-driven on every log
write: entries resolved in a *previous* session/write move to the archive;
entries resolved in the *current* session stay one cycle.

## Gotchas
- Always start skill edits from the LIVE file, not a cached/stale copy; diff
  before overwriting any staged copy or you may silently drop another session's
  additions.
- No persistent storage (web chat): switch to handoff-doc mode — collect
  observations in-session and present a structured handoff doc (decisions,
  full observations, current principles, action items, working artifacts) before
  the session winds down; the user pastes it into the next session.
- Session-start staleness: if `log.md` was modified in the last few hours
  (parallel session), re-read immediately before every append.
