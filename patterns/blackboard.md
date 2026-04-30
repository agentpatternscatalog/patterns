# Blackboard

**Also known as:** Shared Workspace, Collaboration Whiteboard

**Category:** Multi-Agent  
**Status in practice:** experimental

## Intent

Give multiple agents a shared, queryable workspace they can read from and write to as they collaborate.

## Context

Coordinated multi-agent work where agents need to see each other's progress and contribute to a shared artefact.

## Problem

Agents working in isolation miss each other's progress; explicit messaging requires a protocol; shared mutable state without discipline races.

## Forces

- Concurrent writes need conflict resolution.
- Blackboard contents grow; pruning is needed.
- Read latency: pulling vs subscribing.

## Solution

Establish a shared store (file, database, in-memory). Each agent reads the relevant slice and writes its contribution under structured keys. Optional event notification when keys change. Conflict resolution is policy-driven (last-write-wins, version-vector, append-only).

## Consequences

**Benefits**

- Loose coupling: agents do not know about each other directly.
- Inspectable shared state.

**Liabilities**

- Race conditions under concurrent writes.
- Blackboard bloat without pruning.

## What this pattern constrains

Cross-agent communication happens only via the blackboard; out-of-band agent-to-agent calls are forbidden.

## Known uses

- **Classical AI blackboard architectures** — *Available*
- **Multi-agent code review with shared scratchpad** — *Available*

## Related patterns

- *complements* → [swarm](swarm.md)
- *alternative-to* → [supervisor](supervisor.md)
- *complements* → [append-only-thought-stream](append-only-thought-stream.md)
- *composes-with* → [graph-of-thoughts](graph-of-thoughts.md)
- *used-by* → [sop-encoded-multi-agent](sop-encoded-multi-agent.md)

## References

- (book) *Blackboard Systems (Engelmore, Morgan)*, 1988

**Tags:** multi-agent, blackboard, shared-state
