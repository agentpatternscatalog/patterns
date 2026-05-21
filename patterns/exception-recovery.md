# Exception Handling and Recovery

**Also known as:** Error Recovery, Failure Mode Handler

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Catch and react to predictable failure modes (tool errors, rate limits, validation failures) with structured recovery paths.

## Context

A team runs a production agent that calls many tools in a loop: search APIs, internal databases, third-party services, model endpoints. In real traffic those tools fail in predictable, repeating ways — the API is briefly down, the caller hit a rate limit, the response came back malformed, the credential was rejected, the request timed out. Each of those failure modes wants a different response from the agent.

## Problem

If the tool layer returns errors as opaque strings stuffed back into the conversation, the agent treats them as text and reacts with whatever the model invents — sometimes a retry, sometimes a confident hallucinated explanation to the user, sometimes a stall. The agent has no way to branch deterministically on a rate-limit versus a validation error, so it cannot back off correctly on the first or replan on the second. Without typed errors and named recovery branches, the team is forced to choose between blanket retries that mask real bugs and giving up on partial-failure handling altogether.

## Forces

- Recovery logic must not mask bugs.
- Some errors are user-visible; others should be silent.
- Retry storms on transient errors.

## Therefore

Therefore: catalogue each predictable failure as a typed error with a defined recovery branch (retry, fall back, surface, replan), so that the agent reacts deterministically instead of hallucinating an explanation.

## Solution

Catalogue failure modes. For each, define: detect (typed error), respond (retry / fall back / surface to user / replan), and log. The agent receives a structured error message and can react with a typed branch in its loop.

## Example scenario

A research agent calls a search tool that returns a rate-limit error. Without typed handling the error string flows back into the conversation as an opaque blob; the agent invents a plausible-sounding explanation and stalls. The team adds Exception Recovery: each tool wraps known failure modes (rate-limit, auth, validation, timeout) into typed error envelopes, and the agent's prompt has explicit recovery branches — back off and retry on rate-limit, switch tool on validation, escalate on auth. Failures stop becoming silent confusion.

## Diagram

```mermaid
flowchart TD
  Step[Agent step] --> E{Error?}
  E -- no --> Next[Continue]
  E -- typed error --> R{Recovery branch}
  R -- transient --> Retry[Retry with backoff]
  R -- rate limit --> Wait[Wait + retry]
  R -- validation --> Fall[Fall back / replan]
  R -- unknown --> Surface[Surface to user]
  Retry --> Step
  Wait --> Step
  Fall --> Next
  Surface --> L[Log structured error]
```

## Consequences

**Benefits**

- Failure modes become first-class.
- Reliability under partial failures rises.

**Liabilities**

- Exception-handling code is its own surface to maintain.
- Hidden retries can mask deeper issues.

## What this pattern constrains

Errors must arrive at the agent as typed events from the catalogue; untyped errors are escalated to the operator.

## Applicability

**Use when**

- Tool errors, rate limits, or validation failures occur often enough that random retries waste effort.
- Failure modes can be catalogued with typed errors and structured recovery responses.
- The agent loop can branch on typed error messages.

**Do not use when**

- Failures are rare enough that a single generic retry handles them.
- Failure modes change faster than the catalogue can be maintained.
- The agent has no loop to react in (single-shot pipelines).

## Known uses

- **Production agent platforms** — *Available*
- **Gulli Exception Handling pattern** — *Available*

## Related patterns

- *complements* → [fallback-chain](fallback-chain.md)
- *complements* → [circuit-breaker](circuit-breaker.md)
- *complements* → [replan-on-failure](replan-on-failure.md)
- *generalises* → [graceful-degradation](graceful-degradation.md)

## References

- (book) *Agentic Design Patterns (Gulli)*, 2025

**Tags:** safety, error, recovery
