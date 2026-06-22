---
name: IMA Copilot (Tencent IMA skill installer/repair)
description: Use when installing, troubleshooting, or personalizing the official Tencent IMA skill — one-command install across agents, XDG credential setup, runtime repair of upstream SKILL.md bugs (with consent), and fan-out KB search.
tags: [ima, tencent, knowledge-base, installer, diagnose, repair, fan-out-search, xdg-credentials, wrapper]
source: daymade/claude-code-skills
derived_from: ima-copilot
---

# IMA Copilot

Wrapper layer (NOT a replacement) for the official Tencent IMA skill: install, configure, diagnose/repair, fan-out search.

## Wrapper contract (do not violate)
- **Never vendor upstream files** — carry repair *instructions*, not patched files.
- **Repairs at runtime, not ship time** — idempotent, re-detect after upstream updates.
- **Always ask before touching upstream files** (AskUserQuestion).
- **Teach, don't hide** — show exactly what changed + backup location.

## Routing by intent
install ima → Cap 1; configure key → Cap 2; error/SKILL.md warning/frontmatter → Cap 3; search X → Cap 4; "run from scratch" → 1→2→3→4. When in doubt start Cap 3 (diagnose) — it shows what's blocked.

## Cap 1 — Install
`bash scripts/install_ima_skill.sh` — downloads latest official release, stages in temp, hands to `npx skills add` across Claude Code/Codex/OpenClaw. Auto-detects installed agents, skips absent ones, installs `-g` in symlink mode (first agent canonical, rest symlinked → one repair propagates).

## Cap 2 — Credentials (XDG)
`~/.config/ima/client_id` + `api_key` (mode 600), dir 700. Env `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY` override. Setup: create Client ID + API Key at `ima.qq.com/agent-interface` → write XDG → liveness call to `.../openapi/wiki/v1/search_knowledge_base` with `{"query":"","cursor":"","limit":1}` (expect `code:0, msg:success`).

## Cap 3 — Diagnose & repair (core)
1. `bash scripts/diagnose.sh` — read-only, one line per check (install per agent, creds valid, ISSUE-NNN found).
2. Look up each ⚠️/❌ in `references/known_issues.md` (symptom, root cause, strategies A/B/skip, exact commands, files touched).
3. **AskUserQuestion** for every issue with >1 strategy — frame in user-outcome terms, never offer a single "just fix it" when multiple strategies exist.
4. Execute chosen strategy — **idempotent + backed up** to `/tmp/ima-copilot-backups/<ts>/` + reversible.
5. Re-run diagnose, show diff (⚠️→✅); if not flipped, surface raw before/after, don't silently retry.
Repairs are temporary by design — upstream upgrades replace everything; rerun repair after upgrade (if upstream ever fixes it, diagnose reports ✅ with no prompt).

## Cap 4 — Fan-out search
IMA OpenAPI constraints: no cross-KB endpoint (client-side fan-out), no relevance score in results, silent 100-result/KB truncation (no `is_end`). `python3 scripts/search_fanout.py "<query>"` reads `~/.config/ima/copilot.json` (priority KBs, skip list — 100% user-configured, never hardcode), enumerates KBs, fans out parallel, detects truncation by exact-100 length, groups results with priority on top. No config → neutral default (all KBs, sort by hit count, no boost).
