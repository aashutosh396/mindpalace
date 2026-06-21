---
name: epub-builder
description: "Use when asked to convert markdown/notes/docs/research/blog posts/chat summaries into an EPUB ebook (.epub), make a Kindle/Apple Books/Kobo-readable book, build an ebook from markdown, or generate an EPUB3 file with chapters and a table of contents."
version: 1.0.0
license: MIT
tags: [epub, ebook, markdown, kindle, apple-books, converter, documents, publishing, epub3]
source: https://github.com/smerchek/claude-epub-skill
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# EPUB Builder

Convert markdown documents into a professional EPUB3 ebook file that opens in any
reader: Apple Books, Amazon Kindle (Kindle app), Google Play Books, Kobo, etc.

## When to use

- User has markdown (research notes, articles, blog post, docs) and wants an `.epub`.
- "Turn this into an ebook", "make a Kindle file", "convert to EPUB".
- "Summarize our chat as markdown and export it as an ebook for reference."

## What it produces

A valid EPUB3 file with:
- Chapters auto-split on `#` (H1), sections on `##` (H2).
- Auto table of contents + EPUB3 nav document.
- Metadata (title, author, language). Title defaults to first H1.
- Styled rendering of bold, italic, links, ordered/unordered (nested) lists,
  code blocks (monospace, accent border), inline code, tables (zebra rows,
  styled headers), blockquotes, horizontal rules.

## How to run

The skill is two importable Python modules, not a CLI. Get them from the source repo:
`markdown-to-epub/scripts/epub_generator.py` and `markdown_processor.py`
(github.com/smerchek/claude-epub-skill). Place both in the working dir.

Install deps (pin to known-good versions):

```bash
python3 -m pip install ebooklib==0.18.0 markdown2==2.4.12 Pygments==2.17.2
```

Convert — the simplest path is the convenience function:

```python
from epub_generator import create_epub_from_markdown

# markdown_content can be read from a file or passed inline
ok = create_epub_from_markdown(
    markdown_content,           # raw markdown string
    "output.epub",             # output path
    title="My Book",           # optional; falls back to first H1
    author="Author Name",      # optional
)
```

For finer control (custom metadata, language, reusing parsed chapters), use the
classes directly: `MarkdownProcessor().process(md)` returns `{'metadata',
'chapters'}`, then `EPUBGenerator(metadata).generate(chapters, output_path)`.

## Authoring tips for clean output

- Use H1 (`#`) for chapter breaks — these become TOC entries and page breaks.
- Use H2 (`##`) for sections inside a chapter.
- Make headers descriptive; they ARE the table of contents.
- Stick to standard markdown for cross-reader compatibility.

## Gotchas

- Empty TOC = no H1 headers in the source. Add `#` chapter headings.
- EPUB doesn't open = malformed markdown (e.g. unmatched link brackets). Validate syntax.
- Fonts/styling differ per reader — readers apply their own; this is expected, not a bug.
- Memory use is ~3-5x the markdown source size for large documents.
- HTML special chars in content are escaped automatically.

## Not (yet) supported

Cover-image generation, image embedding, .mobi output, syntax-highlight colors
(language tag is captured but rendered monospace only), multi-document merge.
