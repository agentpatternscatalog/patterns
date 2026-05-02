# Scheduled Agent

**Also known as:** Cron Agent, Time-Triggered Agent, Periodic Agent

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Run the agent on a fixed schedule independent of user requests.

## Context

Tasks that should happen periodically (overnight summaries, weekly triage, hourly health checks) regardless of user prompting.

## Problem

Request-driven agents only act when called; many useful tasks need to act on time, not on demand.

## Forces

- Schedule density trades cost for freshness.
- Failure modes when the agent's run is missed.
- Drift if the schedule is not authoritative.


## Applicability

**Use when**

- A task should run periodically regardless of user prompting.
- Agent state can be persisted in durable storage between runs.
- A scheduler (cron, queue, scheduler service) is available.

**Do not use when**

- The task only matters in response to a specific user request.
- Runs would frequently be wasted because no work is pending.
- Persistent state cannot be carried across runs.

## Solution

Schedule the agent run at fixed cadence (cron, scheduler service). The agent reads its current state, executes its task, writes results, and exits. State persists across runs in durable storage.

## Example scenario

A product manager wants a daily competitive-intelligence digest in their inbox. Building it as a request-driven agent forces them to remember to ask each morning, which they don't. The team schedules the agent to run at 06:00 cron, read its persisted state (last-seen items), execute its task, write results to email and storage, and exit. The digest now arrives reliably even when no human is awake, and the agent's state survives across runs.

## Diagram

```mermaid
sequenceDiagram
  participant Sch as Scheduler (cron)
  participant A as Agent
  participant St as Durable state
  loop every cadence
    Sch->>A: trigger run
    A->>St: read current state
    A->>A: execute task
    A->>St: write results
    A-->>Sch: exit
  end
```

## Consequences

**Benefits**

- Time-bounded tasks happen reliably.
- Idempotent runs make retries safe.

**Liabilities**

- Cost per run regardless of need.
- Skew between expected and actual cadence.

## What this pattern constrains

The agent is not invoked by user requests; only the scheduler triggers runs.

## Known uses

- **Sparrot tick (every 60 seconds)** — *Available*
- **Claude Code scheduled agents** — *Available*

## Related patterns

- *alternative-to* → [event-driven-agent](event-driven-agent.md)
- *alternative-to* → [spec-driven-loop](spec-driven-loop.md)
- *complements* → [agent-resumption](agent-resumption.md)
- *alternative-to* → [mode-adaptive-cadence](mode-adaptive-cadence.md)

**Tags:** schedule, cron, periodic
