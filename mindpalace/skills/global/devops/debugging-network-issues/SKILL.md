---
name: Debugging Network / Streaming Issues (evidence-driven)
description: Use when debugging connection resets (ECONNRESET, HTTP/2 RST_STREAM, INTERNAL_ERROR), SSE/long-poll stalls, fixed-time drops, CDN/proxy/CGNAT idle timeouts, or "works sometimes/fails after N seconds" symptoms — applies falsification-first layered isolation to pin the responsible layer.
tags: [network, debugging, sse, http2, econnreset, cdn, proxy, timeout, falsification, layered-isolation, cloudflare-524]
source: daymade/claude-code-skills
derived_from: debugging-network-issues
---

Evidence-driven methodology for incidents where the obvious cause is probably wrong. Its job is to slow the reflex to diagnose from one log line.

## Triage first — known domain?
If the symptom is macOS Tailscale⨯proxy conflict → tunnel-doctor skill. Cloudflare config (redirects/SSL mode) → cloudflare-troubleshooting. AVD/RDP transport → windows-remote-desktop-connection-doctor. Otherwise continue.

## Core principles
1. **Evidence over assumption** — if you can't point to a concrete artifact (log line, pcap frame, probe output, metric), you're guessing. Add instrumentation/capture before continuing.
2. **Falsification over confirmation** — N confirming sources don't make it true; one falsifier rules it out. Always answer "what observation would make me abandon this hypothesis?" If "nothing", it's unfalsifiable — don't act on it.
3. **Layered isolation** — multi-hop systems (client→CDN→LB→proxy→app→upstream) concentrate bugs at seams. Don't reason about which layer; **test**: run the same request through ≥3 paths differing by exactly one hop, compare where the symptom appears.
4. **Counter-review before committing** — independent reviewers challenge (not confirm) the root cause; filter findings through probability/cost/realistic-scenario/verifiability.

## Workflow
- **Step 0 — Scope:** exact error string (copy-paste; `socket closed` ≠ `ECONNRESET` ≠ `HTTP/2 RST_STREAM INTERNAL_ERROR`), exact ISO-8601 timestamps, reproducibility, who's affected/not, what changed. "Slow" is not a symptom; "took 130.898s then HTTP/2 INTERNAL_ERROR" is.
- **Step 0.5 — Verify the premise:** confirm the symptom is actually happening (timestamped log / DevTools screenshot / repro command / metrics chart), not inferred from frustration or an alert title. If premise fails, the fix is observation, not investigation.
- **Step 0.6 — Large POST bodies: upload-timeout vs processing-timeout.** For CDN-fronted POST/PUT with `Content-Length > ~500KB` returning 524/522/504: compare `bytes_read` to `Content-Length` in the edge/proxy access log. `bytes_read < Content-Length` + connection closed near the timeout = **upload problem**. `bytes_read == Content-Length` + 5xx = processing problem. `status=0` (Caddy) / `-` (nginx) = proxy never wrote a response (downstream closed first). If the request ID never reaches upstream logs, it never finished uploading.
- **Step 1 — Gather direct evidence at every hop:** server logs per hop, client logs (HAR/SDK traces), metrics over the window, distributed trace, packet capture if wire-level. Fill gaps before guessing (env-gated `TRACE_*` flag beats an hour of hypothesis-stacking).
- **Step 2 — Hypotheses (≥3):** for each, name what confirms it, **what falsifies it**, and **which layer boundary the fix targets** (prevents fixing the wrong hop — e.g. a downstream keepalive is useless for an upstream idle timeout).
- **Step 3 — Decisive experiment:** layered isolation. Path A full via CDN (baseline), B `--resolve` to origin IP (rules out CDN if it passes), C server loopback (rules out CDN+LB). If only A fails → CDN; A+B fail, C passes → LB.
- **Step 4 — Instrumentation when needed:** default off, one env var to enable, greppable tags (`[SSE-CHUNK] ts=... req=... bytes=...`), ship permanently.
- **Step 5 — Execute & record:** command/env/inputs/outputs/timestamps vs prediction. If actual ≠ predicted, the hypothesis is wrong — **do not rescue it with ad-hoc auxiliary hypotheses**; write new ones from scratch.
- **Step 6 — Counter-review** before acting.
- **Step 7 — Fix + re-run the same experiment.** If the pre-fix repro can no longer be produced, figure out why before declaring victory.
- **Step 8 — Document wrong turns** (more valuable than the answer).

## Cognitive traps
Circumstantial-evidence convergence; field-semantic confusion (`duration` means different things across tools — verify against docs); single-cause bias; naming assumption (a `spot-instance` may not be one — verify via API); probe self-verification (don't test a broken connection through itself); assumption-rescue cycle; unverified premise; threat-model mismatch (fix targets wrong layer); **reverse-path/directional asymmetry** (A→B healthy ≠ B→A healthy; measure the user's traffic direction from the user's side); edge timeouts masquerading as upstream client aborts (a CF 524 makes the origin log a `status=0` "client abort" — correlate edge code+timestamp+origin logs first).
