---
name: exploratory-data-analysis
description: "Use when you need to explore, profile, summarize, or sanity-check a data file before analysis — CSV/Parquet/JSON/Excel/SQLite and 200+ formats. Triggers: 'explore this data', 'profile this dataset', 'what's in this file', 'data quality check', 'summarize this CSV', 'EDA', 'understand the structure', 'is this data clean', 'what analysis fits this data'. Auto-detects file type and produces a structured markdown report with schema, stats, quality metrics, and next-step recommendations."
version: 1.0.0
license: MIT
tags: [eda, data-profiling, data-quality, csv, dataframe, statistics, schema, data-cleaning, reporting]
source: https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/skills/exploratory-data-analysis
derived_from: awesomeclaude
---

# Exploratory Data Analysis

## What it does
Automated exploratory data analysis on a data file: detect the format, extract schema and metadata, compute statistical summaries and distributions, assess data quality (missingness, outliers, type consistency), and write a structured markdown report that recommends appropriate downstream analyses. Originally built for scientific formats but the workflow applies to any tabular/structured data a solo dev or analyst hits day to day (CSV, TSV, Parquet, JSON, NDJSON, Excel, SQLite, log dumps).

## When to use
- Someone hands you a data file and asks "what's in here?" / "is this usable?"
- Before modeling, dashboarding, or importing — profile first, decide later
- Data-quality / completeness assessment, schema discovery
- Choosing which analysis or visualization fits a dataset
- Documenting a dataset for a teammate or client

## Workflow

1. **Detect the format.** Use the file extension and magic bytes. For tabular data prefer `polars` or `pandas`; for large files, read a representative sample, not the whole thing.

2. **Extract structure.**
   - Dimensions (rows x columns), column names, inferred dtypes
   - For nested/JSON: key paths, depth, array shapes
   - Encoding, delimiter, header presence, file size

3. **Statistical summary.**
   - Numeric columns: count, mean, std, min/max, quartiles, skew
   - Categorical: cardinality, top values, frequency
   - Datetime: range, granularity, gaps
   - Correlations between numeric columns when relevant

4. **Quality assessment.**
   - Missing values per column (count and %)
   - Outliers (IQR and z-score)
   - Duplicate rows, constant columns, mixed-type columns
   - Cross-check stated vs actual dimensions/metadata

5. **Report.** Write a markdown report named `{original_filename}_eda_report.md` with sections: Overview, File Details, Data Analysis (structure + stats + quality), Key Findings (patterns, issues), Recommendations (preprocessing steps, suitable analyses, visualization approaches, tools).

## Best practices
- **Sample large files.** For millions of rows, analyze a representative sample and say so in the report.
- **Don't load everything into context.** Summarize; surface only the load-bearing numbers.
- **Validate metadata** against actual data (stated row count vs real).
- **Note provenance** when known: source, export date, processing steps, units.
- **Be honest about quality** — flag issues that would break downstream work (high missingness, inconsistent types, suspicious distributions) rather than burying them.

## Output
A single self-contained markdown report. Keep it comprehensive but skimmable: a reader should know in 60 seconds whether the data is usable and what to do next.
