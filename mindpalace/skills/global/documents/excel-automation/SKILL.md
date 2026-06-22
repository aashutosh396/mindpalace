---
name: Excel Automation (create / parse / control)
description: Use when creating formatted Excel reports, parsing complex xlsm financial models that openpyxl chokes on, or controlling Excel on macOS via AppleScript — covers IB color conventions and stdlib zipfile+xml parsing.
tags: [excel, openpyxl, xlsm, financial-models, applescript, macos, zipfile, xml, spreadsheets]
source: daymade/claude-code-skills
derived_from: excel-automation
---

# Excel Automation

Three capabilities — pick by file complexity.

## Tool selection
- Simple (data export, no VBA, <1MB) → **openpyxl / pandas**
- `.xlsm` / from investment bank / >1MB / VBA → **zipfile + xml.etree** (stdlib)
- True `.xls` (BIFF) → **xlrd**

**Always run `file <path>` first** — extensions lie (a `.xls` may be a ZIP xlsx).

## Create (openpyxl) — IB color convention
Blue `0000FF` = input/assumption; Black `000000` = calculated; Green `008000` = cross-sheet ref; white-on-`4472C4` = headers. Number formats: `$#,##0`, `0.0%`, `0.0x`. Sensitivity tables: `ColorScaleRule` red→yellow→green. Run via `uv run --with openpyxl scripts/create_formatted_excel.py`.

## Parse complex xlsm (when openpyxl fails)
XLSX is a ZIP. Internal: `xl/workbook.xml` (sheet names+order), `xl/sharedStrings.xml` (text lookup), `xl/worksheets/sheetN.xml` (cells), `xl/_rels/workbook.xml.rels` (maps rId→sheetN).

**Sheet name resolution (two-step)**: workbook.xml → find rId for sheet name → workbook.xml.rels → map rId to physical file path.

**Cell extraction**: build sharedStrings list; for each `<c>` read `r` (ref), `t` (type; `s`=shared string else number), `<v>` value; resolve `data[ref] = shared[int(v)]` if shared else float.

**Fix corrupted DefinedNames**: IB xlsm often has `<definedName>` containing "Formula removed" — extract ZIP, parse workbook.xml, remove those `<definedName>` entries, repackage with ZIP_DEFLATED.

Full template: `scripts/parse_complex_excel.py` (list sheets / extract sheet / `--fix`).

## Control Excel on macOS (AppleScript)
`osascript -e 'tell application "Microsoft Excel" to activate'`; also `open POSIX file`, `set zoom of active window to 120`, `set scroll row/column`, `select range "A1"`, `activate object sheet "DCF"`. **Always wrap with `timeout 5`** (osascript hangs forever if Excel not running; exit 124 = timed out). Add `sleep 1` before screenshots for UI render.

## Common mistakes
openpyxl monkey-patching → switch to zipfile immediately. `wc -c` on Chinese → use `wc -m`. Trusting extension → `file` first. `load_workbook` hanging on big xlsm → targeted zipfile extraction.
