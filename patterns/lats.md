# Language Agent Tree Search

**Also known as:** LATS, MCTS for Agents, Tree-Search Agent, Backtracking Agent

**Category:** Planning & Control Flow  
**Status in practice:** experimental

## Intent

Lift the agent loop into a search tree with a learned value function and backtracking.

## Context

The task has multiple plausible reasoning paths and committing to the first one yields suboptimal answers.

## Problem

ReAct and Plan-and-Execute commit to a single chain; ambiguous problems benefit from exploring alternatives.

## Forces

- Search is expensive; the value function must be cheap.
- Branch ranking determines whether search beats greedy.
- Memory of failed branches must not leak into successful ones.


## Applicability

**Use when**

- Single-chain agent loops commit too early on ambiguous problems.
- A learned or heuristic value function can score partial trajectories.
- Backtracking from failing branches is worth the search overhead.

**Do not use when**

- ReAct or Plan-and-Execute already solves the task without search.
- No useful value function or step-level signal exists.
- Latency and token cost cannot absorb tree expansion and rollouts.

## Solution

Apply Monte Carlo Tree Search (MCTS) to the agent loop. Each node is a partial trajectory. Expansion samples next thoughts/actions. Backpropagation updates a value estimate. Selection chooses the next node by UCT. The agent can backtrack from a failing branch instead of committing.

## Consequences

**Benefits**

- Higher answer quality on hard / ambiguous tasks.
- Explicit exploration / exploitation trade-off.

**Liabilities**

- Token cost can be 5-10x ReAct.
- The value function is hard to train without supervision signals.

## What this pattern constrains

Each node may be expanded only by sampling actions consistent with the parent state.

## Known uses

- **Pure future for Stash2Go** — *Pure future*. Conversational answerer for ambiguous knitting questions ('can I substitute X for Y?').

## Related patterns

- *uses* → [react](react.md)
- *complements* → [self-consistency](self-consistency.md)
- *specialises* → [tree-of-thoughts](tree-of-thoughts.md) — LATS adds learned value function and MCTS-style search.
- *complements* → [exploration-exploitation](exploration-exploitation.md)
- *specialises* → [test-time-compute-scaling](test-time-compute-scaling.md)
- *complements* → [graph-of-thoughts](graph-of-thoughts.md)
- *complements* → [process-reward-model](process-reward-model.md)
- *complements* → [automatic-workflow-search](automatic-workflow-search.md)

## References

- (paper) Zhou, Yan, Shlapentokh-Rothman, Wang, Wang, *Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*, 2023, <https://arxiv.org/abs/2310.04406>

**Tags:** search, mcts, planning
