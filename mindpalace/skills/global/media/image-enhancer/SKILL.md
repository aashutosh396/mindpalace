---
name: image-enhancer
description: "Use when the user wants to enhance, upscale, sharpen, or clean up an image or screenshot — keywords: enhance image, improve image quality, upscale, sharpen blurry screenshot, reduce compression artifacts, 4K, retina, prep image for blog/docs/social/presentation/print."
version: 1.0.0
license: MIT
tags: [image, screenshot, enhance, upscale, sharpen, denoise, resolution, media]
source: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/image-enhancer
derived_from: awesomeclaude
---

# Image Enhancer

Improves image and screenshot quality — sharper, clearer, higher resolution — for
blog posts, documentation, social media, presentations, and print.

## When to use
- Improve / enhance screenshot quality for blog posts or docs.
- Upscale a low-res image (e.g. to retina / 2x / 4K).
- Sharpen a blurry photo or screenshot.
- Reduce JPEG compression artifacts or noise.
- Batch-process every image in a folder.
- Optimize an image for a specific target (web, print, Twitter/LinkedIn/Instagram).

Trigger phrases: "improve the image quality of X", "enhance this screenshot",
"upscale to 4K", "sharpen this", "reduce compression artifacts", "make this image
crystal clear".

## What it does
1. Analyze: report current resolution, format, and quality issues (blur, artifacts).
2. Upscale resolution intelligently.
3. Sharpen edges / improve text clarity.
4. Reduce compression artifacts and noise.
5. Optimize for the intended use case and output format.

## How (steps)
1. Read the source image to inspect specs (dimensions, format).
2. **Always preserve the original** — copy it to `<name>-original.<ext>` before editing.
3. Apply enhancement with whatever local image tooling is available:
   - **ImageMagick** (`magick` / `convert`) for upscale + sharpen + denoise:
     `magick in.png -resize 200% -unsharp 0x1.0 -strip out.png`
   - **ffmpeg** for resize/scale filters when ImageMagick is absent.
   - For text-heavy screenshots, prefer Lanczos resampling: `-filter Lanczos`.
   - Convert to WebP/JPG only when smaller size matters; keep PNG for sharp UI/text.
4. Save as `<name>-enhanced.<ext>` (do not overwrite the source).
5. Report before/after specs and the enhancements applied.

For batch jobs, loop the same pipeline over each matching file in the folder and
keep per-file `-original` backups.

## Output format (mirror the source skill)
```
Analyzing <file>...
Current specs: resolution, format, quality notes
Enhancements applied:
  ✓ Upscaled to <new res>
  ✓ Sharpened edges
  ✓ Enhanced text clarity
  ✓ Optimized file size
Saved as: <file>-enhanced.<ext>
Original preserved as: <file>-original.<ext>
```

## Gotchas
- Never overwrite or delete the original — always back it up first.
- Upscaling cannot invent detail; set expectations on very small/heavily-blurred inputs.
- PNG preserves text/UI fidelity; JPG/WebP trade quality for size — choose by use case.
- For social media, ask which platform to size correctly.
- Over-sharpening (high `-unsharp`) creates halos; keep amounts conservative.

## Output format depends on tooling
This skill is tool-agnostic: it leans on locally available image binaries
(ImageMagick / ffmpeg). If none are installed, install ImageMagick (`brew install
imagemagick`) or fall back to any available image-processing capability before
enhancing.
