---
name: invoice-organizer
description: "Use when organizing invoices, receipts, or financial documents for taxes/bookkeeping — reading messy PDFs/scans, extracting vendor/date/amount, renaming to a standard format, sorting into folders by vendor/category/year, and exporting an accountant CSV. Triggers: 'organize my invoices', 'sort receipts for taxes', 'rename these invoices', 'clean up my receipts folder', 'tax-ready filing'."
version: 1.0.0
license: MIT
tags: [invoices, receipts, taxes, bookkeeping, file-organization, pdf, expenses, accounting]
source: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/invoice-organizer
derived_from: awesomeclaude
---

# Invoice Organizer

Turn a chaotic folder of invoices, receipts, and financial documents into a clean,
tax-ready filing system: extract the key fields, rename consistently, sort into
folders, and produce a CSV for the accountant.

## When to use

- Prepping for tax season / need organized records for an accountant or audit
- A messy folder of receipts, email downloads, or screenshots needs filing
- Reconciling monthly business expenses or reimbursements
- Archiving multiple years of invoices by year/vendor/category
- Files all named `invoice.pdf`, `invoice(1).pdf`, `IMG_2847.jpg`, etc.

## Workflow

### 1. Scan the folder
Enumerate candidate files and report count, types, date range, current structure:
```bash
find . -type f \( -name "*.pdf" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -print
```

### 2. Extract info from each file
Read each document (PDF text, or read visible text from images) and pull:
- Vendor / company name (usually top of the doc)
- Date — look for "Invoice Date:", "Date:", "Issued:"
- Invoice number — "Invoice #:", "Invoice Number:"
- Amount — "Amount Due:", "Total:", "Amount:"
- Product/service description
- Payment method (if present)

Fallback when unclear: use filename clues, then file mtime, then flag for review.

### 3. Confirm organization strategy
Ask the user (or use default `Year/Category/Vendor`). Common patterns:
- By vendor: `Adobe/`, `Amazon/`, `Stripe/`
- By year + category (tax-friendly): `2024/Software/`, `2024/Travel/`
- By quarter: `2024/Q1/Software/`
- By tax category: `Deductible/`, `Partially-Deductible/`, `Personal/`

### 4. Standardize filenames
Pattern: `YYYY-MM-DD Vendor - Invoice - Description.ext`
- e.g. `2024-03-15 Adobe - Invoice - Creative Cloud.pdf`
- Strip special chars except hyphens; capitalize vendor; keep description concise;
  always `YYYY-MM-DD` for sortability; preserve original extension.

### 5. Show plan, then execute (after approval)
Print the proposed folder tree plus a few before/after samples and a file count,
then ask "Process N files? (yes/no)". On approval:
```bash
mkdir -p "Invoices/2024/Software/Adobe"
# Prefer copy to preserve originals; move only if the user asks:
cp "original.pdf" "Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf"
```

### 6. Generate CSV summary
Write `Invoices/invoice-summary.csv` for import into accounting software:
```csv
Date,Vendor,Invoice Number,Description,Amount,Category,File Path
2024-03-15,Adobe,INV-12345,Creative Cloud,52.99,Software,Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf
```

### 7. Report completion
Summarize: count processed, date range, total amount (if extracted), unique
vendors, the new tree, files needing review, and next steps.

## Gotchas / special cases

- Missing date or vendor → flag to a `Needs-Review/` folder; use file mtime as a
  date fallback. Never guess critical fields silently.
- Duplicates → compare file hashes, keep the best copy, note duplicates in the CSV.
- Multi-page / split invoices → merge PDFs if needed, note the split in the CSV.
- Preserve originals by default (copy, not move) unless the user opts into moving.
- Standard retention is ~7 years (audit period) — don't delete originals.
- For ongoing use, offer a watcher/script over `~/Downloads/invoices` that
  auto-applies the same naming + folder rules to new files.
