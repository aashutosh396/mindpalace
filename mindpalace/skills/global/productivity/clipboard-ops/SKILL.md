---
name: clipboard-ops
description: "Use when copying to or pasting from the system clipboard, or transforming clipboard contents — pbcopy/pbpaste on macOS, xclip/xsel on Linux. Copy command output, save clipboard to file, uppercase/sort/word-count clipboard text."
version: 1.0.0
license: MIT
tags: [clipboard, copy, paste, pbcopy, pbpaste, xclip, transform, productivity]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-clipboard
derived_from: awesomeclaude
---

# Clipboard Operations

Read, write, and transform the system clipboard. Built in on macOS; Linux uses
xclip/xsel.

## When to use
"Copy this", "what's in my clipboard", "paste", or transforming clipboard text.

## macOS

```bash
pbpaste                              # Read clipboard
echo "hello" | pbcopy               # Copy text
pbcopy < /path/file.txt             # Copy file contents
pbpaste > /path/out.txt             # Save clipboard to file
ls -la | pbcopy                     # Copy command output
printf "%s" "exact text" | pbcopy   # No trailing newline

# Transform: paste -> process -> copy back
pbpaste | tr '[:lower:]' '[:upper:]' | pbcopy   # uppercase
pbpaste | sort | pbcopy                          # sort lines
pbpaste | wc -w                                  # word count
```

## Linux

```bash
xclip -selection clipboard          # copy (pipe into)
xclip -selection clipboard -o       # paste
```

## Guidelines
- Confirm what was copied with a brief summary.
- Never display clipboard contents unless asked — may contain sensitive data.
