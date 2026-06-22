---
name: macOS Programmatic Screenshot Capture
description: Use when automating screenshots on macOS, capturing specific application windows for documentation, or building multi-shot visual workflows — finds window IDs via Swift, controls windows via AppleScript, captures via screencapture.
tags: [macos, screenshot, screencapture, applescript, swift, window-id, excel, automation, capture]
source: daymade/claude-code-skills
derived_from: capture-screen
---

Programmatic screenshot capture on macOS: find window → control view → capture image.

## Three-step workflow
```
1. Find Window  →  Swift CGWindowListCopyWindowInfo  →  numeric Window ID
2. Control View →  AppleScript (osascript)           →  zoom, scroll, select
3. Capture      →  screencapture -l <WID>            →  PNG/JPEG
```

## Step 1 — Window ID (Swift, the only reliable method)
```bash
swift scripts/get_window_id.swift Excel    # or Chrome, or omit to list all
# Output: WID=12345 | App=Microsoft Excel | Title=workbook.xlsx
```
Re-fetch the WID right before capturing — CGWindowID is invalidated when an app restarts or a window is closed/reopened.

## Step 2 — Control window (AppleScript)
Excel has the richest dictionary (activate, `set zoom of active window to 120`, `set scroll row of active window to 45`, `select range "A1"`, `activate object sheet "DCF" of active workbook`, `open POSIX file "..."`). Any app: `osascript -e 'tell application "X" to activate'` or `AXRaise` via System Events.
Always `sleep 1` after AppleScript before capturing. **Wrap osascript in `timeout`** — it hangs forever if the app isn't running: `timeout 5 osascript -e '...'`.

## Step 3 — Capture
```bash
screencapture -x -l <WID> output.png      # -x silent
screencapture -l <WID> -t jpg output.jpg
screencapture -l <WID> -T 2 output.png    # delay
```
Retina outputs 2x by default; downscale with `sips --resampleWidth 2032 output.png --out output_1x.png`. Verify: `file output.png` shows "PNG image data".

## Failed approaches (do NOT use)
- `System Events` → `id of window` → error -1728 (wrong ID format).
- Python `import Quartz` (PyObjC) → not installed in system Python; use Swift.
- `osascript` window id → returns AppleScript index, not CGWindowID.

## Permissions
`get_window_id.swift` needs Screen Recording permission. If it errors `Failed to enumerate windows`:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```
Grant the real app bundle (not `swift`/Terminal helper); restart the app. The OS only shows permissions for a concrete `.app` bundle — if a helper binary makes the request, the settings list can be misleading/empty. For mic: same with `Privacy_Microphone`.
