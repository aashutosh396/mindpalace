---
name: Inbox Setup (Triage Onboarding)
description: Use once before inbox-triage — interviews the user (one question at a time) about email patterns, business context, reply voice, and priorities, then builds the 7-file knowledge base that powers triage.
tags: [email, inbox-setup, onboarding, knowledge-base, email-taxonomy, voice-calibration, grill-me, interview]
source: alirezarezvani/claude-skills
derived_from: productivity/email/skills/inbox-setup
---

# Inbox-Setup — Email Triage Onboarding

Run once (re-run when business/priorities change). Interview the user, then generate the structured KB at `${WORKSPACE}/Email/` that `inbox-triage` reads every run. File contracts MUST match between the two skills exactly.

## Conduct discipline
Do NOT generate all files at once — walk the 8 sections one at a time, committing each section's file(s) before moving on (partial completion still produces a usable partial KB). Grill-me: one question per turn (even across section boundaries), "why I'm asking" on every question, forcing/multi-choice format where possible, dependency-ordered.

## Knowledge base contract (files at `${WORKSPACE}/Email/`)
| File | Purpose | Required |
|---|---|---|
| email-taxonomy.md | classification + report preferences | Yes |
| email-patterns.md | reply voice, tone, templates, hard rules | Yes |
| evaluation-framework.md | decision tree for opportunity emails | only if pitches received |
| rate-card.md | pricing/terms/negotiation | only if pricing exists |
| blocklist.md | auto-skip senders + learned patterns | Yes (seeded, grows) |
| tracker.md | active follow-ups, overdue, deadlines | Yes (starts empty) |
| triage-log/ | per-run logs | Yes (empty dir) |

## 8 sections (~25-31 questions, hard ceiling 35)
1. **Big picture** — role/business, dominant categories, volume split, addresses covered, run frequency (drives default search window), helpers/solo.
2. **Categories** — propose 5-7 (New Opportunities, Active Conversations, Action Required, Financial, Important/Personal, Informational, Ignore); confirm yes/mostly/no, missing categories, most-time category. → email-taxonomy.md.
3. **Reply style & voice** — register, 3 pet peeves (forbidden tokens), always-used phrases/sign-offs, persona, typical length, hard rules. **Critical: ask for 3-5 real sent emails** (self-description of voice is unreliable; real samples are the best signal). → email-patterns.md.
4. **Evaluation framework (conditional — only if opportunity emails are a category)** — gut filter, 3 deal-breakers (PASS-auto), 3 instant-interest (TAKE-IT), pricing/terms, negotiation posture, VIP senders. → evaluation-framework.md (+ rate-card.md if pricing).
5. **Blocklist** — always-skip senders/domains, delete patterns, time-wasting companies. → blocklist.md.
6. **Current state** — active threads, overdue replies, deadlines. → tracker.md.
7. **Report preferences** — delivery format, detail level, always-show-first items. → into email-taxonomy.md.
8. **Confirmation & handoff** — list files created; tell user to run inbox-triage; remind first runs need oversight.

## Privacy boundary
Never persist passwords, full account numbers, SSNs, or credentials. If volunteered, acknowledge but write `[stored separately by user]` in place.

## Re-run behavior
Detect existing `${WORKSPACE}/Email/`; ask per-file replace/merge/skip; walk only the chosen sections.
