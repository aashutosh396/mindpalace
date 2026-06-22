---
name: ASR Transcribe to Text (Qwen3-ASR)
description: Use when the user wants to transcribe audio/video, do speech-to-text, or convert meeting recordings/lectures/interviews/podcasts to text — uses Qwen3-ASR via local MLX on Apple Silicon (no API key) or a remote vLLM/OpenAI-compatible endpoint.
tags: [asr, speech-to-text, transcription, qwen3-asr, mlx, apple-silicon, vllm, audio-to-text, video-transcription]
source: daymade/claude-code-skills
derived_from: asr-transcribe-to-text
---

# ASR Transcribe to Text

Transcribe audio/video with Qwen3-ASR. Two paths:
| Mode | When | Speed | Cost |
|---|---|---|---|
| Local MLX | macOS Apple Silicon | 15-27× realtime | free |
| Remote API | any platform / local unavailable | depends on GPU | API/self-hosted |
Config persists in `${CLAUDE_PLUGIN_DATA}/config.json`.

## Step 0: detect platform + load config
`cat "${CLAUDE_PLUGIN_DATA}/config.json" 2>/dev/null`. If missing, detect platform (Apple Silicon → recommend local-mlx; else remote-api) and ask the user mode + proxy-bypass, then save config:
```json
{"mode":"local-mlx|remote-api","model":"mlx-community/Qwen3-ASR-1.7B-8bit|Qwen/Qwen3-ASR-1.7B","max_tokens":200000,"endpoint":"URL","noproxy":true,"max_timeout":900}
```

## Step 1: extract audio (if video)
`ffmpeg -i INPUT -vn -acodec pcm_s16le -ar 16000 -ac 1 OUT.wav -y`. Audio files (wav/mp3/m4a/flac/ogg) used directly. Duration: `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 FILE`. Delete extracted WAVs after success.

## Step 2: transcribe
**Local MLX**: `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/transcribe_local_mlx.py IN [IN2 ...] --output-dir OUT`. Loads model once, transcribes sequentially.
**Critical**: upstream `mlx-audio` default `max_tokens=8192` silently truncates audio > ~40 min. Bundled script defaults to `200000`; always pass `max_tokens=200000` if calling `model.generate()` directly.
**Remote API**: health-check `{base}/models` first (with `--noproxy '*'` if config says so), then `curl` the endpoint with `-F file=@AUDIO -F model=...`. On health failure diagnose: ping host / tailscale status → `tailscale ssh USER@HOST "curl localhost:PORT/v1/models"` → toggle `--noproxy '*'`.

## Step 3: verify output (truncation is the #1 failure)
Not empty; plausible char count (~400 chars/min Chinese, ~200 words/min English); check the **ending** — trailing off mid-sentence = max_tokens exhausted. Show first/last ~200 chars. If truncated, ask: retry with higher max_tokens / switch mode / save as-is / abort.

## Step 4: fallback overlap-merge (remote only)
On single-request timeout/OOM: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/overlap_merge_transcribe.py --config "${CLAUDE_PLUGIN_DATA}/config.json" IN OUT.txt` — 18-min chunks, 2-min overlap, fuzzy punctuation-stripped merge. Local MLX needs no overlap-merge (script chunks internally).

## Step 5: recommend correction
ASR output always has recognition errors. Proactively suggest running a transcript-fixer pass on the output (transcribe → correct → review).

Reconfigure: `rm "${CLAUDE_PLUGIN_DATA}/config.json"` then re-run Step 0.
