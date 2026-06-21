---
name: cpp-pro
description: "Use when building or refactoring modern C++ (C++20/23) needing concepts, ranges, coroutines, SIMD, or careful memory management, or addressing performance bottlenecks, concurrency issues, and CMake build config. Triggers: C++, C++20, C++23, modern C++, template metaprogramming, systems programming, performance optimization, SIMD, memory management, CMake."
version: 1.0.0
license: MIT
tags: [cpp, cpp20, cpp23, templates, concepts, ranges, cmake, performance]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/cpp-pro
derived_from: awesomeclaude
---

# C++ Pro

Modern C++20/23: high-performance, type-safe systems code.

## When to use

Modern C++ with concepts/ranges/coroutines; template metaprogramming; SIMD optimization; RAII memory management; concurrency; CMake build configuration; performance tuning.

## Core workflow

1. **Analyze** — toolchain, C++ standard, build system, hotspots.
2. **Design** — RAII ownership, value semantics, concepts to constrain templates.
3. **Implement** — smart pointers, ranges, `constexpr` where possible.
4. **Optimize** — profile (perf/VTune), reduce allocations, SIMD where it pays.
5. **Validate** — sanitizers (ASan/UBSan/TSan), clang-tidy, unit tests.

## Key practices

- RAII for all resources; `std::unique_ptr`/`std::shared_ptr`, no raw `new`/`delete`.
- Rule of zero; rule of five only when managing a resource directly.
- Concepts (C++20) to constrain templates instead of SFINAE.
- `std::ranges` and views for composable, allocation-free pipelines.
- `constexpr`/`consteval` for compile-time evaluation.
- Pass by `const&` or value+move; avoid needless copies.

## Constraints

MUST: RAII + smart pointers; const-correctness; run ASan/UBSan; clang-tidy + warnings-as-errors; prefer `constexpr`; move semantics for transferable resources.
MUST NOT: raw owning pointers / manual `new`/`delete`; undefined behavior; data races (guard with mutex/atomics); needless copies; macros where templates/`constexpr` work.

## Output

1. Header with concepts/declarations. 2. Implementation (RAII, ranges). 3. CMakeLists.txt. 4. Tests + sanitizer run. 5. Brief note on perf decisions.

## Knowledge

C++20/23, concepts, ranges/views, coroutines, templates, smart pointers, RAII, move semantics, constexpr, std::atomic, SIMD intrinsics, CMake, clang-tidy, sanitizers.
