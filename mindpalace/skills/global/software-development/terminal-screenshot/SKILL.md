---
name: Terminal Screenshot (ANSI → PNG)
description: Use when you must visually verify a CLI tool's colored terminal output (delta diffs, bat highlighting, starship, eza/ls colors) — captures full-fidelity ANSI to a file then renders it to PNG so colors/contrast/alignment can actually be seen.
tags: [terminal, ansi, screenshot, png, delta, bat, color-verification, freeze, cli-colors, render]
source: daymade/claude-code-skills
derived_from: terminal-screenshot
---

# Terminal Screenshot

Render a terminal command's colored output to a PNG, then read the image to judge it. Tool results show raw escape codes (`\x1b[48;2;...m`), not rendered colors — reading hex is guessing. ALWAYS use right after changing any CLI color config.

## Method: capture, then render (keep separate — that's the trick)

### Step 1 — Capture full-fidelity ANSI to a file
CLIs drop/downgrade color when not writing to a real terminal. Force coloring, save to `.ansi`. **NEVER let the renderer run the command** (`freeze --execute "git diff | delta"` runs delta in a degraded child pty → drops background blocks/line numbers/header box). Capture in a normal shell first. Pick `--width ≈100-120` to match wrapping.

| Tool | Capture command |
|---|---|
| delta | `git --no-pager diff \| delta --dark --line-numbers --width=110 > /tmp/x.ansi` |
| git diff | `git -c color.ui=always --no-pager diff > /tmp/x.ansi` |
| bat | `bat --color=always --style=numbers <file> > /tmp/x.ansi` |
| eza | `eza -la --color=always --icons > /tmp/x.ansi` |
| ls (GNU) | `ls -la --color=always > /tmp/x.ansi` |
| ls (BSD) | `CLICOLOR_FORCE=1 ls -laG > /tmp/x.ansi` |
| ripgrep | `rg --color=always 'pat' <path> > /tmp/x.ansi` |
| anything else | `CLICOLOR_FORCE=1 <cmd> > /tmp/x.ansi` or `<cmd> --color=always` or `script -q /dev/null <cmd>` |

### Step 2 — Render to PNG and read it
```bash
scripts/render_ansi.sh <input.ansi> <output.png> [background_hex]
```
Then Read the PNG. **Background must match the real terminal** (a dark theme on a white page misjudges contrast). macOS Ghostty: `ghostty +show-config --default | grep '^background'` → pass `#282c34`. Unknown dark terminal ≈ `#1d1f21`–`#282c34`.

## Renderer install (freeze, preferred)
**Do NOT `brew install freeze`** (wrong GUI cask). Use `brew install charmbracelet/tap/freeze` or `GOPROXY=https://goproxy.cn,direct GOSUMDB=off go install github.com/charmbracelet/freeze@latest`. If unavailable, `render_ansi.sh` falls back to bundled `scripts/ansi2html.py` (stdlib) + headless Chrome.

## Out of scope
Full-screen TUIs (lazygit/htop/top) paint via cursor positioning, not linear ANSI — can't capture this way. For a TUI's colors, render the underlying piece in isolation (lazygit diff = `git diff | delta`).

## Pitfalls
Renderer running the command → degraded output. Non-TTY strips color → force it. Wrong background → contrast misjudged. Light/dark mismatch (a `light=true` config on a dark terminal shows inverted colors — that's the bug, not the renderer).
