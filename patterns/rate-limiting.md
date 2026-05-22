# Rate Limiting

**Also known as:** Throttling, Quota Enforcement

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Cap the number of requests, tokens, or tool calls per user (or session) within a time window.

## Context

A team runs a multi-tenant agent product where many users share the same backend resources — token budgets with model providers, tool API quotas, compute capacity. Any one of those users can, accidentally or maliciously, send much more traffic than the operator priced for: a runaway script, a compromised account, or simply a single power user opening hundreds of concurrent sessions.

## Problem

Without per-identity limits, a single caller can drain the month's token budget in a few hours, hit downstream provider rate limits and starve every other user, or simply run up an unbounded bill the operator did not authorise. Imposing one global cap is too blunt — it punishes everyone for one bad actor — and trusting users to behave reasonably has never worked at scale. The team is forced to choose between generous limits that hurt cost and tight limits that hurt legitimate users.

## Forces

- Generous limits hurt cost; tight limits hurt UX.
- Per-tier limits add complexity.
- Distributed counters need coordination.

## Applicability

**Use when**

- A single user or compromised account could otherwise bankrupt the product or starve others.
- Limits per identity can be enforced at API gateway and inside the agent loop.
- Limit hits can be surfaced to users in a clear, actionable way.

**Do not use when**

- The deployment is a closed internal tool with trusted volume.
- Existing infrastructure already rate-limits effectively at the boundary.
- False rate-limit denials would block more legitimate work than they protect.

## Therefore

Therefore: enforce per-identity token-bucket counters at multiple horizons in both the gateway and the agent loop, so that no single caller can starve the system or run up an unbounded bill.

## Solution

Define limits per identity at multiple horizons (per minute, per hour, per day). Use token-bucket or sliding-window counters. Apply at API gateway and at agent loop level. Surface limit hits to the user clearly.

## Example scenario

A coding assistant ships a free tier and within a week one signed-up account opens 400 concurrent agent loops, draining the month's token budget in two hours. The team adds per-identity token-bucket counters at three horizons (per minute, per hour, per day) at the API gateway and inside the agent loop itself. Over-budget callers get a clear 429 naming which window tripped and when it resets. Cost stops being a single hostile user away from blowing up.

## Diagram

```mermaid
flowchart TD
  Req[Request] --> ID[Identify caller]
  ID --> B[Token bucket /<br/>sliding window]
  B -->|under limit| Allow[Allow]
  B -->|over limit| Deny[429 + clear message]
  Allow --> Agent[Agent loop]
  Agent --> B2[Inner limit:<br/>tool calls / tokens]
```

## Consequences

**Benefits**

- Cost predictability.
- Abuse becomes detectable as limit hits.

**Liabilities**

- Legitimate burst usage is throttled.
- Tier definitions ossify.

## What this pattern constrains

Requests beyond the limit are rejected or queued; no code path may bypass the limiter.

## Known uses

- **Most production agent APIs** — *Available*
- **[Sparrot](https://marco-nissen.com/sparrot/)** — *Available* — A sliding-window token cap is enforced per minute per provider so a chatty stretch cannot exhaust the budget for a calmer one.

## Related patterns

- *complements* → [circuit-breaker](circuit-breaker.md)
- *complements* → [cost-gating](cost-gating.md)
- *complements* → [event-driven-agent](event-driven-agent.md)
- *complements* → [kill-switch](kill-switch.md)

**Tags:** safety, throttle, quota
