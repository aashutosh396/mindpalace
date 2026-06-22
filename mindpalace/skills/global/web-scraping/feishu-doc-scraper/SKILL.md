---
name: Feishu/Lark Doc Scraper
description: Use when a source is a Feishu/Lark URL (docs, wiki, collection, sheets, minutes) and you need faithful local Markdown — prefer the lark-cli API (no model paraphrasing), with docx-export and browser-DOM fallbacks.
tags: [feishu, lark, wiki, scraping, markdown, lark-cli, minutes, fidelity, doc-export]
source: daymade/claude-code-skills
derived_from: feishu-doc-scraper
---

# Feishu Doc Scraper

Extract a Feishu/Lark source into faithful Markdown. **Prefer lark-cli API** — extracts body programmatically, follows collection reference graphs, reads permission from error codes. Browser is fallback, rarely needed.

**Scope**: faithful per-source Markdown + a record of what was extracted. Naming/indexing/dedup belong to the host PKM, not this skill.

## Choose path
- Feishu/Lark URL + lark-cli authed → **Path A** (API). Hit code 131006/99991679 → **Path B** (owner docx export).
- lark-cli not installed → install/auth it (worth it); only if truly impossible → **Path D** (browser DOM).
- Minutes/妙记 link → **Path C**.
- Handed a `.docx` → **Path B**.
A collection/hub is a docx whose body references other docs — Path A handles it by recursively following the reference graph.

## Path A — lark-cli API (primary)
1. `export LARK_CLI_NO_PROXY=1` — Feishu `*.feishu.cn` is direct-connect; proxy leaks creds + DNS hijack.
2. Classify URL → resolve to doc token. `wiki/<node>` is NOT a doc token: `lark-cli wiki spaces get_node --params '{"token":"<node>"}'` → `.data.node.obj_token`. `docx/<token>` fetch directly. `sheets/...` use sheets cmds. `minutes/...` → Path C.
3. Fetch body programmatically (NEVER through the model): `lark-cli docs +fetch --doc <token> --format json > /tmp/f.json 2>/tmp/f.err`, then `jq -r '.data.markdown' /tmp/f.json > source.md`. Keep stdout/stderr separate (deprecation note to stderr; blind-piping `2>/dev/null|jq` gave false Exit 5).
4. Collection → BFS the reference graph: `python3 scripts/feishu_extract_refs.py source.md` enumerates `<mention-doc>`/`<sheet>`/`<image>`/cross-tenant/Minutes refs; fetch each, repeat on new docs until leaves.
5. Acceptance gate: `grep -rlE '<(lark-table|lark-tr|sheet token=|mention-doc|view type=)' .` must be empty.

## Path B — permission denied (131006)
Hard server-side boundary — lark-cli/curl/browser all fail. Ask permission holder to export `.docx`, convert with fidelity (font-size→heading, `w:shd`→highlight via `scripts/restore_docx_headings.py`), then **visually verify** (Feishu docx uses font-size+bold not Word heading styles, so text checks pass while hierarchy is silently flat).

## Path C — Minutes transcript
`lark-cli minutes` returns only metadata. Transcript = native endpoint via `lark-cli api` + extra scope (device-flow login). Never download media and re-ASR — native transcription is far better.

## Path D — browser DOM (last resort)
Virtual-scroll / TOC-driven capture via `scripts/feishu_dom_capture.js`. Slow, flaky; anonymous Chrome only sees publicly-reachable pages.

## Hard rules
- Body NEVER passes through the model — `jq`/`cat`/scripts straight to disk (paraphrasing is undetectable + destroys fidelity).
- `LARK_CLI_NO_PROXY=1` for feishu.cn.
- Transcripts from native transcription, never re-ASR.
- docx Markdown not done until visually verified vs source.
- HTTP 200 from anonymous curl ≠ accessible (login wall returns 200 w/ `accounts.feishu.cn`/`login`/`passport`).
- Final check: `LC_ALL=C grep -rl $'\xef\xbf\xbd' .` must be empty (U+FFFD = encoding corruption).

## Verified dead-ends (don't retry)
Bypassing 131006; downloading docx embedded images via lark-cli; `WebFetch` on `open.feishu.cn/document/...` (use `llms-docs/...txt`); CDP port 9222; `minimax-docx` for docx→md.
