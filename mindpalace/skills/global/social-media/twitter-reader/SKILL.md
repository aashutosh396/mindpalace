---
name: Twitter/X Reader
description: Use when fetching tweet or X Article content (text, author, engagement metrics, embedded images) into local Markdown — downloads all images and generates frontmatter for PKM.
tags: [twitter, x, tweets, x-articles, jina, scraping, markdown, image-download, pkm]
source: daymade/claude-code-skills
derived_from: twitter-reader
---

# Twitter/X Reader

Fetch tweet/article content with full media support.

## Full article mode (recommended for X Articles w/ images)
```bash
uv run --with pyyaml python scripts/fetch_article.py <article_url> [output_dir]
```
Does: structured data via `twitter-cli` (likes/retweets/bookmarks) → content+images via `jina.ai` → downloads images to `attachments/YYYY-MM-DD-AUTHOR-TITLE/` → complete Markdown w/ local image refs + YAML frontmatter. No setup (twitter-cli auto-installed via uv).

## Simple mode (text-only, Jina API)
```bash
export JINA_API_KEY="..."   # from jina.ai
curl "https://r.jina.ai/https://x.com/USER/status/ID" -H "Authorization: Bearer ${JINA_API_KEY}"
scripts/fetch_tweets.sh url1 url2 url3   # batch
```

## Output
```
output_dir/
├── YYYY-MM-DD-title.md          # frontmatter: source, author, date, likes, retweets, bookmarks
└── attachments/YYYY-MM-DD-author-title/ {01-image.jpg, ...}
```

## URL formats
`x.com/USER/status/ID` (posts), `x.com/USER/article/ID` (long-form), `twitter.com/...` (legacy).

Prefer full article mode for X Articles with images (Jina is text-only).
