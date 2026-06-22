---
name: YouTube / HLS Downloader
description: Use when downloading YouTube videos/audio or HLS (m3u8) streams with yt-dlp/ffmpeg — handles PO token providers, browser cookies, 403/nsig failures, quality selection, and authenticated stream headers.
tags: [yt-dlp, youtube, hls, m3u8, ffmpeg, po-token, cookies, video-download, audio-extract, nsig]
source: daymade/claude-code-skills
derived_from: youtube-downloader
---

# YouTube Downloader

Reliable video/audio from YouTube + HLS platforms (Mux, Vimeo) via yt-dlp + ffmpeg.

## Non-technical default flow
Assume non-technical user; execute everything yourself, report in plain language. Get URL → fetch metadata (title/uploader/duration/thumbnail; oEmbed fallback if bot-blocked) → render thumbnail `![Thumbnail](URL)` → offer choices (video best/audio MP3/quality preset/subtitles/save location) → proceed with defaults (best MP4, single video). Never mention cookie details ("used your Chrome login session"). Confirm playlist/dep-install/cookie access first. Brief legal reminder (rights to download).

## Reliable SOP (internal)
1. Quote URLs (zsh globs `?`).
2. Proxy active for yt-dlp AND PO token providers.
3. "Sign in to confirm not a bot" → request permission, use browser cookies; don't proceed without.
4. Start PO token provider before download (fail fast). Docker bgutil if available; else browser WPC.
5. Cookies in use → `web_safari` client; else `mweb` for PO tokens.
6. Keep browser open while WPC mints tokens.
7. "Only images available"/"Requested format not available" → PO token failure, retry after fixing provider/browser.
8. SSL EOF/fragment errors → proxy/network, retry progressive formats / better proxy.

## High-quality workflow
Verify yt-dlp ≥ 2025.10.22 (`yt-dlp --version`; outdated → nsig failures). Check formats `yt-dlp -F URL` (only format 18/360p → need PO token). Install provider: `<ytdlp-python> -m pip install bgutil-ytdlp-pot-provider` (find python via `head -1 $(which yt-dlp)`). Download: `yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" URL`. Verify: `ffprobe ... video.mp4`.

## Alternatives & tasks
Cookies: `yt-dlp --cookies-from-browser chrome -f "..." URL` (same IP/proxy; no Android client with cookies). Audio: `yt-dlp -x --audio-format mp3 URL`. Subtitles: `--write-subs --sub-lang en`. WebM→MP4: `ffmpeg -i v.webm -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k v.mp4`.

## Troubleshooting
Only 360p → update yt-dlp + PO token or cookies. nsig fail → update + PO token, or Android client `--extractor-args "youtube:player_client=android"`. Bot check → cookies + web_safari.

## HLS (m3u8) via ffmpeg
Get rendition URL from DevTools Network (filter m3u8). Identify headers (Referer/Origin/User-Agent). Download:
```bash
ffmpeg -headers "Referer: https://example.com/" \
  -protocol_whitelist file,http,https,tcp,tls,crypto,httpproxy \
  -i "https://cdn.../rendition.m3u8?params" -c copy -bsf:a aac_adtstoasc out.mp4
```
Separate audio/video → download each then `ffmpeg -i video.mp4 -i audio.m4a -c copy merged.mp4`. 403 → check Referer matches source + query params present. yt-dlp hangs on cookie extraction → use ffmpeg directly. Empty segments → expired signatures, get fresh URLs and download immediately.

## Bundled
`scripts/download_video.py URL` — auto-starts PO token provider; flags `-q`, `-a`, `--subtitles`, `--cookies-from-browser`, `--player-client`, `--proxy`, `--playlist`, `--info`.
