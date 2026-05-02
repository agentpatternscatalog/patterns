# Scratchpad

**Also known as:** Working Notes, Thinking Tool, Notepad

**Category:** Memory  
**Status in practice:** mature

## Intent

Give the agent a writable scratch space for intermediate notes that informs later turns but does not pollute the response.

## Context

Long tasks where the agent benefits from writing things down (computations, plans, lists of unresolved questions) without showing the user.

## Problem

Without a scratchpad, intermediate work pollutes the response or is lost between turns.

## Forces

- Scratchpad content adds tokens to subsequent turns.
- What stays in the scratchpad vs the response is a UX choice.
- Scratchpad content can leak via traces.


## Applicability

**Use when**

- Long tasks benefit from intermediate notes that should not appear in user output.
- The agent needs to carry computations or unresolved questions across turns.
- A separate writable space (tool, file, prompt section) can be added.

**Do not use when**

- Tasks are short and intermediate state fits in one inference.
- Mixing intermediate notes with output would not actually pollute UX.
- The scratchpad would never be purged and would grow unbounded.

## Solution

Provide a tool or convention for writing to a scratchpad (a section of the prompt, a tool call, a file). The agent reads from and writes to it across turns. The user-visible response is separate. The scratchpad is purged at task completion or expires with the session.

## Consequences

**Benefits**

- Intermediate work persists without cluttering output.
- Useful for chain-of-thought style reasoning that should not be visible.

**Liabilities**

- Token cost grows with scratchpad size.
- Scratchpad becomes shadow state if not purged.

## What this pattern constrains

Scratchpad contents are visible only to the agent loop; user-facing output draws from the response slot.

## Known uses

- **OpenAI o1-style internal reasoning** — *Available*
- **Anthropic <thinking> blocks** — *Available*

## Related patterns

- *complements* → [short-term-memory](short-term-memory.md)
- *uses* → [chain-of-thought](chain-of-thought.md)
- *complements* → [extended-thinking](extended-thinking.md)
- *generalises* → [todo-list-driven-agent](todo-list-driven-agent.md)
- *alternative-to* → [preoccupation-tracking](preoccupation-tracking.md)

## References

- (paper) Nye et al., *Show Your Work: Scratchpads for Intermediate Computation with Language Models*, 2021, <https://arxiv.org/abs/2112.00114>

**Tags:** memory, scratchpad, thinking
