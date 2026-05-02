# Short-Term Thread Memory

**Also known as:** Conversation State, Per-Thread State, Working Memory

**Category:** Memory  
**Status in practice:** mature

## Intent

Carry the relevant slice of conversation context across turns within a session.

## Context

A multi-turn agent needs continuity (the user's most recent screen, the active plan, prior tool results) but does not need it forever.

## Problem

Replaying the entire conversation every turn is expensive and pollutes context with stale facts.

## Forces

- TTL choice (minutes? hours? days?) trades freshness for cost.
- What to keep vs. summarise is a quality-vs-cost tension.
- Multi-device sessions complicate where state lives.


## Applicability

**Use when**

- Multi-turn agent needs continuity across turns within a session.
- Replaying full conversation each turn is expensive or pollutes context.
- A typed state object with TTL can capture the relevant slice.

**Do not use when**

- The agent is single-turn or stateless by design.
- All history truly matters and pruning would lose important context.
- TTL semantics cannot be enforced reliably in storage.

## Solution

Define a typed state object per thread (messages, current screen, active plan, agent step). Persist with a TTL (commonly 24h). Reload on the next turn; expire and reset on TTL.

## Example scenario

A chat assistant replays the entire conversation each turn and by message thirty the prompt is bloated with stale facts and the cost-per-turn has tripled. The team defines a typed thread state (recent messages, current screen, active plan, agent step) persisted with a 24-hour TTL and reloads only that on the next turn. Token cost per turn flatlines; the assistant still feels continuous within a session and resets cleanly on TTL.

## Consequences

**Benefits**

- Continuity without full-history replay.
- Bounded memory footprint per active user.

**Liabilities**

- TTL boundaries surprise users when state vanishes mid-task.
- Schema migrations are painful for live state.

## What this pattern constrains

The agent cannot rely on facts older than the TTL window without re-fetching them.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. Per-thread state in chat/backend/state.py with 24h TTL.
- **LangGraph MemorySaver checkpoints** — *Available*

## Related patterns

- *complements* → [episodic-summaries](episodic-summaries.md)
- *complements* → [session-isolation](session-isolation.md)
- *used-by* → [agent-resumption](agent-resumption.md)
- *complements* → [cross-session-memory](cross-session-memory.md)
- *complements* → [scratchpad](scratchpad.md)
- *generalises* → [reasoning-trace-carry-forward](reasoning-trace-carry-forward.md)
- *complements* → [co-located-memory-surfacing](co-located-memory-surfacing.md)
- *used-by* → [interrupt-resumable-thought](interrupt-resumable-thought.md)
- *used-by* → [echo-recognition](echo-recognition.md)

## References

- (doc) *LangGraph: Persistence*, <https://langchain-ai.github.io/langgraph/concepts/persistence/>

**Tags:** memory, state, ttl
