---
name: StepFun stepaudio-2.5-asr
description: Use when transcribing Chinese/English audio with StepFun's stepaudio-2.5-asr, landing long recordings (5-30 min) in one call, migrating from step-asr, or hitting the misleading `model stepaudio-2.5-asr not supported` error — SSE endpoint at /v1/audio/asr/sse, not /v1/audio/transcriptions.
tags: [asr, stepfun, stepaudio, speech-recognition, transcription, sse, long-audio, chinese, audio-to-text]
source: daymade/claude-code-skills
derived_from: stepfun-asr
---

# StepFun stepaudio-2.5-asr

Transcribe audio with `stepaudio-2.5-asr` — long audio in one call (no chunking) — but only if the request hits the right endpoint with the right body.

> Companion: for TTS with the sibling `stepaudio-2.5-tts`, use the stepfun-tts skill (shared key, different endpoint).

## Three traps this exists for
1. **Wrong endpoint, wrong error**. It lives on `/v1/audio/asr/sse` (SSE streaming, JSON body, base64 audio), NOT `/v1/audio/transcriptions` (that serves older step-asr). Wrong endpoint returns `model stepaudio-2.5-asr not supported` — identical in structure to a genuinely nonexistent model. Don't waste time filing whitelist tickets.
2. **Plan key vs Normal key**. Plan (text-only) keys can't call audio endpoints; failure is a silent 4xx with no auth-shaped message. Get a Normal key.
3. **SSE error events are real**. Censorship can fire on ASR too — handle `type: error` events, don't assume only `delta`/`done` arrive.

## Config and auth
Resolve order (fail-fast, no defaults): `$STEPFUN_API_KEY`, then `${CLAUDE_PLUGIN_DATA}/config.json` `{"api_key":"..."}`. If unset, ask the user to paste it. Keys at https://platform.stepfun.com/ → API Keys. **Use a Normal key.**

## Quick start
```bash
python3 scripts/asr_transcribe.py /path/to/audio.mp3            # plain text on stdout
python3 scripts/asr_transcribe.py /path/to/audio.mp3 --json     # usage/timing
python3 scripts/asr_transcribe.py /path/to/audio.mp3 --language en
```
The script handles base64, the nested `{audio:{data, input:{transcription, format}}}` body, SSE parsing, and the misleading-endpoint pitfall.

## Decision table
| Scenario | Action |
|---|---|
| <5 min, zh/en, mp3/wav/ogg/opus | `asr_transcribe.py audio.mp3` |
| 5-30 min | same script — 32K context, single call, no chunking |
| >30 min | split with ffmpeg first (API rejects oversized) |
| need billing data | `--json` → `usage.input_tokens`/`total_tokens` from `transcript.text.done` |
| highly repetitive (same phrase 5+×, >90s) | cross-validate with step-asr-1.1 (repetition hallucination) |
| `model not supported` | wrong endpoint — switch to `/v1/audio/asr/sse` |
| silent 4xx | key is Plan not Normal |

## Formats
`.mp3` (default), `.wav`, `.ogg`, `.opus` (→ ogg flag), `.pcm` (needs rate/channel/bits). For mp4/m4a/webm transcode to one of the above first. Production often pre-transcodes to OGG/Opus 16kHz mono to shrink base64 payload.

## Performance (verified 2026-04)
32K context (≤30 min single call); ~85-101× RTF on long audio; ~5.3× vs step-asr-1.1 at 100s+; only ~2× at 5-15s (LLM spin-up dominates short clips — modest ROI for many short clips).

## Design invariants
1. Always go through SSE (no non-streaming buffer).
2. Take final text from `transcript.text.done.text` (concatenated deltas can drift; deltas are for progressive UI only).
3. Handle `error` events — a blocked-content event returns `type: error` with no `done`.
4. Fail-fast on missing key — never default to placeholder/empty.

## Pricing
In invitation beta (2026-04), no public per-minute rate. step-asr-1.1 baseline 2.2 元/小时; invitation PDF implies ~0.4 元/小时 ("成本直降 80%"), not yet on pricing page. Re-verify before quoting.
