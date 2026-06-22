---
name: Full Page Screenshot
description: Use when capturing a full-page / long / complete screenshot of a web page — handles SPA scroll containers, lazy-loaded images, and very tall pages via Chrome DevTools Protocol with no external dependencies.
tags: [screenshot, full-page, cdp, chrome-devtools, lazy-load, spa, scroll-container, tiled-capture, browser-automation]
source: alirezarezvani/claude-skills
derived_from: engineering/skills/full-page-screenshot
---

# Full Page Screenshot

Capture a full-page screenshot of any web page via Chrome DevTools Protocol — a single PNG including all content that requires scrolling. Needs Node.js 22+ (built-in WebSocket) and Chrome/Chromium with remote debugging enabled.

## Setup
Check readiness with the script's `--check`. If Chrome fails, open `chrome://inspect/#remote-debugging` and enable "Allow remote debugging for this browser instance".

## Workflow
**Option A — already-open tab (recommended for authenticated pages):** `--list` tabs, identify target by title/URL, then capture by `<targetId>` to an output path.
**Option B — a URL** (opens a background tab, captures, closes): pass `--url`. Background tabs can't see SSO/login walls — use Option A for those.

## Parameters
`output` (PNG path, default `/tmp/screenshot.png`) · `--width` (CSS px; articles 1200, dashboards 1440-1920) · `--dpr` (1 default; 2 = Retina but 4x file size) · `--wait` (load timeout ms, `--url` only, default 15000) · `--css` (inject CSS before capture, e.g. hide elements). Verify output: `sips -g pixelWidth -g pixelHeight` (macOS) or `file` (Linux).

## How it captures everything
1. Discover Chrome debugging port (DevToolsActivePort file, fallback probe 9222/9229/9333).
2. Connect via WebSocket (CDP), attach to target or create a background tab.
3. Set viewport width; wait for `readyState=complete` + DOM-count stability (SPA frameworks finish rendering).
4. Detect `overflow-y: auto/scroll` containers, scroll through to trigger lazy-loading, then remove overflow constraints (incl. Tailwind `h-[calc(...)]`) so all content renders in one pass.
5. Scroll viewport incrementally to fire IntersectionObserver, wait for all `<img>` to complete.
6. Measure final height; `Page.captureScreenshot`. Pages >16,000px captured in 8,000px tiles, stitched with Python PIL (falls back to separate tiles if PIL absent).
7. Restore viewport, detach, clean up. CDP-proxy fallback uses proxy `/eval`, `/screenshot`, `/scroll` endpoints when a proxy holds the WebSocket.

## Anti-patterns
`--dpr 2` on pages >10,000px (Chrome memory — use 1) · `--url` for authenticated pages (use `--list` + targetId) · `--wait` <5000 for SPAs (use 10000-15000) · capturing without `--check` first · one hardcoded width for all pages · skipping output verification.
