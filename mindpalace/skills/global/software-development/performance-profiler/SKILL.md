---
name: Performance Profiler
description: Use when investigating a slow endpoint, planning a performance budget, or hunting a memory leak in Node.js/Python/Go — CPU/memory/IO profiling, flamegraphs, bundle analysis, query optimization, load tests. Always measures before and after.
tags: [performance, profiling, flamegraph, memory-leak, bundle-size, load-test, k6, n+1, py-spy, pprof]
source: alirezarezvani/claude-skills
derived_from: performance-profiler
---

# Performance Profiler

Systematic performance profiling for Node.js, Python, and Go. Identify CPU/memory/IO bottlenecks, generate flamegraphs, analyze bundles, optimize queries, detect leaks, run load tests with k6/Artillery. Always measure before and after.

## Golden rule: measure first
Establish a baseline BEFORE any optimization — record P50/P95/P99 latency, RPS, error rate, memory. Wrong: "I think the N+1 is slow, let me fix it." Right: profile → confirm bottleneck → fix → measure again → verify improvement.

## When to use
App is slow and bottleneck unknown · P99 exceeds SLA before release · memory grows over time (suspected leak) · bundle size grew after adding deps · preparing for a traffic spike · DB queries >100ms.

## Capabilities
- **CPU profiling**: flamegraphs for Node, py-spy for Python, pprof for Go.
- **Memory**: heap snapshots, leak detection, GC pressure.
- **Bundle analysis**: webpack-bundle-analyzer, Next.js bundle analyzer.
- **Database**: EXPLAIN ANALYZE, slow query log, N+1 detection.
- **Load testing**: k6 scripts, Artillery scenarios, ramp-up patterns.
- **Before/after**: baseline → profile → optimize → verify.

## Project risk scan
Run a static analyzer over the project for performance risk indicators (large files, configurable threshold); JSON output for CI integration. Then drill into the flagged areas with the language-specific profilers above.

## Optimization quick wins
DB (indexes, batch queries, avoid N+1), Node (avoid sync I/O, await correctly), bundle (code splitting, tree-shaking, drop heavy deps), API (caching, pagination). Verify every change against the recorded baseline.
