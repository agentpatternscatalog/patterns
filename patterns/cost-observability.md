# Cost Observability

**Also known as:** Token Telemetry, Cost Dashboard

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Surface per-request, per-user, and per-feature cost and token consumption to operators in near-real-time.

## Context

Production agent products where cost surprises (a runaway feature, a bad routing decision) blow up bills before anyone notices.

## Problem

Without per-feature cost visibility, expensive failures hide in aggregate metrics until billing arrives.

## Forces

- Telemetry schema must capture which feature, which model, which user.
- Real-time vs daily aggregation.
- Privacy on per-user attribution.

## Solution

Tag every model and tool call with feature, route, user (anonymised), and model id. Stream to a telemetry store. Build dashboards by feature, by model, by tier, by hour. Set alerts on anomalies. Pair with cost-gating for prevention.

## Example scenario

An ops team notices the monthly LLM bill has tripled but can't say which feature drove it — the dashboard only shows total tokens. By the time billing arrives the runaway feature has been live for weeks. They add Cost Observability: every request is tagged with feature, user, and tenant, and per-feature spend rolls up in near-real-time. Within an hour of a regression the team can see which feature now costs ten times what it did yesterday.

## Consequences

**Benefits**

- Fast detection of cost regressions.
- Inputs for capacity planning and pricing.

**Liabilities**

- Telemetry overhead.
- Per-user attribution has privacy implications.

## What this pattern constrains

Calls without telemetry tags fall into an 'unattributed' bucket; some internal gateways enforce tag-or-reject.

## Applicability

**Use when**

- Per-feature cost visibility is needed before billing reveals a problem.
- Telemetry can be tagged with feature, route, model id, and anonymised user.
- Operators will actually act on dashboards and alerts that surface cost anomalies.

**Do not use when**

- Total spend is small enough that aggregate metrics suffice.
- Telemetry pipeline cost exceeds the cost it would help you control.
- No operator owns cost — the dashboards would go unwatched.

## Known uses

- **Langfuse** — *Available*
- **Helicone** — *Available*
- **OpenAI usage dashboard** — *Available*
- **Anthropic Console usage** — *Available*

## Related patterns

- *complements* → [cost-gating](cost-gating.md)
- *complements* → [lineage-tracking](lineage-tracking.md)

## References

- (doc) *Langfuse*, <https://langfuse.com/docs>
- (doc) *Helicone*, <https://docs.helicone.ai>

**Tags:** observability, cost, telemetry
