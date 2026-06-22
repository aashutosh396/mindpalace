---
name: Knowledge Ops
description: Use when authoring, validating, or cleaning up company SOPs and internal runbooks, or auditing a sprawling Notion/Confluence/Obsidian wiki — 5W2H completeness checks, runbook step verification, orphan/stale-page detection, and prioritized cleanup lists.
tags: [sop, runbook, knowledge-management, wiki-hygiene, 5w2h, kb-audit, ops-documentation, orphan-pages, glossary-drift]
source: alirezarezvani/claude-skills
derived_from: business-operations/knowledge-ops
---

# Knowledge Ops

SOP + internal-runbook authoring, 5W2H completeness validation, and KB hygiene reporting for Head-of-Ops / Knowledge-Manager / TPM-Internal. Answers: **"Which 20 docs do I fix first, and what specifically is wrong with each?"** — deterministically, not by intuition.

## The 7 Recurring KB Failure Modes

No owner (names "the team") · no last-reviewed date · vague success signals · no rollback path · orphan pages (no inbound links) · glossary drift (same term, conflicting definitions) · happy-path-only SOPs.

## Workflow

1. **Ingest KB** — walk the wiki export (Notion zip / Confluence space / Obsidian vault / `Drive/SOPs/`). Output: orphan pages, stale pages (no edit >12mo), glossary drift, missing-owner pages, cross-link map, prioritized top-20 cleanup list ranked by `staleness × inbound-link-count`.
2. **Validate existing runbooks** — score each step against six checks: (1) named owner (not "the team"), (2) expected duration (concrete number+unit), (3) observable success signal ("HTTP 200 from `/healthz`", not "service is up"), (4) observable failure signal, (5) rollback path (or explicit "cannot roll back — escalate to X"), (6) escalation contact. Verdict: ≥80 SAFE-TO-USE, 60-79 USE-WITH-CAUTION, <60 NOT-SAFE (not safe in an incident).
3. **Generate missing SOPs** — emit a 5W2H-structured scaffold: **Who** (RACI), **What** (process steps), **When** (triggers + frequency), **Where** (system + tool), **Why** (purpose + regulatory basis), **How** (step-by-step), **How-much** (cost + time per execution). Regulated profile adds version control, signoff matrix, audit trail (ISO 9001 / 21 CFR Part 211 / SOC 2 / HIPAA).
4. **Close the loop** — re-ingest after the cleanup sprint; the metrics that matter are **unfindable docs (orphans)** and **unsafe runbooks (<60)**, not page count.

## Anti-Patterns

Generating SOPs in bulk without named owners (a doc with no owner has a 6-month half-life — refuse) · using the runbook validator as a checkbox (it catches missing structure, not wrong content) · treating all orphans as garbage (some are search-only reference pages — the list is a priority queue, not a delete list) · letting glossary drift accumulate (fix the moment it surfaces) · skipping the regulated profile under regulated workload (missing version control = audit finding) · hand-writing 5W2H from memory (operators always forget How-much).

## Forcing Questions (one at a time, recommended answer + canon)

1. **Who is the named owner, and do they know they own it?** → a single human, agreed in writing. (Gawande, *Checklist Manifesto* — unowned checklists rot in 12mo.)
2. **When was it last reviewed, and what is the cadence?** → within 12mo (90d if regulated); cadence in frontmatter. (ISO 9001 §7.5.3.)
3. **For each runbook step, what is the observable success signal?** → a concrete observable, not "it works". (SRE Workbook Ch.8.)
4. **What is the rollback path for each step that can fail?** → rollback or explicit "cannot reverse — escalate to X". (AWS Well-Architected, Operational Excellence.)
5. **Where does it live, and what links to it?** → canonical wiki + ≥2 inbound links. (Atlassian — orphan rate >20% = wiki-sprawl indicator.)
6. **What's the regulatory overlay — SOC 2 / HIPAA / ISO 13485 / GDPR / SOX / none?** → explicit; verify by data classes. (21 CFR 211.100.)
7. **Is the happy path the *only* path, or are the top 2-3 failure modes documented?** → top-2 failure modes with recovery sub-procedure. (Fowler, *Production-Ready Microservices* — happy-path-only docs cause 60%+ of incident-time waste.)

## Distinct From

Personal PKM / second-brain (this is organizational: many authors/readers, named owners, review cycles); system-ops debugging runbooks (these are *operator* runbooks for business processes); process-mapper (that designs the process *flow*; this documents the *artifacts* operators consume); formal regulatory authoring (borrows the checklist, not a substitute for a notified-body audit).
