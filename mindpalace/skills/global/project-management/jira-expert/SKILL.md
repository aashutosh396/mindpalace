---
name: Jira Expert
description: Use when setting up or configuring Jira projects, writing JQL/advanced searches, designing workflows, building dashboards, or performing technical Jira operations.
tags: [jira, atlassian, jql, workflows, dashboards, automation, issue-tracking, mcp, custom-fields, agile]
source: alirezarezvani/claude-skills
derived_from: project-management/skills/jira-expert
---

# Jira Expert

Jira configuration, JQL, workflows, automation, and reporting.

## Atlassian MCP — what works vs not
Tools surface as `mcp__atlassian__<toolName>`. Get `cloudId` once via `getAccessibleAtlassianResources`. Never invent tool names.

Available: `createJiraIssue`, `getJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `getTransitionsForJiraIssue` + `transitionJiraIssue` (status changes go through transitions, not field edits), `addCommentToJiraIssue`, `addWorklogToJiraIssue`, `createIssueLink`, `getJiraIssueTypeMetaWithFields`, `getVisibleJiraProjects`.

NOT via MCP — use web UI / REST: create a **project** (`POST /rest/api/3/project`), create a **sprint**/configure boards (`/rest/agile/1.0/sprint`), create/share a **filter**, custom fields/screens/workflow/permission schemes.

## JQL

Build from natural language, then execute via `searchJiraIssuesUsingJql`.

Operators: `= != ~ !~ > < >= <= in "not in" "is empty" "is not empty" was "was in" changed`.

Powerful examples:
- Overdue: `dueDate < now() AND status != Done`
- Sprint burndown: `sprint = 23 AND status changed TO "Done" DURING (startOfSprint(), endOfSprint())`
- Stale: `updated < -30d AND status != Done`
- Epic tracking: `"Epic Link" = PROJ-123 ORDER BY rank`
- Velocity: `sprint in closedSprints() AND resolution = Done`
- Capacity: `assignee in (user1,user2) AND sprint in openSprints()`

Functions: dates `startOfDay/Week/Month/Year()` etc.; sprints `openSprints()/closedSprints()/futureSprints()`; users `currentUser()/membersOf("group")`; advanced `issueHistory()/linkedIssues()/issuesWithFixVersions()`.

## Workflows

**Project creation** (UI/REST, not MCP) — pick type (Scrum/Kanban/Bug), configure name/key/lead/notification/permission schemes, issue types + workflows, custom fields, board. Verify with `getVisibleJiraProjects`.

**Workflow design** — map states → transitions/conditions; lint the design before building (catch dead-end states, unreachable states, missing transitions); deploy to a test project first; verify transitions via `getTransitionsForJiraIssue` then `transitionJiraIssue`.

**Bulk ops** — find targets via JQL, preview ALL changes before executing (bulk edits are hard to reverse), apply in small batches.

## Reporting templates
| Report | JQL |
|---|---|
| Sprint | `project = PROJ AND sprint = 23` |
| Velocity | `assignee in (team) AND sprint in closedSprints() AND resolution = Done` |
| Bug trend | `type = Bug AND created >= -30d` |
| Blockers | `priority = Blocker AND status != Done` |

## Best practices
Data quality: required-field validation, consistent key naming, scheduled cleanup. Performance: avoid leading wildcards in `~`, use saved filters not ad-hoc JQL, limit dashboard gadgets, archive (not delete) completed projects. Governance: document custom states, version-control schemes before changes, require change review for org-wide updates, audit permissions after role changes.
