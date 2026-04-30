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

## Solution

Define explicit personas (system prompts) for each role: planner, executor, critic. The agent loop steps through personas at fixed points. Each persona sees only the inputs its role needs, not the full context of the others.

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

- **Sparrot** — *Available*. Executor + critic + planner; one model worn three ways.

## Related patterns

- *specialises* → [inner-critic](inner-critic.md)
- *alternative-to* → [debate](debate.md)
- *alternative-to* → [role-assignment](role-assignment.md)

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** multi-persona, single-model
