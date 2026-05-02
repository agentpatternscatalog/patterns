# Tool Result Caching

**Also known as:** Memoised Tools, Idempotent Cache

**Category:** Tool Use & Environment  
**Status in practice:** mature

## Intent

Cache the result of expensive deterministic tool calls keyed by their arguments so repeat calls within a session return immediately.

## Context

Agents that re-call the same tool with the same arguments multiple times within one task (lookups, computations, immutable reads).

## Problem

Repeat calls on the same arguments waste latency and money; the tool layer often has no awareness of caller behaviour.

## Forces

- Cache invalidation: when does the underlying data change?
- Per-user vs global caches differ on isolation guarantees.
- Cache hits hide tool latency the agent might benefit from learning about.


## Applicability

**Use when**

- Agents re-call the same tool with the same arguments multiple times within a task.
- Tools are deterministic enough to cache by normalised arguments.
- TTL and per-user vs global scoping can be defined per tool.

**Do not use when**

- Tool results are non-deterministic or time-sensitive (live state).
- Per-user scoping cannot be enforced and shared cache would leak data.
- Repeat-call rate is too low to recover the cache infrastructure cost.

## Solution

Wrap deterministic tools in a cache layered on `(tool_name, normalised_args)`. Set TTLs by tool type. On cache hit, return immediately without invoking the underlying tool. Per-user scoping for tools that read user data; global for read-only public data. Cache keys must include the auth subject (caller identity), not just args; args-only keys leak data when callers change.

## Example scenario

An agent that researches companies calls the same `get_company_profile(domain)` tool four times per session because different sub-tasks need it. Latency and per-call cost stack up. The team wraps deterministic tools in a cache keyed on `(tool_name, normalised_args)` with TTLs by tool type; per-user scoping keeps tenant-sensitive results from crossing accounts. Repeat calls return immediately, the underlying tool quota lasts longer, and session latency drops.

## Consequences

**Benefits**

- Latency drops on repeat calls.
- Cost reduction for paid APIs.

**Liabilities**

- Stale cache hits when underlying data changes.
- Non-deterministic tools cannot be cached safely.

## What this pattern constrains

Only tools declared deterministic may be cached; nondeterministic tools bypass the cache.

## Known uses

- **Most production agent platforms** — *Available*

## Related patterns

- *specialises* → [tool-use](tool-use.md)
- *complements* → [session-isolation](session-isolation.md)

**Tags:** cache, tool-use, performance
