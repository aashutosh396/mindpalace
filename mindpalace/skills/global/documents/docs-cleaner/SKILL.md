---
name: Documentation Cleaner / Consolidator
description: Use when documentation is bloated, redundant, or sprawled across multiple files covering the same topic — consolidates into a single source of truth while preserving 100% of valuable content.
tags: [documentation, consolidate, cleanup, dedupe, merge-docs, single-source-of-truth, refactor]
source: daymade/claude-code-skills
derived_from: docs-cleaner
---

Consolidate redundant documentation. **Core principle: critical evaluation before deletion** — analyze each section's unique value first. Reduction without information loss.

## Workflow
**Phase 1 — Discovery:** find all docs covering the topic; count total lines; map content overlap.

**Phase 2 — Value Analysis:** per document, build a section-by-section table:

| Section | Lines | Value | Reason |
|---------|-------|-------|--------|
| API Reference | 25 | Keep | Unique endpoint docs |
| Setup Steps | 40 | Condense | Verbose but essential |
| Test Results | 30 | Delete | One-time record, not reference |

Value categories: **Keep** (unique/essential/frequently referenced), **Condense** (valuable but verbose), **Delete** (duplicate/one-time/self-evident/outdated).

**Phase 3 — Consolidation Plan:** propose target structure with before/after metrics:
```
Before: 726 lines (3 files, high redundancy)
After:  ~100 lines (1 file + reference in CLAUDE.md)
Reduction: 86%   Value preserved: 100%
```

**Phase 4 — Execution:** create consolidated doc with all valuable content → delete redundant sources → update references (CLAUDE.md, README, imports) → verify no broken links.

## Value-preservation checklist
Confirm preserved: essential procedures (setup/config), key constraints/gotchas, troubleshooting guides, tech-debt/roadmap items, external links, debug tips/code snippets.

## Anti-patterns
| Pattern | Problem | Solution |
|---------|---------|----------|
| Blind deletion | Loses info | Section-by-section analysis first |
| Keeping everything | No reduction | Apply value criteria strictly |
| Multiple sources of truth | Future divergence | Single authoritative location |
| Orphaned references | Broken links | Update all references after |

## Output artifacts
Consolidated document, value analysis (per-section justification), before/after metrics, updated references pointing to the new location.
