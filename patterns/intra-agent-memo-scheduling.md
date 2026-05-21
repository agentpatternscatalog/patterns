# Intra-Agent Memo Scheduling

**Also known as:** Self-Scheduled Future Thought, Past-Self-To-Future-Self Note, Personal Cron

**Category:** Cognition & Introspection
**Status in practice:** emerging

## Intent

Let an agent drop a note for its own future self at a specified time so present decisions can hand off context to a later run without external infrastructure.

## Context

A team is running an agent that ticks continuously across many sessions and frequently has the thought 'I should come back to this tomorrow' or 'check whether X resolved by Friday afternoon.' The present-self has context the future-self will need, but the natural prompt window only carries a handful of recent turns, so by tomorrow that intention has fallen out of context entirely.

## Problem

Without some way to drop a note for its own future self, the agent has only two unsatisfying options. It can act on the thought right now — pinging the user at 9am about something that should have waited until 4pm — or it can hope to remember on its own, which it will not. External scheduling systems like cron or a queue can fire on time but live outside the agent's working memory, so when they do fire the agent has no idea why the reminder is showing up or what its past-self intended.

## Forces

- The agent needs to commit to future action without acting now.
- External cron is brittle, opaque, and lives outside the agent's prompt.
- Forgetting is a real failure mode in multi-turn / multi-day work.
- The future-self should treat the past-note as a SYSTEM message, not as an unprompted user input.

## Therefore

Therefore: give the agent a tool to drop a note for its own future self into a persistent queue that drains as SYSTEM messages at fire time, so that present thoughts can commit to future action without spamming now or being forgotten by then.

## Solution

Provide a tool `schedule_future_thought(when, content, intent)` that appends to a persistent scheduled-thoughts queue. At each tick or turn, drain due entries and prepend them into the next prompt as `[SYSTEM: scheduled note from past-self (set <ts>, fires <when>): <content>]`. Mark fired so they only run once. Accept ISO timestamps and relative offsets (`+1h`, `+2d`).

## Example scenario

A long-running personal agent decides at 09:00 that it should remind the user about a tax deadline at 16:00, but the only options it has are tell them now (annoying) or hope it remembers (it won't). The team adds intra-agent-memo-scheduling: the agent calls schedule_future_thought(when='16:00', content='nudge user re Form 1040 deadline', intent='time-sensitive reminder'), which appends to a persistent scheduled-thoughts queue. At 16:00 the next tick prepends '[SYSTEM: scheduled note from past-self ...]' into the prompt and the agent acts. No external cron required.

## Consequences

**Benefits**

- Agent can defer action without forgetting.
- Past-self can leave context for future-self across long gaps.
- Provides 'check back on this' semantics native to the agent.

**Liabilities**

- Without expiry or dismissal, scheduled notes accumulate and waste prompt tokens; obsolete future-self commitments can pollute attention long after they've stopped being relevant.
- Drift between schedule time and actual tick time depending on tick cadence.
- Risk of accumulating stale promises that pollute the agent's sense of obligation.

## What this pattern constrains

Future thoughts must surface at or after their fire time; failures to drain are observable bugs.

## Applicability

**Use when**

- The agent runs across many ticks or sessions and present-self has context the future-self will need.
- External schedulers (cron, queues, durable workflows) are unavailable or overkill.
- Future-fire memos are a small enough volume to keep in the agent's own store.

**Do not use when**

- A real workflow engine (LangGraph durable execution, Temporal) is already integrated and reliable.
- Memos must survive the agent process being deleted; intra-agent storage is too fragile.
- Memo volume is high enough that an external scheduler is required for performance.

## Variants

### Append-and-scan

Memos are appended to a single file; every tick scans for entries whose fire-time has passed.

*Distinguishing factor:* no index

*When to use:* Default for small memo volumes.

### Indexed by fire-time

Memos are stored in a min-heap or sorted index keyed by fire-time; tick pops only what is due.

*Distinguishing factor:* O(log n) drain

*When to use:* When memo volume is large enough that linear scan is wasteful.

### Recurring memo

Each memo carries a recurrence rule (e.g. 'every Monday 09:00') and is re-scheduled after firing.

*Distinguishing factor:* self-rescheduling

*When to use:* When the agent needs cron-like behaviour without an external scheduler.

## Diagram

```mermaid
sequenceDiagram
  participant A1 as Agent (now)
  participant F as Scheduled-thoughts queue
  participant A2 as Agent (later tick)
  A1->>F: schedule_future_thought(when, content, intent)
  Note over F: persisted note
  A2->>F: drain due entries
  F-->>A2: matured notes
  A2->>A2: prepend as [SYSTEM: scheduled note from past-self]
  A2->>F: mark fired
```

## Known uses

- **Long-running personal agent loops (private deployment)** — *Available*

## Related patterns

- *specialises* → [scheduled-agent](scheduled-agent.md)
- *complements* → [append-only-thought-stream](append-only-thought-stream.md)
- *complements* → [decision-log](decision-log.md)
- *complements* → [salience-triggered-output](salience-triggered-output.md)

## References

- (doc) *LangGraph — durable execution and scheduled tasks*, 2025, <https://langchain-ai.github.io/langgraph/concepts/durable_execution/>
- (paper) Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, 2023, <https://arxiv.org/abs/2304.03442>

**Tags:** self-scheduling, future-self, memory, tick-loop
