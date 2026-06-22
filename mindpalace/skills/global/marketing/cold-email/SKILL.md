---
name: Cold Email Outreach
description: Use when writing, improving, or sequencing B2B cold outreach to prospects who haven't opted in — first-touch emails, multi-step follow-up sequences, voice calibration by seniority, subject lines, and deliverability basics. Distinct from lifecycle/nurture emails.
tags: [cold-email, cold-outreach, prospecting, sdr, sales-email, follow-up-sequence, subject-lines, deliverability, b2b]
source: alirezarezvani/claude-skills
derived_from: marketing-skill/skills/cold-email
---

# Cold Email Outreach

Write cold sequences that sound like a thoughtful human, not a sales machine, and get replies. (For opted-in lifecycle/nurture, use an email-sequence skill instead.)

## Three modes
- **Write first email** — understand ICP + problem + trigger → pick framework → draft subject/opener/body/CTA → cut anything that doesn't earn its place → deliver copy + 2-3 subject variants + rationale.
- **Build a sequence** — first email + follow-up angles (each a different angle, not a nudge) + cadence + standalone hooks + a breakup email.
- **Iterate from data** — diagnose: subject lines (low open) / body (opens, no reply) / CTA (replies, wrong outcome) → rewrite the failing element → recommend a test.

## Core writing principles
1. **Write like a peer, not a vendor.** Test: would a friend send this to another friend in business?
2. **Every sentence earns its place** — create curiosity / establish relevance / build credibility / drive the ask, else cut. Read aloud; the moment you drone, cut.
3. **Personalization connects to the problem** — "I saw you're hiring 3 SDRs — usually a signal you're scaling outbound, exactly what we help with." Fake personalization ("I saw you went to MIT") is worse than none.
4. **Lead with their world, not yours.**
5. **One ask per email.**

## Voice calibration
| Audience | Length | Subject style | What works |
|---|---|---|---|
| C-suite | 3-4 sentences | short, vague, internal-looking | big problem → relevant proof → one question |
| VP/Director | 5-7 | slightly specific | specific observation + business angle |
| Mid-level | 7-10 | descriptive | problem + practical value + easy CTA |
| Technical | 7-10 | technical specificity | exact problem → precise solution → low-friction ask |
Higher up the org = shorter.

## Subject lines
Goal = get it opened, nothing else. Best look like internal email: 2-3 words ("quick question"), specific trigger ("your TechCrunch piece"), shared context ("re: Series B"), referral hook ("[name] suggested I reach out"). Kills opens: ALL CAPS, emojis, fake Re:/Fwd:, a question in the subject, your company name, blog-headline numbers.

## Follow-up strategy
Cadence with widening gaps: Day 1, 4, 9, 16, 25, breakup Day 35. Each follow-up needs a NEW angle (new evidence / new angle on the problem / related insight / direct question / reverse referral ask). **Never "just check in."** Each follow-up stands alone — don't make them scroll. Breakup email signals it's the last (paradoxically lifts reply rate).

## Deliverability basics
Dedicated sending subdomain (`outreach.yourdomain.com`) · SPF + DKIM + DMARC all passing · 4-6 week domain warmup (start 20/day) · plain-text or minimal HTML · unsubscribe (CAN-SPAM/GDPR) · 100-200/day/domain cap until established · keep bounce rate <5% (verify lists).

## Avoid: "I hope this finds you well", "I wanted to reach out because...", feature dumps in email 1, HTML templates with logos, "just checking in" follow-ups, opening with "My name is X and I work at Y", passive CTAs ("let me know if interested").
