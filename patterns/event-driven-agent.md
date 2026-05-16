# Event-Driven Agent

**Also known as:** Event Subscriber, Reactive Agent, Webhook Agent

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Trigger the agent on external events (webhooks, message queues, file changes) instead of user requests or schedules.

## Context

Tasks that should happen in response to something happening (PR opened, message received, alert fired) — not on a clock and not on demand.

## Problem

Pulling for state on a schedule wastes effort; pushing on events is timely and efficient when an event source exists.

## Forces

- Event source reliability.
- Burst handling: event storms can overwhelm.
- Dedup of events that fire multiple times.

## Therefore

Therefore: subscribe to a validated event stream and invoke the agent only on deduplicated, rate-limited events, so that the agent reacts at event time without paying for idle polling.

## Solution

Subscribe to event source (webhook, queue, watcher). On event, validate, deduplicate, and invoke the agent with event payload as input. Apply rate limiting and idempotency. Acknowledge after successful processing.

## Example scenario

A monitoring agent polls a status endpoint every thirty seconds to see whether a build has finished. Most polls find nothing, burning tokens. The team flips to Event-Driven Agent: the build system fires a webhook on completion, and the agent wakes up only when an event arrives. Latency to react drops from up to thirty seconds to roughly the webhook round-trip, and idle cost drops to near zero.

## Diagram

```mermaid
sequenceDiagram
  participant Src as Event source
  participant H as Handler
  participant A as Agent
  Src->>H: event (webhook / queue / file change)
  H->>H: validate + dedupe
  H->>H: rate limit check
  H->>A: invoke with payload
  A-->>H: result
  H->>Src: ack
```

## Consequences

**Benefits**

- Timely action without polling cost.
- Composes with downstream automations naturally.

**Liabilities**

- Event-source failures stop the agent silently.
- Idempotency is its own engineering.

## What this pattern constrains

The agent runs only on validated events; spurious or duplicate events are filtered.

## Applicability

**Use when**

- An external event source (webhook, queue, file watcher) exists and pulling on a schedule wastes effort.
- Events can be validated, deduplicated, and processed idempotently.
- Acknowledgement after successful processing is supported by the event source.

**Do not use when**

- No event source exists and polling is the only available trigger.
- Event volume is so low that a daily cron is simpler than a subscription.
- Idempotency cannot be guaranteed and duplicate events would cause harm.

## Known uses

- **GitHub Actions agent triggers** — *Available*
- **Pub/Sub-driven agent platforms** — *Available*

## Related patterns

- *alternative-to* → [scheduled-agent](scheduled-agent.md)
- *complements* → [rate-limiting](rate-limiting.md)
- *complements* → [agent-resumption](agent-resumption.md)
- *complements* → [salience-triggered-output](salience-triggered-output.md)

**Tags:** events, reactive, webhook
