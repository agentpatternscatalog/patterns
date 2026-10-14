# Semantic Memory

**Also known as:** Fact Memory, Agent Knowledge Store, Knowledge Memory

**Category:** Memory  
**Status in practice:** emerging

## Intent

Maintain a dedicated store of what the agent holds to be true about the user and the world, separate from event records (episodic) and learned how-to (procedural).

## Context

An agent operates across many sessions and accumulates durable knowledge: who the user is, what they prefer, what is definitionally true about the domain, what conclusions have settled. This knowledge needs to survive across sessions, be retrievable when relevant, and stay separate from the raw event history that produced it. The team is choosing how this fact layer is represented and queried independently of any single storage technology.

## Problem

Without a dedicated semantic store, every fact the agent 'knows' either lives in a static system prompt (frozen, cannot grow with experience) or is re-derived from raw episodes on every turn (slow, lossy, and prone to drift between runs). Mixing facts with raw events also confuses retrieval — 'user prefers dark mode' gets stored as 'on 2026-03-12 the user said: I prefer dark mode' and surfaces only by similarity to that timestamp's wording, not as a stable assertion. The CoALA framework names semantic memory as a distinct long-term type for exactly this reason: the agent needs a layer that holds *what is true*, separately from *what happened* and *how to act*.

## Forces

- Substrate is a separate choice from function: vector index, knowledge graph, JSON profile, or text can all back semantic memory, with different retrieval and update characteristics.
- Facts decay: yesterday's truth ('user is on Pacific time') becomes today's fiction, so invalidation and recency must be explicit.
- Conflict resolution: two contradicting assertions must be resolved at write time or read time, not papered over.
- Provenance matters: extracted facts can be wrong; the agent must record whether a fact came from the user, was inferred, or was imported, and what episode produced it.

## Therefore

Therefore: maintain a dedicated semantic-memory layer keyed by entity and attribute, populated by explicit extraction or assertion with provenance, and queried at decision-time independently from episodic recall — choose the substrate (vector, graph, profile) to fit the retrieval pattern, not the other way round.

## Solution

The CoALA framework (Sumers et al. 2023) names semantic memory as one of three long-term memory types alongside episodic and procedural, defined by function rather than storage. Implementations vary by substrate: LangMem's semantic channel uses profile (single JSON document) or collection (many documents) stores; knowledge-graph implementations (cognee, Zep) store assertions as typed triples; vector stores can back it when retrieval is by similarity over fact text. The function is the same regardless: extract durable assertions from interactions, store them with entity/attribute keys and provenance, retrieve them when the situation calls for 'what does the agent know about X'. Refer to [[vector-memory]] and [[knowledge-graph-memory]] as substrate options.

## Structure

```
Episode / interaction --extractor--> Assertion (entity, attribute, value, provenance) --> Semantic memory (substrate: vector store | knowledge graph | JSON profile); Query 'what is known about X' --entity/attribute lookup--> Fact + provenance --> Context; contradiction --> invalidate
```

## Diagram

```mermaid
flowchart TD
  Ev[Episode / interaction] --> Ext[Extractor]
  Ext --> A[Assertion: entity, attribute, value, provenance]
  A --> Sem[(Semantic memory)]
  Sem -.substrate.-> V[Vector store]
  Sem -.substrate.-> KG[Knowledge graph]
  Sem -.substrate.-> P[JSON profile]
  Q[Decision: what does the agent know about X?] --> Lookup[Entity/attribute lookup]
  Lookup --> Sem
  Lookup --> Out[Fact + provenance]
  Out --> Ctx[Prepend to context]
  Sem --> Inv[Invalidate on contradiction]
```

## Example scenario

A long-running personal assistant has logged hundreds of conversations with one user. Buried in those logs are durable facts: the user's timezone, their preferred language, their dietary restrictions, the names of their kids, their employer. Treating all of this as episodic recall is wasteful — every time the agent needs the timezone, it would have to semantically retrieve old messages, parse out a date claim, and trust whichever match came up first. The team instead adds a semantic-memory layer: a small extraction step writes assertions like (user, timezone, 'Europe/Berlin', source-episode-id, 2026-04-12) into a profile store. Retrieval at decision time is now a direct lookup, the episode that produced the fact is still recoverable via provenance, and invalidating the timezone when the user moves is one write.

## Consequences

**Benefits**

- Stable facts survive across sessions without re-derivation from raw episodes.
- Retrieval becomes assertion-shaped rather than event-shaped — 'what is the user's timezone' returns the fact, not the conversation in which it was set.
- Substrate decisions can change (vector → graph, profile → collection) without changing the agent's contract with the memory.

**Liabilities**

- Extraction errors are sticky — a wrong fact poisons every later turn until invalidated.
- Conflict resolution policy is its own design problem.
- Provenance and update governance add real implementation cost beyond the substrate itself.

## Failure modes

- Sticky wrong fact — the extractor stores a misheard preference, and every later turn acts on it until someone invalidates it.
- Unresolved conflict — two contradicting assertions about the same attribute coexist, and the agent picks one at random.
- Event stored as fact — a raw event is written in place of an assertion, and lookups by entity and attribute miss it.
- Missing provenance — a fact has no source attached, so nobody can tell why the agent believes it or whether to keep it.

## What this pattern constrains

Forbids treating raw event records as facts. The semantic layer stores assertions about *what is true*; the episodic layer stores happenings; assertions are written by an explicit extraction or assertion step, not by appending raw events.

## Applicability

**Use when**

- The agent needs to remember durable facts (user preferences, domain truths, settled conclusions) across sessions.
- Retrieval by 'what does the agent know about X' must be cheap and substrate-agnostic.
- Facts must be updatable and invalidatable independently of the events that produced them.

**Do not use when**

- Memory needs are session-scoped and a typed short-term state suffices.
- The agent has no extraction pipeline and assertions would be polluted by raw event text.
- Provenance and conflict resolution cannot be enforced — without them the store rots quickly.

## Components

- Extractor — converts raw episodes into typed assertions with entity, attribute, value, and provenance
- Assertion store — substrate-agnostic layer holding facts keyed by entity/attribute
- Substrate adapter — concrete backing: vector index, knowledge graph, JSON profile, or document collection
- Provenance tracker — records which episode produced each assertion so facts can be audited and invalidated
- Conflict resolver — handles contradicting assertions at write time or read time per chosen policy

## Tools

- LangMem semantic channel — production library implementing profile and collection stores
- Knowledge graph backend — Neo4j, RDF triple store, or in-memory graph for symbolic substrate
- Vector database — Pinecone, Weaviate, pgvector when similarity-over-fact-text is the right retrieval shape
- Extraction LLM — typically a smaller model that distils assertions from raw episodes

## Evaluation metrics

- Fact recall — fraction of labelled durable facts retrievable when the situation requires them
- Stale-fact rate — share of returned facts that no longer hold (the user moved, the preference changed)
- Conflict-resolution latency — time between a contradicting assertion arriving and the store stabilising
- Provenance coverage — share of stored assertions with traceable source episodes
- Substrate-swap cost — engineering days to change vector→graph or profile→collection without breaking the agent contract

## Known uses

- **[LangChain LangMem SDK — semantic channel (profile and collection stores)](https://www.langchain.com/blog/langmem-sdk-launch)** _available_
- **[CoALA framework — semantic memory as third long-term memory type](https://arxiv.org/abs/2309.02427)** _available_
- **[cognee — knowledge-graph-backed semantic store for agents](https://www.cognee.ai/)** _available_
- **[Mem0 — facts and preferences API for agent memory](https://mem0.ai/)** _available_

## Related patterns

- _complements_ **Episodic Memory**
- _complements_ **Procedural Memory**
- _uses_ **Vector Memory** — Vector store is one substrate option for semantic memory.
- _uses_ **Knowledge Graph Memory** — Knowledge graph is one substrate option for semantic memory.
- _specialises_ **Cross-Session Memory**
- _complements_ **Self-Corpus Vocabulary**
- _composes-with_ **Agentic Memory**
- _complements_ **World-Model Graph Memory**
- _complements_ **Memory-Type Storage Specialization**
- _complements_ **Three Layers of Agentic AI Memory**

## References

- [Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427) — Sumers, Yao, Narasimhan, Griffiths, 2023
- [LangGraph Memory Concepts — semantic, episodic, procedural types](https://docs.langchain.com/oss/python/concepts/memory) — 2025
- [LangMem SDK launch — semantic, episodic, procedural channels](https://www.langchain.com/blog/langmem-sdk-launch) — 2025
