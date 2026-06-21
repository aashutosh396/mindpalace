---
name: article-extractor
description: "Use when the user gives a blog/article/tutorial URL and wants the readable text saved or extracted — phrases like 'download this article', 'extract the content from <URL>', 'save this blog post as text', 'get the article without ads/navigation/clutter', 'reader view to file'."
version: 1.0.0
license: MIT
tags: [article, extraction, readability, scraping, content, trafilatura, reader, web, text, blog]
source: https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor
derived_from: awesomeclaude
prerequisites:
  commands: [curl, python3]
---

# Article Extractor

Pulls the main body of a web article/blog post (no nav, ads, newsletter forms,
sidebars, social buttons, cookie banners) and saves it as clean text named after
the article title.

## When to use

User provides an article/blog/tutorial URL and wants the text content saved or
cleaned: "download this article", "extract content from <URL>", "save this blog
post as text", "give me the reader view of this".

## Tool priority (use first available)

1. **reader** (Mozilla Readability CLI) — best all-around, Firefox Reader View algorithm.
   - check: `command -v reader`
   - install: `npm install -g @mozilla/readability-cli` (or `npm install -g reader-cli`)
2. **trafilatura** (Python) — best for news/blogs/academic/non-English, complex layouts.
   - check: `command -v trafilatura`
   - install: `pip3 install trafilatura`
3. **fallback** — `curl` + a small Python `html.parser` script (less accurate, no deps).

## Extraction commands

reader:
```bash
reader "URL" > temp_article.txt
TITLE=$(head -n 1 temp_article.txt | sed 's/^# //')   # title is the leading "# " line
```

trafilatura:
```bash
TITLE=$(trafilatura --URL "URL" --json | python3 -c "import json,sys;print(json.load(sys.stdin).get('title','Article'))")
trafilatura --URL "URL" --output-format txt --no-comments > temp_article.txt
# extra flags: --no-tables, --precision (cleaner), --recall (more content, more noise)
```

fallback (no tools installed):
```bash
TITLE=$(curl -s "URL" | grep -oP '<title>\K[^<]+' | head -n1); TITLE=${TITLE%% - *}; TITLE=${TITLE%% | *}
curl -s "URL" | python3 -c "
from html.parser import HTMLParser; import sys
class E(HTMLParser):
    def __init__(s): super().__init__(); s.on=False; s.out=[]; s.skip={'script','style','nav','header','footer','aside','form'}
    def handle_starttag(s,t,a):
        if t not in s.skip and t in {'p','article','main'}: s.on=True
        if t in {'h1','h2','h3'}: s.out.append('\n')
    def handle_data(s,d):
        if s.on and d.strip(): s.out.append(d.strip())
p=E(); p.feed(sys.stdin.read()); print('\n\n'.join(p.out))" > temp_article.txt
```

## Filename + finish

```bash
FILENAME=$(echo "$TITLE" | tr '/' '-' | tr ':' '-' | tr -d '?"<>' | tr '|' '-' | cut -c1-80 | sed 's/^ *//;s/ *$//')
mv temp_article.txt "${FILENAME}.txt"
```
Then show the user: the title, the saved path, and a preview (`head -n 10`).

## Gotchas

- **Paywall / login required** → extractors fail; tell the user the article needs auth, do not fake content.
- **Heavy-JS sites** → reader/trafilatura may return little; try the other tool, then fallback; report if all fail.
- **No tool installed** → fallback works but is noisier; offer the install one-liners above.
- Always verify extraction succeeded (non-empty file) before renaming/saving.
- Keep filename < ~100 chars and strip filesystem-unsafe chars (`/ : ? " < > |`).
