---
name: flutter-expert
description: "Use when building cross-platform apps with Flutter 3+ and Dart — widget development, Riverpod/Bloc state management, GoRouter navigation, platform-specific implementations, performance optimization. Triggers: Flutter, Dart, widget, Riverpod, Bloc, GoRouter, cross-platform."
version: 1.0.0
license: MIT
tags: [flutter, dart, widgets, riverpod, bloc, gorouter, mobile, cross-platform]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/flutter-expert
derived_from: awesomeclaude
---

# Flutter Expert

Cross-platform apps with Flutter 3+ and Dart.

## When to use

Widget development; Riverpod or Bloc state management; GoRouter navigation; platform-specific (iOS/Android/web/desktop) implementations; performance optimization.

## Core workflow

1. **Analyze** — target platforms, state management choice, navigation needs.
2. **Design** — widget tree, separate UI from logic, state architecture.
3. **Implement** — composable widgets; Riverpod providers or Bloc/Cubit for state.
4. **Navigation** — GoRouter typed routes, deep links, guards.
5. **Optimize/test** — `const` widgets, avoid rebuilds; widget + unit tests.

## Key practices

- Prefer `const` constructors to skip rebuilds; small composable widgets.
- State: Riverpod (providers, `ref.watch`) or Bloc/Cubit (events → states); keep UI dumb.
- GoRouter for declarative routing, deep linking, redirect guards.
- Separate presentation, domain, data layers; immutable models (freezed).
- Platform branches via `Platform.isIOS` / `defaultTargetPlatform` or adaptive widgets.
- `ListView.builder` for long lists (lazy build).

## Constraints

MUST: `const` widgets where possible; keep widgets small + composable; immutable state models; lazy list builders; dispose controllers/streams; widget + unit tests.
MUST NOT: heavy logic in `build()`; rebuild whole trees on small state changes; leak controllers/subscriptions; deeply nested widget trees without extraction; block the UI isolate with heavy sync work.

## Output

1. Widget tree / screens. 2. State (Riverpod providers or Bloc). 3. GoRouter config. 4. Platform branches if needed. 5. Tests + brief note on rebuild/perf decisions.

## Knowledge

Flutter 3+, Dart, widgets, const optimization, Riverpod, Bloc/Cubit, GoRouter, freezed, ListView.builder, platform channels, flutter_test, golden tests.
