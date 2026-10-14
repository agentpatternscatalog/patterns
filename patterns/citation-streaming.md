# Citation Streaming

**Also known as:** Inline Citations, Source-Anchored Output

**Category:** Streaming & UX  
**Status in practice:** mature

## Intent

Stream citations alongside generated text so the UI can render source links in place as content appears.

## Context

A team is building a retrieval-augmented agent — Retrieval-Augmented Generation, where the model answers from a set of documents pulled in at query time — and the user needs to see which source each claim came from. The answer streams to the user token by token so the interface feels responsive. The team has to decide when and how the citations should appear alongside the streaming text.

## Problem

Two obvious choices both fail. Generating the answer first and the citation list afterwards hides every source until the streaming finishes, which defeats the responsiveness the streaming was meant to deliver and trains users to wait for the end before they trust anything. Asking the model to weave citation markers into its prose and hoping it does so consistently is unreliable: marker formats drift, citations attach to the wrong span, and a free-form text channel cannot tell the user-interface code which characters are a citation and which are prose.

## Forces

- Citation events must align with generated tokens.
- Source spans need stable ids.
- UI needs to render mid-stream without flickering.

## Therefore

Therefore: emit citations as typed events on the same stream as the text, so that the UI can render verifiable source links in place as content appears.

## Solution

Define a streaming event vocabulary that includes citation events linked to source ids. The model is prompted to emit citation markers; the host extracts them into typed events alongside text deltas. The UI renders sources progressively. Final output includes a citation map.

## Structure

```
Retrieved sources (ids) -> LLM generates with citation markers -> Host splits stream into {text_delta | citation(source id, span)} events -> UI paints text and links spans to sources as they arrive -> done + final citation map
```

## Diagram

```mermaid
sequenceDiagram
  participant LLM
  participant Stream
  participant UI
  loop while generating
    LLM->>Stream: token
    Stream->>UI: paint token
    LLM->>Stream: cite[doc:42, span:300-340]
    Stream->>UI: linkify span to source
  end
```

*Citation Streaming attaches source spans to tokens as they arrive, so the UI can render verifiable links inline.*

## Example scenario

A medical-information agent answers 'what are the side effects of metformin?' As the answer streams to the user, each clinical claim arrives with a citation pointing back to the exact paragraph in the prescribing-information PDF. The user can click any sentence to verify the source — they don't have to trust the model alone.

## Consequences

**Benefits**

- Trust UX: claims trace to sources visibly.
- Hallucinations become visible (no source = suspicious).

**Liabilities**

- Streaming protocol is more complex.
- Citation event quality depends on model compliance.

## Failure modes

- Dropped markers — the model forgets to emit a citation marker for a claim, so the sentence streams with no source and the check fails only at the end.
- Misattached span — the citation event points at the wrong character range, and the UI links a sentence to a source that does not support it.
- Invalid source id — the model invents an id that is not in the retrieved set, and the UI renders a dead or wrong link.
- Marker leakage — the host fails to extract a marker in a drifted format, and raw citation syntax shows up in the prose.

## What this pattern constrains

Source claims in the output must reference a citation event with a valid source id.

## Applicability

**Use when**

- Outputs cite documents and users need to verify each claim.
- Regulatory or audit requirements demand source attribution at the span level.
- Trust depends on traceability from claim back to evidence.

**Do not use when**

- Outputs are creative and not grounded in retrievable documents.
- Latency-critical paths cannot afford citation rendering overhead.
- Citations would be noise — speed is more valuable than verifiability.

## Components

- LLM — emits prose tokens and citation markers anchored to source spans
- Stream multiplexer — separates text deltas from citation events into a typed channel
- Citation tracker — resolves marker ids to stable source records and maintains the final citation map
- UI renderer — paints tokens and linkifies cited spans progressively as events arrive
- Source index — document store the citation ids point back to for verification

## Tools

- Streaming LLM API — token-by-token output with structured citation emission
- Server-Sent Events transport — typed event channel carrying text and citation events in order
- Vector or document store — backs the source ids referenced by citation events

## Evaluation metrics

- Citation-attach rate — fraction of claim-bearing sentences that arrived with a resolved source
- Span-alignment error — distance between cited span and the sentence it should anchor
- Source-id validity rate — share of citation events whose id resolves in the source index
- Time-to-first-citation — latency from stream start to the first verifiable source link
- User click-through on citations — proxy for whether inline sources are trusted and used

## Known uses

- **[Perplexity](https://www.perplexity.ai/)** _available_
- **Anthropic Citations API** _available_
- **[ChatGPT](https://chat.openai.com/)** _available_
- **Gemini Deep Research** _available_
- **[Glean](https://www.glean.com/)** _available_

## Related patterns

- _specialises_ **Streaming Typed Events**
- _complements_ **Naive RAG**
- _alternative-to_ **Hallucinated Citations**
- _alternative-to_ **Attention-Manipulation Explainability**
- _complements_ **Citation Attribution**

## References

- [Anthropic: Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
