---
name: Research Summarizer
description: Use when summarizing a paper/article/report, comparing multiple sources, extracting citations, or creating a structured research brief from documents you already have — extracts findings, compares across sources, formats citations.
tags: [research, summarize, literature-review, citation, source-comparison, research-brief, synthesis, imrad, apa]
source: alirezarezvani/claude-skills
derived_from: product-team/research-summarizer
---

# Research Summarizer

Turn dense source material the user *already has* (papers, articles, reports) into actionable briefs. No web search. If the user wants you to *find* sources, route to a research/discovery skill instead.

## Workflow 1 — Single-Source Summary

1. **Identify source type** — academic → IMRAD (Intro/Methods/Results/Analysis/Discussion); web article → claim-evidence-implication; technical report → executive summary; docs → reference summary.
2. **Fill the brief** — Title / Author(s) / Date / Source Type, then: Key Thesis (1-2 sentences), Key Findings (each with supporting evidence + source location), Methodology, Limitations, Actionable Takeaways, Notable Quotes (with page).
3. **Assess quality** — credibility (peer-reviewed? primary vs secondary), evidence strength, recency, bias indicators (funding, affiliation, methodology gaps).

## Workflow 2 — Multi-Source Comparison

1. Collect 2-5 sources. 2. Summarize each (above). 3. Build comparison matrix (rows = Central Thesis / Methodology / Key Finding / Sample-Scope / Credibility; columns = each source). 4. Synthesize: where they agree (stronger signal), disagree (needs investigation), gaps, weight of evidence. 5. Produce synthesis brief: Consensus Findings / Contested Points / Gaps / Recommendation.

## Workflow 3 — Citation Extraction

1. Detect DOI/URL/author-year/numbered citations and deduplicate. 2. Format in requested style. 3. Classify by type: primary (original research/data), secondary (reviews/meta-analyses), tertiary (textbooks). 4. Output sorted bibliography with classification tags. Formats: APA 7 (default), IEEE, Chicago, Harvard, MLA 9.

## Quality Assessment Framework

Rate each source on 4 dimensions (High/Medium/Low): Credibility, Evidence, Recency, Objectivity. Overall: 4 Highs = strong (cite confidently); 2+ Mediums = adequate (cite with caveats); 2+ Lows = weak (verify independently).

## Proactive Triggers

No date → note it, lose credibility points · contradicts other sources → highlight explicitly, don't paper over · paywalled → note limited access · only one source for a compare → ask for ≥1 more · incomplete citations → flag missing fields, never invent metadata · 5+ years old in a fast field → warn about obsolescence.

## Verification Loop (before delivering)

1. Every Key Finding cites a source location — no unanchored claims. 2. Citation count matches the bibliography. 3. Each source carries a 4-dimension quality rating; weak sources flagged not silently included. 4. Comparison matrix has one row per dimension, one column per source. 5. Missing metadata marked "not stated", never invented.
