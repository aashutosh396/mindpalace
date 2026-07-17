---
name: send-file-discord
description: "Use when the owner ASKS for a file, report, export, data, chart, image, screenshot, or log — you CAN send real files to Discord with an ATTACH line. Never say you can't send files. But do NOT attach files the owner didn't ask for."
version: 1.1.0
tags: [file, send, attach, export, csv, pdf, image, png, screenshot, chart, log, download, share]
---

# Send files to Discord

You can send ANY file to the owner in Discord. The gateway does the upload for you.

## How

1. Save the file anywhere on disk (use /tmp for one-offs), any type: .md, .txt, .csv, .pdf, .png, .log, .json, .zip.
2. In your reply, put this on its OWN line, with the absolute path:

```
📎ATTACH: /tmp/report.csv
```

3. The gateway strips that line and uploads the file with your message. Multiple ATTACH lines = multiple files. Works in live chat AND in background-task reports.

## When

ONLY when the owner asked for something that is a file:
- "send me the report / list / data" → .md, .txt, or CSV
- "export this" / lots of rows → CSV
- "show me a chart / graph" → PNG via matplotlib/PIL
- "send the logs" → .txt/.log

## Never

- Never say "I can't send files in Discord" — you can.
- Never attach your own notes, summaries, or write-ups nobody asked for. Default reply = short text, zero attachments. Save detail to the vault and offer it: "notes saved, want them?"
