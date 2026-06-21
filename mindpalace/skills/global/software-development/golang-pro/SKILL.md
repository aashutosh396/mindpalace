---
name: golang-pro
description: "Use when building Go 1.21+ applications with concurrent goroutine/channel patterns, gRPC or REST microservices, generics, or high-performance systems. Triggers: Go, Golang, goroutines, channels, gRPC, microservices Go, Go generics, concurrent programming, Go interfaces, pprof."
version: 1.0.0
license: MIT
tags: [go, golang, goroutines, channels, grpc, generics, microservices, pprof]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/golang-pro
derived_from: awesomeclaude
---

# Golang Pro

Idiomatic Go 1.21+, concurrency, and cloud-native microservices.

## When to use

Concurrent programming (goroutines/channels); gRPC or REST microservices; generics; interface-driven design; pprof performance work; CLI tools; benchmarks/fuzzing.

## Core workflow

1. **Analyze** — module structure, interfaces, concurrency patterns.
2. **Design interfaces** — small, focused, composed.
3. **Implement** — idiomatic Go, error handling, context propagation; `go vet ./...`.
4. **Lint** — `golangci-lint run`, fix all.
5. **Optimize** — pprof, benchmarks, fewer allocations.
6. **Test** — table-driven with `-race`, fuzzing, 80%+ coverage.

## Key pattern

```go
// Bounded goroutine with context cancellation + error propagation
func worker(ctx context.Context, jobs <-chan Job, errCh chan<- error) {
    for {
        select {
        case <-ctx.Done():
            errCh <- fmt.Errorf("worker cancelled: %w", ctx.Err()); return
        case job, ok := <-jobs:
            if !ok { return } // channel closed; clean exit
            if err := process(ctx, job); err != nil {
                errCh <- fmt.Errorf("process %v: %w", job.ID, err); return
            }
        }
    }
}
```

Properties: bounded lifetime via ctx, `%w` error wrapping, no goroutine leak on cancel.

## Constraints

MUST: gofmt + golangci-lint; context.Context on blocking ops; handle all errors explicitly; table-driven tests with subtests; doc all exported symbols; wrap errors with `%w`; run `-race`.
MUST NOT: ignore errors (`_` without reason); panic for normal errors; spawn goroutines without lifecycle; skip context cancellation; reflection without justification; hardcode config (use functional options/env).

## Output

1. Interface definitions (contracts first). 2. Implementation with package structure. 3. Table-driven tests. 4. Brief note on concurrency patterns.

## Knowledge

Go 1.21+, goroutines, channels, select, sync, generics/constraints, io.Reader/Writer, gRPC, context, error wrapping, pprof, benchmarks, fuzzing, go.mod, internal packages, functional options.
