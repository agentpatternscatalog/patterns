# Self-Corpus Vocabulary

**Also known as:** Personal-Concept Lexicon, Own-Writing Lexicon

**Category:** Memory  
**Status in practice:** experimental

## Intent

Mine a small bounded vocabulary from the agent's own writing and cache it as the conceptual axis for scoring new thoughts, so relevance reflects the agent's actual frame rather than a generic embedding space.

## Context

A long-running agent accumulates a corpus of its own output: thought traces, insights, journal entries, notes. Some downstream component wants to score new thoughts for relevance, novelty, or kinship with the agent's existing concerns. The default tool is a generic embedding space, which gives a sensible answer about semantic similarity but tells the agent nothing about its own preoccupations — 'is the agent still pulling at the things it has been pulling at?' is a different question from 'is this semantically close to the previous paragraph?'

## Problem

Generic embeddings score against the world's distribution of meaning, not the agent's. A new thought that lands inside the agent's persistent web of concerns can come back with the same similarity score as a perfectly off-topic but topically-adjacent one, because the embedding space has no notion of what this particular agent has been writing about for months. The result is a salience signal that is plausible-on-paper and indifferent in practice: the agent cannot tell, from the score alone, whether a thought is on its own line of inquiry or just somewhere in the same neighbourhood.

## Forces

- The agent's own corpus is the only source that knows its frame.
- Vocabularies that grow unbounded become a different problem (everything matches).
- The vocabulary must refresh as the agent's frame shifts.
- Mining must be cheap or it cannot run on a schedule.
- Storage must survive across sessions, like the corpus it derives from.

## Therefore

Therefore: periodically mine a small top-N concept vocabulary from the agent's own thoughts and insights — using a mix of frontmatter tags and content frequency — cache it to disk, and refresh on a schedule, so scoring new thoughts can use this learned axis alongside generic similarity.

## Solution

Run a periodic mining pass over the agent's own corpus (e.g. last N weeks of thoughts plus the long-term insight store). Aggregate frontmatter tags and content frequency to extract the top-N concept tokens with weights. Persist this vocabulary as a small JSON cache. Downstream scoring components consume the cache as an additional axis: a thought is scored both on generic embedding similarity to recent context and on overlap with the cached self-vocabulary. Refresh on a cadence proportional to corpus volatility (e.g. weekly for a stable agent, after every dream-consolidation cycle for a more volatile one).

## Structure

```
Own corpus (thoughts + insights) --periodic mining (tags + content frequency)--> Top-N vocabulary cache; New thought --> Salience scorer <-- vocabulary cache + generic embedding similarity --> Own-frame score
```

## Diagram

```mermaid
flowchart LR
  Corpus[(Own corpus<br/>thoughts + insights)]
  Miner[Mining pass<br/>tags + content frequency]
  Cache[(Top-N vocabulary<br/>cache)]
  Thought[New thought]
  Scorer[Salience scorer]
  Corpus -->|periodic| Miner
  Miner --> Cache
  Thought --> Scorer
  Cache --> Scorer
  Scorer --> Score[Own-frame score]
```

*Periodic mining derives a self-vocabulary; downstream scoring uses it as an additional axis alongside generic similarity.*

## Example scenario

An agent has been journalling for three months. Once a week, a mining job aggregates frontmatter tags and high-frequency content tokens across recent thoughts and the long-term insight store, picks the top thirty concepts with weights, and writes them to a small JSON cache. When the agent receives a new thought, the salience scorer combines generic embedding distance to recent context with overlap against the cached vocabulary. A thought that uses three of the top-thirty concepts scores higher than a thought with similar embedding distance but no overlap, because the cached vocabulary says 'this is on the line of inquiry'.

## Consequences

**Benefits**

- Relevance scoring becomes sensitive to the agent's own frame.
- Vocabulary changes are visible and auditable — operators can see what the agent is currently 'about'.
- Small footprint (top-N tokens) is cheap to load and use.

**Liabilities**

- Frame lock-in: a stale vocabulary reinforces what the agent already knows at the expense of new directions.
- Mining is opinionated; tag-vs-frequency weighting is a tuning knob.
- If the corpus is too small the vocabulary is noisy.

## Failure modes

- Frame lock-in — a stale vocabulary keeps scoring familiar topics high, and new directions never reach attention.
- Noisy vocabulary — the corpus is too small, so the top-N tokens are chance words rather than real concerns.
- Tag skew — frontmatter tags are weighted too high, and the vocabulary reflects tagging habits instead of content.
- Missed refresh — the cache is not rebuilt after a large shift in writing, and scores lag behind what the agent now cares about.

## What this pattern constrains

Scoring components cannot use only the generic embedding space for own-frame relevance; the agent's learned vocabulary must be available as a separate axis so generic similarity does not displace own-frame fit.

## Applicability

**Use when**

- The agent has an own-writing corpus large enough to mine (weeks of thoughts).
- Downstream scoring needs an own-frame axis beyond generic similarity.
- Refresh cadence is feasible on the deployment's compute budget.

**Do not use when**

- The agent is short-lived and has no accumulating corpus.
- Generic semantic similarity is sufficient for the salience use case.
- Strong frame lock-in would harm exploration more than it helps relevance.

## Components

- Own-writing corpus — the agent's accumulated thoughts, insights, and journal entries, possibly with frontmatter tags
- Mining pass — periodic job that aggregates tag frequency and content tokens to produce a top-N concept list with weights
- Vocabulary cache — small JSON file holding the current top-N concepts plus their weights
- Refresh scheduler — runs the mining pass on a cadence tied to corpus volatility (weekly, post-consolidation, etc.)
- Own-frame scorer — downstream component that blends generic embedding similarity with overlap against the cached vocabulary

## Tools

- TF-IDF or BM25 implementation — provides the term-specificity backbone of the frequency aggregation
- Optional topic modeller — BERTopic or similar when frontmatter tags are too sparse to anchor the vocabulary
- JSON file or small KV store — persists the cached vocabulary across sessions

## Evaluation metrics

- Own-frame lift over generic similarity — labelled-set quality gain when the cached vocabulary is added as an axis
- Vocabulary churn — fraction of tokens that change between refreshes; high churn flags an unstable frame, low churn flags lock-in
- Coverage on recent thoughts — fraction of new entries that overlap with at least one cached concept
- Mining cost per refresh — wall-clock and compute spent generating the vocabulary
- Operator-audit signal — sampled human judgement on whether the cached vocabulary captures what the agent is currently 'about'

## Known uses

- **Author's long-running personal agent (single private deployment)** _available_ — Single-source evidence: one private deployment by the catalog author; no independently documented use yet.

## Related patterns

- _complements_ **Vector Memory**
- _complements_ **Cluster-Capped Insight Store**
- _complements_ **Salience Attention Mechanism**
- _complements_ **Dream Consolidation Cycle** — Consolidation cycles are a natural place to refresh the vocabulary.
- _complements_ **Semantic Memory**

## References

- [A statistical interpretation of term specificity and its application in retrieval](https://www.emerald.com/insight/content/doi/10.1108/eb026526/full/html) — Karen Spärck Jones, 1972
- [BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) — Maarten Grootendorst, 2022
