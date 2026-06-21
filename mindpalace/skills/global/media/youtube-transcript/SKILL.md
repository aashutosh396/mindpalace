---
name: youtube-transcript
description: "Use when the user gives a YouTube URL or asks to download / get / fetch / extract a transcript, captions, or subtitles from a YouTube video, or to transcribe a YouTube video to text."
version: 1.0.0
license: MIT
tags: [youtube, transcript, subtitles, captions, yt-dlp, whisper, vtt, transcription, media, video]
source: https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [yt-dlp]
---

# YouTube Transcript Downloader

Download a transcript (subtitles/captions) from a YouTube video using `yt-dlp`,
falling back to Whisper speech-to-text only when no captions exist. Output is a
deduplicated plain-text `.txt`.

## When to use
- User pastes a YouTube URL and wants the text.
- "Download / get / fetch transcript", "get captions/subtitles", "transcribe this video".

## Priority order
1. Ensure `yt-dlp` is installed.
2. List available subtitles (`--list-subs`) — never download blind.
3. Try manual subtitles (`--write-sub`) — best quality, human-made.
4. Fall back to auto-generated (`--write-auto-sub`) — usually present.
5. Last resort: Whisper transcription — requires user confirmation (audio download + model install).
6. Convert the `.vtt` to deduplicated plain text and clean up temp files.

## Install check
```bash
command -v yt-dlp
# macOS: brew install yt-dlp
# Debian/Ubuntu: sudo apt update && sudo apt install -y yt-dlp
# any system: pip3 install yt-dlp
```
If install fails, point user to https://github.com/yt-dlp/yt-dlp#installation

## List subtitles first
```bash
yt-dlp --list-subs "YOUTUBE_URL"
```
Note manual vs auto-generated and available languages.

## Download subtitles (no video)
```bash
# Manual (preferred)
yt-dlp --write-sub --skip-download --output "transcript_temp" "YOUTUBE_URL"
# Fallback: auto-generated
yt-dlp --write-auto-sub --skip-download --output "transcript_temp" "YOUTUBE_URL"
```
Both produce `transcript_temp.<lang>.vtt`. Restrict language with `--sub-langs en` if needed.

## Whisper fallback (only if NO subtitles exist)
Confirm with the user before each heavy step.
```bash
# 1. Show size/duration so user can decide
yt-dlp --print "%(duration)s %(filesize_approx)s %(title)s" "YOUTUBE_URL"
# 2. Ensure whisper (ask before installing ~1-3GB models): pip3 install openai-whisper
command -v whisper
# 3. Download audio only
yt-dlp -x --audio-format mp3 --output "audio_%(id)s.%(ext)s" "YOUTUBE_URL"
# 4. Transcribe (base model = good balance; tiny/small/medium/large trade speed vs accuracy)
whisper audio_<id>.mp3 --model base --output_format vtt
# 5. Offer to rm the mp3 afterward
```
Whisper also needs `ffmpeg` (and sometimes rust). Check disk space (models 1-10GB).

## Convert VTT -> deduplicated plain text
YouTube auto-captions repeat lines (progressive/overlapping timestamps). Dedupe while
keeping speaking order:
```bash
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "YOUTUBE_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')
VTT_FILE=$(ls *.vtt | head -n 1)
python3 -c "
import re
seen = set()
with open('$VTT_FILE') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith(('WEBVTT','Kind:','Language:')) and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line).replace('&amp;','&').replace('&gt;','>').replace('&lt;','<')
            if clean and clean not in seen:
                print(clean); seen.add(clean)
" > "${VIDEO_TITLE}.txt"
rm "$VTT_FILE"
```

## Gotchas
- Output filename pattern: `{output}.{lang}.vtt` (e.g. `transcript_temp.en.vtt`).
- By default yt-dlp grabs ALL languages — use `--sub-langs en` to limit.
- Private / age-restricted / geo-blocked videos fail; surface yt-dlp's exact error.
- SSL issues: retry with `--no-check-certificate`.
- Always verify each step succeeded before moving on; clean up temp `.vtt`/`.mp3` after.
- A full end-to-end bash workflow (install -> list -> manual -> auto -> whisper -> dedupe)
  exists in the source SKILL.md if a single scripted run is preferred.
