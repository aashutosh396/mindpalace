---
name: GitHub Operations (gh CLI + API)
description: Use when managing PRs, issues, repos, workflows, or calling the GitHub REST/GraphQL API — covers gh CLI commands, auth (incl. Enterprise), JSON/jq output, and bulk automation patterns.
tags: [github, gh-cli, pull-request, issues, workflows, github-api, graphql, enterprise, automation]
source: daymade/claude-code-skills
derived_from: github-ops
---

# GitHub Operations

Comprehensive GitHub work via `gh` CLI and REST/GraphQL APIs.

## Pull requests
```bash
gh pr create --title "NOJIRA: Title" --body "Description"  # NOJIRA bypasses JIRA enforcement
gh pr list --state open
gh pr view 123
gh pr checks 123
gh pr merge 123 --squash
gh pr review 123 --approve
gh pr comment 123 --body "LGTM"
```
PR title convention: `GR-1234: Title` with a ticket, else `NOJIRA: Title`.

## Issues
```bash
gh issue create --title "Bug: Title" --body "..."
gh issue list --state open --label bug
gh issue edit 456 --add-label "priority-high"
gh issue close 456
```

## Repos & workflows
```bash
gh repo view --web ; gh repo clone owner/repo ; gh repo create my-repo --public
gh workflow list ; gh workflow run name ; gh run watch <id> ; gh run download <id>
```

## API
```bash
gh api repos/{owner}/{repo}/pulls/{n}
gh api repos/{owner}/{repo}/issues/{n}/comments -f body="text"
gh api repos/{owner}/{repo}/actions/runs
```
Use GraphQL for multi-resource queries.

## Auth & config
```bash
gh auth login ; gh auth login --hostname github.enterprise.com ; gh auth status
gh repo set-default owner/repo
gh config set editor vim ; gh config set git_protocol ssh
```

## Output for scripting
```bash
gh pr list --json number,title,state,author
gh pr list --json number,title | jq '.[] | select(.title | contains("bug"))'
gh pr list --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
```
For bulk ops: paginate, add retry logic, parallelize where safe.
