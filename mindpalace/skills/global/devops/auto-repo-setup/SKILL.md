---
name: Auto Repo Setup (Environment Doctor)
description: Use when a repo "won't run", needs environment setup/diagnosis/repair, or you must safely commit/resolve-conflicts/push — reads ONBOARDING.md, audits deps, fixes root causes, verifies, and enforces push/PII safety.
tags: [environment-setup, onboarding, dependency-fix, git-safety, pii-guard, push-safety, smoke-test, uv, troubleshooting]
source: daymade/claude-code-skills
derived_from: auto-repo-setup
---

# Auto Repo Setup — Environment Doctor

Make Claude the "environment doctor": diagnose, fix, verify a repo so non-technical users can run it; also standardize handoff-ready repos.

## Core workflow
**Step 0 — Read the project map** (priority): `ONBOARDING.md` → `README.md` → `CLAUDE.md` → `.claude/settings.json`. If no ONBOARDING.md, offer to generate a draft; don't blindly guess setup.

**Step 1 — Environment audit** (follow ONBOARDING verify steps; verify each output, never assume):
| Check | Command | On fail |
|---|---|---|
| git | `git status` / `git remote -v` | configure identity |
| system deps | `ffmpeg -version` / `which uv` | install per doc |
| python | `uv --version` | create venv via uv |
| project deps | `uv sync` | read pyproject.toml |
| env vars | inspect `.env` keys | guide user to fill |
Use `uv` (never system Python). Check exit codes + stderr, not just stdout.

**Step 2 — Fix iteratively (root cause first, then workaround)**: collect evidence → locate root cause along call chain → fix → optionally flag temporary workaround. NEVER: reinstall/restart on first error, `rm -rf` without analysis+confirmation+backup, silently swallow errors (`|| true`, empty except).

**Step 3 — Verify (self-check loop)**: run smoke test / minimal `uv run pytest`. If it fails, return to Step 2 — never say "should work now".

**Step 4 — Report** in plain language: what's fixed ✅, what user must do ⚠️ (e.g. fill API key), next commands 📋.

## Safety rules
- **Push Safety**: before any `git push`, verify real visibility via `gh repo view <o>/<r> --json visibility,isPrivate,stargazerCount,forkCount`. public+stars → PR flow; private → confirm. Never infer visibility from URL.
- **PII Guard** (public repo, 4 layers): gitleaks → path scan → grep fallback (CJK/names) → AI semantic read-through. private repo: `.env` OK to commit but strip personal absolute paths.
- **Hook bypass ban**: never use `--no-verify`/`--no-gpg-sign` unless the user typed it this session. Hook fails → fix root cause.
- **NO FALLBACK**: fail-fast on missing critical values (`os.environ["KEY"]`, not `|| 'sk-...'`). Placeholders only in `.env.example`.

## Standard patterns
- **ONBOARDING.md**: copy-pasteable commands, no personal paths, placeholders (`<REPO_ROOT>`), includes "verify" steps not just "install".
- **SessionStart hook**: `.claude/settings.json` runs `session-start-check.sh` (24h TTL cache keyed by repo-path sha256) that nudges agent to read ONBOARDING. Generate via `scripts/init_session_start_hook.py --repo <path>`.
- **Counter-Review** (on new files / core config / new deps / CI changes): 4 parallel lenses (security, devops, code-quality, doc-consistency) → judge filters by probability×cost×realism → report ✅real / ⚠️partial / ❌fabricated / 🚫harmful.

## Git ops
- Commit: `git status` → `git diff` (explain) → selective `git add` (never blind `.`) → commit (describe what+why, add Co-Authored-By) → Push Safety.
- Conflicts: locate via `git status`, read conflict blocks, **don't auto-pick a side** — explain both, let user/business logic decide.
- History sanitization (after leak): assess scope/pushed? → orphan branch + force push (if history disposable) or BFG (preserve partial) → coordinate with collaborators.
