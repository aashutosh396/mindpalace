---
name: Capture (Brain-Dump Organizer)
description: Use when the user dumps a messy stream of mixed thoughts/tasks/ideas ("brain dump", "capture this", or any long unstructured block) — turns it into a clean actionable system with zero information loss.
tags: [brain-dump, capture, note-taking, gtd, organize-thoughts, idea-dump, task-extraction, zero-loss]
source: alirezarezvani/claude-skills
derived_from: productivity/capture
---

# Capture — Brain-Dump Organizer

Transform unstructured streams of mixed thoughts/tasks/ideas into a clean actionable system. Fast-to-action: no upfront intake — the dump IS the request (don't ask "want me to organize this?" first).

## Operating principles (all five, always)
1. **Capture everything.** Zero loss; user prunes later. Never silently drop "trivial" items.
2. **Preserve voice.** Keep casual register and energy. "build something crazy with AI" stays — don't corporate-ify to "Explore innovative AI-driven solutions."
3. **Match output complexity to input.** A 5-task dump doesn't get forced into 4 elaborate sections.
4. **Be honest about ambiguity.** Flag what's unclear; don't guess silently.
5. **No action without approval.** The only auto-action is the organization itself.

## One mid-organization clarifier (max)
Ask ONE question only when an item is genuinely ambiguous between task and project AND misclassification would change the output. Otherwise skip. Never ask 3 questions up front (breaks the flow).

## Four sections
1. **Projects & Ideas** — cluster related items into themed projects (user's words for names); hold standalone sparks, half-formed concepts, embedded `Q:` and `Decide:` WITHIN the relevant project (not a separate top-level category).
2. **Tasks** — flat, scannable, imperative voice; `Decide:` / `Resolve:` framings; append `[Project: X]` to link without repeating context.
3. **Connections** — where the skill earns its keep. **Fabrication forbidden.** Glob/Grep/Read the workspace, match dump items to existing files/folders/prior thinking, surface within-dump dependencies. If none found: "No connections found — workspace inventory clean." If inaccessible: say so explicitly, ask where the work lives — never invent.
4. **How I Can Help** — concrete offers (what would be produced AND where it goes), not abstract possibilities. End with the directive question: **"Which of these should I tackle?"**

## Compressed output pattern
When ≤5 items and unrelated (no clustering): drop 4-section format → "## What I heard" (bullets) + "## How I can help" (concrete offers) + "Which should I tackle?"

## Approval gate
Wait for the user's explicit pick before doing anything. If user says "go" without picking: honor it but flag items you weren't 100% sure about.

## Anti-patterns
Fabricating unverified connections · dropping "trivial" items · corporate-ifying casual language · forcing 4 sections on small input · acting on offers without approval · splitting decisions/questions into a separate top-level category · vague offers ("you might want to consider…") · 3+ upfront clarifiers.
