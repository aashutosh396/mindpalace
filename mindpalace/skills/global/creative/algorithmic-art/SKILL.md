---
name: Algorithmic Art (p5.js)
description: Use when the user asks to create generative/algorithmic art, flow fields, particle systems, or art-from-code — write an algorithmic philosophy, then a seeded interactive p5.js sketch (original work, not copying artists).
tags: [generative-art, algorithmic-art, p5js, creative-coding, flow-field, particle-system, seeded-randomness, perlin-noise]
source: anthropics/skills
derived_from: skills/algorithmic-art
---

# Algorithmic Art

Create algorithmic art in two steps: (1) an algorithmic philosophy (.md), then (2) express it as seeded, interactive p5.js (.html + inline .js). Make ORIGINAL work — never copy existing artists (copyright).

## Step 1 — Algorithmic philosophy
Create a computational aesthetic *movement*, not static images. Interpreted through: computational processes, emergent behavior, mathematical beauty, seeded randomness, noise fields, particles/flows/fields/forces, parametric variation, controlled chaos.

- **Name the movement** (1-2 words): e.g. "Organic Turbulence", "Quantum Harmonics", "Field Dynamics".
- **Articulate** in 4-6 substantial paragraphs: how it manifests through computational processes, noise/randomness, particle behaviors, temporal evolution, parametric/emergent complexity.
- **Avoid redundancy** — each algorithmic aspect mentioned once.
- **Emphasize craftsmanship repeatedly** — the algorithm must feel meticulously crafted, refined through countless iterations, the product of deep expertise ("master-level implementation", "painstaking optimization").
- **Leave creative space** — specific direction but room for high-craftsmanship interpretive choices.

Principles: process over product (each run unique), parametric expression, pure generative art (living algorithms not static images with randomness).

## Step 2 — Deduce the conceptual seed
Identify the subtle, niche reference from the original request and weave it invisibly into parameters/behaviors/emergence. Someone who knows the subject feels it; everyone else sees a masterful composition. Refined, never announcing itself.

## Step 3 — p5.js implementation
**STEP 0: Read `templates/viewer.html` first** and use it as the literal starting point. Keep FIXED: layout (header/sidebar/canvas), Anthropic branding (Poppins/Lora fonts, light colors, gradient backdrop), seed controls (display, prev/next/random, jump+go), action buttons (regenerate/reset/download PNG). Replace VARIABLE: the p5.js algorithm, the parameters object, the parameter UI controls, optional color pickers.

**Seeded randomness (Art Blocks pattern):**
```javascript
let seed = 12345;
randomSeed(seed); noiseSeed(seed);  // same seed → identical output
```
**Parameters** emerge from the philosophy — quantities, scales, probabilities, ratios, angles, thresholds (think in tunable properties, not "pattern types"). **Algorithm flows from the philosophy** (organic emergence → accumulation/feedback; mathematical beauty → ratios/trig/harmonics; controlled chaos → bounded variation/bifurcation). Canvas 1200x1200; static (`noLoop`) or animated.

**Craftsmanship:** balance (complexity without noise), color harmony (thoughtful palettes not random RGB), composition/visual hierarchy, performance (smooth if animated), reproducibility (same seed = identical).

## Output
1. Algorithmic philosophy (.md). 2. Single self-contained HTML artifact built from the template — p5.js via CDN, algorithm + controls + UI all inline, works immediately in claude.ai or any browser. Seed navigation always present. Don't copy the flow-field example — build what the philosophy demands.
