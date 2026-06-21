---
name: llm-cli
description: "Use when piping text through an LLM from the shell — summarize files, generate commit messages from git diff, fix grammar, analyze code, run prompts in scripts, or generate shell commands from natural language via llm or aichat."
version: 1.0.0
license: MIT
tags: [ai, llm, cli, summarize, chat, pipe, shell, automation, aichat]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-ai
derived_from: awesomeclaude
prerequisites: ["llm or aichat installed; provider API key configured separately (user pays per token)"]
---

# LLM CLI (llm / aichat)

Run LLM prompts from the terminal — pipe text in, get processed text out. Great
inside scripts and pipelines. These use the user's own API keys, separate from
Claude Code.

## When to use
Summarizing/translating/analyzing piped text, generating commit messages from a
diff, batch text processing in scripts, or turning natural language into shell
commands.

## llm (Simon Willison)

```bash
llm "What is the capital of France?"
cat article.txt | llm "Summarize in 3 bullets"
git diff | llm "Write a commit message for these changes"
pbpaste | llm "Fix the grammar"
llm chat                          # Interactive
llm -m claude-3.5-sonnet "..."   # Specific model
llm models                        # List models
llm install llm-ollama            # Add local-model plugin
llm logs last                     # History
```

## aichat (Rust, fast)

```bash
aichat "Explain Docker simply"
cat code.py | aichat "Find bugs"
aichat -e "find all files larger than 100MB"   # Generate+run a shell command
aichat                            # Interactive REPL
```

## Guidelines
- Use `llm` for piping text through models; richest plugin ecosystem (100+ providers).
- Use `aichat -e` to generate shell commands from natural language.
- Both store API keys locally — set up once.
