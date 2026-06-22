---
name: Course Supplementary Reading List
description: Use when the user uploads a syllabus/course outline/curriculum and wants supplementary readings ("create a reading list from this syllabus", "find recent papers for my course") — parses topics, searches recent peer-reviewed papers per section, and produces a formatted .docx with audience-calibrated summaries and Bloom discussion questions.
tags: [syllabus, reading-list, curriculum, course, academic, consensus, teaching, papers]
source: alirezarezvani/claude-skills
derived_from: research/syllabus (Course Supplementary Reading List)
---

# Syllabus — Course Supplementary Reading List

For an instructor/student with a syllabus: produce a professional supplementary reading list (.docx) of recent peer-reviewed papers per course section, via Consensus search.

## Phase 0: Intake (3 forcing questions)
1. **Syllabus input** — file path (PDF/DOCX/text) / pasted / image. Refuse to start without one.
2. **Course audience** — undergrad-intro / undergrad-advanced / grad-masters / grad-doctoral / professional / mixed. Drives summary jargon level + discussion-question complexity.
3. **Year range** — last 1 / 2 (default) / 5 years. Drives `year_min` on every search.

## Phase 1: Parse
Extract by format. Pull course title/instructor/term, topic list, learning outcomes (infer 3-5 if missing, mark `[inferred]`).

## Phase 2: Group + Confirm (forcing checkpoint)
Cluster topics into 6-12 sections. Present proposed sections with item counts; offer merge/split/add/remove. **Refuse Phase 3 without explicit choice** — last cheap moment before searches consume budget.

## Phase 3: Search Consensus per Section (sequential, 1 q/sec)
**Applied-domain weaving (critical):** search topic + applied domain, not topic alone ("enzyme kinetics food processing", not "enzyme kinetics"). Boosts relevance dramatically. 1-2 queries/section; fallback without domain angle if thin. Select 1-3 papers/section (15-25 total). Priorities: relevance → reviews/meta-analyses → citation count → applied-domain fit.

## Phase 4: Summaries + Discussion Questions
- **Summaries** — plain language, 2-3 sentences, calibrated to audience (define jargon for undergrads; assume fluency for grads). Good: concrete, names the real-world stakes. Bad: jargon-dense restatement.
- **Discussion questions** — Bloom higher-order (apply/analyze/evaluate), tied to a learning outcome, promotes discussion not recall. Reject "What did the authors find?"

## Phase 5-6: Generate + Deliver
DOCX with title page, intro + Consensus link, learning-outcomes box, numbered papers per section (full ExternalHyperlink URLs, never truncated; LevelFormat.BULLET lists), audit log footer. Validate zip integrity, confirm sections present. Chat summary: file path + sections × papers / cited + plan tier.

## Agent Integrity Rules
Only Consensus-returned papers from this session; training tagged + excluded. Three counts. Confirm each response before next. Surface gaps (section with one paper + note) instead of fabricating.

## Anti-Patterns
Parallelizing Consensus; searching without applied-domain angle; padding sections with fabrications; generic discussion questions; jargon-heavy summaries for undergrads; skipping the group-and-confirm step; truncating URLs.
