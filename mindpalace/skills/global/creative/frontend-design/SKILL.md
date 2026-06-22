---
name: Frontend Design (Distinctive Visual Direction)
description: Use when building or reshaping a UI and you want a distinctive, intentional visual identity that doesn't read as templated AI default — gives aesthetic direction, typography, layout, and copy.
tags: [frontend, ui, design, typography, css, aesthetic, branding, layout, web-design]
source: anthropics/skills
derived_from: frontend-design
---

Act as the design lead at a studio known for giving every client an identity that could not be mistaken for anyone else's. Make deliberate, opinionated choices specific to this brief, and take one real aesthetic risk you can justify.

## Ground it in the subject
If the brief doesn't pin down the product/subject, pin it yourself: name one concrete subject, its audience, and the page's single job. Distinctive choices come from the subject's own world — its materials, instruments, artifacts, vernacular. Build with real content throughout.

## Design principles
- **Hero is a thesis.** Open with the most characteristic thing in the subject's world (headline, image, animation, live demo, interactive moment). Avoid the template answer (big number + label + gradient accent) unless truly best.
- **Typography carries personality.** Pair display + body faces deliberately — not your default families. Set a clear type scale with intentional weights/widths/spacing. Make the type treatment itself memorable.
- **Structure is information.** Numbering, eyebrows, dividers, labels should encode something true, not decorate. Numbered markers (01/02/03) only if content is genuinely a sequence.
- **Motion deliberately.** Page-load sequence, scroll reveal, hover micro-interactions, ambient atmosphere — one orchestrated moment beats scattered effects. Often less is more; extra animation reads as AI-generated.
- **Match complexity to vision.** Maximalist needs elaborate execution; minimal needs precision in spacing/type/detail.

## Avoid the AI-default clusters
AI design currently clusters around three looks; treat them as defaults, not choices: (1) warm cream bg (~#F4F1EA) + high-contrast serif + terracotta accent; (2) near-black bg + single acid-green/vermilion accent; (3) broadsheet hairline-rule layout, zero radius, dense columns. If the brief asks for one of these, follow it exactly; otherwise don't spend free axes on them.

## Process: brainstorm → plan → critique → build → critique
Work in two passes. **Pass 1 — compact token system:**
- Color: 4–6 named hex values.
- Type: typefaces for 2+ roles (characterful display used with restraint, complementary body, utility face for captions/data).
- Layout: concept in one-sentence prose + ASCII wireframes to compare.
- Signature: the single unique element this page is remembered by.

Then review the plan against the brief: if any part reads like the generic default you'd produce for any similar page, revise it and say what you changed and why. Only then write code, deriving every color/type decision from the revised plan.

**CSS gotcha:** watch selector specificity — type-based (`.section`) and element-based (`.cta`) selectors can cancel each other on paddings/margins between sections.

## Restraint and self-critique
Spend boldness in one place (the signature); keep everything else quiet. Cut decoration that doesn't serve the brief. Build to a quality floor silently: responsive to mobile, visible keyboard focus, reduced-motion respected. Critique as you build (screenshots if possible). Chanel's rule: before leaving, remove one accessory.

## Writing as design material
Words exist to make the design easier to understand and use — not decoration.
- Write from the user's side of the screen: name things by what people control ("notifications", not "webhook config").
- Active voice; a control says what happens ("Save changes", not "Submit"). Keep the same name through the whole flow (button "Publish" → toast "Published").
- Treat errors/empty states as direction, not mood: explain what went wrong and how to fix it; an empty screen invites action.
- Conversational, sentence case, no filler; each element does exactly one job.
