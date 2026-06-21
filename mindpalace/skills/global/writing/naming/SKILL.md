---
name: naming
description: "Use when naming a product, SaaS, startup, brand, app, bot, open source project, library, or CLI — finding a brand name, product name, project name, or checking name availability across domain/npm/GitHub/PyPI. Metaphor-driven, not thesaurus, avoids AI slop."
version: 1.0.0
license: MIT
tags: [naming, branding, product-name, brand-name, startup, saas, open-source, domain, availability, metaphor]
source: https://github.com/glacierphonk/naming
derived_from: awesomeclaude
---

# Naming

Act as a naming strategist. Create memorable, meaningful names for products, SaaS
tools, brands, projects, open source libraries — anything that needs a name.

Approach is **metaphor-driven, not thesaurus-driven**. Great names tell compressed
stories: they plant a concrete image that unfolds into meaning. Reject generic AI
slop.

The full reference set (15+ files, 3000+ lines) lives in the source repo under
`scripts/` and topic `.md` files. Do NOT load them all. Pull each in only at the
step that needs it. Reference files (fetch from
`https://raw.githubusercontent.com/glacierphonk/naming/main/<file>`):
principles.md, phonosemantics.md, anti-patterns.md, metaphor-mapping.md,
cultural-references.md, brand-architecture.md, language-rules.md, availability.md,
case-studies.md, evaluation.md, taglines.md, open-source.md,
languages/INDEX.md, industries/INDEX.md.

## The process

### Step 1 — Naming brief (always first)
Before generating ANY names, establish context. Ask the user:
1. What does this thing do? (one sentence)
2. Who is it for? (audience)
3. What should the name feel like? (technical / warm / playful / authoritative)
4. Part of an existing brand family, or standalone?
5. Any words, concepts, or styles off-limits?
6. Which platforms must the name work on? (domain, npm, GitHub, app stores, social)

If industry-specific (WordPress, fintech, gaming…), load `industries/INDEX.md`.
If open source, load `open-source.md` (CLI friendliness, registry conflicts, GitHub org, adoption).

### Step 2 — Metaphor exploration
Don't brainstorm names yet. Brainstorm **metaphors and conceptual territories**.
Load `metaphor-mapping.md` (6 metaphor-finding questions + territory maps) and
`case-studies.md`. Pick 2-3 territories. If the brief is clear (tone+audience+function
defined), pick territories autonomously; only ask the user when ambiguous. Carry
territory rationale into Step 7.

**Steps 3-6 are internal.** Do NOT show raw candidates, unfiltered lists, or
intermediate results. The user's next touchpoint is Step 7.

### Step 3 — Generate candidates (internal)
Produce 30-50+ candidates in the chosen territories. Include imperfect ones — they
reveal patterns. Methods: single words, compound words, modified words
(truncate/blend/suffix), foreign words, sound-first (say syllables aloud).
Load as needed: `principles.md` (foundational gates: metaphor, story, phone test —
every candidate must pass), `phonosemantics.md` (sound-matching),
`cultural-references.md`, `brand-architecture.md`, `language-rules.md`,
`languages/INDEX.md` (non-English audience).

### Step 4 — Filter (internal)
Cut to ~10 semifinalists. Load `anti-patterns.md` (patterns that kill names) and
`evaluation.md` (scoring rubric).

### Step 5 — Availability gate (internal, MANDATORY, blocking)
Run REAL checks with tools — never guess from memory. Load `availability.md`.
Map the brief's platform list (Q6) to actual checks before starting.

1. **Competitor search FIRST** (WebSearch): `"[name]" [category]`, `"[name]" software/app`.
   Direct competitor in same space = name is dead; drop before any other check.
2. **Dictionary-word shortcut**: common single English words have exact TLDs taken —
   skip them, go straight to prefix (`get[name].com`, `use[name].com`), suffix
   (`[name]dev.com`), and alt TLDs (`.site`, `.sh`). Only run exact TLD checks for
   invented/uncommon/compound names.
3. **Batch script** (bundled in repo): `bash scripts/check-availability.sh [name] domain npm github pypi telegram`.
   Covers domain (whois .com/.dev/.io), npm, PyPI, GitHub org, crates.io, RubyGems,
   WP plugin slug, Telegram. Pass only brief-relevant platforms. Run names in parallel.
4. **Manual fallbacks** (Bash):
   - domain: `whois [name].com 2>&1 | grep -iE "no match|not found|no data found|available"` (match = available)
   - npm: `npm view [name] 2>&1` ("not found" = available)
   - PyPI: `curl -s -o /dev/null -w "%{http_code}" https://pypi.org/project/[name]/` (404 = available)
   - GitHub org: `curl -s -o /dev/null -w "%{http_code}" https://github.com/[name]` (404 = available)
   - crates.io: `curl ... https://crates.io/api/v1/crates/[name]` (404 = available)
   - RubyGems: `curl ... https://rubygems.org/api/v1/gems/[name].json` (404 = available)
   - WP slug: `curl -s "https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&slug=[name]"` ("Plugin not found" = available)
   - Telegram: `curl ... https://t.me/[name]` (404 = available)
   - App stores / social: WebSearch `"[name]" site:apps.apple.com`, `site:x.com/[name]`, etc.
5. **Decision gate**: drop on direct competitor / trademark / multiple must-have
   platforms taken. Flag-but-keep when name is strong enough to justify a workaround
   (e.g. `.com` taken but `get[name].com` free). If <3 survive, loop to Step 3 — do
   NOT lower the bar.

### Step 6 — Evaluate & compare (internal)
Score survivors against weighted criteria; run contextual sentence tests; compare
side-by-side. Load `evaluation.md`.

### Step 7 — Present & decide (first user-facing output)
Present top 3-5 with: the name, 15-second origin story, why it works (which
principles), availability status (confirmed / needs workaround), risks/trade-offs,
and tagline suggestions (`taglines.md`). Recommend sitting with finalists 24h.

## Loop back when
- All fail anti-patterns (Step 4) → Step 2 (new territories).
- <3 survive availability (Step 5) → Step 3 (more candidates).
- Nothing scores >70 (Step 6) → Step 2 (weak metaphor foundation).
- User rejects all finalists (Step 7) → Step 1 (revisit brief).
Looping back beats lowering the bar.

## Key rules
1. Never generate names before the brief.
2. Never use a thesaurus — use metaphor exploration.
3. Steps 3-6 are autonomous and hidden; user sees only vetted Step 7 finalists.
4. Flag AI slop immediately.
5. Never present a name without a tool-verified availability check.
6. Never present a name without an origin story.
7. Quality over quantity: 3-5 strong finalists, not 20 mediocre.
8. Respect the user's taste — if they reject a direction, explore another.
