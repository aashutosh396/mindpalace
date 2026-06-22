---
name: Gangtise Copilot (investment-research API installer)
description: Use when installing, configuring, or diagnosing the Gangtise (岗底斯投研) OpenAPI skill suite, or routing an investment-data question to the right Gangtise skill — one-command install of 19 skills, accessKey/secretAccessKey setup, health diagnostics, skill registry.
tags: [gangtise, 岗底斯, investment-research, financial-data, installer, credentials, diagnose, skill-registry, openapi]
source: daymade/claude-code-skills
derived_from: gangtise-copilot
---

# Gangtise Copilot

Wrapper for the Gangtise investment-research OpenAPI skill suite: install 19 skills, configure creds, diagnose, route data questions.

## One-shot install
1. Download this skill (git clone `daymade/claude-code-skills` → copy `gangtise-copilot/`; fallback: GitHub contents API per file, retry 3× on failure).
2. Register with agent (OpenClaw: symlink + enable in gateway config).
3. `bash scripts/install_gangtise.sh --preset full` — downloads 4 ZIP bundles from official Huawei OBS (`gts-download.obs.myhuaweicloud.com/skills/`), extracts 19 skill dirs, symlinks into detected agents (`~/.claude/skills/`, `~/.agents/skills/`, `~/.openclaw/skills/`).
4. `bash scripts/configure_auth.sh --access-key <ak> --secret-key <sk>` — writes `~/.config/gangtise/authorization.json` (600) + live auth verify + `~/.GTS_AUTHORIZATION` runtime token + **symlinks every skill's `.authorization` to the shared file**. ⚠️ Run this even if authorization.json exists — it creates missing symlinks.
5. `bash scripts/diagnose.sh` — expect 9 pass ✅. Cross-ref `references/known_issues.md` on any ❌.

## Install presets
- **minimal** (default): `gangtise-data`, `-file`, `-kb` — public `open-*` endpoints, works on any authed account.
- **workshop**: alias for minimal.
- **full**: all 19 — most `-client` skills fail without `skills-backend/*` ACL (check ISSUE-007 first).
- `--only data-client,kb-client` for custom subset.

## Wrapper contract
Never vendor/fork upstream; never pin a version in SKILL.md; ask before touching installed skills; teach (show what downloaded from where); never hardcode keys; never make investment recommendations.

## Credentials
Shape A: `{accessKey, secretAccessKey}` (common, auto-refresh). Shape B: `{long-term-token: "Bearer ..."}`. One shared XDG file, 19 symlinks → rotate by editing one file then `configure_auth.sh --verify-only`. Live auth: `open.gangtise.com/application/auth/oauth/open/loginV2`.

## Diagnose (read-only, exit 0/1/2)
Checks skill presence per agent, authorization.json mode 600, symlink validity, live auth, RAG endpoint liveness (proves `rag` scope).

## Skill registry — route a data question
- **Data layer** → `gangtise-data-client` (OHLC `quote`, `financial`, `valuation`, `main_business`, `shareholder`, `industry_indicator`, `security`, `block_component`, `index`); `gangtise-kb-client` (semantic KB search); `gangtise-file-client` (list docs by type/date/security); `gangtise-web-client` (open web).
- **Workflow layer** → `stock-research` (L1-L4 reports), `opinion-pk` (adversarial thesis), `thematic-research`, `stock-selector`, `event-review`, `interview-outline`, `announcement-digest`, `opinion-summarizer`, `wechat-summary`, `data-processor`. These enforce compliance (no 买入/卖出/目标价/推荐 language).
- **Utility** → `stockpool-client`, `file-client-no-download`, legacy `data`/`file`/`kb`.
Note: `file-client-no-download` + `stockpool-client` exist ONLY inside `gangtise-skills-client.zip`.
