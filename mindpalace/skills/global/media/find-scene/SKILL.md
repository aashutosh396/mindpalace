---
name: find-scene
description: "Use when the user wants to find a movie/TV scene by quote, dialog, time, or visual description, identify a movie from a quote, download a video clip, make a GIF, extract a frame/screenshot/sticker/meme, fetch subtitles, find which episode contains a line, or query IMDB info — via the find-scene.com API."
version: 1.0.0
license: MIT
tags: [movies, tv, scenes, video, clips, subtitles, imdb, quotes, frames, gif]
source: https://github.com/uriva/find-scene-skill
derived_from: awesomeclaude
prerequisites:
  commands: [curl]
---

# find-scene

REST API for searching and downloading movie/TV scenes by dialog, time, or
visual description. Also identifies movies from quotes, finds episodes, extracts
frames, builds memes/GIFs, and queries IMDB.

Note: the original `uriva/find-scene-skill` repo is no longer public. This skill
was harvested from a verified mirror. The live API at `find-scene.com` is the
source of truth; the OpenAPI spec is at
`https://api.find-scene.com/api/openapi.json`.

## When to use
- "Find the scene where …" / "what movie has the line …" / "which episode says …"
- "Download / clip / GIF that scene", "screenshot / frame", "make a meme/sticker"
- "Get the subtitles around …", "popular quotes from …", IMDB id/year lookup

## Setup
- Base URL: `https://api.find-scene.com`
- All endpoints are `POST` with `Content-Type: application/json` (except
  `GET /api/operation/{id}`).
- Every request body needs a `_token` field.
- Token: sign in at https://find-scene.com → https://find-scene.com/settings →
  "Generate new token" (shown once — copy it). Revoke from the same page.

## Conventions
- Responses wrap as `{ "result": <object> }`. Errors: `{ "error": "..." }`
  (HTTP 4xx/5xx) or `{ "result": { "error": "..." } }` (domain error in a 200).
- Time format is always `HH:MM:SS` (e.g. `00:01:30`).
- Two distinct internal hashes — never swap them:
  - **videoHash** — prefix `video-` (from `get_best_video_source`); needed for
    downloads, frame extraction, high-accuracy text lookup.
  - **textSource** — prefix `text-` (from `get_text_source` /
    `get_high_accuracy_text_source`); needed for phrase search + subtitles.
- **Async endpoints** return `{ "operationId": "..." }`. Poll
  `GET /api/operation/{id}` until `status` is `completed`, then read result
  fields. Statuses: `in_progress`, `completed`, `failed`, `cancelled`. Never hand
  an operationId to the user as a link — always resolve it first.
  Async: `get_best_video_source`, `get_text_source`,
  `get_high_accuracy_text_source`, `download_by_time`, `extract_frame`,
  `stitch_videos`, `stitch_videos_side_by_side`, `transcribe_by_time`.

## Key endpoints (all POST, body needs `_token`)
- `quote_to_movie` `{quote}` → candidate movie names.
- `is_string_a_movie_name` `{string}` → `{isMovieName}`.
- `query_imdb` `{query:{title,...}}` → name/imdb id/year/season/episode.
- `popular_quotes_from_title` `{limit, query:{title,...}}` → quotes.
- `find_episode_by_phrase` `{phrase, query:{title,...}, limit}` → season/episode
  (TV shows only, not movies).
- `get_best_video_source` `{query:{title,year,isSeries,season,episode,...}, timeoutSeconds?}`
  → videoHash (async). `timeoutSeconds` caps at 120; leave empty unless user gave a value.
- `get_text_source` `{query, language?, minDuration?}` → textSource (async).
- `get_high_accuracy_text_source` `{query, videoHash, language?}` → textSource
  (async) — prefer this when you already have a videoHash (better timing).
- `search_phrase` `{textSource, phraseSearchParams:{phraseStart, phraseEnd?, nSkip, maxOccurrences}}`
  → occurrences with timestamps.
- `get_srt_entries_around_phrase` / `get_srt_entries_by_time_range` → subtitle text + times.
- `find_by_scene_description` `{description, query?, nResults, nSkip, scoreThreshold?}`
  → visual-search results with timestamps. Do NOT put the title in `description`.
  Use `scoreThreshold` ~0.6 for specific scenes, ~0.3 for vague ones.
- `request_indexing_for_scene_description` `{query}` → request indexing when
  visual search returns nothing; retry later.
- `download_by_time` `{videoHash, startTime, endTime, textSource?, srtOffset?, displayParams?}`
  → clip (async; delivered to user UI+email and billed).
- `extract_frame` `{videoHash, time, textSource?, overrideTextTop?, overrideTextBottom?, displayParams?}`
  → frame/screenshot; the two override fields = meme generator mode (async).
- `stitch_videos` / `stitch_videos_side_by_side` `{urls[], displayParams}` →
  combine clips from completed downloads (async).
- `compute_running_time` `{imdbId}` → runtime seconds.
- `check_quota` → `{creditsRemaining, nextCreditReturnMs}`. Credits roll on a
  30-day window (each returns 30 days after use); if low, tell user when next returns.
- `cancel_operation` `{id}` → cancel a stuck async op.
- `displayParams` (clips/frames): `{removeWatermark, gif, mobile, cropMode?}`.

## Typical workflows
1. **Quote → clip**: `quote_to_movie` → `get_best_video_source` (poll → videoHash)
   → `get_text_source` (poll → textSource) → `search_phrase` (timestamp) →
   `download_by_time` → poll for URL.
2. **Time → clip**: `get_best_video_source` → `download_by_time` → poll.
3. **Visual scene → clip**: `find_by_scene_description` →
   `get_best_video_source` → `download_by_time` → poll.
4. **Episode from quote (TV)**: `find_episode_by_phrase` → `get_best_video_source`
   → `get_text_source` → `search_phrase` → `download_by_time` → poll.
5. **Frame / screenshot / meme**: `get_best_video_source` → `extract_frame` → poll.

## Gotchas
- Always resolve a videoHash first before downloads, frame extraction, or
  high-accuracy text lookups.
- Keep clip durations reasonable (< 60s) to avoid long processing.
- Downloads are billed — confirm intent before calling `download_by_time`.
- If `find_by_scene_description` returns nothing, the video isn't indexed: call
  `request_indexing_for_scene_description`, then retry later.
- 400 = bad/missing params, 401 = bad/missing `_token`, 500 = retry/report.
