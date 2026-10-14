# Episodic Summaries

**Also known as:** Compaction, Conversation Summarisation, Chunk Summaries, Reduce Token Cost, Shrink Context, Cuts Token Use, Too Many Tokens Reduction

**Category:** Memory  
**Status in practice:** mature

## Intent

Compress past episodes into summaries that preserve gist while shedding token cost.

## Context

A long-running agent has accumulated more conversation history, tool results, and intermediate reasoning than fits in the model's context window. Replaying the raw history on every turn is impossible because of size, and even when it would fit, it is wasteful to re-read all of it for what is usually a small follow-up step.

## Problem

Without some form of compaction, the agent has only two bad options. Either the context grows unboundedly until it overflows the window, at which point the call fails or the most recent state is silently dropped. Or a sliding-window strategy truncates the oldest content, which lets important early facts (the original task, an early decision the agent made, a constraint the user stated up front) fall off the back even though the agent still needs them. The team needs a way to summarise older history into compact episodes that retain the load-bearing facts while shedding the verbatim noise.

## Forces

- Token savings vs summary fidelity loss.
- Compaction LLM cost vs context-window relief.
- Single source of truth vs raw-archive availability.

## Therefore

Therefore: compress older episodes into tiered summaries while keeping originals archived, so that recent reasoning stays cheap to load and old reasoning stays recoverable on demand.

## Solution

On a schedule (or at thresholds), summarise blocks of recent thoughts/conversation into compact representations. Store summaries in a higher tier; archive originals. Reads consult summaries first, originals on demand.

## Structure

```
Recent thoughts / messages --threshold reached--> Summariser --> Higher-tier summary store + Archived originals; Read query --> Summaries first --need detail--> Originals
```

## Diagram

```mermaid
flowchart TD
  T[Recent thoughts / messages] --> Th{Threshold reached?}
  Th -- no --> T
  Th -- yes --> S[Summarise block into compact form]
  S --> H[Store in higher tier]
  S --> A[Archive originals]
  Q[Read query] --> H
  H -- need detail --> A
```

## Example scenario

A long-running customer-success agent has accumulated forty-five conversation episodes with one account over six months. The full history blows the context window; a sliding window drops the early conversation where the customer's renewal terms were set. The team uses Episodic Summaries: each closed episode is compressed into a few sentences capturing what happened, what was decided, and any open threads, and the summaries replace the raw transcripts in the prompt. Token cost stays bounded and the renewal-terms decision survives.

## Consequences

**Benefits**

- Bounded effective context size despite unbounded history.
- Summaries are easier to embed and search.

**Liabilities**

- Summary errors are sticky; the agent reasons over the summary, not the original.
- Compaction policy is its own configuration burden.

## Failure modes

- Summary drift — an error in one summary is reasoned over for many turns, and nobody checks the archived original.
- Dropped constraint — the summariser treats an early user constraint as noise, and the agent later breaks it.
- Poor thresholds — compaction runs too often and loses detail, or too rarely and the window still overflows.
- Dead archive — originals are archived but the read path never falls back to them when detail is needed.

## What this pattern constrains

Past events older than the compaction horizon are accessible only via summary, not raw.

## Applicability

**Use when**

- Conversation or thought history grows unboundedly without compaction.
- Summaries can preserve gist while shedding token cost meaningfully.
- Summarised tiers are consulted first with originals available on demand.

**Do not use when**

- History is naturally bounded and never approaches token limits.
- Lossy summarisation would drop critical facts the agent needs verbatim.
- Originals are not retained and summarisation errors would be irrecoverable.

## Components

- Threshold trigger — token-count, turn-count, or time-based rule that decides when a block is ready for compaction
- Summariser — LLM call that compresses a block of raw history into a compact representation
- Higher-tier summary store — holds the compact representation that reads consult first
- Originals archive — keeps verbatim source material available for on-demand reads when detail is needed
- Read router — looks at the summary tier first and falls back to the archive only on demand

## Tools

- Summarisation LLM — typically a smaller model than the agent's main one to keep compaction cost down
- Object or document store — durable archive for originals (S3, GCS, Postgres JSONB)
- Summary store — separate index or table for the compacted tier so it can be queried independently

## Evaluation metrics

- Token-saving ratio — verbatim tokens replaced per summary token; targets the 5-10x range typical in published work
- Summary-fidelity audit — sampled diff between summary and originals on load-bearing facts
- Sticky-error rate — frequency of downstream mistakes traced to a wrong summary that hid the truth
- Fallback-to-original rate — how often reads have to drop down to the archive, signalling weak summaries
- Compaction cost per episode — money and latency spent on the summariser per closed block

## Known uses

- **Generative Agents (Park et al. 2023)** _available_

## Related patterns

- _used-by_ **Five-Tier Memory Cascade**
- _complements_ **Reflexion**
- _used-by_ **Context Window Packing**
- _complements_ **Short-Term Thread Memory**
- _complements_ **Self-Archaeology**
- _complements_ **Salience Attention Mechanism**
- _complements_ **Dream Consolidation Cycle**
- _alternative-to_ **Cluster-Capped Insight Store**
- _complements_ **Sleep-Time Compute**
- _used-by_ **Episodic Memory**
- _complements_ **Procedural Memory**
- _complements_ **Agentic Memory**
- _complements_ **Context Window Dumb-Zone Cap**
- _complements_ **Information Chunking for Agent Memory**
- _complements_ **Trajectory-Summary Test-Time Scaling** — Both compress a trajectory to a summary; episodic-summaries does it to save memory cost, this does it to make rollouts selectable.

## References

- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — Park, O'Brien, Cai, Morris, Liang, Bernstein, 2023
