---
name: Roadmap Communicator
description: Use when preparing roadmap narratives, release notes, changelogs, or stakeholder updates tailored for executives, engineering, or customers — picks the right format and framing per audience.
tags: [roadmap, release-notes, changelog, stakeholder-update, communication, now-next-later, feature-announcement, product]
source: alirezarezvani/claude-skills
derived_from: product-team/roadmap-communicator
---

# Roadmap Communicator

Create clear roadmap communication artifacts for internal and external stakeholders.

## Roadmap Formats

1. **Now / Next / Later** — best for uncertainty and strategic flexibility; direction without false precision.
2. **Timeline** — best for fixed-date commitments and launch coordination; requires active risk + dependency management.
3. **Theme-based** — best for outcome-led planning and cross-team alignment; groups by problem space / strategic objective.

## Stakeholder Update Patterns

- **Board / Executive** — outcome and risk oriented; progress against strategic goals; highlight trade-offs and required decisions.
- **Engineering** — scope, dependencies, sequencing clarity; status, blockers, resourcing implications.
- **Customers** — value narrative and timing; what's available now vs upcoming; clear expectation setting.

## Release Notes

- **User-facing** — lead with user value not implementation; group by workflows/user jobs; call out migration/behavior changes explicitly.
- **Internal** — technical details, operational impact, known issues; rollout plan, rollback criteria, monitoring notes.

## Changelog Generation

Read a git log range, parse conventional-commit prefixes, group by type (`feat`, `fix`, `chore`, …), output markdown or plain text.

## Feature Announcement Framework

1. Problem context → 2. What changed → 3. Why it matters → 4. Who benefits most → 5. How to get started → 6. Call to action + feedback channel.

## Quality Checklist

- [ ] Audience-specific framing is explicit
- [ ] Outcomes and trade-offs are clear
- [ ] Terminology consistent across artifacts
- [ ] Risks and dependencies not hidden
- [ ] Next actions and owners specified
