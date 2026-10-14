# Unbounded Subagent Spawn

**Also known as:** Recursive Spawn, Subagent Fan-Out Bomb

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: a supervisor or orchestrator spawns sub-agents that can themselves spawn sub-agents without a global cap.

## Context

A team is operating a multi-agent system that uses supervisor, orchestrator-workers, or lead-researcher style decomposition. At each level a parent agent breaks the task down and spawns child agents to handle the pieces, and those children can themselves spawn further sub-agents if their slice of the task is still too large. There is no global cap on how many agents the whole tree is allowed to contain or how deep the recursion can go.

## Problem

Per-agent safety mechanisms — step-budget caps the loop of a single agent, cost-gating caps the cost of a single action — do not constrain total system spend through fan-out. A buggy decomposition that always splits a task into too many pieces can recursively explode the agent tree, with each individual agent looking well-behaved while the whole system burns budget exponentially. Killing one instance does not kill its descendants, and detecting recursive spawn requires global tree state that is rarely tracked. The result is that a single bad decomposition prompt can run up costs that no per-agent limit ever sees.

## Forces

- Per-agent caps look like sufficient governance until fan-out is observed.
- Detecting recursive spawn requires global agent tree state.
- Killing a single instance does not kill its descendants.

## Therefore

Therefore: maintain one global step budget across all descendants of a root request, cap fan-out per supervisor at five to ten children, and thread a `parent_run_id` through every spawn so the entire agent tree is inspectable and killable as a whole, so that recursive decomposition cannot blow the cost ceiling beneath per-agent caps.

## Solution

Don't. Maintain a global step budget across all descendants of a root request. Cap fan-out per supervisor (typically 5-10 children). Track parent_run_id in lineage so the agent tree is inspectable. Pair with kill-switch for emergency descent halt.

## Structure

```
Anti-pattern: Root request -> supervisor spawns children -> children spawn children (no global cap) -> exponential spend. Corrected: Root request -> shared global step budget + per-supervisor fan-out cap + parent_run_id lineage -> kill-switch halts the whole tree.
```

## Diagram

```mermaid
flowchart TD
  Root[Root request] --> Sup[Supervisor]
  Sup --> A1[Sub-agent A]
  Sup --> A2[Sub-agent B]
  A1 --> A1a[Sub-sub-agent]
  A1 --> A1b[Sub-sub-agent]
  A2 --> A2a[Sub-sub-agent]
  A1a --> A1aX[Sub-sub-sub-agent ...]
  A1aX -.no global cap.-> Boom[Cost explosion]
  Sup -.fix.-> GB[Global step budget across descendants]
  GB --> FC[Cap fan-out per supervisor]
  FC --> Trk[Track parent_run_id for inspectability]
```

## Example scenario

A research orchestrator decomposes a topic into ten sub-topics, each spawning a sub-agent; each of those decomposes into ten more sub-agents, and there is no global cap. One run consumes the month's budget in fifteen minutes through fan-out alone, even though each individual loop has a step budget. The team adds a global step budget across all descendants of a root request, caps fan-out per supervisor (5-10 children), and tracks `parent_run_id` so the agent tree is inspectable and killable as a whole.

## Consequences

**Benefits**

- Short-term: letting any agent spawn helpers freely makes decomposition flexible and needs no shared tracking state.
- Naming it lets a team ask for a global budget and lineage tracking before any recursive spawning ships.

**Liabilities**

- Catastrophic cost spikes from runaway decomposition.
- Untracked descendants survive a top-level halt.
- Provider rate-limits cascade through the tree.

## Failure modes

- Recursive explosion — a bad decomposition prompt splits every task into many pieces, and each child does the same, so the tree grows exponentially.
- Orphaned descendants — the operator kills the top-level agent, but its grandchildren keep running and spending.
- Invisible spend — each agent stays inside its own step budget while the total across the tree runs far past any limit.
- Rate-limit cascade — the growing tree hits provider rate limits, and the failures spread to unrelated work.

## What this pattern constrains

Avoiding it imposes a global cap: descendants of a root request share one step budget; per-supervisor fan-out cannot exceed a small bound (typically 5-10 children), and every child records parent_run_id so the tree stays inspectable.

## Applicability

**Use when**

- Cite this entry when sub-agents can spawn sub-agents with no global budget.
- You are already here if one request can recursively explode into an agent tree nobody can enumerate.
- Enforce a shared step budget across descendants, cap fan-out per supervisor, and track parent_run_id (pair with kill-switch).

**Do not use when**

- Sub-agents may spawn further sub-agents.
- Total system cost across the agent tree is bounded by SLOs.
- A kill-switch is available for emergency descent halt.

## Components

- Recursive supervisor — each level spawns children that themselves spawn more children
- Per-agent caps — bound a single loop's spend but do nothing about tree-wide cost
- Missing global budget — would track total descendants of a root request across all levels
- Missing parent-run-id thread — leaves the agent tree unkillable and uninspectable as a whole

## Tools

- Supervisor spawn API — allows unbounded fan-out and recursion by default
- Tree-wide kill-switch — missing emergency control that would halt all descendants on one signal

## Evaluation metrics

- Agent-tree depth per root request — counts recursion levels; exponential growth fires the anti-pattern
- Total descendants spawned per root request — multiplies past per-agent caps when fan-out compounds
- Tree-wide cost per task — sum across all descendants, distinct from per-agent cost
- Orphaned-descendant count after top-level halt — descendants still running after the root was stopped

## Known uses

- **Observed in early multi-agent demos (AutoGPT-style 2023)** _available_

## Related patterns

- _alternative-to_ **Step Budget**
- _alternative-to_ **Cost Gating**
- _alternative-to_ **Kill Switch**
- _complements_ **Subagent Isolation**
- _conflicts-with_ **Clone Fan-Out Research**
- _complements_ **Cascading Agent Failures**
- _complements_ **Supervisor Cognitive Overload** — The more sub-agents spawned, the heavier the human supervision surface becomes.

## References

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic, 2024
