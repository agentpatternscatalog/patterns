# Open-Weight Cascade

**Also known as:** Permissive-License Cascade, Sovereign Routing, Self-Hostable Cascade

**Category:** Routing & Composition  
**Status in practice:** emerging

## Intent

Build a multi-model cascade where the lower tiers are deliberately open-weight, self-hostable models that can run inside the operator's boundary, and only escalations cross to a hosted frontier model — giving cost arbitrage *and* a sovereign fast-path.

## Context

European or regulated deployments that want both cost optimisation and a fast-path that does not depend on a non-EU hosted API.

## Problem

A naïve cheap-first cascade still falls through to a hosted frontier model for hard requests, meaning every borderline request leaks data. Open-weight-only cascades miss capability on the rare hard request.

## Forces

- Most requests are easy; cheap models handle them.
- Hard requests need frontier capability.
- Some requests must never leave the boundary regardless of difficulty.
- Open-weight models close the capability gap at a delay.

## Solution

Stratify requests by sensitivity *and* difficulty before routing. (1) Sensitive requests: forced down the open-weight path even if confidence is low; degrade gracefully or refuse rather than escalate. (2) Insensitive easy requests: small open-weight model. (3) Insensitive hard requests: escalate to hosted frontier model. The router enforces the sensitivity classification before any model call.

## Structure

```
Request -> Sensitivity classifier -> [sensitive: open-weight only path] | [insensitive: cheap-first cascade with hosted frontier as fallback].
```

## Consequences

**Benefits**

- Compliant fast-path for sensitive workloads.
- Cost arbitrage on the insensitive path.
- Operator can swap model tiers without re-architecting.

**Liabilities**

- Sensitivity classifier is the new failure surface.
- Quality cliff at the sensitive boundary if the open-weight tier under-performs.
- Operational overhead of running two stacks.

## What this pattern constrains

A request classified as sensitive may not be routed to a hosted frontier model; the hosted tier is only reachable from the insensitive path.

## Known uses

- **[Mistral](https://mistral.ai/)** — *Available*. Open-weight (Mistral 7B, Mixtral) plus hosted (Mistral Large, Medium 3.5) tiers — operators commonly cascade them.
- **Aleph Alpha PhariaAI multi-model** — *Available*. On-prem Pharia models plus optional hosted escalation.

## Related patterns

- *specialises* → [multi-model-routing](multi-model-routing.md)
- *uses* → [fallback-chain](fallback-chain.md)
- *complements* → [sovereign-inference-stack](sovereign-inference-stack.md)
- *complements* → [pii-redaction](pii-redaction.md)
- *complements* → [provider-fallback](provider-fallback.md)

## References

- (doc) *Mistral AI — Models*, <https://mistral.ai/>

**Tags:** routing, sovereignty, france-origin, mistral
