# Planner-Executor-Observer

**Also known as:** Three-Role Loop, POE

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Add an explicit Observer role between Planner and Executor so progress is checked against the plan instead of trusted blindly.

## Context

Plan-and-Execute systems either let the executor run blind (planner finds out at the end) or report at every step (rebuilding ReAct with extra coordination overhead).

## Problem

The missing third role is supervision of execution against intent; without it, plan quality is invisible until the run completes.

## Forces

- Observation must be cheap or it negates the plan-execute speedup.
- Triggering replans too eagerly thrashes; too lazily wastes effort.
- The Observer needs visibility into plan and tool results both.


## Applicability

**Use when**

- Plan quality must be checked against execution evidence rather than trusted blindly.
- Three roles (planner, executor, observer) can be defined with their own prompts.
- Observer signals (loop, respond, replan) drive the agent's next move.

**Do not use when**

- The task is short enough that planner-executor without supervision suffices.
- Observer cost dominates and there is no payoff in catching mid-run drift.
- Roles cannot be cleanly separated without overlapping prompts.

## Solution

Three roles: Planner produces a plan; Executor runs steps; Observer reads the cumulative result and decides loop / respond / replan. Each role has its own prompt and (optionally) its own model.

## Consequences

**Benefits**

- Catches plan failure earlier than end-of-run.
- Cleaner separation of concerns than ReAct's monolithic step.

**Liabilities**

- Three coordinated prompts to maintain.
- Latency adds up if Observer runs every step.

## What this pattern constrains

The Executor cannot decide to stop or replan; only the Observer can.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. planner / screen_executor / observe with route_after_observe edge.

## Related patterns

- *specialises* → [plan-and-execute](plan-and-execute.md)
- *composes-with* → [evaluator-optimizer](evaluator-optimizer.md)
- *alternative-to* → [react](react.md)
- *used-by* → [replan-on-failure](replan-on-failure.md)
- *generalises* → [outer-inner-agent-loop](outer-inner-agent-loop.md)

## References

- (blog) *Marco Nissen, Working with the models (Code Different #14)*, 2026

**Tags:** planning, three-role
