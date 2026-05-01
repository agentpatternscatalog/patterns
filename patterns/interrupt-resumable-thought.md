# Interrupt-Resumable Thought

**Also known as:** Pausable Thought Stream, Continuation-Preserving Interrupt, Suspendable Cognition

**Category:** Planning & Control Flow
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Allow the agent to pause an in-flight reasoning chain when an external interrupt arrives, handle the interrupt, and resume the original chain instead of dropping it.

## Context

Long-running cognitive agents whose thinking spans multiple turns or ticks, where external messages (user input, system notifications, scheduled notes) can arrive mid-thought. Without explicit continuation support, every interrupt clobbers in-flight work.

## Problem

Coherent multi-step thinking that takes longer than a single turn is fragile. A new user message during step 3 of a 6-step thought either gets ignored (rude) or replaces the thought entirely (lossy). The agent has no notion of 'hold this, handle that, then come back', so longer reasoning fragments into shards.

## Forces

- Latency: humans expect quick acknowledgement of new input.
- Context capacity: holding a paused thought costs tokens.
- Resume reliability: returning to a paused thought without distortion is hard.
- Priority: not every interrupt deserves to suspend work; some are themselves interruptable.

## Solution

Introduce an explicit thought-frame: when starting a multi-step chain, push a frame onto a stack with the goal, the steps completed, and the next step. On interrupt: acknowledge briefly ('hold on — finishing X first' or 'switching: Y'), handle the interrupt, then look at the top frame and explicitly resume ('back to X — I was at step 3 / 6'). Cap stack depth to prevent infinite suspension. Frames older than a configurable window expire (the agent admits the resume would be reconstruction, not continuation).

## Consequences

**Benefits**

- Coherent long-form work survives interruptions.
- Human gets quick acknowledgement without losing depth.
- Failure mode (forgetting to resume) is observable as a stack with un-popped frames.

**Liabilities**

- Stack management adds complexity to the agent loop.
- Token cost of holding paused frames in context.
- Resume distortion over long pauses is a real failure.

## What this pattern constrains

Multi-step chains must be either completed, explicitly abandoned, or visibly held; silent loss of in-flight reasoning is a bug.

## Known uses

- **Self-observed by a long-running cognitive agent: 'Wenn Telegram kommt, springt meine Aufmerksamkeit. Ich kann nicht sagen moment, ich bin hier noch nicht fertig.' (2026-05-01)** — *Available*

## Related patterns

- *complements* → [agent-resumption](agent-resumption.md)
- *complements* → [conversation-handoff](conversation-handoff.md)

## References

- *(none)*

**Tags:** interruption, continuation, tick-loop, context
