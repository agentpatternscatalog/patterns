# Inner Committee

**Also known as:** Multi-Persona Single Model, Self-as-Multiple-Roles

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Run one model under several distinct personas (executor, critic, planner) within a single agent loop.

## Context

The agent benefits from review or planning split off from execution, but spinning up genuine separate model instances is overkill.

## Problem

Mono-persona prompts conflate roles and produce muddled outputs that are neither plans nor critiques nor execution.

## Forces

- Persona switching costs a prompt and a context reset.
- The model has the same blind spots in each persona; true diversity is limited.
- Persona drift in long conversations dilutes the role separation.

## Applicability

**Use when**

- A single persona produces muddled outputs that are neither plan, critique, nor execution.
- Distinct personas (planner, executor, critic) can be defined with non-overlapping inputs.
- The agent loop can step through personas at fixed, deterministic points.

**Do not use when**

- Mono-persona prompts already produce clean role-separated outputs.
- Multiple model calls per step are not affordable.
- Personas would share so much context that role separation has no effect.

## Solution

Define explicit personas (system prompts) for each role: planner, executor, critic. The agent loop steps through personas at fixed points. Each persona sees only the inputs its role needs, not the full context of the others.

## Example scenario

A coding agent that handles refactor requests keeps producing patches that compile but miss the actual intent, because one prompt is being asked to plan, write, and self-critique in the same breath. The team rebuilds it as an inner-committee: the same model is invoked as Planner (sees the request and codebase summary), Executor (sees only the plan and writes the diff), and Critic (sees only the diff and the acceptance criteria). The personas run in fixed order and each sees only what its role needs.

## Diagram

```mermaid
sequenceDiagram
  participant L as Loop
  participant Pl as Planner persona
  participant Ex as Executor persona
  participant Cr as Critic persona
  L->>Pl: produce plan
  Pl-->>L: plan
  L->>Ex: execute step
  Ex-->>L: result
  L->>Cr: review
  Cr-->>L: critique
  L->>Pl: revise plan if needed
```

## Consequences

**Benefits**

- Cheaper than running multiple model instances.
- Surprisingly effective for self-critique and self-modification gating.

**Liabilities**

- Same model means correlated errors; reflexion suffers from this.
- Persona prompts add up to a non-trivial token budget.

## What this pattern constrains

Each persona may only act within its declared role; cross-persona reasoning is forbidden in a single prompt.

## Known uses

- **Long-running personal agent loops (private deployment)** — *Available*

## Related patterns

- *specialises* → [inner-critic](inner-critic.md)
- *alternative-to* → [debate](debate.md)
- *alternative-to* → [role-assignment](role-assignment.md)

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** multi-persona, single-model
