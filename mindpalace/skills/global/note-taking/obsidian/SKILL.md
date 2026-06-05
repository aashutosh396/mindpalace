---
name: obsidian
description: Read, list, search, create, append to, and edit notes in an Obsidian vault on the filesystem. Use for any Obsidian note-taking task (vault is just markdown files plus [[wikilinks]]).
platforms: [linux, macos, windows]
tags: [obsidian, notes, note-taking, markdown, knowledge]
---

# Obsidian Vault

An Obsidian vault is just a folder of markdown (`.md`) files linked with `[[wikilinks]]`. This skill is filesystem-first: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks — all with normal file tools.

## Vault path

Resolve a concrete absolute vault path before doing anything.

- Convention: the vault path may be in the `OBSIDIAN_VAULT_PATH` environment variable. Resolve it with bash: `echo "$OBSIDIAN_VAULT_PATH"`.
- If unset, fall back to `~/Documents/Obsidian Vault` (check it exists: `ls -d ~/Documents/Obsidian\ Vault`).
- Vault paths often contain spaces — always quote them in bash, and pass a fully-resolved absolute path (not `$OBSIDIAN_VAULT_PATH`) to the Read/Write/Edit tools, which do not expand shell variables.

## Read a note

Use the **Read** tool with the resolved absolute path. It gives line numbers and pagination — better than `cat`.

## List notes

Use the **Glob** tool against the vault path.

- All markdown notes: pattern `**/*.md` under the vault path.
- A subfolder: pattern `**/*.md` rooted at that subfolder's absolute path.

## Search

- **Filename search** → Glob with a name pattern (e.g. `**/meeting*.md`).
- **Content search** → Grep with the regex as the pattern, `path` set to the vault, and `glob: "*.md"` to restrict matches to notes.

## Create a note

Use the **Write** tool with the resolved absolute path and the full markdown content. Avoids shell-quoting issues from heredocs/`echo`.

## Append to a note

- Read the target note first (Read tool).
- For an anchored append (after a known heading or before a known trailing block), use **Edit**: replace the anchor text with the anchor plus the new content.
- When rewriting the whole note is clearer than a fragile edit, use **Write**.
- For a trivial append with no stable anchor, a quoted bash append is acceptable, e.g. `printf '%s\n' "new line" >> "/abs/path/to/note.md"`.

## Targeted edits

Use the **Edit** tool for focused changes when the current content gives stable context. Prefer it over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
