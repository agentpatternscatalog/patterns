# MapReduce for Agents

**Also known as:** LLM×MapReduce, Divide-and-Conquer

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Split an oversize task into independent chunks, process each in parallel, then aggregate.

## Context

The input does not fit the model's context window or the task naturally decomposes (per-row, per-document, per-section).

## Problem

Long-context models still degrade with size; chunked processing without coordination loses cross-chunk dependencies.

## Forces

- Naive chunking loses dependencies that span chunks.
- Conflicts between chunk answers need a resolver.
- Aggregation must not become its own context-window problem.

## Solution

Map: split input into chunks; process each independently (per-chunk LLM call). Reduce: aggregate intermediate answers via a structured information protocol that surfaces dependencies, plus a confidence-calibration step to resolve conflicts.

## Consequences

**Benefits**

- Scales to inputs orders of magnitude larger than the context window.
- Embarrassingly parallel; latency scales with chunk count, not input size.

**Liabilities**

- Cross-chunk dependencies must be modelled explicitly.
- Reduce stage can become the new bottleneck.

## What this pattern constrains

Each Map step sees only its chunk; cross-chunk reasoning is forbidden until the Reduce stage.

## Known uses

- **LLM×MapReduce paper implementation** — *Available*

## Related patterns

- *specialises* → [parallelization](parallelization.md)
- *alternative-to* → [self-consistency](self-consistency.md) — Both aggregate multiple LLM outputs but differ in whether inputs are the same.
- *used-by* → [graphrag](graphrag.md)
- *composes-with* → [pipes-and-filters](pipes-and-filters.md)

## References

- (paper) Zhou, Li, Chen, Wang et al., *LLM×MapReduce: Simplified Long-Sequence Processing using Large Language Models*, 2024, <https://arxiv.org/abs/2410.09342>

**Tags:** mapreduce, long-context, parallel
