---
name: Video Comparer
description: Use when comparing two videos for compression results or quality differences (before/after, codec/bitrate impact) — generates an interactive HTML report with PSNR/SSIM metrics and frame-by-frame visual comparison.
tags: [video, compression, quality, psnr, ssim, ffmpeg, comparison, codec, bitrate]
source: daymade/claude-code-skills
derived_from: video-comparer
---

# Video Comparer

Compare two videos and generate a self-contained interactive HTML report: metadata, quality metrics (PSNR, SSIM), and frame-by-frame visual comparison (slider / side-by-side / grid modes).

## Usage
```bash
python3 scripts/compare.py original.mp4 compressed.mp4              # → comparison.html
python3 scripts/compare.py original.mp4 compressed.mp4 -o report.html
python3 scripts/compare.py original.mp4 compressed.mp4 --interval 10   # fewer frames, faster
```
Batch:
```bash
for original in originals/*.mp4; do
  compressed="compressed/$(basename "$original")"
  python3 scripts/compare.py "$original" "$compressed" -o "reports/$(basename "$original" .mp4).html"
done
```

## Requirements
- **FFmpeg + FFprobe** (`brew install ffmpeg` / `apt install ffmpeg`).
- Python 3.8+.
- Formats: `.mp4` (recommended), `.mov`, `.avi`, `.mkv`, `.webm`. Default 500MB/video limit (configurable). ~1-2 min typical.

## What it does
- Validates FFmpeg availability, file existence/extension/size, path security (no traversal).
- **PSNR** (pixel similarity, 20-50 dB, higher better); **SSIM** (perceptual, 0.0-1.0, higher better).
- Extracts frames at intervals (default 5s), scales to 800px height, embeds as base64 in offline HTML; temp files auto-cleaned.
- Report: slider (default), side-by-side, grid, zoom 50%-200%, works offline.

## Common errors
- "FFmpeg not found" → install via package manager.
- "File too large" → compress first or raise `MAX_FILE_SIZE_MB`.
- "Operation timed out" → raise `FFMPEG_TIMEOUT` or use larger `--interval`.
- "Frame count mismatch" → different durations/fps; auto-truncates to min frame count with warning.

Adjustable constants (file-size limit, timeouts, frame dims, interval) live at the top of `scripts/compare.py`.
