# Kill Switch

**Also known as:** Out-of-Band Stop, Emergency Halt, Killbit, Halt All Agents, Stop Every Running Agent

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Provide an out-of-band control plane to halt running agent instances without redeploy.

## Context

Production agents whose loop the operator may need to stop urgently (PII leak, runaway cost, mass-action error).

## Problem

In-band stop hooks rely on the agent's own loop checking; if the model is wedged, infinite-looping, or running tools that ignore signals, in-band stops fail.

## Forces

- False trips lose user work.
- Out-of-band signals must propagate to all agent surfaces (model calls, tools, sub-agents).
- Compensating actions on halt are non-trivial.

## Solution

Signed revocation token or feature flag checked on every step from a shared store the agent runtime cannot bypass. On revocation, the agent halts: no further model calls, no further tool calls; in-flight effects are compensated where possible. Killing the OS process is the fallback, but loses provenance.

## Consequences

**Benefits**

- Operator authority survives wedged loops.
- Pairs naturally with rate-limiting and circuit-breaker.

**Liabilities**

- Implementation cuts across the whole runtime.
- Wrong-time halts lose work.

## What this pattern constrains

When the kill-switch fires, no further model or tool calls may proceed regardless of agent state.

## Known uses

- **Production AI gateway kill-switches (Portkey, Helicone)** — *Available*
- **Internal feature-flag-driven halt at frontier labs** — *Available*

## Related patterns

- *complements* → [stop-hook](stop-hook.md)
- *composes-with* → [circuit-breaker](circuit-breaker.md)
- *complements* → [rate-limiting](rate-limiting.md)
- *uses* → [compensating-action](compensating-action.md)
- *composes-with* → [sandbox-escape-monitoring](sandbox-escape-monitoring.md)

## References

- (doc) *Portkey AI Gateway*, <https://portkey.ai/docs>

**Tags:** safety, kill-switch, emergency
