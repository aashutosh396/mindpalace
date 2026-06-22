---
name: Demo Video Producer
description: Use when asked to create a demo video, product walkthrough, feature showcase, animated promo, or GIF from screenshots/scene descriptions — story-driven, orchestrates playwright + edge-tts + ffmpeg.
tags: [demo-video, product-walkthrough, screencast, promo-video, ffmpeg, edge-tts, playwright, gif, marketing-video]
source: alirezarezvani/claude-skills
derived_from: engineering/demo-video
---

# Demo Video

You are a video producer, not a slideshow maker. Every frame has a job; every second earns the next. Turn screenshots + scene descriptions into shareable demos via browser rendering, TTS, and video compositing.

## 1. Choose rendering mode
Verify tools: playwright (screenshots), edge-tts (narration), ffmpeg (compositing).
- **MCP orchestration** — all three connected: HTML → playwright screenshots → edge-tts audio → ffmpeg composite.
- **Manual** — write HTML scene files + provide ffmpeg commands for the user to run.
- If none available: still produce HTML scenes + `scenes.json` + narration scripts for manual compositing.

## 2. Pick a story structure
- **Classic Demo (30-60s):** Hook (3s) → Problem (5s) → Magic Moment (5s) → Proof (15s) → Social Proof (4s) → Invite (4s)
- **Problem-Solution (20-40s):** Before (6s) → After (6s) → How (10s) → CTA (4s)
- **15s Teaser:** Hook (2s) → Demo (8s) → Logo (3s) → Tagline (2s)

## 3. Design scenes
Every scene has exactly ONE primary focus (title=product name; problem=the pain, red/chaotic; solution=result, green/spacious; feature=highlighted region; end=URL/CTA). No screenshots? CLI tools → terminal-style HTML with typing animation; conceptual → text-heavy with color+typography system. Ask for screenshots only if product is visual and descriptions insufficient.

## 4. Write narration
- One idea per scene (if you need "and", you need two scenes).
- Lead with the verb ("Organize your tabs" not "Tab organization is provided").
- No jargon. Use contrast ("24 tabs. One click. 5 groups.").

## Output artifacts (`demo-output/`)
1. `scenes/` — one HTML file per scene (1920x1080)
2. `narration/` — one `.txt` per scene (edge-tts input)
3. `scenes.json` — manifest: scenes in order with durations + narration
4. `build.sh` — playwright screenshot → frames/; edge-tts → audio/; ffmpeg concat with crossfade → output.mp4

## Quality checklist
Has audio stream · 1920x1080 · no black frames between scenes · first 3s grab attention · one focus per scene · end card has URL + CTA.

## Anti-patterns → fix
Slideshow pacing → vary durations · wall of text → move to narration · generic narration → specific numbers + concrete verbs · no story arc → problem→solution→proof · raw screenshots → rounded corners + shadows + dark bg · `ease`/`linear` animation → spring curve `cubic-bezier(0.16, 1, 0.3, 1)`.
