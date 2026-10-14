# Episodic Memory

**Also known as:** Event Memory, Experience Store, Memory Stream

**Category:** Memory  
**Status in practice:** mature

## Intent

Record past events as time-stamped first-person experiences the agent can recall later, separately from extracted facts (semantic) and learned how-to (procedural).

## Context

An agent needs to remember what happened — when, in what order, with what context and outcome. This is the autobiographical layer: a record that yesterday the user asked about X, the agent answered Y, the user pushed back, and the two converged on Z. Whether the events are conversations, tool calls, observations, or internal reasoning steps, the function is the same: preserve the temporal-experiential structure of past interactions so the agent can reflect, learn, and surface relevant prior episodes.

## Problem

If the agent has only a fact store, it can answer 'what is true' but not 'what happened' — it loses the ability to learn from specific past interactions, to surface relevant prior episodes by recency or salience, or to reflect on its own behaviour. If the agent collapses every interaction into facts at write-time, it destroys the causal chain — the user said this, then the agent did that, then it broke — that makes debugging and reflection possible. The CoALA framework names episodic memory as a distinct long-term type for this reason: the agent needs a layer that preserves events as events, with their temporal structure intact.

## Forces

- Episodic stores grow unboundedly with time — needs compaction, paging, or salience-based pruning.
- Retrieval by similarity alone misses temporal queries ('what did I do yesterday') and recency-sensitive queries.
- Raw episode replay is too noisy for prompt context — needs salience scoring, summarisation, or reflection passes to be useful.
- Privacy and tenant isolation: episodes contain user content and must respect session and user boundaries.

## Therefore

Therefore: maintain an append-only episodic store of time-stamped events, retrievable by some combination of recency, similarity, and salience, and feed it into compaction or reflection passes that distil reusable insights into the semantic and procedural layers.

## Solution

Park et al.'s Generative Agents memory stream (2023) is the canonical implementation: every observation is logged with a timestamp and an importance score; retrieval combines recency, relevance, and importance; a periodic reflection pass derives higher-level insights from clusters of recent episodes. LangMem's episodic channel stores past interactions for few-shot retrieval and procedure distillation. Substrate is orthogonal to function: vector store ([[vector-memory]]), append-only log ([[append-only-thought-stream]]), or structured journal can all back episodic memory. Compaction is typically delegated to [[episodic-summaries]]; consolidation into facts feeds [[semantic-memory]]; consolidation into skills feeds [[procedural-memory]].

## Structure

```
Observation --stamp time + importance--> Episodic memory (vector store | append-only log | journal); Query --recency + similarity + importance--> Top-k episodes --> Context; Episodic memory --reflection pass--> {Semantic facts, Procedural recipes, Episodic summaries}
```

## Diagram

```mermaid
flowchart TD
  Obs[Observation / interaction] --> Stamp[Stamp with time + importance]
  Stamp --> Ep[(Episodic memory)]
  Ep -.substrate.-> V[Vector store]
  Ep -.substrate.-> Log[Append-only log]
  Ep -.substrate.-> J[Structured journal]
  Q[Query: what happened around X?] --> Ret[Retrieve by recency + similarity + salience]
  Ret --> Ep
  Ret --> Top[Top-k relevant episodes]
  Top --> Ctx[Prepend to context]
  Ep --> Refl[Reflection / consolidation pass]
  Refl --> Sem[Semantic memory: extracted facts]
  Refl --> Proc[Procedural memory: learned recipes]
  Refl --> Sum[Episodic summaries: compacted tier]
```

## Example scenario

A coding agent has worked with a developer across hundreds of tickets over six months. The developer later asks the agent to explain how the team ended up with the weird workaround in the auth module. A pure semantic store would return facts like (auth-module, uses-workaround, true) — useless. An episodic store returns the actual sequence: on 2026-02-14 the developer flagged a CVE, on 2026-02-15 the agent proposed a fix, the proposed fix broke a downstream test, on 2026-02-16 they agreed on a workaround instead with a TODO. The agent can now answer the why. The episodic store also feeds a weekly reflection pass that consolidates 'workaround in auth-module' into a semantic fact and 'CVE-flag → propose fix → test → workaround-with-TODO' into a procedural template.

## Consequences

**Benefits**

- Causal chains survive — the agent can reconstruct what happened, in order, with context.
- Reflection and consolidation become possible: episodes feed semantic and procedural extraction.
- Temporal queries ('what did I do yesterday', 'what changed since last week') are answerable directly.

**Liabilities**

- Unbounded growth — needs compaction, decay, or tiered storage.
- Raw episode prompts are noisy — direct injection without salience scoring degrades reasoning.
- Privacy and retention boundaries are harder to enforce on event logs than on extracted facts.

## Failure modes

- Unbounded log — episodes pile up with no compaction, and retrieval slows and costs more over time.
- Noisy injection — raw episodes are put into the prompt without salience scoring, and the model reasons from irrelevant detail.
- Flattened causality — interactions are turned into facts at write time, and the order of events needed for debugging is lost.
- Retention breach — event logs keep personal details past their allowed retention because no boundary is enforced on them.

## What this pattern constrains

Forbids collapsing every interaction into facts at write-time. Episodes keep their identity (timestamp, context, outcome) and are queried as events; extraction into facts or skills is a separate, downstream step.

## Applicability

**Use when**

- The agent needs to recall specific past interactions, not just distilled facts.
- Reflection or consolidation passes need raw episodes as input to derive insights or procedures.
- Temporal queries ('what did I do yesterday', 'what changed since last week') matter.

**Do not use when**

- Retention or privacy constraints make event logs untenable and only extracted facts are allowed.
- Session is single-turn and there is no future to reflect from.
- Storage and compaction infrastructure cannot be maintained at the required scale.

## Components

- Event logger — time-stamps each observation/interaction and writes it to the episodic store
- Importance scorer — assigns a salience score per event to drive later retrieval and consolidation
- Episodic store — substrate-agnostic layer holding time-stamped events with metadata
- Substrate adapter — concrete backing: vector index, append-only log, or structured journal
- Retriever — combines recency, similarity, and salience to surface top-k relevant past episodes
- Reflection pass — periodically reads recent episodes and consolidates into semantic/procedural memory

## Tools

- Vector database — Pinecone, Weaviate, pgvector when similarity is the dominant retrieval axis
- Append-only log store — Postgres, S3+object-log, or event store preserving strict order
- Reflection LLM — periodically reads recent episodes and writes back consolidated assertions
- LangMem episodic channel — production library implementing few-shot-from-episodes retrieval

## Evaluation metrics

- Episode recall — fraction of labelled relevant past episodes returned by the retriever for matching queries
- Temporal-query accuracy — share of 'what did I do at time T' style queries answered correctly
- Reflection yield — number of episodic clusters that produce a useful semantic or procedural artifact per pass
- Storage growth — episodes per day vs the compaction policy's target steady-state
- Privacy-boundary breach rate — incidents where episodes from one user surfaced to another

## Known uses

- **[Generative Agents memory stream (Park et al. 2023)](https://arxiv.org/abs/2304.03442)** _available_
- **[LangChain LangMem SDK — episodic channel](https://www.langchain.com/blog/langmem-sdk-launch)** _available_
- **[CoALA framework — episodic memory as second long-term type](https://arxiv.org/abs/2309.02427)** _available_
- **[Letta recall and archival memory — partial implementation (episodic + semantic conflated)](https://docs.letta.com/)** _available_

## Related patterns

- _complements_ **Semantic Memory**
- _complements_ **Procedural Memory**
- _uses_ **Vector Memory** — Vector store is one substrate option for episodic memory.
- _uses_ **Append-Only Thought Stream** — Append-only log is one substrate option preserving causal order.
- _uses_ **Episodic Summaries** — Summarisation is the standard compaction mechanism for episodic stores.
- _complements_ **Salience Attention Mechanism**
- _complements_ **Hippocampal Rehearsal**
- _composes-with_ **Agentic Memory**
- _complements_ **Memory-Type Storage Specialization**
- _complements_ **Three Layers of Agentic AI Memory**
- _complements_ **Test-Time Memorization (Titans)**

## References

- [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) — Park, O'Brien, Cai, Morris, Liang, Bernstein, 2023
- [Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427) — Sumers, Yao, Narasimhan, Griffiths, 2023
- [LangGraph Memory Concepts — semantic, episodic, procedural types](https://docs.langchain.com/oss/python/concepts/memory) — 2025
- [LangMem SDK launch — semantic, episodic, procedural channels](https://www.langchain.com/blog/langmem-sdk-launch) — 2025
