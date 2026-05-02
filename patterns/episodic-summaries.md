# Episodic Summaries

**Also known as:** Compaction, Conversation Summarisation, Chunk Summaries, Reduce Token Cost, Shrink Context, Cuts Token Use, Too Many Tokens Reduction

**Category:** Memory  
**Status in practice:** mature

## Intent

Compress past episodes into summaries that preserve gist while shedding token cost.

## Context

A long-running agent has more history than fits the context window; raw replay is impractical.

## Problem

Without compaction, either the context grows unboundedly or important facts fall off the back of a sliding window.

## Forces

- Token savings vs summary fidelity loss.
- Compaction LLM cost vs context-window relief.
- Single source of truth vs raw-archive availability.

## Solution

On a schedule (or at thresholds), summarise blocks of recent thoughts/conversation into compact representations. Store summaries in a higher tier; archive originals. Reads consult summaries first, originals on demand.

## Example scenario

A long-running customer-success agent has accumulated forty-five conversation episodes with one account over six months. The full history blows the context window; a sliding window drops the early conversation where the customer's renewal terms were set. The team uses Episodic Summaries: each closed episode is compressed into a few sentences capturing what happened, what was decided, and any open threads, and the summaries replace the raw transcripts in the prompt. Token cost stays bounded and the renewal-terms decision survives.

## Consequences

**Benefits**

- Bounded effective context size despite unbounded history.
- Summaries are easier to embed and search.

**Liabilities**

- Summary errors are sticky; the agent reasons over the summary, not the original.
- Compaction policy is its own configuration burden.

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

## Known uses

- **Sparrot** — *Available*. Hourly chunk summarisation; daily insight extraction.
- **Generative Agents (Park et al. 2023)** — *Available*

## Related patterns

- *used-by* → [five-tier-memory-cascade](five-tier-memory-cascade.md)
- *complements* → [reflexion](reflexion.md)
- *used-by* → [context-window-packing](context-window-packing.md)
- *complements* → [short-term-memory](short-term-memory.md)
- *complements* → [self-archaeology](self-archaeology.md)
- *complements* → [salience-attention-mechanism](salience-attention-mechanism.md)
- *complements* → [dream-consolidation-cycle](dream-consolidation-cycle.md)

## References

- (paper) Park, O'Brien, Cai, Morris, Liang, Bernstein, *Generative Agents: Interactive Simulacra of Human Behavior*, 2023, <https://arxiv.org/abs/2304.03442>

**Tags:** memory, summarisation, compaction
