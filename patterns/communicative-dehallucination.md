# Communicative Dehallucination

**Also known as:** Instructor-Reversal Clarification, Inter-Agent Clarifying Question

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

When an instructed agent would have to invent missing context to comply, have it reverse roles and ask the instructor for the missing detail before answering.

## Context

Two agents communicate (instructor → assistant) and the instruction is under-specified in a way that would force the assistant to fabricate (e.g. a missing class name, an unspecified API version, an ambiguous unit).

## Problem

Without a clarification channel between agents, the assistant fabricates the missing detail; the fabrication propagates and is hard to detect at the artefact boundary.

## Forces

- Speed of completion vs. fidelity of context.
- Adding a clarification round costs latency and tokens.
- Asking too eagerly degrades into chatter; not asking at all produces hallucinated outputs.

## Solution

Define an explicit role-reversal protocol: when the assistant detects that the instruction is missing a deciding piece of context, it pivots and emits a focused question back to the instructor ("the precise name of the dependency, please"). The instructor answers, and only then does the assistant produce its conclusion. Bound the depth (one or two reversals) to prevent infinite ping-pong.

## Structure

```
Instructor -> instruction -> Assistant; if context_gap_detected: Assistant -> question -> Instructor -> answer -> Assistant -> conclusion.
```

## Consequences

**Benefits**

- Targets the specific dehallucination point instead of after-the-fact verification.
- Cheaper than full multi-agent debate; the question is scoped.
- Produces a more faithful artefact at the next hand-off.

**Liabilities**

- Adds latency for every clarification round.
- Detecting the gap is itself a model judgement and can fail.
- Risk of infinite ping-pong without a depth bound.

## What this pattern constrains

The assistant may not produce a final answer when a designated context slot is unfilled; it must instead emit a clarifying question.

## Known uses

- **[ChatDev](https://github.com/OpenBMB/ChatDev)** — *Available*. Original demonstration; assistant reverses to instructor role to request missing detail before delivering a conclusive response.

## Related patterns

- *specialises* → [disambiguation](disambiguation.md) — Same shape, but agent-to-agent rather than agent-to-user.
- *alternative-to* → [human-in-the-loop](human-in-the-loop.md)
- *alternative-to* → [debate](debate.md)
- *conflicts-with* → [infinite-debate](infinite-debate.md) — Requires a depth bound to avoid this anti-pattern.
- *uses* → [inter-agent-communication](inter-agent-communication.md)

## References

- (paper) Qian et al., *ChatDev: Communicative Agents for Software Development*, 2023, <https://arxiv.org/abs/2307.07924>

**Tags:** multi-agent, verification, china-origin, chatdev
