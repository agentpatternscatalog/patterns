# LLMCompiler

**Also known as:** LLM Compiler, Parallel ReWOO

**Category:** Planning & Control Flow  
**Status in practice:** experimental

## Intent

Take ReWOO's plan-as-DAG and run independent steps in parallel through a task-fetching dispatcher.

## Context

Sequential ReWOO leaves parallelism on the table when steps have no mutual dependency.

## Problem

Latency-sensitive agents waiting on tools sequentially are slower than they need to be.

## Forces

- Concurrency control: limits per provider, rate limits, fan-out costs.
- Failure isolation: one branch failing should not kill others.
- Joiner correctness: combining out-of-order results.

## Solution

Three roles. Planner builds the dependency DAG. Task-Fetching Unit dispatches steps as their inputs become available, with bounded concurrency. Joiner assembles the final answer from the resolved DAG.

## Consequences

**Benefits**

- End-to-end latency drops to the longest dependency chain.
- Cost remains roughly the same as ReWOO.

**Liabilities**

- Concurrency adds operational complexity.
- Planner mistakes are amplified by parallel execution.

## What this pattern constrains

Steps run only when all referenced upstream variables are resolved.

## Known uses

- **Pure future for Bobbin** — *Pure future*. Agent-lane plans with two unrelated tools could run concurrently.

## Related patterns

- *specialises* → [rewoo](rewoo.md)
- *uses* → [parallelization](parallelization.md)
- *alternative-to* → [parallel-tool-calls](parallel-tool-calls.md)
- *composes-with* → [subagent-isolation](subagent-isolation.md)
- *complements* → [graph-of-thoughts](graph-of-thoughts.md)

## References

- (paper) Kim, Moon, Tabrizi, Lee, Mahoney, Keutzer, Gholami, *An LLM Compiler for Parallel Function Calling*, 2023, <https://arxiv.org/abs/2312.04511>

**Tags:** planning, parallel, dag
