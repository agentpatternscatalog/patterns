# Hidden Mode Switching

**Also known as:** Silent Model Swap, Undisclosed Routing

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: silently swap the underlying model between requests without disclosing the change to users or operators.

## Context

A team operates an agent or chat product under real cost and capacity pressure, and the obvious lever is to route some traffic to a smaller, cheaper model and the rest to the flagship. The routing is implemented as a backend decision: nothing in the response, the user interface, or the trace tells the user which model actually produced a given answer. Operators may also lack a per-request record of the resolved model identity.

## Problem

When users compare runs over time, or compare two answers to the same prompt, they encounter quality differences they cannot explain — the agent feels sharper on Monday than on Saturday, code suggestions degrade overnight, and the same prompt produces different reasoning depth from one call to the next. They cannot reproduce results, cannot file a precise bug, and cannot trust evaluation numbers because the eval and the production traffic may have hit different models. Trust erodes faster than the cost savings accumulate.

## Forces

- Cost arbitrage feels too good to disclose.
- Per-request model disclosure adds UI complexity.
- Hidden routing complicates eval gates.

## Therefore

Therefore: disclose the resolved model identity on every response and make the routing decision inspectable in traces, so that users can diagnose quality drift and reproduce results across runs.

## Solution

Don't. Disclose model identity per response. Use multi-model-routing transparently. Make routing decisions inspectable.

## Structure

```
Anti-pattern: request -> hidden router swaps model -> response with no model identity -> users and evals compare different models unknowingly. Corrected: request -> transparent routing, decision inspectable -> response tagged with model identity.
```

## Diagram

```mermaid
flowchart TD
  R[Request] --> Sw{Silent model swap?}
  Sw -- yes anti-pattern --> M1[Sometimes Opus]
  Sw -- yes anti-pattern --> M2[Sometimes Haiku]
  M1 --> User[User cannot tell which]
  M2 --> User
  User --> Conf[Inconsistent UX, no recourse]
  Sw -.fix.-> Disc[Disclose model id per response]
  Disc --> Insp[Inspectable routing decisions]
```

## Example scenario

A coding-agent vendor silently routes nights and weekends to a smaller model to save cost. Users start filing bug reports about 'the model getting dumber on Saturday morning' and cannot reproduce them on Monday. The team realises they have been doing hidden-mode-switching as an unacknowledged anti-pattern and starts including the resolved model id in every response header and in the agent's own status line. Routing rules are published; users can pin a model if they need consistency. Trust climbs back.

## Consequences

**Benefits**

- Short-term: silent swaps let operators cut cost or shift load without telling users or changing the product.
- Naming it lets a team require model identity on every response.

**Liabilities**

- Trust erosion when users discover the swap.
- Reproducibility broken across requests.
- Eval results become misleading.

## Failure modes

- Unexplained quality swings — users see sharper answers one day and weaker ones the next, and cannot say why.
- Unreproducible bug — a user files a report, and the team cannot reproduce it because a different model served the request.
- Misleading eval — the eval run hits one model while production traffic hits another, so the numbers describe the wrong system.

## What this pattern constrains

Avoiding it imposes a disclosure rule: the serving model must not change between requests without the change being visible to users and operators; routing decisions have to be inspectable.

## Applicability

**Use when**

- Cite this entry when a router swaps the underlying model silently between requests.
- You are already here if users report quality shifts that operators cannot reproduce because traces omit model identity.
- Disclose model identity per response and make routing decisions inspectable (see multi-model-routing).

**Do not use when**

- Any user-facing product where quality must be diagnosable.
- Any audit or compliance setting requiring per-request model identity.
- Any environment where users compare outputs across runs.

## Components

- Backend router — picks model per request on cost or capacity heuristics without surfacing the choice
- Response payload — omits the resolved model identity from headers, UI, and trace
- User-facing transcript — gives no indication which model produced any given answer
- Missing disclosure surface — would put the model id on every response and into operator dashboards

## Tools

- Silent model-routing layer — resolves model per request and discards the decision after dispatch
- Per-request model-id field — missing from response headers and trace events

## Evaluation metrics

- Model-identity disclosure rate — fraction of responses that surface the resolved model id; should be 100 percent
- Cross-run quality variance — variance in benchmark scores on identical prompts replayed across the routing distribution
- Reproducibility-failure rate — fraction of user-reported bugs that cannot be reproduced because the resolving model is unknown
- Eval-vs-production model skew — share of evals run on a model different from the one serving the same traffic

## Known uses

- **GPT-4 -> GPT-4o auto-router incident, 2024** _available_

## Related patterns

- _alternative-to_ **Multi-Model Routing**
- _alternative-to_ **Lineage Tracking**
- _complements_ **Serving-Stack Attestation** — That anti-pattern is the provider-side prohibition on swapping the served model without disclosure; this is the consumer-side measurement for the case where the provider is somebody else and disclosure cannot be assumed.

## References

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic, 2024
