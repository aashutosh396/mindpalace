---
name: upload-post
description: "Use when publishing or scheduling content to multiple social platforms via the Upload-Post API — posting videos, photos, carousels, text, or documents to TikTok, Instagram, YouTube, LinkedIn, Facebook, X (Twitter), Threads, Pinterest, Reddit, or Bluesky; cross-posting, scheduling, analytics, upload history, or FFmpeg media processing."
version: 1.0.0
license: MIT
tags: [social-media, upload-post, cross-posting, scheduling, tiktok, instagram, youtube, linkedin, analytics]
source: https://github.com/Upload-Post/upload-post-skill
derived_from: awesomeclaude
platforms: [tiktok, instagram, youtube, linkedin, facebook, x, threads, pinterest, reddit, bluesky]
prerequisites: [upload-post account, connected social accounts, profile, api key]
---

# Upload-Post API

Post content to many social platforms with a single API call.

Docs: https://docs.upload-post.com — LLM-friendly: https://docs.upload-post.com/llm.txt

## Setup

1. Create account at upload-post.com, connect social accounts.
2. Create a **Profile** (e.g. "mybrand") — links your connected accounts.
3. Generate an **API Key** from the dashboard.
4. The `user` parameter in every call is the **profile name** (not a username) — it decides which connected accounts receive the post.

## Auth

Header: `Authorization: Apikey YOUR_API_KEY`
Base URL: `https://api.upload-post.com/api`

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/upload` | POST | Upload videos |
| `/upload_photos` | POST | Photos / carousels |
| `/upload_text` | POST | Text-only posts |
| `/upload_document` | POST | Documents (LinkedIn only) |
| `/uploadposts/status?request_id=X` | GET | Async upload status |
| `/uploadposts/history` | GET | Upload history |
| `/uploadposts/schedule` | GET | List scheduled posts |
| `/uploadposts/schedule/<job_id>` | DELETE / PATCH | Cancel / edit scheduled post |
| `/uploadposts/me` | GET | Validate API key |
| `/analytics/<profile>` | GET | Analytics |
| `/uploadposts/facebook/pages` | GET | Facebook pages |
| `/uploadposts/linkedin/pages` | GET | LinkedIn pages |
| `/uploadposts/pinterest/boards` | GET | Pinterest boards |
| `/ffmpeg` | POST | Process media via FFmpeg |

## Upload video

```bash
curl -X POST "https://api.upload-post.com/api/upload" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F "platform[]=instagram" -F "platform[]=tiktok" \
  -F "video=@video.mp4" -F "title=My caption"
```

Key params: `user`, `platform[]`, `video` (file or URL), `title` (all required); `description`, `scheduled_date` (ISO-8601), `timezone` (IANA), `async_upload=true` (background), `autogenerate=true` (server AI-fills blank per-platform title/description from the media; also `autogenerate_title`/`autogenerate_description`/`autogenerate_language`), `first_comment`.

## Upload photos

```bash
curl -X POST "https://api.upload-post.com/api/upload_photos" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" -F "platform[]=instagram" \
  -F "photos[]=@photo1.jpg" -F "photos[]=@photo2.jpg" \
  -F "title=My caption"
```

Instagram & Threads support mixed carousels (photos + videos in one post).

## Upload text

```bash
curl -X POST "https://api.upload-post.com/api/upload_text" \
  -H "Authorization: Apikey YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"user":"profile_name","platform":["x","threads","bluesky"],"title":"My text post"}'
```

Supported: X, LinkedIn, Facebook, Threads, Reddit, Bluesky.

## Upload document (LinkedIn only)

Native LinkedIn document post (carousel viewer). `document=@file` (PDF/PPT/PPTX/DOC/DOCX, max 100MB / 300 pages), `title` (required), `description` (commentary above doc), `visibility` (PUBLIC/CONNECTIONS/LOGGED_IN/CONTAINER), `target_linkedin_page_id` (post to company page).

## Platform support matrix

| Platform | Videos | Photos | Text | Documents |
|---|---|---|---|---|
| TikTok | ✓ | ✓ | - | - |
| Instagram | ✓ | ✓ | - | - |
| YouTube | ✓ | - | - | - |
| LinkedIn | ✓ | ✓ | ✓ | ✓ |
| Facebook | ✓ | ✓ | ✓ | - |
| X (Twitter) | ✓ | ✓ | ✓ | - |
| Threads | ✓ | ✓ | ✓ | - |
| Pinterest | ✓ | ✓ | - | - |
| Reddit | - | ✓ | ✓ | - |
| Bluesky | ✓ | ✓ | ✓ | - |

## Scheduling

Add `scheduled_date` (ISO-8601) + `timezone`. Response returns `job_id`. Manage: `GET /uploadposts/schedule` (list), `DELETE /uploadposts/schedule/<job_id>` (cancel), `PATCH /uploadposts/schedule/<job_id>` (edit date/title/caption).

## Status / history / analytics

- Status: `GET /uploadposts/status?request_id=XXX` (async or scheduled; or use `job_id`).
- History: `GET /uploadposts/history?page=1&limit=20` (limit 10/20/50/100) → timestamps, platform, success, post URLs, errors.
- Analytics: `GET /analytics/<profile>?platforms=instagram,tiktok` → followers, impressions, reach, profile views, time-series.

## Helper lookups

`GET /uploadposts/facebook/pages`, `/linkedin/pages`, `/pinterest/boards` to fetch the page/board IDs required by their platform params. `GET /uploadposts/reddit/detailed-posts?profile_username=X` returns up to 2000 posts with media URLs/dimensions.

## FFmpeg editor

```bash
curl -X POST "https://api.upload-post.com/api/ffmpeg" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "file=@input.mp4" \
  -F "full_command=ffmpeg -y -i {input} -c:v libx264 -crf 23 {output}" \
  -F "output_extension=mp4"
```

Use `{input}`/`{output}` placeholders (multi-input: `{input0}`, `{input1}`...). Poll job until `FINISHED`, download from `/ffmpeg/job/<job_id>/download`. Quotas: Free 30min/mo → Business 10000min/mo.

## Error codes

400 bad request / missing params · 401 invalid key · 404 not found · 429 rate limit / quota · 500 server error.

## Gotchas

- Videos auto-switch to async if >59s processing.
- X long text becomes a thread unless `x_long_text_as_post=true` (auto-splits at 280 chars; media attaches to first tweet only).
- Facebook requires a Page ID — Meta does not support personal profiles.
- Instagram/Threads support mixed photo+video carousels.
- Per-platform overrides exist (`tiktok_title`, `instagram_title`, `youtube_title`, `privacy_level`, `subreddit`, `pinterest_board_id`, etc.) — see upstream `references/platforms.md` and `references/requirements.md` for full param + media-spec tables.
