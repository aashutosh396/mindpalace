---
name: video-downloader
description: "Use when the user asks to download, save, grab, or rip a YouTube video or its audio — handles quality (best/1080p/720p/480p/360p), format (mp4/webm/mkv), and audio-only MP3 extraction via yt-dlp."
version: 1.0.0
license: MIT
tags: [youtube, video, download, yt-dlp, mp4, mp3, audio, media]
source: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/video-downloader
derived_from: awesomeclaude
prerequisites:
  commands: [python3, yt-dlp, ffmpeg]
---

# Video Downloader

Download YouTube videos with control over quality and format, or extract audio as MP3. Backed by `yt-dlp` (auto-installs if missing; `ffmpeg` needed for stream merging and MP3 conversion).

## When to use

The user wants to download / save / grab / rip a YouTube video, get a specific quality, convert to a format, or pull just the audio as MP3.

## How (helper script)

The upstream skill ships `scripts/download_video.py`. Either fetch it from the source repo (`video-downloader/scripts/download_video.py` on the `master` branch) or just call `yt-dlp` directly — the script is a thin wrapper.

Basic download (best quality, mp4):

```bash
python3 scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Options

- `-q` / `--quality`: `best` (default), `1080p`, `720p`, `480p`, `360p`, `worst`
- `-f` / `--format`: `mp4` (default), `webm`, `mkv` (video only)
- `-a` / `--audio-only`: download audio as MP3
- `-o` / `--output`: output directory (default `/mnt/user-data/outputs/`; on a normal machine set this to a real local path like `~/Downloads`)

Examples:

```bash
python3 scripts/download_video.py "URL" -q 720p
python3 scripts/download_video.py "URL" -a                 # MP3
python3 scripts/download_video.py "URL" -q 1080p -f webm -o ~/Downloads
```

## Direct yt-dlp equivalents (no script)

```bash
# Best mp4 video+audio merged
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"

# Cap at 720p
yt-dlp -S "res:720" --merge-output-format mp4 "URL"

# Audio-only MP3
yt-dlp -x --audio-format mp3 "URL"
```

## Gotchas

- Default output `/mnt/user-data/outputs/` is the sandbox path from the original skill — override with `-o` for a real local download dir.
- Filenames are derived from the video title.
- Playlists are skipped by default (single video only); add `--yes-playlist` to yt-dlp to override.
- `ffmpeg` must be installed for high-quality merges and MP3 extraction.
- Respect copyright / YouTube ToS — only download content you have the right to.
- Higher quality = larger files and slower downloads.
