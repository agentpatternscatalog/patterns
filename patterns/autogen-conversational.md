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

## Example scenario

A finance team wants an agent that drafts an internal memo, has a 'reviewer' poke holes in it, and revises until the reviewer signs off. A linear pipeline can't represent the back-and-forth, and a free-form group chat is too loose. They use an AutoGen-style conversational setup: a writer agent and a reviewer agent take turns until the reviewer emits an explicit approval token. Each turn drives the next; the loop ends when the role-defined criterion fires.

## Consequences

**Benefits**

- Natural way to model peer collaboration.
- Each agent has a clean role definition.

**Liabilities**

- Conversation drift is real.
- Hard to reason about correctness of the multi-agent flow.

## What this pattern constrains

Each agent's outputs must conform to its role's allowed action set; agents may not act outside their role's vocabulary.

## Applicability

**Use when**

- The task naturally maps to dialogue between roles (e.g. user-proxy and assistant, planner and executor).
- A conversation manager can pick the next speaker by rule, condition, or model decision.
- Termination criteria (task complete, max turns, explicit handoff) are easy to express.

**Do not use when**

- A single-agent loop already captures the work without dialogue overhead.
- Strict orchestration (fixed step order) is required and conversational drift is unacceptable.
- Termination is hard to detect, risking runaway turn counts.

## Known uses

- **[Microsoft AutoGen](https://microsoft.github.io/autogen/)** — *Available*

## Related patterns

- *complements* → [role-assignment](role-assignment.md)
- *alternative-to* → [supervisor](supervisor.md)
- *alternative-to* → [camel-role-playing](camel-role-playing.md)

## References

- (paper) Wu, Bansal, Zhang, Wu, Zhang, Zhu, Li, Jiang, Zhang, Wang, *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*, 2023, <https://arxiv.org/abs/2308.08155>

**Tags:** multi-agent, conversation, autogen
