---
name: interview-prep
description: Use when prepping for an interview at a specific company + role — researches the real interview process (rounds, format, difficulty, reported questions), maps each round to an audience (recruiter / hiring-manager / peer-tech / panel), drafts candidate-specific answers from your CV, and maps your story bank to likely questions. Triggers on "prep for my interview", "interview at {company}", "what will they ask", "interview questions for {role}", "company interview process".
version: 1.0.0
license: MIT
tags: [job-search, interview-prep, behavioral, system-design, star, glassdoor, recruiter-screen, hiring-manager]
source: https://github.com/santifer/career-ops
derived_from: awesomeclaude
---

# Interview Prep — Company-Specific Intelligence

Run when prepping for a specific company+role interview. Inputs: company + role (required), any existing evaluation report (for archetype/gaps), a story bank, the CV, and the candidate profile.

## Step 1 — Research
Run targeted web searches; extract structured data, cite every claim. Cover all three audiences (the first round is usually a recruiter screen, not a technical panel):
- **Recruiter/HR:** comp ranges (Levels.fyi, Glassdoor/Salary), process timeline + screening questions (Glassdoor reviews), candid leverage/negotiation notes (Blind), official benefits/visa/location policy (careers page).
- **Hiring manager:** engineering/team blog (recent work, named challenges), company news/launches/roadmap (last 12 months), HM round structure.
- **Peer/technical panel:** reported questions and difficulty (Glassdoor), specific coding/system-design problems and round structure (LeetCode discuss), technical hiring bar (Blind).

If the company is small/obscure, broaden to the archetype at similar-stage companies and note sparse intel — but always do the recruiter-screen comp/logistics queries (data exists for almost everyone).

**Never fabricate questions.** Report what sources say; tag JD-derived questions `[inferred from JD]` and inferred audience classifications `[inferred]`.

## Step 2 — Process overview
Rounds count + end-to-end days, format (e.g. recruiter screen → technical phone → take-home → onsite → HM), difficulty X/5 (Glassdoor avg + N reviews), positive-experience rate, known quirks, sources. Missing field → "unknown — not enough data".

## Step 2.5 — Audience map
Classify each round into exactly one audience: `recruiter-screen` (fit gate: motivation/comp/visa/timeline), `hiring-manager` (why this role, scope, leadership), `peer-tech` (depth + collaboration on the real stack), `panel-mixed` (onsite loop). If "conducted by" is unknown, infer from duration/position: round 1 short → recruiter-screen; round 2 → do NOT default (peer-tech if "technical screen"/coding, hiring-manager if manager/skip-level, else `panel-mixed [inferred]` and prep both); deep coding/design block → peer-tech; multi-round onsite → panel-mixed.

## Step 3 — Round-by-round breakdown
Per round: type + audience, duration, conducted by, what they evaluate, reported questions (each cited with source + date), and 1-2 concrete prep actions.

## Step 4 — Likely questions (grouped by audience)
Draft candidate-specific answers from the CV/profile. Per audience:
- **recruiter-screen:** "walk me through your CV / why looking" (60-90s narrative), comp expectation (concrete range from Step 1; defer to band when leverage is thin), why this company (specific public signals), location/remote/visa, timeline/notice, other processes, background red flags (honest, forward-looking).
- **hiring-manager:** "why this role, why now" (narrative ↔ named team challenge), first-90-days plan (JD scope + team's recent work), leadership/collaboration (→ story bank), 2-3 sharp questions tied to something the team shipped.
- **peer-tech:** technical questions (system design/coding/architecture/domain) with what a strong answer looks like for this candidate; role-specific questions mapped to JD requirements; reverse questions (on-call, code review, deploy cadence).
- **panel-mixed:** look up named interviewers and route to an audience; cap unlabeled slots to 3-5 items each; vary the angle so the same proof point isn't repeated verbatim; reserve freshest material for the depth slot.

## Step 5 — Story bank mapping
Per audience pack, table: # | audience | likely question/topic | best story | fit (strong/partial/none) | gap. For each gap, suggest a CV experience that could become a STAR+R story; offer to draft and append to the story bank.

## Step 6 — Technical prep checklist
Max 10 items, prioritized by frequency/relevance, each with evidence ("asked in N/M Glassdoor reviews", "their blog suggests this"). Based on what they actually test, not generic advice.

## Step 7 — Company signals (per audience)
What to say/do/avoid, segmented by who's listening. To recruiter: volunteer motivation/fit, withhold hard comp number when leverage is uncertain. To HM: lead with narrative ↔ named challenge, use internal vocabulary. To peers: lead with stack-relevant proof points, avoid review-flagged anti-patterns. To mixed panels: one framing that lands for all, never contradict yourself on comp/timeline across slots.

## Output
Save to `interview-prep/{company-slug}-{role-slug}.md` with header: company/role, URL, legitimacy tier (from the eval report's Block G if any), researched date, sources count, audiences covered. After delivering: offer to draft stories for gaps, note days until interview, suggest deeper company research if Step 1 was thin.

## Rules
- Never invent questions and attribute them to sources; inferred → `[inferred from JD]`.
- Never fabricate Glassdoor ratings/stats — if absent, say so.
- Cite everything. Be direct — a working doc, not a pep talk. Language of the JD (EN default).
