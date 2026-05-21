# Scratchpad

**Also known as:** Working Notes, Thinking Tool, Notepad

**Category:** Memory  
**Status in practice:** mature

## Intent

Give the agent a writable scratch space for intermediate notes that informs later turns but does not pollute the response.

## Context

An agent is working on a long task where it benefits from writing things down as it goes — intermediate computations, plans, lists of unresolved questions, candidate options it is considering. None of this scratch work is something the user should see; it is the agent's internal working surface, the equivalent of notes on a whiteboard.

## Problem

Without a dedicated scratchpad, the intermediate work has nowhere appropriate to live. Either it pollutes the user-visible response, so the user sees half-finished computations and the agent's running commentary, or it is held only in the conversation history and is lost the moment that history gets trimmed. Either way the agent loses the artifact that was supposed to support its own reasoning, and the user is forced to read through clutter that was never meant for them.

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

## Therefore

Therefore: give the agent a separate writable surface for intermediate notes that informs later turns but is not shown to the user, so that working notes can be messy without polluting the response.

## Solution

Provide a tool or convention for writing to a scratchpad (a section of the prompt, a tool call, a file). The agent reads from and writes to it across turns. The user-visible response is separate. The scratchpad is purged at task completion or expires with the session.

## Example scenario

A research agent that has to read ten papers and answer one question keeps repeating itself in the visible response because every intermediate note is also output to the user. The team adds a scratchpad tool: the agent writes intermediate notes to a private buffer it can reread on later turns; the user-visible response is composed at the end. Responses become tight while the agent's working memory stays rich.

## Diagram

```mermaid
flowchart TD
  T[Turn n] --> A[Agent]
  A -->|write notes| SP[(Scratchpad)]
  SP -->|read on| T2[Turn n+1]
  T2 --> A
  A --> Resp[User-visible response]
  Resp -.does not include.-> SP
  Done[Task done] -->|purge| SP
```

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
