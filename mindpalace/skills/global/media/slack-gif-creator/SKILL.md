---
name: Slack GIF Creator
description: Use when the user wants an animated GIF optimized for Slack ("make a GIF of X for Slack", custom Slack emoji) — Slack size/dimension constraints, PIL drawing, easing, and GIF optimization.
tags: [gif, slack, animation, slack-emoji, pillow, pil, easing, gif-optimization, animated-gif]
source: anthropics/skills
derived_from: skills/slack-gif-creator
---

# Slack GIF Creator

Create animated GIFs optimized for Slack using PIL primitives + a GIF builder.

## Slack requirements
- **Dimensions:** emoji GIFs 128x128; message GIFs 480x480.
- **FPS:** 10-30 (lower = smaller file).
- **Colors:** 48-128 (fewer = smaller).
- **Duration:** keep emoji GIFs under 3 seconds.

## Core workflow
```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

builder = GIFBuilder(width=128, height=128, fps=10)
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)
    # draw animation with PIL primitives
    builder.add_frame(frame)
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## Drawing
User-uploaded image → decide: use directly ("animate this") or as inspiration ("make something like this"); load with `Image.open`. From scratch → PIL ImageDraw: `ellipse`, `polygon`, `line`, `rectangle`. **Don't** use emoji fonts (unreliable cross-platform) or assume pre-packaged graphics exist.

**Make it look polished:** thick lines (`width>=2`, never 1); visual depth (gradient backgrounds, layered shapes); interesting shapes (highlights, rings, glows, combined shapes); vibrant complementary colors with contrasting outlines; complex shapes (hearts/snowflakes) from polygon+ellipse combos with careful symmetry + details.

## Utilities
- **GIFBuilder** (`core.gif_builder`) — `add_frame`/`add_frames`, `save(num_colors, optimize_for_emoji, remove_duplicates)`.
- **Validators** (`core.validators`) — `validate_gif(path, is_emoji, verbose)`, `is_slack_ready(path)`.
- **Easing** (`core.easing`) — `interpolate(start, end, t, easing=...)`: linear, ease_in/out/in_out, bounce_out, elastic_out, back_out. Smooth motion beats linear.
- **Frame helpers** (`core.frame_composer`) — create_blank_frame, create_gradient_background, draw_circle, draw_text, draw_star.

## Animation concepts
Shake (sin/cos offset + small random) · Pulse/heartbeat (`sin(t*freq*2π)`, scale 0.8-1.2; two quick pulses then pause) · Bounce (`bounce_out` landing, `ease_in` falling, gravity adds to vy) · Spin (`image.rotate(angle, resample=BICUBIC)`; sin wave for wobble) · Fade (RGBA alpha 0↔1 or `Image.blend`) · Slide (off-screen→target, `ease_out`; `back_out` for overshoot) · Zoom (scale + crop center) · Explode (particles random angle/velocity, vy += gravity, fade out). Combine concepts.

## Optimization (only when asked to shrink file)
Fewer frames (lower FPS / shorter) · fewer colors (48) · smaller dimensions (128 vs 480) · `remove_duplicates=True` · `optimize_for_emoji=True`.

Dependencies: `pip install pillow imageio numpy`.
