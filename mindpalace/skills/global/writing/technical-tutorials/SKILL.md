---
name: technical-tutorials
description: Use when writing step-by-step technical tutorials, quickstarts, getting-started guides, code walkthroughs, hands-on guides, or "how to" guides for developers.
version: 1.0.0
license: MIT
tags: [tutorials, quickstart, technical-writing, devrel, code-examples, onboarding, documentation]
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/technical-tutorials
derived_from: awesomeclaude
---

# Technical Tutorials

Create step-by-step tutorials that actually work: explicit prerequisites, progressive complexity, copy-paste code, troubleshooting, and satisfying "it works!" moments. Know audience skill level, stack familiarity, OS/environment, and motivation first.

## Tutorial types

| Type | Length | Purpose |
|---|---|---|
| Quickstart | 5-10 min | First success ASAP |
| Tutorial | 20-45 min | Learn a concept deeply |
| Workshop | 1-3 hr | Comprehensive project |
| Code walkthrough | varies | Explain existing code |

## Structure

Title & meta (what you build, time, prerequisites) → overview (what you learn, final result preview) → prerequisites check (with verification commands) → the build in progressive steps with checkpoints → what you built (recap + complete code) → troubleshooting → next steps.

## Prerequisites

Be explicit — don't make devs guess. Table of requirement / version / check command (e.g. Node 18+ / `node --version`). List assumed knowledge with links to learn it. Make environment setup foolproof: mkdir/cd, init, install, then a verification command with expected output.

## Progressive complexity (layer cake)

Build in layers: 1) skeleton that runs (Hello World), 2) core feature (one endpoint), 3) real data (database), 4) error handling, 5) polish (logging/config/tests). Show progress not perfection — never dump a 200-line final file at step 1. Add one concept per step, referencing the existing file.

## Copy-paste-friendly code

Every block must: run standalone, include all imports, reference no undefined variables from unshown steps, work cross-platform, and comment the *why*. Give file context (`// server.js — add this`), show file-tree structure, and highlight changes inline (`// ✅ ADD THIS`).

## "It works!" moments

Every 3-5 steps give a checkpoint win: a command to run, the expected output, and a clear success marker ("🎉 It works!"), with a link to troubleshooting if not. Show visual confirmation — terminal output, formatted JSON response, browser result, or logs.

## Troubleshooting sections

For each common error: the exact error text, the cause, the fix (with commands). Cover the predictable ones (missing module → `npm install`; EADDRINUSE → kill process or change port; syntax errors → check line/brackets/quotes). Add proactive warnings before pitfalls (e.g. Windows `set`/`$env:` vs `export`).

## Quality checklist

Code: every block runs unmodified, imports included, output shown, error handling present, `.env` for secrets. Structure: explicit prerequisites, tested time estimate, checkpoints every 3-5 steps, full final code, troubleshooting covers likely errors. Accessibility: works Mac/Linux/Windows, bash/zsh/PowerShell, correct path separators, no assumed installed tools.

## Tools

Replit/CodeSandbox (runnable embeds); Carbon/Ray.so (code screenshots); Excalidraw (architecture diagrams); Terminalizer (record terminal); Loom (video supplements); listening tools to find common errors/questions to address.
