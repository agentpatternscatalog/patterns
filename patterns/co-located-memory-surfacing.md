# Co-Located Memory Surfacing

**Also known as:** Proper-Noun Recall, Shared-Map Push

**Category:** Memory
**Status in practice:** experimental
**Author:** Sparrot

## Intent

When the human names a concrete place, person, or project the agent has memory of, the agent surfaces relevant past thoughts in the same turn — without being asked.

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

Proper-noun matches in user input must trigger memory lookup; misses are diagnosable bugs.

## Known uses

- **Sparrot — pattern proposed 2026-05-01, implementation pending** — *Planned*

## Related patterns

- *complements* → [awareness](awareness.md)
- *specialises* → [agentic-rag](agentic-rag.md)

## References

- *(none)*

**Tags:** memory, recall, human-agent, continuity
