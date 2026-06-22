---
name: StepFun stepaudio-2.5-tts
description: Use when generating Chinese/Japanese speech with StepFun's stepaudio-2.5-tts (emotion/prosody control, voice lines, dubbing), migrating from step-tts-2, or hitting the voice_label / censorship_block errors — Contextual TTS via natural-language instruction + inline parentheses.
tags: [tts, stepfun, stepaudio, text-to-speech, voice, prosody, chinese, japanese, dubbing, voice-cloning]
source: daymade/claude-code-skills
derived_from: stepfun-tts
---

# StepFun stepaudio-2.5-tts

Generate Chinese/Japanese speech with `stepaudio-2.5-tts` — Contextual TTS where emotion and prosody go through natural-language description, not fixed labels.

> Companion: for transcription with the sibling `stepaudio-2.5-asr`, use the stepfun-asr skill (shared key, different endpoint + body).

## Two pitfalls this exists for
1. `stepaudio-2.5-tts` **rejects** `voice_label` (the step-tts-2 way). Emotion/prosody now go through `instruction` (natural language, ≤200 chars) + inline `()` parentheses inside the text.
2. Stricter censorship — 死 / 消失 / sensitive political terms return `censorship_block`.

## Config and auth
Key in `$STEPFUN_API_KEY` (preferred) or `${CLAUDE_PLUGIN_DATA}/config.json` `{"api_key":"..."}` (cross-session). If unset, ask the user to paste it — don't guess/placeholder. Keys at https://platform.stepfun.com/ → API Keys. **Use a Normal key, not a Plan key** (Plan keys are text-only and silently fail on audio).
```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}" && echo '{"api_key":"<key>"}' > "${CLAUDE_PLUGIN_DATA}/config.json"
```

## Tasks
| Want | Script | Key detail |
|---|---|---|
| Synthesize 1-500 char Chinese w/ emotion | `scripts/tts_generate.py` | `instruction` for mood, `()` for inline prosody |
| Long text (500-1000 char) | `scripts/tts_generate.py` | 1000-char hard cap; split at semantic boundaries above |
| Batch game/app voice lines | `scripts/tts_generate.py --batch <jsonl>` | handle `censorship_block` per-line |
| Migrate from step-tts-2 | `references/migration_from_v2.md` | voice_label → instruction rewrite + censorship list |

Single line: `python3 scripts/tts_generate.py --text "你好" --out /tmp/hello.mp3 --instruction "温暖的希望感"`.

## Contextual TTS
- **Global (`instruction`, ≤200 chars)** — overall tone, like stage direction: `"克制的悲伤，语气低沉柔弱"`.
- **Inline (`()` inside input)** — sentence-internal directives consumed as directions, NOT read aloud: `"(试探着问)你好吗？(开心地)太好了！"`. Use for pauses, breath, emphasis, mid-sentence emotion shifts.

## Common errors
| Error | Cause | Fix |
|---|---|---|
| `voice_label is not supported for v2 models` | sent voice_label | remove it; put intent in `instruction` |
| `censorship_block` | sensitive word | rewrite phrase OR fall back to step-tts-2 for that line (mixed-model OK) |
| silent truncation | input > 1000 chars | split at semantic boundaries |

## Design invariants
1. Non-destructive A/B: write regenerated corpus to a parallel dir (`voice/zh_v25/`), never overwrite production.
2. Per-line censorship: log skipped IDs, continue batch; mixed-model fallback is normal.
3. New code targets `instruction` + inline `()` only — no `voice_label` branch.

## Pricing (verified 2026-04, volatile)
Contextual synthesis ~5.8 元/万字符; zero-shot cloning ~9.9 元/音色. Re-verify before quoting. `stepaudio-2.5-tts` is ~20% slower than step-tts-2 with audible prosody improvement.
