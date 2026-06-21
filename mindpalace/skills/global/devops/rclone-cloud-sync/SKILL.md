---
name: rclone-cloud-sync
description: "Use when syncing, copying, backing up, or mounting files to/from cloud storage — Google Drive, S3, Dropbox, OneDrive, Backblaze B2, Azure Blob, SFTP, FTP, WebDAV and 70+ providers via rclone."
version: 1.0.0
license: MIT
tags: [files, cloud, sync, backup, storage, rclone, s3, google-drive, dropbox]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-files
derived_from: awesomeclaude
---

# rclone Cloud Sync

Copy, sync, mount, and back up files across 70+ cloud providers with one tool.

## When to use
Moving files to/from cloud storage, scheduled backups, mounting a remote as a
local folder, verifying local and remote match.

## Commands

```bash
rclone listremotes                # List configured remotes
rclone ls remote:path             # List files (lsd for dirs only)
rclone copy local/path remote:path        # Copy up (or remote->local)
rclone sync local/path remote:path        # Make remote MATCH local (deletes extras!)
rclone move local/path remote:path        # Move
rclone check local/path remote:path       # Verify match without transferring
rclone mount remote:path /mnt/cloud --daemon   # Mount as local folder
rclone about remote:              # Storage usage
rclone ncdu remote:path           # Interactive file explorer
```

## Setup
Run `rclone config` to add remotes (Google Drive, S3, Dropbox, OneDrive,
Backblaze B2, Azure Blob, SFTP/FTP/WebDAV, etc.).

## Safety guidelines
- `rclone sync` DELETES files on the destination — use `copy` if unsure.
- Always run with `--dry-run` first to preview changes.
- Confirm with the user before any sync that removes remote files.
- Use `rclone check` to verify integrity without transferring.
