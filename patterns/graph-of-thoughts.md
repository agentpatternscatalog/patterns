# Graph of Thoughts

**Also known as:** GoT, DAG Reasoning

**Category:** Reasoning  
**Status in practice:** experimental

## Intent

Model reasoning as an arbitrary DAG so thoughts can be merged, refined, and aggregated across branches.

## Context

Tasks with subproblems whose results combine non-trivially (sorting partial lists, set operations, summarisation merge); tree-shaped reasoning loses these aggregation opportunities.

## Problem

Tree of Thoughts cannot combine partial solutions or reuse intermediate results across sibling branches.

## Forces

- Richer reasoning topology vs orchestration complexity.
- Cross-branch reuse vs aggregation prompt cost.
- DAG expressiveness vs cycle-safety enforcement.


## Applicability

**Use when**

- Reasoning benefits from merging or refining partial solutions across branches.
- Intermediate thoughts can be reused or aggregated rather than discarded.
- Problems have a DAG-shaped structure rather than a single linear chain.

**Do not use when**

- A simple chain-of-thought or tree-of-thoughts already solves the task at lower cost.
- Operations to score, aggregate, or refine thoughts cannot be defined for the domain.
- Latency budgets cannot absorb multi-node graph traversal.

## Solution

Reasoning state is a DAG of thoughts. Operations include generate (CoT-style), aggregate (merge multiple thoughts), refine (improve one thought), and score. The orchestrator chains operations to produce a final thought; the agent can reuse intermediate nodes across branches.

## Variants

- **Generate-only GoT** — Only the generate operator is used, but multiple thoughts per node give a tree-like shape inside the DAG.
- **Aggregate-heavy GoT** — Aggregate operator merges sibling thoughts repeatedly, ideal for sort/merge or set-union style problems.
- **Refine-loop GoT** — A single thought is refined in a self-loop until a score plateau, with periodic aggregation against earlier versions.

## Consequences

**Benefits**

- Strict superset of CoT and ToT.
- Most useful when subproblems have non-tree dependencies.

**Liabilities**

- Orchestration overhead.
- Hard to debug when the DAG grows.

## What this pattern constrains

Thought operations must be composed via the named operators; ad-hoc reasoning outside the operator vocabulary is forbidden.

## Known uses

- **GoT paper benchmarks (sorting, set intersection, document merge)** — *Available*

## Related patterns

- *generalises* → [tree-of-thoughts](tree-of-thoughts.md)
- *complements* → [lats](lats.md)
- *composes-with* → [blackboard](blackboard.md)
- *complements* → [llm-compiler](llm-compiler.md)

## References

- (paper) Besta, Blach, Kubicek, Gerstenberger, Podstawski, Gianinazzi, Gajda, Lehmann, Niewiadomski, Nyczyk, Hoefler, *Graph of Thoughts: Solving Elaborate Problems with Large Language Models*, 2023, <https://arxiv.org/abs/2308.09687>

**Tags:** reasoning, graph, dag
