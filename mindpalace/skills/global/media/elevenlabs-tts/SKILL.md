---
name: elevenlabs-tts
description: "Use when converting text or documents to audio with ElevenLabs — create a podcast, generate a podcast from a document, narrate a file, read aloud, text-to-speech, TTS, or make an audio version of a PDF/DOCX/Markdown."
version: 1.0.0
license: Apache-2.0
tags: [elevenlabs, tts, text-to-speech, podcast, audio, narration, voice, speech]
source: https://github.com/sanjay3290/ai-skills/tree/main/skills/elevenlabs
derived_from: awesomeclaude
prerequisites:
  commands: [python3, ffmpeg]
---

# ElevenLabs Text-to-Speech & Podcast

Converts text and documents into audio via the ElevenLabs TTS API. Two modes:
single-voice narration, and two-host conversational podcast.

## When to use

- "create podcast", "generate podcast", "podcast from document"
- "narrate document", "narrate this file", "read aloud"
- "text to speech", "TTS", "convert to audio"
- "audio from document", "audio version of"

## Setup

Auth via `ELEVENLABS_API_KEY` env var, or a `config.json` next to the helper
scripts:

```json
{
  "api_key": "your-elevenlabs-api-key",
  "default_voice": "JBFqnCBsd6RMkjVDRZzb",
  "default_model": "eleven_multilingual_v2",
  "podcast_voice1": "JBFqnCBsd6RMkjVDRZzb",
  "podcast_voice2": "EXAVITQu4vr4xnSDxMaL"
}
```

Only `api_key` is required.

Deps: `pip install PyPDF2 python-docx` (only for PDF/DOCX input). `ffmpeg` is
required for multi-chunk narration and podcasts.

Helper scripts live in the source repo at `skills/elevenlabs/scripts/`
(`elevenlabs.py`, `extract.py`). Fetch them from the source URL rather than
recreating; they handle text extraction, sentence-boundary chunking (~4000
chars), per-chunk TTS with voice continuity, and ffmpeg concatenation.

## Commands

List voices (find voice IDs to offer the user):

```bash
python scripts/elevenlabs.py voices
python scripts/elevenlabs.py voices --json
```

Single-voice TTS:

```bash
# From text
python scripts/elevenlabs.py tts --text "Hello world" --output ~/Downloads/hello.mp3
# From a document
python scripts/elevenlabs.py tts --file /path/to/doc.pdf --output ~/Downloads/narration.mp3
# With a specific voice
python scripts/elevenlabs.py tts --file doc.md --voice VOICE_ID --output out.mp3
```

Podcast (needs a JSON script of conversation segments):

```bash
python scripts/elevenlabs.py podcast --script /tmp/script.json --voice1 ID1 --voice2 ID2 --output ~/Downloads/podcast.mp3
```

Script format:

```json
[
  {"speaker": "host1", "text": "Welcome to our podcast! Today..."},
  {"speaker": "host2", "text": "That's right! I found..."}
]
```

## Podcast workflow (from a document)

1. Extract document text: `python scripts/extract.py /path/to/document.pdf`
2. Write a natural two-host conversation script from the text:
   - Host 1 leads/introduces; Host 2 adds analysis and reactions.
   - Brief intro stating the topic; summary/outro at the end.
   - Keep each turn under 3000 chars; vary turn lengths.
   - Conversational language; reference specific source details; do NOT read
     the document verbatim — discuss and interpret it.
3. Save the script as a JSON array to a temp file (e.g. `/tmp/podcast_script.json`).
4. Run the `podcast` command above.
5. Clean up the temp script file.

## Gotchas

- Run `voices` first so the user can pick voices they like; for podcasts suggest
  contrasting voice pairs (e.g. one deep, one bright).
- Default output to `~/Downloads/` unless the user specifies otherwise.
- For large documents, warn the user about character usage against their
  ElevenLabs plan quota.
