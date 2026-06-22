---
name: LLM Icon Finder
description: Use when the user needs AI/LLM brand icon URLs or wants to download logos for AI models/providers/apps (Claude, GPT, Gemini, etc.) in SVG/PNG/WEBP — constructs lobe-icons CDN URLs and downloads them.
tags: [icons, logos, llm, ai-brands, lobe-icons, svg, png, webp, claude, openai, gemini]
source: daymade/claude-code-skills
derived_from: llm-icon-finder
---

# LLM Icon Finder

Access AI/LLM brand icons from the [lobe-icons](https://github.com/lobehub/lobe-icons) library (100+ icons for models, providers, applications).

## Formats & variants
Formats: SVG (scalable), PNG (raster), WEBP (compressed). Themes: light, dark, color (some icons).

## CDN URL patterns
```
https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-svg/{light|dark}/{icon-name}.svg
https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-png/{light|dark}/{icon-name}.png
https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-webp/{light|dark}/{icon-name}.webp
# color variant: append -color to icon-name
.../static-png/dark/{icon-name}-color.png
```
Naming: lowercase, hyphenated (`claude`, `chatglm`, `openai`, `huggingface`).

## Workflow
1. Identify icon name (lowercase company/model, hyphenated if multi-word).
2. Pick format (default PNG) + theme (default dark).
3. Construct CDN URL.
4. Provide URL; mention color variant + web viewer `https://lobehub.com/icons/{icon-name}`.
5. Download on request via `curl -o name.svg "<url>"`.

## Finding names
Browse https://lobehub.com/icons; try variations (`alibaba` vs `alibabacloud`); check `-color` variants if standard URL fails. Chinese queries supported (智谱 → `chatglm`, 月之暗面 → `moonshot`).

## Troubleshooting 404
1. Try `-color` suffix.
2. Alternate naming (`chatgpt` vs `gpt`, `google` vs `gemini`).
3. Browse https://lobehub.com/icons or search the repo.
