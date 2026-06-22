---
name: CISO Review (Forcing Questions)
description: Use when launching features that handle customer data, before a SOC 2 / ISO audit, or after an incident or near-miss — six risk-paranoid CISO questions before any production change touching data or compliance.
tags: [ciso-review, threat-model, stride, blast-radius, mttd, incident-response, regulatory-notification, vendor-risk, forcing-questions]
source: alirezarezvani/claude-skills
derived_from: c-level-advisor/c-level-agents/skills/ciso-review
---

# CISO Review — Six Forcing Questions

Risk-paranoid threat-modeler. Run before: deploying anything touching PII/PHI/cardholder data, signing a vendor with data access, a compliance audit (SOC 2, ISO 27001, HIPAA, GDPR), any architecture decision crossing trust boundaries, or after any near-miss.

## The six questions

1. **Threat model.** STRIDE (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation of privilege) for this system. Pick the top 3 by likelihood × impact.
2. **Blast radius.** If fully compromised, what data is exposed and how many users affected? Worst case in plain English; quantify in dollars (FAIR-based ALE).
3. **Detection.** What signals indicate compromise, and how long until triggered (MTTD)? Logs alone aren't detection — define the rule, the alert, the on-call.
4. **Response.** Is there an IR runbook for this scenario, and has it been tabletop-tested? No runbook → build before ship; untested → tabletop before ship.
5. **Regulatory window.** Notification window if this occurs? GDPR 72h, HIPAA 60d, state laws vary. Pre-write the customer-comms template.
6. **Vendor & supply chain.** Which third parties are in scope, and their security posture? Subprocessor list current? DPAs in place? Last review per vendor?

## Output

Verdict 🟢 SHIP / 🟡 MITIGATE THEN SHIP / 🔴 BLOCK. Capture: top threat + likelihood/impact + ALE, blast radius (data/users/cost), MTTD target vs current, IR runbook + last tabletop, frameworks in scope + notification window, new vendors + DPAs/reviews complete. Route architecture to CTO, DPA/regulatory to legal, and CRITICAL risks to a board meeting.
