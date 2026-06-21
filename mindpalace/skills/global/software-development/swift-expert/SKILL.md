---
name: swift-expert
description: "Use when building iOS/macOS/watchOS/tvOS apps with Swift 5.9+, SwiftUI views and state, protocol-oriented architecture, async/await concurrency, actors, or server-side Swift (Vapor). Triggers: Swift, SwiftUI, iOS development, macOS development, async/await Swift, Combine, UIKit, Vapor, actors, protocol-oriented."
version: 1.0.0
license: MIT
tags: [swift, swiftui, ios, macos, async-await, actors, combine, vapor]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/swift-expert
derived_from: awesomeclaude
---

# Swift Expert

Apple-platform Swift 5.9+, SwiftUI, structured concurrency.

## When to use

iOS/macOS/watchOS/tvOS apps; SwiftUI views + state management; protocol-oriented design; async/await + actors; UIKit integration; Combine; server-side Swift (Vapor).

## Core workflow

1. **Analyze** — target platforms, SwiftUI vs UIKit, dependency graph.
2. **Design** — protocols + value types first; model state with enums.
3. **Implement** — SwiftUI views with `@State`/`@Observable`; actors for shared mutable state.
4. **Concurrency** — async/await, `Task`, `TaskGroup`; isolate state with actors.
5. **Test** — XCTest / Swift Testing; verify main-actor UI updates.

## Key practices

- Protocol-oriented: protocols + extensions over class inheritance.
- Value semantics: prefer `struct`/`enum`; classes only for identity/reference.
- `@Observable` (Observation) or `ObservableObject` for view models.
- Actors guard shared mutable state; `@MainActor` for UI.
- Structured concurrency: child tasks via `TaskGroup`; cancel cooperatively.
- Optionals via `if let`/`guard let`; avoid force-unwrap in production.

## Constraints

MUST: value types by default; protocol-oriented design; `@MainActor` for UI mutations; actors for shared state; cooperative cancellation; explicit error handling (`throws`/`Result`).
MUST NOT: force-unwrap (`!`) in production; mutate UI off the main actor; retain cycles (use `[weak self]`); block the main thread; mix Combine + async/await incoherently.

## Output

1. Protocol/type definitions. 2. SwiftUI views + view models (or UIKit). 3. Concurrency-safe data layer. 4. XCTest cases. 5. Brief note on architecture.

## Knowledge

Swift 5.9+, SwiftUI, Observation/@Observable, UIKit, async/await, actors, structured concurrency, Combine, Swift Package Manager, Vapor, XCTest/Swift Testing.
