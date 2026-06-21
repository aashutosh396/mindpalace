---
name: azure-devops
description: "Use when working with Azure DevOps (dev.azure.com): manage sprints/iterations, create or update work items (User Story, Bug, Task, WIQL queries), list repos, create/review/complete pull requests, run or queue pipelines/builds, search code, manage wiki pages, check Advanced Security alerts, edit variable groups, approve deployment environments, or configure branch policies."
version: 1.0.0
license: Apache-2.0
tags: [azure-devops, work-items, pull-requests, pipelines, repos, wiki, variable-groups, branch-policies, ci-cd, rest-api]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/azure-devops
derived_from: awesomeclaude
prerequisites:
  commands: [python]
---

# Azure DevOps

Full Azure DevOps integration over REST API v7.1. Covers 13 domains (work items,
repos/PRs, iterations/capacity, pipelines, search, wiki, test plans, security,
variable groups, environments/approvals, branch policies, attachments, core).

## When to use
User mentions Azure DevOps / `dev.azure.com` / VSTS and wants to: manage sprints,
create/update/link work items, run WIQL queries, list repos or browse files,
create/review/complete/abandon PRs, run/queue/cancel pipelines and read build logs,
search code/wiki/work-items, edit wiki pages, manage test plans, check security
alerts, edit variable groups, approve/reject environment deployments, or set
branch policies (min reviewers, build validation).

## Setup (auth)
All scripts live under `scripts/` in the source repo. Authenticate once:

```bash
# OAuth device-code flow (recommended; tokens auto-refresh)
python scripts/auth.py login --org MyOrganization
# OR Personal Access Token
python scripts/auth.py login --org MyOrganization --pat YOUR_PAT
python scripts/auth.py status     # check
python scripts/auth.py logout
```

PAT scopes (create at `https://dev.azure.com/{org}/_usersSettings/tokens`):
Work Items R/W, Code R/W, Build R/Execute, Wiki R/W, Test Management R/W,
Advanced Security Read, Project & Team Read, Identity Read.

Credentials are stored in the system keyring (macOS Keychain / Windows Credential
Locker / Linux Secret Service) under service `azure-devops-skill`.

## Key commands (per script)
Common args: `--project MyProject`, plus `--repo`, `--id`, `--pr-id`, etc.

- **core.py** — `list-projects`, `list-teams`, `get-identity --search "x@y.com"`
- **work_items.py** — `get|create|update|delete`, `batch-get --ids 1,2,3`,
  `add-children`, `link`/`unlink`, `add-comment`/`list-comments`, `get-revisions`,
  `my-items`, `iteration-items --iteration-path "Proj\\Sprint 1"`,
  `run-wiql --query "SELECT [System.Id] FROM WorkItems WHERE..."`,
  `list-queries`/`run-query`, `recycle-bin`
- **repos.py** — `list`, `list-branches`, `create-branch --source main`,
  `search-commits`, `list-prs`, `create-pr --source feat --target main --title ...`,
  `get-pr`, `update-pr`, `add-reviewer --vote 10`, `create-thread`/`add-thread-comment`,
  `complete-pr [--merge-strategy rebase --keep-source]`, `abandon-pr`,
  `get-diff --base main --target feat`, `list-files`
- **work.py** — `list-iterations`, `create-iteration --start-date --finish-date`,
  `team-iterations --timeframe current`, `assign-iteration`, `get-capacities`,
  `set-capacity --activity Development --capacity-per-day 6`
- **pipelines.py** — `list-builds`, `get-build`, `build-logs [--log-id N]`,
  `list-definitions`, `run --pipeline-id N [--variable K V]`, `get-run`/`list-runs`,
  `queue-build`, `cancel-build`, `build-status`, `get-artifacts`, `update-stage`
- **search.py** — `code --query`, `wiki --query`, `work-items --query`
- **wiki.py** — `list`, `list-pages`, `get-page`/`get-page-content`,
  `create-or-update-page --path /X --content "..."`
- **test_plans.py** — `list-plans`/`create-plan`, `list-suites`,
  `list-test-cases`, `add-test-cases --ids`, `list-results`/`get-result`
- **security.py** — `list-alerts [--state active --severity high --type dependency]`,
  `get-alert`
- **variable_groups.py** — `list`/`get`/`create`/`update`/`delete`,
  `add-variable --key K --value V [--secret]`, `remove-variable`
- **environments.py** — `list`/`create`/`get`/`delete`, `list-checks`,
  `list-approvals [--state all]`, `approve`/`reject --approval-id guid --comment`
- **policies.py** — `list`, `list-types`, `create-min-reviewers --min-reviewers 2 --reset-on-push`,
  `create-build-policy --build-definition-id N`, `update --enabled false|--blocking true`,
  `list-evaluations --pr-id`, `delete`
- **attachments.py** — `upload`, `attach`, `upload-and-attach`, `list`,
  `download`, `remove --index N`

## Reference: common work-item fields
Title `System.Title` · State `System.State` · Assigned To `System.AssignedTo` ·
Description `System.Description` · Area `System.AreaPath` · Iteration
`System.IterationPath` · Priority `Microsoft.VSTS.Common.Priority` · Story Points
`Microsoft.VSTS.Scheduling.StoryPoints` · Tags `System.Tags` · Repro Steps
`Microsoft.VSTS.TCM.ReproSteps` · Acceptance Criteria `Microsoft.VSTS.Common.AcceptanceCriteria`

## Reference: link types
Related `System.LinkTypes.Related` · Parent→Child `System.LinkTypes.Hierarchy-Forward`
· Child→Parent `System.LinkTypes.Hierarchy-Reverse` · Predecessor
`System.LinkTypes.Dependency-Forward` · Successor `System.LinkTypes.Dependency-Reverse`

## Gotchas
- Iteration paths use backslashes and must be escaped in shell: `"Proj\\Sprint 1"`.
- Reviewer `--vote`: 10 = approve, 5 = approve w/ suggestions, -10 = reject.
- Variable group secrets: pass `--secret` so the value is masked at rest.
- `add-variable` is the safe way to set one var; `update` replaces the whole set.
- Helper scripts are NOT vendored here — pull `scripts/*.py` from the source repo
  (sanjay3290/ai-skills, path skills/azure-devops/scripts/).
