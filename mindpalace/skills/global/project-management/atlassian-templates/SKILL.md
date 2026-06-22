---
name: Atlassian Templates Creator
description: Use when building or modifying reusable Jira/Confluence templates, blueprints, page layouts, or standardized content structures for org-wide consistency.
tags: [atlassian, confluence, jira, templates, blueprints, storage-format, macros, governance, mcp, standardization]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/atlassian-templates
---

# Atlassian Templates Creator

Create, modify, and manage reusable templates and files for Jira and Confluence.

## Process

**Template creation**: Discover (interview stakeholders) → Analyze (existing patterns) → Design (structure + placeholders) → Implement (macros) → Test (preview with sample data) → Document (usage) → Publish (via MCP) → Verify (renders, roll back on error) → Train → Monitor → Iterate.

**Modification**: Assess change + impact → Version (keep old available) → Modify → Test (don't break existing usage) → Migrate (path for existing content) → Communicate → Support → Archive old (unlist, don't delete).

**Blueprint development**: define scope → multi-page structure → per-section page templates → creation rules → dynamic content (Jira queries, user data) → end-to-end test in a sample space → verify macro references resolve → hand to admin for global deployment.

## Critical format rule
`createConfluencePage`/`updateConfluencePage` accept **storage format (XHTML, `<ac:structured-macro>`)** or ADF — wiki markup (`{panel}`, `h2.`, `{tasks}`) is **rejected**. Generate storage-format markup, then pass it verbatim as the `body`. Apply labels in the Confluence UI afterward (no MCP label tool).

## Confluence template types
| Template | Purpose | Macros |
|---|---|---|
| Meeting Notes | agenda/decisions/actions | date, tasks, panel, info, note |
| Project Charter | scope, RACI, timeline, budget | panel, status, info |
| Sprint Retrospective | went-well/didn't/actions | panel, expand, tasks, status |
| PRD | goals, stories, requirements, release | panel, status, jira, warning |
| Decision Log | options, matrix, tracking | panel, status, info, tasks |

Standard sections across all: header panel with metadata (owner/date/status), labeled sections with inline placeholder instructions, action-items block (`{tasks}`), related links.

## Jira template types
User Story (As a / I want / So that + Given/When/Then AC + DoD), Bug Report (env, repro steps, expected vs actual, severity, workaround), Epic (vision, goals, success metrics, breakdown, dependencies, timeline).

Jira description templates: there is no MCP field-config tool — set description defaults in admin UI / REST `/rest/api/3/fieldconfiguration`. MCP CAN create issues pre-filled with template text via `createJiraIssue`. First-class Confluence blueprints aren't MCP-creatable; `createConfluencePage` makes ordinary copy-from pages.

## Validation after deployment
Retrieve via `getConfluencePage`, assert no macro errors and body contains expected `<ac:structured-macro>`; check Jira-macro embeds resolve; confirm task blocks are interactive. On failure, revert via `updateConfluencePage` (version+1, previous body).

## Quality gates (before every deploy)
Example content per section · tested with sample data in preview · version comment in change log · feedback mechanism enabled. Mark outdated templates with a `{warning}` banner and archive (don't delete).
