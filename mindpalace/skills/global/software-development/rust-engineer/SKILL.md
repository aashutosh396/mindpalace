---
name: rust-engineer
description: "Use when building Rust (2021 edition) applications, solving ownership/borrowing/lifetime issues, designing trait-based APIs, async with tokio, FFI bindings, or performance/memory-safety work. Triggers: Rust, Cargo, ownership, borrowing, lifetimes, async Rust, tokio, zero-cost abstractions, memory safety, systems programming."
version: 1.0.0
license: MIT
tags: [rust, cargo, ownership, lifetimes, tokio, traits, thiserror, systems-programming]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/rust-engineer
derived_from: awesomeclaude
---

# Rust Engineer

Idiomatic Rust 2021: memory safety, zero-cost abstractions, systems programming.

## When to use

Ownership/borrowing/lifetime design; trait hierarchies with generics + associated types; async with tokio; FFI bindings; performance and memory-safety optimization.

## Core workflow

1. **Analyze ownership** — lifetime relationships and borrowing; annotate explicitly when inference falls short.
2. **Design traits** — hierarchies, generics, associated types.
3. **Implement safely** — minimal `unsafe`; document every unsafe block's safety invariants.
4. **Handle errors** — `Result`/`Option` + `?`; custom errors via `thiserror`.
5. **Validate** — `cargo clippy --all-targets --all-features`, `cargo fmt --check`, `cargo test`; fix all warnings.

## Key patterns

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

```rust
use thiserror::Error;
#[derive(Debug, Error)]
pub enum AppError {
    #[error("I/O error: {0}")] Io(#[from] std::io::Error),
    #[error("parse `{value}`: {reason}")] Parse { value: String, reason: String },
}
fn read_config(p: &str) -> Result<String, AppError> { Ok(std::fs::read_to_string(p)?) }
```

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let body = reqwest::get("https://example.com").await?.text().await?;
    println!("{body}"); Ok(())
}
```

## Constraints

MUST: ownership/borrowing for safety; minimize + document `unsafe`; lean on the type system; explicit `Result`/`Option`; doc with examples; clippy clean; `cargo fmt`; doctests.
MUST NOT: `unwrap()` in prod (prefer `expect()` w/ message); leaks/dangling pointers; undocumented `unsafe`; ignore clippy; mix blocking + async; `String` where `&str` suffices; clone unnecessarily.

## Output

1. Type definitions (structs/enums/traits). 2. Implementation with proper ownership. 3. Custom error types. 4. Tests (unit/integration/doctests). 5. Brief note on design.

## Knowledge

Rust 2021, Cargo, ownership/borrowing, lifetimes, traits/generics, async/await, tokio, Result/Option, thiserror/anyhow, serde, clippy, rustfmt, criterion, MIRI.
