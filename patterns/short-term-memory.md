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

## Solution

Define a typed state object per thread (messages, current screen, active plan, agent step). Persist with a TTL (commonly 24h). Reload on the next turn; expire and reset on TTL.

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
