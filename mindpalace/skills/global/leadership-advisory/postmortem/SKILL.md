---
name: Blameless Post-Mortem
description: Use after a failed launch, missed quarter, lost deal, or bad hire to run a rigorous blameless retrospective — a proper 5-Whys to root cause, contributing-factor separation, missed-warning-sign review, and an owned/dated change register with a verification date.
tags: [postmortem, retrospective, 5-whys, root-cause, blameless, change-register, failure-analysis]
source: alirezarezvani/claude-skills
derived_from: executive-mentor/postmortem
---

# Post-Mortem — Honest Analysis of What Went Wrong

Not blame, not whitewash. A rigorous investigation into a system failure: "what conditions made this outcome predictable in hindsight?" Goal: extract maximum learning so the failure class doesn't recur.

## The Framework

**1. Define the event precisely.** Expected outcome vs actual; when the gap was first visible; quantified impact. "We missed Q3" is not precise — "$420K closed vs $680K target; $260K miss from 3 slipped deals + 1 competitive loss" is.

**2. The 5 Whys — done properly.** Drive from symptom to root cause. The test for a real root cause: *could you prevent recurrence with a specific, concrete change?* Bad 5-Whys dead-end at "that's just how enterprise sales works." Real ones end at "qualification criteria outdated, no owner, no review process" → fix is actionable.

**3. Contributing factors ≠ root cause.** Contributing factor: made it worse; if removed, the same class of problem still recurs. Root cause: the fundamental condition; fix it and the class doesn't recur. Addressing only contributing factors gives you a structurally identical failure next time.

**4. Warning signs ignored.** At what point was the outcome predictable? What signals were visible? Who saw them, and what happened when raised? Common patterns: signal dismissed by a senior person; nobody felt safe raising it; no clear ownership to act; data available but unwatched; team too optimistic. "We didn't feel safe raising it" is a far deeper root cause than the surface issue.

**5. In control vs out of control.** Process/criteria/capability/decisions = in control. Market/customer/competitor/macro = out. For out-of-control: how to be more resilient. Be rigorous — "outside our control" is sometimes accountability-avoidance.

**6. Change register.** Specific, owned, dated commitments. Bad: "improve our qualification process." Good: "Ravi rewrites qualification criteria by Mar 15 to require champion identification; reviewed in weekly standup from Mar 22." Each action: what changes / who owns / by when / how to verify.

**7. Verification date.** The most-skipped step. Set a date to check whether changes happened and worked. Without it, post-mortems are theater.

## Output Format
```
EVENT / EXPECTED / ACTUAL / IMPACT (quantified)
TIMELINE
5 WHYS → ROOT CAUSE (one sentence)
CONTRIBUTING FACTORS
WARNING SIGNS MISSED (signal + date + why not acted on)
IN CONTROL / NOT IN CONTROL
CHANGE REGISTER table: Action | Owner | Due | Verification
VERIFICATION DATE
```

## Tone
Blame is cheap, understanding is hard. "The salesperson didn't qualify properly" = blame (fires/shames someone). "Our qualification framework wasn't updated when we moved upmarket and nobody owned it" = understanding (builds resilience). Both may be true; pick the one that prevents recurrence.
