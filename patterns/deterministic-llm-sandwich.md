# Deterministic-LLM Sandwich

**Also known as:** Verification-and-Grounding Loop, Bracketed LLM Call, Verify LLM Output, Pre/Post Validation

**Category:** Verification & Reflection  
**Status in practice:** emerging

## Intent

Bracket every LLM call with deterministic checks on both sides.

## Context

A correctness boundary where wrong outputs cause real damage (a wrong stitch count, a malformed migration, a mis-priced order).

## Problem

Trusting the LLM's output unconditionally accepts hallucination at the most expensive moment; banning the LLM entirely loses its strengths.

## Forces

- Bracketing adds latency per call.
- Pre-checks must be cheap to be worth running.
- Post-checks must catch what the model gets wrong, not what is merely surprising.

## Solution

Three layers. Pre: deterministic check decides whether the LLM should run at all (e.g. AST parse must succeed). LLM: produces a candidate output with structured-output schema and frozen rubric. Post: deterministic re-validation (parse, type-check, run tests). If post fails, the original is returned unchanged.

## Structure

```
Pre(input) -> {pass, fail} ; if pass: LLM(input) -> candidate ; Post(candidate) -> {accept, reject}.
```

## Consequences

**Benefits**

- Confidence at the correctness boundary; the model cannot land an unsafe artefact.
- Bug fixes go into the deterministic layer where they are testable.

**Liabilities**

- Building the deterministic checks is itself the bulk of the work.
- Over-strict post-checks reject valid outputs.

## What this pattern constrains

An LLM-produced artefact lands only after passing the post-check; otherwise the prior state is preserved.

## Known uses

- **Knitting-DSL Pipeline (Stash2Go)** — *Available*. deterministicReview.js -> scopedLlmFixer.js -> parse and revalidate.

## Related patterns

- *uses* → [frozen-rubric-reflection](frozen-rubric-reflection.md)
- *uses* → [structured-output](structured-output.md)
- *composes-with* → [code-execution](code-execution.md) — Post-check often runs code (parse/test) to validate output.

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** verification, boundary, sandwich
