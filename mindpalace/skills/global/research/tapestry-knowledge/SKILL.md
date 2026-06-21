---
name: tapestry-knowledge
description: "Use when the user says learn-this/learn this/weave a URL, or asks to extract, download, save, or 'make actionable' an article, blog post, YouTube video transcript, or PDF — extracts clean text from any source and turns it into a Ship-Learn-Next action plan."
version: 1.0.0
license: MIT
tags: [research, content-extraction, youtube-transcript, article-extractor, pdf, ship-learn-next, action-plan, knowledge-capture, learning]
source: https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [curl, python3]
---

# Tapestry — Knowledge Extraction + Action Planning

Master workflow from the Tapestry skills suite. Takes any source URL, pulls clean
readable text out of it, then converts that into a concrete Ship-Learn-Next action
plan. The point: never just consume content — always end with something shippable.

> Note: the upstream repo was renamed to `tapestry-skills`; this skill corresponds
> to its `learn-this` master skill which the author titles "Tapestry". It orchestrates
> three sibling skills: `youtube-transcript`, `article-extractor`, `ship-learn-next`.

## When to use

Trigger phrases: "learn-this <URL>", "learn this <URL>", "weave <URL>",
"help me plan <URL>", "extract and plan <URL>", "make this actionable <URL>",
"turn <URL> into a plan", "download/get/transcribe this YouTube video",
"extract/save this article without the ads", "summarize this PDF into action steps".

Use it whenever the user hands over a URL (video, article, or PDF) and wants the
content captured AND made actionable.

## Workflow

1. Detect content type from the URL.
2. Extract clean text using the right method.
3. Build a Ship-Learn-Next action plan from the extracted text.
4. Save both the content file and the plan file, then summarize.

### Step 1 — Detect type

- YouTube: URL matches `youtube.com/watch`, `youtu.be/`, `youtube.com/shorts`, `m.youtube.com/watch`.
- PDF: URL ends `.pdf`, OR `curl -sI "$URL"` returns `Content-Type: application/pdf`.
- Article: anything else (default / fallback).

### Step 2 — Extract content

**YouTube** (needs `yt-dlp`; auto-install via `brew install yt-dlp`):
- Get title: `yt-dlp --print "%(title)s" "$URL"` (sanitize `/ : ? "` out for filename).
- Download captions: `yt-dlp --write-auto-sub --skip-download --sub-langs en --output temp_transcript "$URL"`.
- Convert the `.en.vtt` to clean text with python3: strip `WEBVTT`/`Kind:`/`Language:`/timestamp (`-->`) lines, strip `<...>` tags, decode `&amp; &gt; &lt;`, and dedupe lines (VTT repeats them). Save as `<Title>.txt`, then `rm` the temp vtt.
- Fallback if no subs: Whisper (`pip3 install openai-whisper`).

**Article** (prefer `reader` (npm `reader-cli`) → else `trafilatura` (pip) → else curl+HTMLParser fallback):
- `reader "$URL"` (Mozilla Readability), title = first `# ` line.
- or `trafilatura --URL "$URL" --output-format txt --no-comments`; title from `--json` metadata.
- fallback: curl the page, parse with python `HTMLParser` keeping only `p/article/main`, skipping `script/style/nav/header/footer/aside/form`; title from `<title>`.
- Save as `<Article Title>.txt` (sanitize, cap ~80 chars).

**PDF** (needs `pdftotext` from poppler — `brew install poppler` / `apt install poppler-utils`):
- `curl -L -o file.pdf "$URL"` then `pdftotext file.pdf out.txt` → `<name>.txt`.

### Step 3 — Ship-Learn-Next plan

Read the extracted text, then produce a plan (don't ask — do it automatically):
- Extract actionable lessons, not a summary.
- Define one specific 4–8 week quest.
- Rep 1 = shippable THIS week; Reps 2–5 = progressive iterations, each with a
  reflection question.
- Framework: SHIP (make something real) → LEARN (honest reflection) → NEXT (plan next rep).
  "100 reps beats 100 hours of study."
- Save as `Ship-Learn-Next Plan - <Quest Title>.md`.

### Step 4 — Present

Report: detected type, content file + word count, plan file, the one-line quest,
Rep 1 goal, and close with the commitment question: "When will you ship Rep 1?"

## Gotchas

- Verify the content file is non-empty BEFORE building a plan — failed extraction
  must not produce a plan.
- Auth-walled pages / private videos will fail extraction; tell the user plainly.
- Show a preview (first ~10 lines) of extracted text so the user can sanity-check.
- macOS-oriented installs (brew); on Linux swap to apt/pip equivalents.
- Full reference scripts live in the source repo under `learn-this/SKILL.md`,
  `youtube-transcript/`, `article-extractor/`, `ship-learn-next/`.
