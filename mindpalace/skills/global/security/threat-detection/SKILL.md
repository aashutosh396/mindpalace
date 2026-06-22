---
name: Threat Detection & Hunting
description: Use when hunting for threats, analyzing IOCs, or detecting behavioral anomalies in telemetry — hypothesis-driven hunting, IOC sweep generation, z-score anomaly detection, MITRE ATT&CK signal prioritization.
tags: [threat-hunting, ioc, anomaly-detection, mitre-attack, z-score, siem, edr, deception, honeypots, behavioral-detection]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/threat-detection
---

# Threat Detection & Hunting

Proactive discovery of attacker activity that evaded automated controls. (Not incident response; not red team.) Needs read access to SIEM/EDR telemetry, endpoint logs, network flow.

## Hunting Methodology (5-step loop)
hypothesis → data source ID → query execution → finding triage → feedback to detection engineering.

## Hypothesis Scoring
`priority = (actor_relevance ×3) + (control_gap ×2) + (data_availability ×1)`. Actor relevance = match to known sector actors; control gap = how many controls miss it; data availability = telemetry to test it. ≥7 → full hunt.

## High-Value Hypotheses
WMI lateral T1047 (WMI spawned from WINRM) · LOLBin T1218 (certutil/regsvr32/mshta + network) · C2 beaconing T1071.001 (regular intervals ±10% jitter) · Pass-the-Hash T1550.002 (NTLM 4624 type 3 from unexpected host) · LSASS access T1003.001 (OpenProcess on lsass from non-system) · Kerberoasting T1558.003 (high-volume 4769 for svc accounts) · scheduled-task persistence T1053.005.

## IOC Analysis
Staleness thresholds: IPs/domains 30d, hashes 90d, URLs 14d, mutexes 180d. **Stale IOCs inflate false positives and erode SOC credibility** — exclude from sweeps, refresh feeds (MISP/OpenCTI/commercial) before every cycle.

## Anomaly Detection (z-score)
< 2.0 normal · 2.0-2.9 soft (log + increase sampling) · ≥ 3.0 hard (escalate to analyst). Needs 14+ days baseline. Recompute after incidents, infra changes, seasonal shifts. High-value targets: DNS queries/hour (beaconing/tunneling/DGA), endpoint unique processes/day, svc-account auth/hour, email attachment types, cloud IAM API calls/identity.

## Deception
Honeypot interaction = unambiguous high-fidelity signal → auto-SEV2 until proven otherwise. Assets: honey credentials in vault (T1555), honey tokens (fake AWS keys, T1552.004), honey files (passwords.xlsx, T1074), honey accounts (dormant AD, T1078.002), honeypot services (T1046/T1190).

## Anti-Patterns
Hunting without a hypothesis · stale IOCs · no baseline before alerting · hunting only known techniques (include open-ended anomaly analysis) · not closing the loop to detection engineering · treating every anomaly as confirmed (require human triage) · ignoring honeypot alerts.
