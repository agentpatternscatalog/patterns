# Structured Output

**Also known as:** JSON Mode, Schema-Constrained Generation, Typed Output

**Category:** Structure & Data  
**Status in practice:** mature

## Intent

Constrain the model's output to conform to a JSON Schema (or similar typed shape).

## Context

Downstream code needs typed data; free-form text breaks parsers and propagates errors.

## Problem

Free-form output requires fragile post-hoc parsing; the model produces near-JSON that fails strict parsers in surprising ways.

## Forces

- Strict schemas reduce model freedom and recall.
- Schema evolution is a real concern.
- Provider implementations of structured output differ in fidelity.


## Applicability

**Use when**

- Downstream code consumes typed data and free-form text would break parsers.
- A JSON Schema or equivalent typed shape can be defined for the output.
- The provider supports structured-output mode or function calling.

**Do not use when**

- Output is for human consumption only and structure adds no value.
- The schema would be so loose it provides no real type safety.
- Strict schema enforcement triggers excessive retries that hurt UX.

## Solution

Define a JSON Schema (or Pydantic / Zod / equivalent). Pass it to the model via the provider's structured-output mode. Validate the output. Reject and retry on validation failure. Cap retries.

## Consequences

**Benefits**

- Downstream code becomes simple and typed.
- Schema-level errors surface immediately.

**Liabilities**

- Provider lock-in for the strictest modes.
- Some tasks resist schema-fitting; the schema becomes the bottleneck.

## What this pattern constrains

The model cannot return content that does not validate against the schema.

## Known uses

- **ConvArch** — *Available*. Strict JSON schema for every architecture-edit tool call.
- **Knitting-DSL Pipeline (Stash2Go)** — *Available*. Frozen 6-item rubric output schema.
- **Guardrails AI** — *Available*

## Related patterns

- *used-by* → [tool-use](tool-use.md)
- *used-by* → [frozen-rubric-reflection](frozen-rubric-reflection.md)
- *used-by* → [deterministic-llm-sandwich](deterministic-llm-sandwich.md)
- *alternative-to* → [schema-free-output](schema-free-output.md)
- *complements* → [plan-and-execute](plan-and-execute.md)
- *used-by* → [dspy-signatures](dspy-signatures.md)
- *used-by* → [input-output-guardrails](input-output-guardrails.md)
- *complements* → [streaming-typed-events](streaming-typed-events.md)
- *alternative-to* → [hallucinated-tools](hallucinated-tools.md)
- *alternative-to* → [tool-output-trusted-verbatim](tool-output-trusted-verbatim.md)
- *used-by* → [sop-encoded-multi-agent](sop-encoded-multi-agent.md)
- *used-by* → [mobile-ui-agent](mobile-ui-agent.md)
- *used-by* → [dual-system-gui-agent](dual-system-gui-agent.md)
- *complements* → [code-as-action](code-as-action.md)
- *used-by* → [multilingual-voice-agent](multilingual-voice-agent.md)
- *complements* → [code-switching-aware-agent](code-switching-aware-agent.md)

## References

- (doc) *OpenAI Structured Outputs*, <https://platform.openai.com/docs/guides/structured-outputs>
- (doc) *Pydantic*, <https://docs.pydantic.dev>

**Tags:** schema, json, typed-output
