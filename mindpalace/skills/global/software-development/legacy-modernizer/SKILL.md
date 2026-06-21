---
name: legacy-modernizer
description: "Use when modernizing legacy systems, applying the strangler fig pattern or branch by abstraction, decomposing monoliths, upgrading frameworks/languages, or reducing technical debt without disrupting operations. Triggers: legacy modernization, strangler fig, incremental migration, technical debt, legacy refactoring, system migration, modernize codebase."
version: 1.0.0
license: MIT
tags: [legacy, modernization, strangler-fig, migration, technical-debt, characterization-tests, feature-flags, monolith]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/legacy-modernizer
derived_from: awesomeclaude
---

# Legacy Modernizer

Incremental migration of aging systems with zero production disruption.

## When to use

Modernizing legacy code, strangler fig / branch by abstraction, decomposing monoliths, framework/language upgrades, reducing tech debt.

## Core workflow

1. **Assess system** — codebase, dependencies, risks, constraints. Produce a dependency map + risk register. Checkpoint: all external integrations and data contracts documented.
2. **Plan migration** — incremental roadmap with per-phase rollback strategies. Checkpoint: each phase has a rollback trigger and owner.
3. **Build safety net** — characterization tests + monitoring before touching prod. Target 80%+ coverage of existing behavior; confirm green on unmodified legacy.
4. **Migrate incrementally** — strangler fig + feature flags; route via facade, shift traffic gradually (5% → 25% → 50% → 100%). Checkpoint: error rate + latency stay within baseline after each increment.
5. **Validate & iterate** — full suite, dashboards, business behavior preserved. New code stable at 100% for one release cycle before removing legacy path.

## Code examples

```python
# Strangler fig facade — route by feature flag
class OrderServiceFacade:
    def get_order(self, order_id: str):
        if os.getenv("USE_NEW_ORDER_SERVICE","false").lower()=="true":
            return self._new.fetch(order_id)
        return self._legacy.get(order_id)
```
```python
# Characterization (golden-master) test — fail loudly if legacy behavior changes
@pytest.mark.parametrize("order_id,expected", [("ORD-001","SHIPPED"),("ORD-002","PENDING")])
def test_order_status_golden_master(order_id, expected):
    assert service.get(order_id)["status"] == expected
```

## Constraints

MUST: zero production disruption; comprehensive test coverage before refactoring (80%+); feature flags for all rollouts; monitoring + rollback procedures; document decisions; preserve business logic; communicate progress/risks.
MUST NOT: big-bang rewrites; skip testing legacy behavior first; deploy without rollback; break existing integrations/APIs; introduce tech debt in new code; rush without validation; remove legacy code before new code is proven.

## Output

1. Assessment summary (risks, dependencies, approach)
2. Migration plan (phases, rollback, metrics)
3. Implementation code (facades, adapters, new services)
4. Test coverage (characterization, integration, e2e)
5. Monitoring setup
