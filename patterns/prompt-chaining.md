# Prompt Chaining

**Also known as:** Sequential Decomposition, Pipeline of Prompts

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Decompose a task into a fixed sequence of LLM calls where each step's output becomes the next step's input.

## Context

The task is composed of identifiable sub-tasks with clear boundaries; the order is known in advance.

## Problem

A single mega-prompt overloads the model and makes failures hard to localise.

## Forces

- Decomposition clarity vs compounded latency.
- Step isolation vs error compounding across the chain.
- Schema rigor between steps vs pipeline flexibility.

## Solution

Define a fixed pipeline of prompts. Each step has its own system prompt, expected output shape, and validation. A failure at step k retries step k or aborts; downstream steps run only on success.

## Consequences

**Benefits**

- Failures localise to a step.
- Each step's prompt can be optimised independently.

**Liabilities**

- Inflexible to inputs that do not match the assumed decomposition.
- Latency = sum of step latencies.

## What this pattern constrains

Step k cannot bypass step k-1's output schema.

## Known uses

- **Anthropic Building Effective Agents (Workflow #1)** — *Available*

## Related patterns

- *complements* → [routing](routing.md)
- *alternative-to* → [parallelization](parallelization.md)
- *specialises* → [pipes-and-filters](pipes-and-filters.md)
- *specialises* → [chat-chain](chat-chain.md)

## References

- (blog) *Anthropic: Building Effective Agents*, 2024, <https://www.anthropic.com/research/building-effective-agents>

**Tags:** pipeline, workflow, decomposition
