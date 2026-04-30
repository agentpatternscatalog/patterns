# Awareness

**Also known as:** Situational Awareness, Capability Self-Knowledge

**Category:** Memory  
**Status in practice:** emerging

## Intent

Maintain the agent's explicit knowledge of its own tools, capabilities, environment, and current context as queryable state.

## Context

Agents that operate over time and across capabilities need to know what they can do and where they are; without explicit awareness, capability is implicit in prompts.

## Problem

Agents that do not know their own capabilities either over-promise (hallucinate tools) or under-deliver (forget tools they have).

## Forces

- Awareness state grows with capability.
- Stale awareness misleads.
- Self-description is itself a prompt-engineering effort.

## Solution

Persist explicit state about: available tools (with descriptions), the environment (what host, what user, what permissions), the current task, and the agent's own identity. Refresh on capability changes. Inject relevant slices of awareness into each turn's context.

## Consequences

**Benefits**

- Reduces hallucinated tool calls.
- Grounds the agent in its own context.

**Liabilities**

- Awareness state is a maintenance burden.
- Excess awareness wastes context tokens.

## What this pattern constrains

Tool calls and self-references must match the awareness state; mismatches are flagged.

## Known uses

- **Sparrot world.md + personality.md** — *Available*
- **Avramovic Awareness pattern** — *Available*

## Related patterns

- *complements* → [tool-use](tool-use.md)
- *specialises* → [model-card](model-card.md)
- *complements* → [tool-discovery](tool-discovery.md)

## References

- (repo) *zeljkoavramovic/agentic-design-patterns*, <https://github.com/zeljkoavramovic.github.io/agentic-design-patterns/>

**Tags:** awareness, state, self-model
