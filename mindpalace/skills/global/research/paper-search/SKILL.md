---
name: paper-search
description: "Use when searching for academic / scientific papers, finding research citations or scholarly references, looking up a paper by DOI or OpenAlex ID, or asking for peer-reviewed backing on a topic (keywords: academic paper, research paper, citation, DOI, OpenAlex, scholar, abstract, journal, peer-reviewed, scientific evidence)."
version: 1.0.0
license: MIT
tags: [research, papers, academic, citations, openalex, doi, science, literature, scholar]
source: https://github.com/ykdojo/paper-search
derived_from: awesomeclaude
prerequisites:
  commands: [curl, jq]
---

# paper-search

Search academic papers and fetch details (title, authors, citation count, DOI,
abstract, open-access PDF link) via OpenAlex — 250M+ works, free, no API key.

## When to use
- User wants scientific/academic backing or citations for a claim or topic.
- User asks to find research papers on a subject.
- User gives a DOI URL or OpenAlex ID and wants the paper details.
- Building a literature review or exploring a citation graph.

## How to use

Two helper scripts ship with the source repo (paths: `scripts/search.sh` and
`scripts/paper.sh` in https://github.com/ykdojo/paper-search). Locate the
installed copies first:

```
find ~/.claude -name "search.sh" -path "*/paper-search/*" 2>/dev/null | sort -V | tail -1
```

`paper.sh` lives in the same directory as `search.sh`.

### Search by keyword
```
<scripts-dir>/search.sh "your search query" [limit] [sort] [page]
```
- `limit`: results per page (default 10, max 200)
- `sort`: `relevance` (default), `cites`, or `date`
- `page`: page number for pagination (default 1)

### Look up one paper by DOI or OpenAlex ID
```
<scripts-dir>/paper.sh <DOI_URL or OpenAlex_ID>
```
- Accepts full DOI URLs (`https://doi.org/10.3390/brainsci8020020`) or OpenAlex
  IDs (`W2789811475`).
- Returns full details: authors, abstract, concepts, open-access PDF link,
  related works.

If the scripts are not installed, the logic is a thin wrapper over the OpenAlex
REST API (`https://api.openalex.org/works`). Equivalent calls:
- Search: `GET /works?search=<query>&per-page=<limit>&page=<page>&sort=relevance_score:desc`
  (sort `cited_by_count:desc` for landmark papers, `publication_date:desc` for recent).
- Single work: `GET /works/<doi-url-or-openalex-id>`.
Include a `mailto=` query param to use OpenAlex's polite pool. Parse JSON with `jq`.

## Tips & gotchas
- Use `relevance` (default) for topical searches; use `cites` to surface
  landmark/highly-cited papers.
- Be specific — "bilingual cognitive advantages executive function" beats
  "bilingualism brain".
- Search results may show "Abstract: N/A" — run `paper.sh` on that work to get
  the full abstract (OpenAlex reconstructs it from an inverted index).
- `related_works` IDs from `paper.sh` can be fed back into `paper.sh` to walk the
  citation graph.
- Recommended flow when asked for scientific backing: search broadly first, pick
  the most relevant/cited papers, then `paper.sh` for full details, and cite as
  (Author, Year, Journal).
