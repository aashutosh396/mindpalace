---
name: package-tracking
description: "Use when tracking a shipment or package by tracking number — UPS, FedEx, USPS, DHL via ordercli. Returns current status, last location, estimated delivery, and full event history. Carrier auto-detected."
version: 1.0.0
license: MIT
tags: [tracking, shipping, packages, delivery, ups, fedex, usps, dhl, ordercli]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-tracking
derived_from: awesomeclaude
---

# Package Tracking

Look up shipments across major carriers with `ordercli` — no browser needed.

## When to use
The user gives a tracking number or asks "where's my package", delivery status,
or estimated arrival.

## Commands

```bash
ordercli track 1Z999AA10123456784                 # Auto-detect carrier
ordercli track --carrier ups 1Z999AA10123456784   # Explicit carrier
ordercli track --carrier fedex 123456789012
ordercli track --carrier usps 9400111899223397623472
ordercli track --carrier dhl 1234567890
ordercli track --history 1Z999AA10123456784        # Full event timeline
ordercli track NUM1 NUM2                            # Multiple at once
```

Carriers: `ups`, `fedex`, `usps`, `dhl`.

## Guidelines
- Try auto-detection first before specifying a carrier.
- Report current status, last known location, and estimated delivery.
- Use `--history` when the user wants the full timeline.
- Tracking numbers must be exact (no stray spaces/dashes).
- Some carriers update slowly — results reflect the last scan.
