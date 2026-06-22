---
name: Confluence Expert
description: Use when building or restructuring a Confluence space, designing page hierarchies/permissions, authoring templates with macros, embedding Jira reports, or auditing a knowledge base.
tags: [confluence, atlassian, documentation, knowledge-base, macros, templates, space-architecture, mcp, storage-format, content-governance]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/confluence-expert
---

# Confluence Expert

Space management, documentation architecture, macros, templates, and knowledge-base governance.

## Atlassian MCP — what works vs not
Tools surface as `mcp__atlassian__<toolName>` (camelCase). Get `cloudId` once via `getAccessibleAtlassianResources`. Never invent tool names.

Available: `getConfluenceSpaces`, `createConfluencePage` (body = storage-format XHTML or ADF — **never wiki markup**), `updateConfluencePage` (fetch current version first, supply version+1), `getConfluencePage`, `searchConfluenceUsingCql`, `getConfluencePageDescendants`, footer comments.

NOT via MCP — use web UI / REST: create/delete a **space** (`POST /wiki/api/v2/spaces`), **delete** a page, apply **labels**, space **permissions**, blueprints/templates as first-class objects.

## Workflows

**Space creation** — space itself via UI/REST; the page tree CAN be built via MCP (one `createConfluencePage` per node, passing parent id to nest). Decide space type (Team/Project/KB/Personal), set homepage, configure permissions, build the tree, verify the URL loads and a non-admin sees the correct level.

**Page architecture** — max 3 levels deep, consistent naming, date-stamp meeting notes. Pattern: Home → Overview → Team Info → Projects (per-project: Overview/Requirements/Meeting Notes) → Processes → Meeting Notes Archive → Resources.

**Template creation** — identify the repeatable pattern, build structure with placeholder instructions, format with macros, save/share, verify a test page renders all placeholders before sharing.

**KB management** — run a content health audit first (export page metadata via `getPagesInConfluenceSpace`/`searchConfluenceUsingCql`); stale/orphaned/low-engagement findings become the archive list + update backlog. Article types: how-to, troubleshooting, FAQ, reference, process. Quality: clear title, headings, visible updated-date, named owner, quarterly review.

## Essential macros
Note: `{macro}` shorthand is legacy wiki markup for readability; MCP-created pages require storage format (`<ac:structured-macro>`).
- Content: `{info}/{note}/{warning}/{tip}`, `{expand}`, `{toc:maxLevel=3}`, `{excerpt}` + `{excerpt-include:Page}`.
- Dynamic: `{jira:JQL=...}`, `{jirachart}`, `{recently-updated}`, `{contentbylabel}`.
- Collaboration: `{status:colour=Green|title=Approved}`, `{tasks}`, `@username`, `{date:format=dd MMM yyyy}`.
- Layout: `{section}/{column}`, `{panel}`, `{code:javascript}`.

## Template library
| Template | Key sections |
|---|---|
| Meeting Notes | Agenda, Discussion, Decisions, Action Items (tasks macro) |
| Project Overview | Quick Facts panel, Objectives, Stakeholders, Milestones (Jira), Risks |
| Decision Log | Context, Options, Decision, Consequences, Next Steps |
| Sprint Retrospective | Went Well (info), Didn't (warning), Actions (tasks), Metrics |

## Permission schemes
Public: all View / team Edit-Create / admin Admin. Team: members View-Edit-Create / leads Admin / others none. Project: stakeholders View / team Edit-Create / PM Admin. (Configured in Space settings UI, not MCP.)

## Governance
Review cycles: critical monthly, standard quarterly, archive annually. Archiving: move to Archive space, label "archived"+date, keep 2 years then delete, retain audit trail. Quality checklist: descriptive title, owner, updated-date, labels, working links, consistent formatting, no sensitive data.
