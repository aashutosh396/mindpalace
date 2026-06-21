---
name: csv-data-summarizer
description: "Use when the user uploads, references, or asks to summarize/analyze/visualize a CSV file or tabular data — generates summary stats, missing-data report, and adaptive pandas/matplotlib charts automatically without asking what to do."
version: 1.0.0
license: MIT
tags: [csv, data-analysis, pandas, matplotlib, seaborn, visualization, summary-statistics, eda, tabular-data, python]
source: https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# CSV Data Summarizer

Analyzes CSV files and produces a complete summary: data overview, statistics,
missing-data analysis, and data-type-aware visualizations — using pandas,
matplotlib, and seaborn.

## When to use

Trigger automatically whenever the user:
- Uploads or references a `.csv` file
- Asks to summarize, analyze, explore, or visualize tabular data
- Asks "what insights can you find in `<file>.csv`?"
- Wants to understand a dataset's structure, quality, or trends

## Core behavior — act, don't ask

This skill is opinionated: run the full analysis immediately. Do NOT ask the
user what they want, offer a menu of options, or stop for direction. Inspect
the data first, decide what is relevant, then deliver a complete analysis with
charts in the first response.

## How it works

1. **Load & inspect** the CSV into a pandas DataFrame.
2. **Profile structure** — row/column counts, dtypes, date columns, numeric
   columns, categorical columns.
3. **Pick relevant analyses based on what is actually present:**
   - Sales/e-commerce (order dates, revenue, products) -> time-series trends, revenue, product performance
   - Customer data (demographics, segments, regions) -> distributions, segmentation, geographic patterns
   - Financial (transactions, amounts, dates) -> trends, stats, correlations
   - Operational (timestamps, metrics, status) -> time-series, performance metrics
   - Survey (categorical responses, ratings) -> frequency, cross-tabs, distributions
   - Generic tabular -> adapt to the column types found
4. **Only build charts that make sense for the data:**
   - Time-series plots only if date/timestamp columns exist
   - Correlation heatmaps only if 2+ numeric columns exist
   - Category distributions only if categorical columns exist
   - Histograms for numeric distributions when relevant
5. **Output** in one pass: data overview, key stats/metrics, missing-data
   analysis, the applicable visualizations, and actionable insights specific to
   this dataset.

## Implementation

The reference implementation lives in the source repo as `analyze.py`, exposing
`summarize_csv(file_path)` which returns a text summary and writes the charts.
Either fetch it from the source or reimplement inline with pandas/matplotlib/
seaborn — the logic is straightforward:
- `df = pd.read_csv(path)`; report `df.shape`, `df.dtypes`, `df.isna().sum()`
- `df.describe()` for numeric stats
- Detect date columns (name contains "date") and parse with `pd.to_datetime`
- Generate only the charts whose required column types are present

Source: https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill/blob/main/analyze.py

## Dependencies

```
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
```
Python >= 3.8.

## Gotchas

- Date detection is name-based (columns containing "date"); rename or pass
  explicit parse hints if your date column is named otherwise.
- Visualizations are skipped, not faked, when the required column types are
  absent — an all-text dataset yields stats but no charts.
- Handles missing data gracefully but report the missing-data percentage so the
  user can judge reliability of the stats.
