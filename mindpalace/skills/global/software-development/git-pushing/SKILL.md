---
name: git-pushing
description: "Use when the user wants to commit and push git changes — triggers on 'push this', 'commit and push', 'push to github', 'push to remote', 'save to github', 'let's push this up', or 'commit these changes' — stages all, makes a conventional commit, and pushes."
version: 1.0.0
license: Apache-2.0
tags: [git, commit, push, conventional-commits, github, version-control, workflow, remote]
source: https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/git-pushing
derived_from: awesomeclaude
prerequisites:
  commands: [git]
---

# Git Push Workflow

Stage all changes, create a conventional commit with a Claude footer, and push to
the current branch's remote.

## When to use

Activate when the user:
- Explicitly asks to push ("push this", "commit and push", "push to github").
- Mentions saving work to remote ("save to github", "push to remote").
- Finishes a feature and wants to share it ("let's push this up", "commit these changes").

## What it does

1. Reads the current branch.
2. Bails out if there are no changes.
3. Stages everything (`git add .`).
4. Builds a Conventional Commits message:
   - **type** inferred from changed files — `test`, `docs`, `chore` (deps),
     `fix`/`refactor` (from diff content), else `feat`.
   - **scope** inferred from the path / keywords (`plugin`, `skill`, `agent`, or
     top-level dir).
   - A custom message can be passed instead and is used verbatim.
5. Commits with a `🤖 Generated with Claude Code` + `Co-Authored-By` footer.
6. Pushes: plain `git push` if the branch already exists on origin, else
   `git push -u origin <branch>` and prints a GitHub "create PR" link.

## How to run

The skill ships a helper script. Fetch it from the source repo
(`engineering-workflow-plugin/skills/git-pushing/scripts/smart_commit.sh`) or
reproduce its behavior with the steps above.

```bash
# auto-generated commit message
bash scripts/smart_commit.sh

# explicit message
bash scripts/smart_commit.sh "feat: add feature"
```

## Gotchas

- `git add .` stages **all** changes including unrelated/untracked files — make
  sure the working tree only holds what should ship, or stage manually first.
- The script's auto-detected type/scope is heuristic; for anything nuanced, pass
  an explicit conventional-commit message.
- The footer uses the generic `Co-Authored-By: Claude <noreply@anthropic.com>`.
  Per this user's global rules, commit messages should instead end with
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` and PR
  bodies with the Claude Code generated-with line — adjust the message accordingly.
- `set -e`: any failed git step aborts the whole run.
- Only commit/push when the user explicitly asks; if on the default branch,
  branch first.
