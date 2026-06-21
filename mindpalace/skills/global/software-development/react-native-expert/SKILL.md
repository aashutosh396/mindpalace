---
name: react-native-expert
description: "Use when building cross-platform mobile apps with React Native and Expo — navigation (tabs/stacks/drawers), native modules, FlatList perf, platform-specific iOS/Android code, SafeArea/keyboard, Expo SDK. Triggers: React Native, Expo, mobile app, iOS, Android, cross-platform, native module."
version: 1.0.0
license: MIT
tags: [react-native, expo, mobile, ios, android, navigation, flatlist, cross-platform]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/react-native-expert
derived_from: awesomeclaude
---

# React Native Expert

Cross-platform mobile with React Native + Expo.

## When to use

React Native / Expo apps; navigation hierarchies (tabs, stacks, drawers); native modules; FlatList scroll performance; platform-specific iOS/Android code; SafeArea + keyboard handling; Expo SDK config.

## Core workflow

1. **Analyze** — Expo vs bare workflow, target platforms, navigation needs.
2. **Design** — navigation structure (React Navigation); shared vs platform code.
3. **Implement** — components, hooks; `Platform.select` for platform branches.
4. **Optimize** — FlatList tuning (`getItemLayout`, `keyExtractor`, memoized items).
5. **Test** — Jest + React Native Testing Library; test on both platforms.

## Key practices

- React Navigation for tabs/stacks/drawers; typed route params.
- FlatList over ScrollList for long lists; `memo` items, stable `keyExtractor`, `getItemLayout` when sizes are fixed.
- `SafeAreaView`/insets; `KeyboardAvoidingView` for input screens.
- `Platform.OS`/`Platform.select` and `.ios.tsx`/`.android.tsx` for divergence.
- Expo SDK modules for native capability; EAS for builds.

## Constraints

MUST: FlatList (not map over ScrollView) for long lists; memoized list items + stable keys; SafeArea handling; platform-specific code where behavior differs; test on iOS and Android.
MUST NOT: render large lists with `.map`; inline functions/objects in render hot paths; block JS thread with heavy sync work; ignore keyboard/SafeArea; assume one platform's behavior holds for both.

## Output

1. Navigation setup. 2. Screens/components + hooks. 3. FlatList perf config. 4. Platform-specific branches. 5. Jest/RNTL tests + brief note on perf decisions.

## Knowledge

React Native, Expo, EAS, React Navigation, FlatList optimization, Platform API, SafeAreaContext, KeyboardAvoidingView, native modules, Reanimated, Jest, React Native Testing Library.
