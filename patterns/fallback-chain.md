# Fallback Chain

**Also known as:** Cascade Fallback, Try-Then-Try-Else, Tool Failed Fall Back, Provider Failed Retry Other

**Category:** Routing & Composition  
**Status in practice:** mature

## Intent

Try a primary handler; on failure or low confidence, fall through to a sequence of fallback handlers.

## Context

An agent in production depends on at least one model or tool that can fail for routine reasons: rate limiting, vendor errors, regional incidents, or outputs the model itself returns with low confidence. End users are sitting on the other end of the call expecting an answer regardless of which upstream had a bad minute. The team has more than one option available — a backup model, a smaller local model, a deterministic rule-based fallback — but those options are not wired in by default.

## Problem

When the single primary handler fails, the user sees an outage even though other working handlers exist in the system. When the primary returns a low-confidence answer, the product silently ships a degraded response with no signal that something better could have been tried. Without a defined ordering of handlers and a rule for moving between them, every team improvises on each incident and quality regressions in the primary go unnoticed.

## Forces

- Fallback handlers may be slower or worse.
- Detecting 'failure' requires a confidence signal.
- Cascade depth must be bounded.

## Therefore

Therefore: order handlers in a confidence-gated chain that pass downward on failure and end in an honest 'I don't know', so that no single handler's outage becomes the user's outage.

## Solution

Define an ordered chain of handlers. Each handler returns either a confident answer or a failure/low-confidence signal. On failure, the next handler runs. Final fallback is a generic 'I don't know' rather than a wrong answer.

## Structure

```
Query --> Handler 1 --confident--> Answer | --fail or low confidence--> Handler 2 --confident--> Answer | --pass--> ... Handler N --pass--> "I don't know"; cascade controller bounds depth and logs which handler served
```

## Diagram

```mermaid
flowchart TD
  Q[Query] --> H1[Handler 1]
  H1 --> C1{Confident?}
  C1 -- yes --> Out[Answer]
  C1 -- no --> H2[Handler 2]
  H2 --> C2{Confident?}
  C2 -- yes --> Out
  C2 -- no --> H3[Handler 3]
  H3 --> C3{Confident?}
  C3 -- yes --> Out
  C3 -- no --> IDK["I don't know"]
```

## Example scenario

A translation feature uses a primary high-quality model, but during incidents that model returns 502s and users see error messages. The team configures a Fallback Chain: try the primary model, on failure or low-confidence output try a secondary model, on failure of that try a smaller local model with a 'degraded quality' indicator. The user gets a translation in every case; the team gets visibility into how often each layer is used.

## Consequences

**Benefits**

- Graceful degradation under partial failures.
- Each layer can be tuned independently.

**Liabilities**

- Cumulative latency on full cascade.
- Hides quality regressions in the primary.

## Failure modes

- Masked primary regression — the primary quietly gets worse, the secondary picks up the slack, and nobody notices because users still get answers.
- Latency stack-up — every handler in a deep chain passes, and the user waits for the sum of all of them before hearing 'I don't know'.
- Broken confidence gate — a handler reports high confidence on a wrong answer, so the chain stops early and ships it.
- Wrong answer instead of none — the final handler is a weak guesser rather than an honest 'I don't know', and the chain ends on a fabrication.

## What this pattern constrains

Each handler may produce a result or pass; only the chain may decide to terminate.

## Applicability

**Use when**

- Single-handler failure would cascade to the user as an outage.
- Multiple handlers exist with meaningful differences in capability or cost.
- Each handler can return a confidence or failure signal that triggers the next.

**Do not use when**

- Only one handler exists and there is nothing to fall back to.
- Handler failure modes are correlated and all handlers fail together.
- An honest 'I don't know' is preferred over fallback chains that mask root cause.

## Components

- Ordered handler chain — primary, secondary, tertiary handlers with a defined progression
- Confidence signal — per-handler indicator (score, error, schema-validation result) that triggers handoff
- Cascade controller — walks the chain, applies the gate at each step, enforces a depth bound
- Honest-failure terminator — final 'I don't know' response when every handler passes
- Per-layer telemetry — records which handler produced the served answer

## Tools

- LangChain `with_fallbacks` runnable or equivalent chaining library — wires the ordered handlers
- Multiple LLM provider APIs or rule-based handlers — the heterogeneous backends the chain calls
- Structured-output validator — schema check that promotes a parse failure into a low-confidence signal

## Evaluation metrics

- Per-layer hit rate — share of requests served by handler 1, 2, 3, and 'I don't know'
- Quality delta between layers — does each fallback genuinely degrade gracefully or sharply
- Cumulative p95 latency under full cascade — worst-case wait when every layer is tried
- Hidden-regression rate — share of requests where the primary returned low confidence on tasks it used to handle
- Honest-IDK rate — share ending in the terminator instead of a wrong answer

## Known uses

- **Most production routing layers** _available_
- **AI-Standards Fallback Chain pattern** _available_

## Related patterns

- _complements_ **Routing**
- _composes-with_ **Circuit Breaker**
- _complements_ **Multi-Model Routing**
- _generalises_ **Provider Fallback**
- _complements_ **Confidence Reporting**
- _complements_ **Exception Handling and Recovery**
- _complements_ **Graceful Degradation**
- _used-by_ **Open-Weight Cascade**
- _complements_ **Complexity-Based Routing**
- _complements_ **Naive Retry Without Backoff**
- _used-by_ **Agentic Behavior Tree**

## References

- [How to add fallbacks to a runnable](https://python.langchain.com/docs/how_to/fallbacks/) — LangChain, 2024
