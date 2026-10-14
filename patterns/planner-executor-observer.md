# Planner-Executor-Observer

**Also known as:** Three-Role Loop, POE

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Add an explicit Observer role between Planner and Executor so progress is checked against the plan instead of trusted blindly.

## Context

A team runs a Plan-and-Execute agent: a planner emits an ordered plan once and an executor walks the steps. The executor's work needs to be checked against the original intent — does the cumulative output still match what the planner asked for, or has the executor wandered onto an adjacent topic? The team is willing to spend a small amount of supervision overhead to catch drift early instead of paying for an entire bad run.

## Problem

Two existing shapes both fail this requirement. Letting the executor run blind means the planner only finds out at the end whether the run was on-track, at which point fixing it requires starting over. Reporting back to the planner after every step rebuilds the ReAct loop and reintroduces the per-step planner cost the team adopted Plan-and-Execute to avoid. There is no clean place for a cheap, focused check that reads the executor's cumulative output against the plan and decides whether to keep going, stop, or replan.

## Forces

- Observation must be cheap or it negates the plan-execute speedup.
- Triggering replans too eagerly thrashes; too lazily wastes effort.
- The Observer needs visibility into plan and tool results both.

## Therefore

Therefore: insert a third Observer role that reads cumulative execution against the plan and is the only one allowed to call loop, respond, or replan, so that mid-run drift is caught early without rebuilding ReAct's monolithic step.

## Solution

Three roles: Planner produces a plan; Executor runs steps; Observer reads the cumulative result and decides loop / respond / replan. Each role has its own prompt and (optionally) its own model.

## Structure

```
Goal --> Planner --plan--> Executor --step result--> Observer --loop--> Executor. Observer --replan--> Planner. Observer --respond--> Final answer
```

## Diagram

```mermaid
flowchart TD
  G[Goal] --> P[Planner]
  P -->|plan| E[Executor]
  E -->|step result| O[Observer]
  O -->|loop| E
  O -->|replan| P
  O -->|respond| R[Final answer]
```

## Example scenario

A research agent that uses a Planner and Executor loop produces fluent reports that quietly drift from the plan: the executor swaps in adjacent topics and the planner never notices because no one is checking. The team adds an Observer role: after each executor step the observer reads the cumulative output against the plan and emits loop, respond, or replan. When the executor wanders into 'related-but-off-plan' territory the observer triggers a replan instead of letting the drift compound.

## Consequences

**Benefits**

- Catches plan failure earlier than end-of-run.
- Cleaner separation of concerns than ReAct's monolithic step.

**Liabilities**

- Three coordinated prompts to maintain.
- Latency adds up if Observer runs every step.

## Failure modes

- Lenient observer — the observer reads the cumulative result as on track when it is not, and the run finishes with a wrong answer.
- Executor self-stop — the executor quits or replans on its own, bypassing the observer and the plan check.
- Per-step latency — the observer runs after every step, and the loop becomes as slow as the ReAct loop it replaced.
- Prompt drift — one of the three role prompts is updated and the others are not, so the observer judges against a plan format the planner no longer emits.

## What this pattern constrains

The Executor cannot decide to stop or replan; only the Observer can.

## Applicability

**Use when**

- Plan quality must be checked against execution evidence rather than trusted blindly.
- Three roles (planner, executor, observer) can be defined with their own prompts.
- Observer signals (loop, respond, replan) drive the agent's next move.

**Do not use when**

- The task is short enough that planner-executor without supervision suffices.
- Observer cost dominates and there is no payoff in catching mid-run drift.
- Roles cannot be cleanly separated without overlapping prompts.

## Components

- Planner — emits an ordered plan once from the goal
- Executor — walks plan steps and accumulates results
- Observer — reads cumulative output against the plan and decides next action
- Decision channel — loop, respond, or replan signal emitted by the observer
- Replan path — return to the planner when the observer triggers it

## Tools

- LLM API — usually three roles, each potentially backed by a different model
- Tool catalogue — what the executor calls per step
- Plan-and-result store — observer reads cumulative state from here

## Evaluation metrics

- Drift-catch latency — turns between off-plan execution and observer signalling replan
- Observer overhead — observer tokens as fraction of total run cost
- Replan-trigger precision — fraction of observer replans that were actually warranted
- False respond rate — observer declaring done when the plan was not satisfied
- End-to-end success vs unsupervised plan-and-execute — quality lift from the third role

## Known uses

- **Bobbin (Stash2Go)** _available_ — planner / screen_executor / observe with route_after_observe edge.

## Related patterns

- _specialises_ **Plan-and-Execute**
- _composes-with_ **Evaluator-Optimizer**
- _alternative-to_ **ReAct**
- _used-by_ **Replan on Failure**
- _generalises_ **Outer-Inner Agent Loop**
- _alternative-to_ **Planner-Generator-Evaluator Harness**
- _alternative-to_ **Planner-Executor-Verifier (PEV)**

## References

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Yao et al., 2022
