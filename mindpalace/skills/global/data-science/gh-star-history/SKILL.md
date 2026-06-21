---
name: gh-star-history
description: "Use when asked to visualize or compare a GitHub repo's star history, plot stargazer growth over time, or generate a regional/geographic breakdown of who starred a repo (star history chart, stargazer locations, star growth, region breakdown)."
version: 1.0.0
license: MIT
tags: [github, stars, star-history, stargazers, visualization, charts, plotly, region-breakdown, cli, data-viz]
source: https://github.com/ykdojo/gh-star-history
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [gh, node, npx]
---

# gh-star-history

Visualize a GitHub repo's star history and the regional breakdown of its
stargazers as interactive Plotly charts. Powered by the GitHub CLI (`gh`) — no
API token needed beyond `gh auth login`.

## When to use

- "Show the star history / star growth of `<owner/repo>`."
- "Compare stars across these repos."
- "Where are the stargazers of `<owner/repo>` from?" / "region breakdown of stars."

## Prerequisites

- Node.js >= 16, and `npx` available.
- GitHub CLI installed and authenticated: `gh auth login`.

## A. Plain star-history chart (fast path)

Single repo:
```
npx gh-star-history <owner/repo>
```
Compare multiple:
```
npx gh-star-history vuejs/vue withastro/astro sveltejs/svelte
```
Useful flags: `--style blue|green|purple` (single repo only), `--output <path>`,
`--no-open` (don't auto-open browser), `--no-cache` (fetch fresh).

Generates a self-contained interactive HTML file. Data is cached per-repo in
`~/.gh-star-history/`; later runs only fetch new stars.

## B. Region breakdown chart (agentic — needs classification)

This produces a chart of stargazers grouped by country/region. It requires an
LLM pass to classify free-text location strings, so follow these steps in order.

### 1. Fetch stargazer locations (caches data)
```
npx gh-star-region <owner/repo> --no-open
```
Paginates all stargazers via the GitHub GraphQL API and caches results.

### 2. Find unclassified locations
```
npx gh-star-unclassified <owner/repo> > /tmp/unclassified.csv
```
If empty / all already classified, skip to step 5.

### 3. Classify locations into regions
Split `/tmp/unclassified.csv` into batches of ~200 rows and spawn parallel
subagents, one per batch. Each subagent:
- Reads its batch (e.g. `/tmp/locations_batch_0.csv`).
- Determines the region per location.
- Writes `/tmp/locations_classified_0.csv` with columns: `location, count, region`.

Classification rules:
- Standard region names, e.g. "United States", "China", "South Korea".
- US cities/states -> "United States".
- Chinese characters (深圳, 北京, …) -> "China".
- Korean characters (서울, …) -> "South Korea".
- Ambiguous / joke values ("Earth", "localhost", "Matrix") -> "Unknown".
- Keep the exact original location string unchanged.

### 4. Update the location map
Merge new classified rows into `~/.gh-star-history/location_region_map.json`,
adding only mappings that don't already exist. Skip "Unknown" entries.

### 5. Generate the chart
```
npx gh-star-region <owner/repo>
```
Opens the chart in the browser automatically. Do NOT run a separate `open`
command.

## Gotchas

- Requires authenticated `gh`; otherwise the GraphQL fetch fails.
- The region map is a persistent local cache (`~/.gh-star-history/`), so
  classification improves over time across repos — reuse it, don't reclassify
  already-mapped locations.
- `--style` color options only apply to single-repo star-history charts.
- Helper CLIs live in the source repo under `bin/` (`cli.js`, `cli-region.js`,
  `list-unclassified.js`) — invoke via `npx`, no need to copy them.
