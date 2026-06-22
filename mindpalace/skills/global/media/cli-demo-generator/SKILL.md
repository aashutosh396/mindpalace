---
name: CLI Demo Generator (VHS GIFs)
description: Use when creating animated terminal demos / GIFs of CLI workflows for README or docs — generates VHS tape files, self-bootstrapping recordings, output filtering, and speed post-processing.
tags: [vhs, terminal-demo, gif, asciinema, cli-recording, readme, demo-tape, gifsicle]
source: daymade/claude-code-skills
derived_from: cli-demo-generator
---

# CLI Demo Generator

Create professional animated CLI demos with VHS. Four approaches, automated to manual.

## Quick start
```bash
python3 scripts/auto_generate_demo.py -c "npm install pkg" -c "npm run build" -o demo.gif
# self-cleaning repeatable demo:
python3 scripts/auto_generate_demo.py -c "..." -o demo.gif --bootstrap "npm uninstall pkg 2>/dev/null" --speed 2
```

## CRITICAL — VHS parser limits
VHS `Type` strings cannot contain `$`, `\"`, or backticks (parse errors). **Workaround: base64-encode the command**, decode at runtime:
```bash
echo 'claude() { command claude "$@" 2>&1 | grep -v "noise"; }' | base64
# in tape:
Type "echo <b64> | base64 -d > /tmp/w.sh && source /tmp/w.sh"
```
Essential for output filtering, function defs, any shell special char.

## Approaches
1. **Automated** — `auto_generate_demo.py` with `-c` (repeatable), `-o`, `--title`, `--theme`, `--font-size`, `--width/--height`, `--bootstrap`, `--filter`, `--speed`, `--no-execute`. Smart timing: install/build/test→3s, ls/echo→1s, else 2s.
2. **Batch** — `batch_generate.py demos.yaml --output-dir ./gifs` from a YAML list.
3. **Interactive** — `record_interactive.sh out.gif` (needs asciinema).
4. **Manual tape** — templates: basic / interactive / self-bootstrap.

## Key patterns
- **Self-bootstrapping**: `Hide` → cleanup cmds → `clear` → `Sleep 500ms` → `Show`. The `clear` wipes buffer so hidden setup never leaks into the GIF.
- **Frame verification**: `ffmpeg -i demo.gif -vf "select=eq(n\,100)" -frames:v 1 /tmp/f.png`, then Read the PNG.
- **Speed-up without re-record**: `gifsicle -d2 in.gif "#0-" > fast.gif` (2x), `-d4` (1.5x).
- **Template placeholders**: keep tape generic, `sed` in real values at build time.

## Sizing
README: 1400×600, font 16-20. Presentation: 1800×900, font 24. Compact: 1200×600.

## Troubleshooting
VHS missing → `brew install charmbracelet/tap/vhs`. GIF too big → smaller dims/sleeps or `--speed 2`. Text wraps → wider `--width`. Parse error on `$`/`"` → base64. Hidden cmds leak → add `clear`+`Sleep` before `Show`.
