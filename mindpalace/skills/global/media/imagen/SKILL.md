---
name: imagen
description: "Use when the user wants to generate, create, or produce an AI image — hero images, UI mockups, icons, logos, illustrations, diagrams, concept art, avatars, placeholder images, or wallpapers — via Google Gemini's image model from a text prompt."
version: 1.0.0
license: Apache-2.0
tags: [image-generation, gemini, ai-image, text-to-image, icons, illustrations, diagrams, media]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen
derived_from: awesomeclaude
prerequisites:
  commands: [python3]
---

# Imagen — Gemini text-to-image generation

Generate images from a text prompt using Google Gemini's image model
(`gemini-3-pro-image-preview`) and save them as PNG files into the project.

## When to use

- User asks to "generate an image of…", "create a picture/icon/logo…", "make a hero image", etc.
- Frontend work needs a placeholder or real asset (avatar, banner, background).
- Docs need an illustration or diagram.
- Visualizing a concept, architecture, or idea as an image.

## How it works

1. Takes a text prompt describing the desired image.
2. POSTs to the Gemini `streamGenerateContent` endpoint with `responseModalities: ["IMAGE","TEXT"]`.
3. Decodes the returned base64 image and writes it to a PNG path (creates parent dirs).
4. Returns the saved file path for use in the project.

## Prerequisites

- `GEMINI_API_KEY` env var must be set. Get a free key at https://aistudio.google.com/.
  - macOS/Linux: `export GEMINI_API_KEY='your-key'`
- Python 3.6+ — standard library only, no pip installs.

## Usage

The skill ships a helper script. In the source repo it lives at
`skills/imagen/scripts/generate_image.py`
(raw: `https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/imagen/scripts/generate_image.py`).
Fetch it once into the skill's `scripts/` dir, then:

```bash
# Basic — saves to current dir
python3 scripts/generate_image.py "A futuristic city skyline at sunset"

# Custom output path
python3 scripts/generate_image.py "A minimalist app icon for a music player" "./assets/icons/music-icon.png"

# Custom size (512 | 1K | 2K; default 1K)
python3 scripts/generate_image.py --size 2K "High resolution landscape" "./wallpaper.png"
```

Optional env overrides used by the script:
- `IMAGE_SIZE` — `512`, `1K` (default), or `2K`.
- `GEMINI_MODEL` — model ID (default `gemini-3-pro-image-preview`).

## Request shape (if scripting directly)

POST `https://generativelanguage.googleapis.com/v1beta/models/<model>:streamGenerateContent?key=<KEY>`
with body:

```json
{
  "contents": [{ "role": "user", "parts": [{ "text": "<prompt>" }] }],
  "generationConfig": {
    "responseModalities": ["IMAGE", "TEXT"],
    "imageConfig": { "image_size": "1K" }
  }
}
```

## Gotchas

- Missing `GEMINI_API_KEY` → script exits with setup hint; set it before running.
- HTTP 429 = Gemini quota exhausted; wait or use a different key/quota.
- Output is always PNG. Pass an explicit path to avoid cluttering the cwd.
- Model is a preview ID (`gemini-3-pro-image-preview`) and may change; override via `GEMINI_MODEL` if Gemini renames it.
- For sensitive/branded assets, review generated output before committing — AI output can be off-prompt.
