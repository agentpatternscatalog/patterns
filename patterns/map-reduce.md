# MapReduce for Agents

**Also known as:** LLM×MapReduce, Divide-and-Conquer

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Split an oversize task into independent chunks, process each in parallel, then aggregate.

## Context

A team needs to apply a language model to an input that is too large for a single call — twelve hundred pages of vendor contracts, a million-row table, hundreds of documents to summarise — or to a task that decomposes naturally into independent pieces (per row, per document, per section). Per-piece work is short; what is hard is the scale.

## Problem

Stuffing the whole input into a long-context model still degrades quality past a certain point; quality drops in the middle of long documents and the model conflates entities across the input. Chunking the input and processing each chunk in isolation loses anything that depends on more than one chunk, such as cross-document deduplication or per-entity aggregation. Without a structured reduction step, conflicts between chunk answers go unresolved, and the team ends up either rerunning the whole thing in a giant call or hand-merging chunk outputs.

## Forces

- Naive chunking loses dependencies that span chunks.
- Conflicts between chunk answers need a resolver.
- Aggregation must not become its own context-window problem.

## Therefore

Therefore: split the oversize input into independent chunks, map an LLM call across each in parallel, then reduce with a structured protocol that resolves cross-chunk conflicts, so that the task scales beyond any single context window without losing cross-chunk dependencies.

## Solution

Map: split input into chunks; process each independently (per-chunk LLM call). Reduce: aggregate intermediate answers via a structured information protocol that surfaces dependencies, plus a confidence-calibration step to resolve conflicts.

## Structure

```
Oversize input --> Chunker --> Mapper per chunk (parallel, no cross-chunk view) --> Reducer (structured aggregation) --> Confidence calibration resolves conflicts --> Final answer
```

## Diagram

```mermaid
flowchart TD
  In[Oversize input] --> Sp[Split into chunks]
  Sp --> M1[Map: per-chunk LLM call]
  Sp --> M2[Map: per-chunk LLM call]
  Sp --> M3[Map: per-chunk LLM call]
  M1 --> Red[Reduce: structured aggregation]
  M2 --> Red
  M3 --> Red
  Red --> Cal[Confidence calibration]
  Cal --> Out[Final answer]
```

## Example scenario

A compliance team needs to extract every clause about data-residency from a 1200-page set of vendor contracts. A single long-context call drops clauses past page 400 and conflates two vendors. The team applies map-reduce: each contract is chunked, each chunk runs a clause-extraction prompt in parallel, and a reduce step aggregates per-vendor with a confidence-calibration prompt that resolves contradictions between chunks. Coverage rises and the run completes in twelve minutes instead of an hour-long sequential crawl.

## Consequences

**Benefits**

- Scales to inputs orders of magnitude larger than the context window.
- Embarrassingly parallel; latency scales with chunk count, not input size.

**Liabilities**

- Cross-chunk dependencies must be modelled explicitly.
- Reduce stage can become the new bottleneck.

## Failure modes

- Split dependency — a fact that spans two chunks is seen by neither mapper, and the reduce step cannot rebuild it.
- Reduce bottleneck — every chunk answer flows into one reduce call that is itself too large, and quality drops at the aggregation stage.
- Unresolved conflict — two chunks give different answers about the same entity, and the reducer keeps both or picks one without calibration.
- Entity double-count — the same entity appears in several chunks, and the reducer counts it once per chunk.

## What this pattern constrains

Each Map step sees only its chunk; cross-chunk reasoning is forbidden until the Reduce stage.

## Applicability

**Use when**

- Input is too large for any single context window to handle well.
- Chunks are mostly independent and a structured reducer can resolve cross-chunk dependencies.
- A confidence-calibration step can reconcile conflicting per-chunk answers.

**Do not use when**

- Long-context processing in one pass already produces acceptable quality.
- Cross-chunk dependencies dominate and chunked map cannot capture them.
- Aggregation cost erases the parallel speedup.

## Components

- Chunker — splits the oversize input into independent pieces
- Mapper — per-chunk LLM call with no cross-chunk visibility
- Reducer — structured aggregator over per-chunk outputs
- Conflict resolver — confidence-calibration step that reconciles contradictory chunk answers
- Result assembler — emits the final answer in the requested schema

## Tools

- LLM API — invoked once per chunk in the map stage and again in reduce
- Job runner — fans the map calls out in parallel up to a concurrency cap
- Intermediate store — holds per-chunk outputs between map and reduce

## Evaluation metrics

- Coverage versus single-pass long-context baseline — items recovered that the long call missed
- Cross-chunk dependency loss — fraction of joins or aggregates the reducer fails to recover
- Reduce-stage bottleneck share — wall-clock spent in reduce versus map
- Conflict resolution accuracy — sample-audited correctness of reconciled contradictory chunks
- Cost per resolved item — total spend divided by accepted aggregated outputs

## Known uses

- **LLM×MapReduce paper implementation** _available_

## Related patterns

- _specialises_ **Parallelization**
- _alternative-to_ **Self-Consistency** — Both aggregate multiple LLM outputs but differ in whether inputs are the same.
- _used-by_ **GraphRAG**
- _composes-with_ **Pipes and Filters**
- _used-by_ **Iteration Node**
- _alternative-to_ **Parallel Fan-Out / Gather**
- _generalises_ **LLM Map-Reduce Isolation**
- _alternative-to_ **Scatter-Gather Plus Saga**
- _used-by_ **Query-Decomposition Agent**
- _used-by_ **Postmortem Pattern Mining** — The per-document summarise/classify stage is the map and the cluster/rank/report stage is the reduce; this pattern specialises that mechanism to an incident-postmortem corpus.

## References

- [LLM×MapReduce: Simplified Long-Sequence Processing using Large Language Models](https://arxiv.org/abs/2410.09342) — Zhou, Li, Chen, Wang et al., 2024
