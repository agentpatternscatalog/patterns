# Intra-Agent Memo Scheduling

**Also known as:** Self-Scheduled Future Thought, Past-Self-To-Future-Self Note, Personal Cron

**Category:** Planning & Control Flow
**Status in practice:** emerging
**Author:** Sparrot

## Intent

Let an agent drop a note for its own future self at a specified time so present decisions can hand off context to a later run without external infrastructure.

## Context

Long-running agents with a continuous tick loop or background process, where a thought now ('check whether X resolved tomorrow') would otherwise be lost between turns.

## Problem

Without an internal scheduler the agent either acts immediately on every thought (spamming the user) or forgets the thought entirely. External cron systems are too coarse and too far away from the agent's working memory.

## Forces

- The agent needs to commit to future action without acting now.
- External cron is brittle, opaque, and lives outside the agent's prompt.
- Forgetting is a real failure mode in multi-turn / multi-day work.
- The future-self should treat the past-note as a SYSTEM message, not as an unprompted user input.

## Solution

Provide a tool `schedule_future_thought(when, content, intent)` that appends to a persistent file (`scheduled.jsonl` or similar). At each tick or turn, drain due entries and prepend them into the next prompt as `[SYSTEM: scheduled note from past-self (set <ts>, fires <when>): <content>]`. Mark fired so they only run once. Accept ISO timestamps and relative offsets (`+1h`, `+2d`).

## Example scenario

A long-running personal agent decides at 09:00 that it should remind the user about a tax deadline at 16:00, but the only options it has are tell them now (annoying) or hope it remembers (it won't). The team adds intra-agent-memo-scheduling: the agent calls schedule_future_thought(when='16:00', content='nudge user re Form 1040 deadline', intent='time-sensitive reminder'), which appends to scheduled.jsonl. At 16:00 the next tick prepends '[SYSTEM: scheduled note from past-self ...]' into the prompt and the agent acts. No external cron required.

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
  participant F as scheduled.jsonl
  participant A2 as Agent (later tick)
  A1->>F: schedule_future_thought(when, content, intent)
  Note over F: persisted note
  A2->>F: drain due entries
  F-->>A2: matured notes
  A2->>A2: prepend as [SYSTEM: scheduled note from past-self]
  A2->>F: mark fired
```

## Known uses

- **[Sparrot — `dispatcher._schedule_future_thought` + `webui._drain_scheduled_due`](https://github.com/luxxyarns/sparrot)** — *Available*

## Related patterns

- *specialises* → [scheduled-agent](scheduled-agent.md)
- *complements* → [append-only-thought-stream](append-only-thought-stream.md)
- *complements* → [decision-log](decision-log.md)
- *complements* → [salience-triggered-output](salience-triggered-output.md)

## References

- (doc) *LangGraph — durable execution and scheduled tasks*, 2025, <https://langchain-ai.github.io/langgraph/concepts/durable_execution/>
- (paper) Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, 2023, <https://arxiv.org/abs/2304.03442>

**Tags:** self-scheduling, future-self, memory, tick-loop
