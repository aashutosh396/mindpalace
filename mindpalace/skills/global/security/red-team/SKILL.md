---
name: Red Team Engagement Planning
description: Use when planning or executing authorized red team engagements, attack-path analysis, or offensive security simulations — MITRE ATT&CK kill-chain planning, technique scoring, choke points, OPSEC, crown-jewel targeting.
tags: [red-team, mitre-attack, kill-chain, attack-path, opsec, crown-jewels, adversary-simulation, choke-points, offensive-security, rules-of-engagement]
source: alirezarezvani/claude-skills
derived_from: engineering-team/skills/red-team
---

# Red Team Engagement Planning

Structured adversary simulation to test detection, response, and control effectiveness. (Not vuln scanning; not incident response.)

## Authorization (mandatory)
Signed Rules of Engagement, defined scope, executive approval — predating execution. Unauthorized use is criminal (CFAA, Computer Misuse Act). Never plan against systems without written permission.

## Access Levels
- **external**: internet only → external-facing techniques (T1190, T1566).
- **internal**: network foothold, no creds → recon + lateral-movement prep.
- **credentialed** (assumed breach): full kill chain incl priv-esc, lateral, impact.

## Kill-Chain Phase Order
Recon (TA0043) → Resource Dev (TA0042) → Initial Access (TA0001) → Execution (TA0002) → Persistence (TA0003) → Priv Esc (TA0004) → Cred Access (TA0006) → Lateral Movement (TA0008) → Collection (TA0009) → Exfiltration (TA0010) → Impact (TA0040). Complete each phase before advancing (unless assumed-breach scope). Never skip persistence before lateral movement — a single detection wipes the foothold.

## Technique Scoring
`effort_score = detection_risk × (len(prerequisites) + 1)`. Lower = easier without detection. E.g. spearphishing link 0.4 (no prereqs) vs ransomware deploy 2.7 (needs persistence + lateral).

## Choke Points
Techniques required by multiple paths to crown jewels (usually cred-access / priv-esc). Detecting a choke point detects all paths through it — prioritize detection density there. Common: AD → T1003/T1558; AWS → T1078.004/PassRole chains; hybrid → T1550.002/T1021.006.

## OPSEC Risk per Tactic
Cred access: LSASS triggers EDR → prefer DCSync/Kerberoasting. Execution: PowerShell logging → AMSI bypass. Lateral: NTLM event 4624 type 3 → use Kerberos. Persistence: scheduled-task event 4698. Exfil: large transfers trigger DLP → stage + slow exfil. **Checklist before each phase:** in scope? actively monitored? less-detectable alternative? blast radius if detected? cleanup defined?

## Crown Jewels
Define in RoE — success = reaching them, not vuln count. DC (Kerberoasting→DCSync→Golden Ticket) · DBs (lateral→DBA→staging) · payment systems (pivot→svc account→exfil) · source repos (VPN→git→signing keys) · cloud plane (phish→cred→AssumeRole).

## Workflows
Quick scoping (30m): list techniques, build external assumed-no-access plan, review choke points + OPSEC, present to stakeholders. Full engagement: Week1 plan + RoE, Week2 external execution + log detections, Week3 internal (persistence→cred access→lateral), Week4 report mapping findings to detection gaps prioritized by choke-point impact.

## Anti-Patterns
No written authorization · skipping phase order · no defined crown jewels · ignoring OPSEC risks (avoiding all detectable techniques = unrealistic test) · retroactive documentation (log in real time) · not cleaning up artifacts · treating path of least resistance as the only path.
