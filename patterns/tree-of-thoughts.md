# Tree of Thoughts

**Also known as:** ToT, Deliberate Reasoning

**Category:** Reasoning  
**Status in practice:** emerging

## Intent

Search over a tree of partial reasoning states with explicit lookahead, evaluation, and backtracking.

## Context

The problem benefits from exploring alternatives (puzzles, planning, creative writing) and committing to a single chain leads to dead ends.

## Problem

Chain-of-Thought commits to a single trace; if an early step is wrong the model cannot recover or compare alternatives.

## Forces

- Search costs many model calls per problem.
- A value or heuristic function is needed to score partial states.
- Termination criteria are non-trivial.


## Applicability

**Use when**

- Problems benefit from exploring alternatives rather than committing to one chain (puzzles, planning, creative writing).
- Each thought step can be evaluated by the model or a programmatic check.
- Compute budget allows BFS, DFS, or beam search over thought nodes.

**Do not use when**

- Single-chain reasoning already reaches the answer reliably.
- Step evaluation is unreliable and search would explore noise.
- Latency or cost of search is unacceptable.

## Solution

Decompose the problem into thought steps. At each node, sample several candidate next thoughts. Evaluate each (model self-evaluation or programmatic check). Apply BFS/DFS/beam to explore the tree. Backtrack from dead ends. Return the best leaf.

## Variants

- **BFS Tree of Thoughts** — Expand all nodes at depth d before moving to d+1; suits short, evaluable thought steps.
- **DFS Tree of Thoughts** — Go deep first and backtrack on dead ends; suits long horizons with cheap pruning.
- **Beam-search ToT** — Keep only the top-k highest-scoring partial paths at each depth; bounded cost.

## Consequences

**Benefits**

- Higher accuracy on tasks where alternatives matter (Game of 24, crosswords, creative writing planning).
- Explicit search vocabulary (lookahead, prune, backtrack).

**Liabilities**

- 5-100x cost over CoT depending on branching factor and depth.
- Value function quality bounds search benefit.

## What this pattern constrains

The agent may only commit to a final answer after exploring at least one full path; search depth and branching are bounded by configuration.

## Known uses

- **ToT paper benchmarks (Game of 24, crosswords, creative writing)** — *Available*
- **LangChain ToT integration** — *Available*

## Related patterns

- *specialises* → [chain-of-thought](chain-of-thought.md)
- *specialises* → [graph-of-thoughts](graph-of-thoughts.md)
- *generalises* → [lats](lats.md)

## References

- (paper) Yao, Yu, Zhao, Shafran, Griffiths, Cao, Narasimhan, *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*, 2023, <https://arxiv.org/abs/2305.10601>

**Tags:** reasoning, search, tree
