# Parallelization

**Also known as:** Sectioning, Voting, Parallel Branches

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Run independent LLM calls concurrently and combine results.

## Context

The task naturally splits (sectioning) or benefits from multiple independent attempts (voting).

## Problem

Sequential execution of independent work wastes wall-clock time; single-attempt execution misses outliers a second look would catch.

## Forces

- Concurrency limits and rate limits.
- Aggregation logic for voting (majority? best? union?).
- Cost multiplies linearly with parallel branches.

## Solution

Two flavours. Sectioning: split a task into independent subtasks, run them concurrently, concatenate results. Voting: run the same task multiple times, aggregate by majority or judge.

## Consequences

**Benefits**

- Wall-clock latency drops; quality rises (voting).
- Independent failures isolate cleanly.

**Liabilities**

- Cost scales with branch count.
- Aggregation logic is its own correctness problem.

## What this pattern constrains

Branches cannot share state during execution; aggregation is the only join point.

## Known uses

- **Anthropic Building Effective Agents (Workflow #3)** — *Available*
- **Self-consistency in mathematical reasoning** — *Available*

## Related patterns

- *generalises* → [self-consistency](self-consistency.md)
- *generalises* → [map-reduce](map-reduce.md)
- *generalises* → [best-of-n](best-of-n.md)
- *used-by* → [llm-compiler](llm-compiler.md)
- *generalises* → [parallel-tool-calls](parallel-tool-calls.md)
- *alternative-to* → [prompt-chaining](prompt-chaining.md)
- *used-by* → [lead-researcher](lead-researcher.md)

## References

- (blog) *Anthropic: Building Effective Agents*, 2024, <https://www.anthropic.com/research/building-effective-agents>

**Tags:** parallel, voting, concurrency
