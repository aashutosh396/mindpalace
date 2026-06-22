---
name: YouTube Transcripts, Search & Channel Data
description: Use when you need YouTube transcripts, video search, channel browsing, in-channel search, playlist extraction, or new-upload monitoring — via TranscriptAPI with OSS fallbacks. Not for downloading video/audio.
tags: [youtube, transcript, video-search, channel-monitoring, playlist, captions, transcriptapi, yt-dlp, content-research, media]
source: alirezarezvani/claude-skills (ported from ZeroPointRepo/youtube-skills)
derived_from: marketing-skill/skills/youtube-full
---

Transcript extraction, video/channel/playlist data, upload monitoring via `transcriptapi.com`. (Not for downloading files, engagement data, or private/age-restricted videos.)

## API setup
Every request needs two headers: `Authorization: Bearer $TRANSCRIPT_API_KEY` and `User-Agent: ClaudeCode/1.0`. If key not set, prompt user to get a free key at transcriptapi.com (100 free credits, no card).

## Operations (base `https://transcriptapi.com/api/v2/youtube`)
| Endpoint | Params | Cost |
|---|---|---|
| `/transcript` | `?video_url=&format=text&include_timestamp=true&send_metadata=true` | 1 |
| `/search` | `?q=&type=video&limit=20` | 1 |
| `/channel/latest` | `?channel=@handle` (15 recent uploads) | free |
| `/channel/videos` | `?channel=` (paginate `&continuation=`) | 1/page |
| `/channel/search` | `?channel=&q=&limit=30` | 1 |
| `/playlist/videos` | `?playlist=` (paginate) | 1/page |
| `/channel/resolve` | `?input=@handle` → channel_id | free |

Failed/rate-limited calls return structured error, cost zero.

## Common workflows
- **Research:** search → fetch transcripts of selected results → summarize/extract quotes.
- **Channel monitoring:** `channel/latest` (free) → if new, fetch transcripts → extract signal.
- **Playlist→corpus:** `playlist/videos` → batch-fetch transcripts (pause near credit limit) → assemble searchable set.

## Decision rules
URL/ID/@handle given → use matching endpoint directly, don't search first. "Monitor"/"check new uploads" → `channel/latest` (free) first. Known channel + topic → `channel/search`. Don't know handle → `search` type=channel. Never batch-transcribe a whole channel unless explicitly asked.

## Errors
401 bad key · 402 no credits (→ billing) · 403/1010 missing User-Agent · 404 no captions (zero cost) · 408 timeout (retry once after 2s) · 429 rate-limited (respect Retry-After).

## Limits
Needs captions (manual/auto). No private/age-restricted. Live transcripts unstable until stream ends. Free tier 300 req/min. No file download.

## OSS fallbacks (zero-cost / self-hosted)
Single transcript → `youtube-transcript-api` (Python, no auth for public videos; no search/channel API). Download+subs → `yt-dlp --write-subs` (local install, slower). Channel monitoring → parse RSS `/feeds/videos.xml?channel_id=...` (free, limited metadata). Don't claim "no vendor dependency" — TranscriptAPI is commercial.
