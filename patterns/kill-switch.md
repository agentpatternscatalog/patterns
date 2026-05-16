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

## Applicability

**Use when**

- An agent runs tools or model calls that can cause real harm if it goes wedged.
- Out-of-band halt must be guaranteed even when the agent loop ignores in-band signals.
- A signed revocation token or feature flag can be checked from a store the runtime cannot bypass.

**Do not use when**

- The agent has no side effects and no unbounded loop risk.
- No shared revocation store is available to the agent runtime.
- Killing the OS process is acceptable as the only stop primitive (and provenance loss is fine).

## Therefore

Therefore: check a signed revocation token from a shared store before every model and tool call in the runtime (not the agent loop), so that operator authority survives a wedged or runaway agent.

## Solution

Signed revocation token or feature flag checked on every step from a shared store the agent runtime cannot bypass. On revocation, the agent halts: no further model calls, no further tool calls; in-flight effects are compensated where possible. Killing the OS process is the fallback, but loses provenance.

## Example scenario

An autonomous trading-research agent is running a multi-hour backtest loop when ops notices it is hammering a third-party data API that just sent a cease-and-desist email. The in-band stop hook is checked by the agent's own loop and the agent is wedged on a long tool call. The team adds an out-of-band kill-switch: a signed revocation token in a shared store that the runtime, not the agent, checks before every step and tool call. Flip the token and every running instance halts within one step. The OS-kill fallback is only there for true emergencies.

## Diagram

```mermaid
flowchart TD
  Op[Operator] --> Rev[Set revocation token / flag]
  Rev --> Store[(Shared store)]
  Loop[Agent step] --> Chk[Check store]
  Chk --> Rk{Revoked?}
  Rk -- no --> Cont[Continue]
  Rk -- yes --> Halt[Halt: no model + no tool calls]
  Halt --> Comp[Compensate in-flight effects]
  Comp -.fallback.-> Kill[Kill OS process loses provenance]
```

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
