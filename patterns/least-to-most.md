# Least-to-Most Prompting

**Also known as:** L2M, Easy-First Decomposition

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Decompose a hard problem into an ordered list of easier subproblems, then solve them sequentially with each answer feeding the next.

## Context

Tasks with poor length or complexity generalisation: the model handles the easy training-style cases but fails on harder, longer instances.

## Problem

CoT generalises poorly out of distribution; the model needs explicit scaffolding for harder instances.

## Forces

- Decomposition prompts are themselves a design problem.
- Two stages double minimum cost.
- Errors in the decomposition cascade.

## Solution

Two-stage prompt. Stage 1 (decomposition): prompt the model to list subproblems from easiest to hardest. Stage 2 (sequential solve): for each subproblem in order, prompt the model with the original question, prior subproblem answers, and the current subproblem.

## Consequences

**Benefits**

- Strong length and complexity generalisation.
- Subproblem answers are inspectable.

**Liabilities**

- Decomposition prompt design is task-specific.
- Two-stage pipeline; ambiguity in stage 1 propagates.

## What this pattern constrains

Subproblems must be solved in the listed order; out-of-order solving is forbidden.

## Known uses

- **L2M paper benchmarks (last letter, SCAN, math)** — *Available*

## Related patterns

- *alternative-to* → [chain-of-thought](chain-of-thought.md)
- *complements* → [self-ask](self-ask.md)
- *complements* → [plan-and-execute](plan-and-execute.md)
- *alternative-to* → [goal-decomposition](goal-decomposition.md)

## References

- (paper) Zhou, Schärli, Hou, Wei, Scales, Wang, Schuurmans, Cui, Bousquet, Le, Chi, *Least-to-Most Prompting Enables Complex Reasoning in Large Language Models*, 2022, <https://arxiv.org/abs/2205.10625>

**Tags:** reasoning, decomposition
