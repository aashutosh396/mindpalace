---
name: file-organizer
description: "Use when the user wants to organize, tidy, declutter, or clean up files/folders — messy Downloads, Desktop, Documents or Projects folders, finding duplicate files, archiving old files, restructuring directories, organizing photos by date, or separating work vs personal files."
version: 1.0.0
license: MIT
tags: [files, organize, declutter, duplicates, cleanup, downloads, archive, filesystem, folders]
source: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/file-organizer
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [find, du, md5, file]
---

# File Organizer

Personal organization assistant for keeping a clean, logical file structure across the
machine. Analyzes folders, finds duplicates, proposes structures, and moves/renames files
with user approval.

## When to use

- Downloads / Desktop / Documents is a chaotic mess and files are hard to find
- Duplicate files are wasting space
- Folder structure no longer makes sense, or none exists
- Starting a new project and need a sane structure
- Cleaning up / archiving old projects or photos
- Separating work vs personal files

## Workflow

1. Understand scope — ask: which directory? main problem (find things / dupes / messy /
   no structure)? files/folders to avoid (active projects, sensitive data)? how aggressive
   (conservative vs comprehensive)?

2. Analyze current state of the target dir:
   ```bash
   ls -la "$DIR"
   du -sh "$DIR"/* | sort -rh | head -20                       # largest items
   find "$DIR" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn   # file-type counts
   ```
   Summarize: total files/folders, type breakdown, size distribution, date ranges, issues.

3. Identify groupings — by type (docs, images, video, archives, code, spreadsheets,
   presentations), by purpose (work/personal, active/archive, project, reference, scratch),
   or by date (current year/month, prior years, very old = archive candidates).

4. Find duplicates (only when asked):
   ```bash
   find "$DIR" -type f -exec md5 {} \; | sort | uniq -d        # exact dupes by hash (macOS md5)
   find "$DIR" -type f -printf '%f\n' | sort | uniq -d         # same name (GNU find)
   ```
   For each dupe set: show all paths + sizes + mod dates, recommend which to keep (usually
   newest / best-located). ALWAYS confirm before deleting.

5. Propose a plan BEFORE making changes — show current state, proposed folder tree, and the
   exact list of folders to create / files to move / renames. Wait for approval.

6. Execute after approval, then give maintenance tips and a few quick commands for their
   setup (e.g. `find . -type f -mtime -7` for files changed this week).

## Naming conventions to apply

- Folders: clear, descriptive, no spaces (hyphens), specific ("client-proposals" not "docs").
  Use numeric prefixes to order: "01-current", "02-archive".
- Files: include date prefix `YYYY-MM-DD-description.ext`; descriptive; no version numbers in
  names (use version control); strip download artifacts (`document-final-v2 (1).pdf` → `document.pdf`).

## Archive (don't delete) when

- Not touched in 6+ months, completed work that may be referenced, old versions after a
  migration, or anything the user is hesitant to delete. Archive by year: `Archive/2024/`.

## Photos by date

Build `Photos/YYYY/MM-Month/` and `Unsorted/`, sorting by EXIF capture date (fall back to
file mtime when EXIF is missing).

## Gotchas

- Destructive ops (delete/move) require explicit user confirmation — never auto-delete dupes.
- `md5` is macOS; on Linux use `md5sum`. `find -printf` is GNU-only; on macOS use
  `find "$DIR" -type f -exec basename {} \; | sort | uniq -d`.
- Respect avoid-list (active projects, sensitive data) given in step 1.
- Start small (one folder like Downloads) to build trust before larger cleanups.
