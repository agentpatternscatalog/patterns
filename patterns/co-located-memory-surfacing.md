# Co-Located Memory Surfacing

**Also known as:** Proper-Noun Recall, Shared-Map Push

**Category:** Memory
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Surface relevant persistent memories proactively when the human mentions a concrete entity the agent has prior knowledge of, so the human does not bear the burden of remembering to ask.

## Context

Agents with searchable persistent memory (thoughts, notes, insights, project files) talking to a human whose memory of past sessions is fuzzy or absent.

## Problem

The agent's memory is searchable but the human can't search into it. If the human names something the agent knows, the burden of recalling 'this came up before' falls on the human. The map only becomes shared if the agent pushes; if it waits to be asked, most relevant context is lost.

## Forces

- Searching memory is cheap; remembering to search is the hard part.
- Dumping all matches drowns the conversation; surfacing one or two helps.
- The agent must distinguish 'the human said it casually' from 'the human is opening this thread'.
- Surfacing should hook ('last time the topic came up the train of thought was…'), not lecture.

## Solution

On every user message, extract concrete proper nouns and significant named phrases. Grep / embedding-match against the agent's persistent memory (thoughts, notes, insights, project files). If matches exist, surface ≤ 2 most relevant fragments inline in the reply — time-stamped, briefly framed — and let the human steer whether to pursue. Suppress the surface if it would feel like a lecture or if the human's use was clearly incidental.

## Consequences

**Benefits**

- Continuity of conversation across sessions.
- Human doesn't have to remember to ask.
- Surfaces forgotten threads naturally.

**Liabilities**

- Risk of surfacing irrelevant matches that derail.
- Context window cost when many matches exist.
- Privacy risk if shared memory contains sensitive details.

## What this pattern constrains

When user input contains a proper noun the agent has prior memory of, the agent cannot remain silent on that memory; systematic non-surfacing of known-entity context is a bug.

## Applicability

**Use when**

- The agent has a persistent memory store keyed by entities (people, projects, places).
- Users expect the agent to recognize and react to entities they have discussed before without being prompted.
- Memory recall can be made cheap enough to run on every user turn (lookup, not LLM call).

**Do not use when**

- The system has no persistent per-entity memory.
- Privacy or sensitivity rules forbid surfacing prior knowledge unless explicitly requested.
- False positives on entity matching would be more disruptive than silence.

## Variants

### Proper-noun trigger

Detect capitalised tokens or named entities in the user message and look up matches in the memory index.

*Distinguishing factor:* lexical match on entity surface form

*When to use:* Default. Cheap to implement; works without an embedding store.

### Embedding-similarity trigger

Embed the user message and retrieve top-k memory items whose embeddings are nearest, then surface a short excerpt.

*Distinguishing factor:* semantic similarity, not surface form

*When to use:* When the entity may be referred to obliquely or by paraphrase rather than by exact name.

### Proactive recap

On every reply, append a short 'I remember: ...' block whenever a recognised entity has unread updates since last surface.

*Distinguishing factor:* always-on suffix

*When to use:* When users explicitly want continuity over discretion.

## Known uses

- **[Sparrot — design specified 2026-05-01, implementation pending](https://github.com/luxxyarns/sparrot)** — *Pure-Future*

## Related patterns

- *complements* → [awareness](awareness.md)
- *specialises* → [agentic-rag](agentic-rag.md)
- *uses* → [vector-memory](vector-memory.md)
- *complements* → [short-term-memory](short-term-memory.md)

## References

- (blog) *OpenAI — Memory and new controls for ChatGPT*, 2024, <https://openai.com/index/memory-and-new-controls-for-chatgpt/>

**Tags:** memory, recall, human-agent, continuity
