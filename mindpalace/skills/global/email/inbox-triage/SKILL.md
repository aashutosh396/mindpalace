---
name: Inbox Triage (Recurring)
description: Use when the user wants their inbox processed ("triage my inbox", "check my email") — classifies, researches senders, recommends decisions, drafts replies (NEVER sends), reports, and updates the KB. Requires inbox-setup first.
tags: [email, inbox-triage, drafts-only, email-classification, recurring, gmail, outlook, sender-research, knowledge-base]
source: alirezarezvani/claude-skills
derived_from: productivity/email/skills/inbox-triage
---

# Inbox-Triage

Run on a recurring schedule (1-3x daily) or on demand. Classify recent emails, research new senders, recommend decisions, draft replies (**NEVER SEND**), deliver a clean report, update the knowledge base. Consumes the 7-file KB written by `inbox-setup` at `${WORKSPACE}/Email/` — halt and route to inbox-setup if core files missing.

## DRAFTS ONLY — never send
This is the safety property that makes it safe to run automatically. Non-negotiable. Any send-shaped tool call fails validation.

## Light intake (0-2 optional override questions)
Default runs skip questions. Q1 only if on-demand outside normal cadence (override the 9h search window). Q2 only if user signals category-skip ("skip newsletters").

## Steps
1. **Search window** — default 9h (2x/day cadence). Map: once daily→26h, 2x→9h, 3x→6h, on-demand→24h. Run label = Morning/Afternoon/Evening.
2. **Search** — primary (inbox+sent after window_start) + secondary (starred unread). Provider adapter: Gmail/Outlook/IMAP MCP; halt with clear message if no email tool.
3. **Classify** — apply taxonomy from KB. Lowest-priority (newsletters/automation/spam): skip thread reads. Everything else: read full thread.
4. **Sender research** — check blocklist (auto-skip), tracker (known context); for opportunity senders web-search legitimacy. Skip for known/internal/automated/low-priority.
5. **Recommendations** (if evaluation-framework.md exists) — TAKE IT (green, draft engaged) / WORTH CONSIDERING (amber, draft + clarifying Qs) / PASS (red, polite decline) / FLAG FOR REVIEW (purple, NO draft).
6. **Drafts** — for reasonable reply candidates using email-patterns.md voice (register, forbidden tokens, sign-offs, persona, hard rules, length). Draft in existing thread; set to/subject `Re:`. **Never call any send operation.** Don't draft for newsletters/automation/already-replied/blocked.
7. **Report** — per KB preference (default: email draft to self, HTML, inline CSS only). Sections: Overview / Stats / Action Needed / Quick Reference (one line per email, alphabetical) / Detailed Cards (no draft previews — they're in the client) / Footer.
8. **KB update** — blocklist (new declines + patterns), tracker (follow-ups, deadlines, resolved). Learn over runs (drafts edited vs sent-as-is, PASS overrides, decline patterns). After 5+ runs suggest KB improvements.
9. **Internal log** — `triage-log/[date]-[label].md` (audit trail for the send-safety check).
10. **Empty inbox** — still check tracker for due/overdue; minimal report.

## Critical rules
DRAFTS ONLY never send (restated) · no credentials in KB · accuracy over speed (when unsure, flag — a wrong auto-draft is worse than none) · respect documented KB preferences · note every KB change in the log · first runs need oversight.
