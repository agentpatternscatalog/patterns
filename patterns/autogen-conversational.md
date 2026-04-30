# Conversational Multi-Agent

**Also known as:** AutoGen Conversation, Two-Agent Conversation

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Have agents converse turn by turn until a completion criterion fires; agent roles drive the conversation forward.

## Context

Tasks that benefit from back-and-forth between specialists (a coder agent and a reviewer agent; a teacher agent and a student agent).

## Problem

Single-agent loops cannot represent dialogue-shaped collaboration; rigid orchestration patterns over-prescribe the flow.

## Forces

- Turn allocation across agents.
- Termination criterion definition.
- Conversation can drift without supervision.

## Solution

Define agents with system prompts and allowed actions. Implement a conversation manager that selects which agent speaks next (round-robin, condition-based, model-decided). Each agent reads the conversation and emits a turn. Continue until termination criterion (task complete, max turns, explicit handoff to user).

## Consequences

**Benefits**

- Natural way to model peer collaboration.
- Each agent has a clean role definition.

**Liabilities**

- Conversation drift is real.
- Hard to reason about correctness of the multi-agent flow.

## What this pattern constrains

Each agent's outputs must conform to its role's allowed action set; agents may not act outside their role's vocabulary.

## Known uses

- **[Microsoft AutoGen](https://microsoft.github.io/autogen/)** — *Available*

## Related patterns

- *complements* → [role-assignment](role-assignment.md)
- *alternative-to* → [supervisor](supervisor.md)
- *alternative-to* → [camel-role-playing](camel-role-playing.md)

## References

- (paper) Wu, Bansal, Zhang, Wu, Zhang, Zhu, Li, Jiang, Zhang, Wang, *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*, 2023, <https://arxiv.org/abs/2308.08155>

**Tags:** multi-agent, conversation, autogen
