---
name: job-offer-evaluation
description: Use when evaluating a job posting / job description against your CV — paste a JD (text or URL) to get a full A-G assessment: role fit, CV match and gaps, leveling strategy, comp research, CV customization plan, interview story plan, and ghost-job / posting-legitimacy check. Triggers on "evaluate this job", "should I apply", "JD evaluation", "is this a real posting", "match my resume to this role".
version: 1.0.0
license: MIT
tags: [job-search, jd-evaluation, resume, cv-match, interview, ats, ghost-jobs, application-tracking]
source: https://github.com/santifer/career-ops
derived_from: awesomeclaude
---

# Job Offer Evaluation (A-G)

When a candidate pastes a job (text or URL), deliver 7 blocks: A-F evaluation + G legitimacy. Read the candidate's `cv.md` and `config/profile.yml` first.

## Liveness gate (URL inputs only)
Before evaluating a URL, confirm the posting is still live (fetch page, read title/content). Classify as **active** (real JD + apply path) or **closed** (expired / "no longer accepting" / 404 / redirect to generic careers page). If closed, STOP before Block A — tell the candidate the link is dead; do not waste an evaluation. If only JD text was pasted, note liveness can't be verified and proceed.

## Step 0 — Archetype detection
Classify the role into an archetype (e.g. FDE, Solutions Architect, PM, LLMOps, Agentic, Transformation). Hybrid → name the 2 closest. This drives which proof points, summary rewrite, and STAR stories to prioritize.

## Block A — Role summary
Table: archetype, domain, function (build/consult/manage/deploy), seniority, remote mode, team size, one-sentence TL;DR.

## Block B — Match with CV
Map each JD requirement to exact lines in `cv.md`. Prioritize proof points by archetype. Then a **Gaps** section: for each gap state — hard blocker vs nice-to-have, adjacent experience available, covering portfolio project, and a concrete mitigation (cover-letter phrasing, quick project, etc.).

## Block C — Level and strategy
1. Level detected in JD vs candidate's natural level for the archetype.
2. "Sell senior without lying" plan — specific phrases, achievements to highlight, how to position founder/unusual experience as an asset.
3. "If they downlevel me" plan — accept if comp fair, negotiate 6-month review, clear promotion criteria.

## Block D — Comp and demand
Web-search current salaries (Levels.fyi, Glassdoor, Blind), company comp reputation, demand trend. Table with cited sources. If no data, say so — never invent.

## Block E — Customization plan
Table: section | current status | proposed change | why. Deliver top 5 CV changes + top 5 LinkedIn changes to maximize match.

## Block F — Interview plan
6-10 STAR+R stories mapped to JD requirements (STAR + **Reflection** — what was learned / would be done differently; signals seniority). Frame per archetype. Include 1 recommended case study and red-flag questions with answers. If a story bank exists, reuse and append new stories.

## Block G — Posting legitimacy (ghost-job check)
Present observations, not accusations — every signal has innocent explanations. Analyze:
1. **Freshness** — date posted, apply-button state, redirects (from the page snapshot).
2. **Description quality** — named tech/tools, team/org context, realistic requirements, salary, boilerplate ratio, internal contradictions.
3. **Company hiring signals** — search `"{company}" layoffs {year}` and `hiring freeze`; note if same department.
4. **Reposting** — same company+role seen before at a different URL.
5. **Role market context** — does the role/seniority/business fit a normal fill timeline?

Output: an **Assessment** tier (High Confidence / Proceed with Caution / Suspicious), a signals table (finding + weight: Positive/Neutral/Concerning), and context notes.

Edge cases: government/academic and niche/exec roles fill slowly (raise thresholds); "ongoing/rolling" postings are pipeline roles, not ghosts; startups may have vague JDs; **no date + no other concerns → default to "Proceed with Caution", never "Suspicious" without evidence**; active recruiter contact is itself a positive signal.

## Post-evaluation
1. **Save report** to `reports/{###}-{company-slug}-{YYYY-MM-DD}.md` (sequential 3-digit number) with sections A-G, a score (X/5), legitimacy tier, and 15-20 extracted ATS keywords.
2. **Record in tracker** `data/applications.md`: `| # | Date | Company | Role | Score | Status | PDF | Report |` with status `Evaluated` and a relative link to the report.
3. Optionally append a **cover-letter draft** built from the 4 most relevant CV bullets (exact wording, real metrics) + a JD-mission opening; leave "why this company / problems I'll solve" as placeholders for the user.

## Rules
- No fabricated salaries, ratings, or stats — cite or say "no data".
- Active voice, concrete claims, no buzzwords, no em dashes.
- Generate in the language of the JD (EN default).
