# Pipes and Filters

**Also known as:** Pipeline, Streaming Pipeline, EIP Pipeline

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Compose stream-shaped processing as a chain of small filters connected by pipes.

## Context

Data flows through several transformations (parse, classify, transform, validate, format); each transformation is independently testable.

## Problem

Monolithic transformations are hard to test; bespoke pipelines reinvent connection plumbing each time.

## Forces

- Filter granularity: too small = overhead; too big = back to monolith.
- Pipe contracts (typed messages) need agreement.
- Backpressure across pipes.

## Solution

Decompose the transformation into small filters with single responsibilities. Connect them via typed pipes (function call, queue, stream). Each filter is testable in isolation. Filters can be reused across pipelines.

## Consequences

**Benefits**

- Composability and testability.
- Reuse across pipelines.

**Liabilities**

- Pipeline visibility: hard to see end-to-end behaviour.
- Latency adds across stages.

## What this pattern constrains

Filters communicate only through pipes with typed contracts.

## Known uses

- **Enterprise Integration Patterns (Hohpe, Woolf)** — *Available*
- **LangChain Runnable composition** — *Available*

## Related patterns

- *generalises* → [prompt-chaining](prompt-chaining.md)
- *composes-with* → [map-reduce](map-reduce.md)
- *used-by* → [chat-chain](chat-chain.md)

## References

- (book) Gregor Hohpe, Bobby Woolf, *Enterprise Integration Patterns*, 2003

**Tags:** pipeline, composition, eip
