# Citation Streaming

**Also known as:** Inline Citations, Source-Anchored Output

**Category:** Streaming & UX  
**Status in practice:** mature

## Intent

Stream citations alongside generated text so the UI can render source links in place as content appears.

## Context

RAG-backed answers where the user must trace claims to sources; post-hoc citation breaks the streaming UX.

## Problem

Generating citations after the answer hides them until the end; trusting the model to inline citations as text fails reliably.

## Forces

- Citation events must align with generated tokens.
- Source spans need stable ids.
- UI needs to render mid-stream without flickering.

## Solution

Define a streaming event vocabulary that includes citation events linked to source ids. The model is prompted to emit citation markers; the host extracts them into typed events alongside text deltas. The UI renders sources progressively. Final output includes a citation map.

## Consequences

**Benefits**

- Trust UX: claims trace to sources visibly.
- Hallucinations become visible (no source = suspicious).

**Liabilities**

- Streaming protocol is more complex.
- Citation event quality depends on model compliance.

## What this pattern constrains

Source claims in the output must reference a citation event with a valid source id.

## Known uses

- **Perplexity** — *Available*
- **Anthropic Citations API** — *Available*
- **ChatGPT** — *Available*
- **Gemini Deep Research** — *Available*
- **Glean** — *Available*

## Related patterns

- *specialises* → [streaming-typed-events](streaming-typed-events.md)
- *complements* → [naive-rag](naive-rag.md)
- *alternative-to* → [hallucinated-citations](hallucinated-citations.md)
- *alternative-to* → [attention-manipulation-explainability](attention-manipulation-explainability.md)

## References

- (doc) *Anthropic: Citations*, <https://docs.anthropic.com/claude/docs/citations>

**Tags:** streaming, citation, ux
