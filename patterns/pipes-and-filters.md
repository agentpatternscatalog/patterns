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


## Applicability

**Use when**

- A transformation can be decomposed into small filters with single responsibilities.
- Filters benefit from being individually testable and reusable across pipelines.
- Typed pipes (call, queue, stream) connect filters cleanly.

**Do not use when**

- The transformation is small enough that a single function is clearer.
- Filter boundaries would be artificial and add plumbing without payoff.
- Strong cross-stage state coupling defeats the filter abstraction.

## Solution

Decompose the transformation into small filters with single responsibilities. Connect them via typed pipes (function call, queue, stream). Each filter is testable in isolation. Filters can be reused across pipelines.

## Example scenario

A document-processing agent has grown into a 1500-line monolith that does PDF extraction, OCR cleanup, language detection, chunking, and embedding all in one function — and is impossible to test in isolation. The team rebuilds it as pipes-and-filters: each stage becomes a small filter with a single responsibility, connected by typed pipes. The OCR-cleanup filter can now be tested against a fixture in isolation, the chunking filter is reused by another product, and a new language-detection filter is dropped in without touching the others.

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
