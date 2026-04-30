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

## Solution

Schedule the agent run at fixed cadence (cron, scheduler service). The agent reads its current state, executes its task, writes results, and exits. State persists across runs in durable storage.

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

**Tags:** schedule, cron, periodic
