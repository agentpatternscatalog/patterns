# Cross-Session Memory

**Also known as:** Persistent User Memory, Long-Lived User Profile, Beat Agent Amnesia, No-Forget Memory, Agent Forgets Between Sessions, Session-to-Session Memory

**Category:** Memory  
**Status in practice:** mature

## Intent

Persist user-specific facts, preferences, and prior context across all sessions, threads, and devices.

## Context

User-facing assistants where users expect continuity beyond a single conversation.

## Problem

Per-thread memory loses everything between sessions; users repeat themselves; the assistant feels amnesic.

## Forces

- What to remember vs forget; user agency.
- Privacy, deletion, portability requirements.
- Cost of always-on memory loading per turn.

## Solution

Maintain a per-user store of distilled facts (preferences, prior context, names, projects). Load relevant slices into each session's context. Provide explicit add/forget tools. Audit and surface memory entries to the user. Deletion controls and a user-visible memory inspector (delete / disable / export) satisfy regulatory and trust requirements.

## Consequences

**Benefits**

- Continuity across sessions and devices.
- Compounding usefulness over time.

**Liabilities**

- Privacy obligations.
- Memory hallucinations are stickier than chat hallucinations.

## What this pattern constrains

Memory entries must be added through declared tools; the model cannot silently mutate persistent user state.

## Applicability

**Use when**

- Per-thread memory loses important user-specific facts between sessions and the assistant feels amnesic.
- A per-user store of distilled facts can be maintained with audit, deletion, and forget controls.
- Loaded memory slices meaningfully improve responses across sessions.

**Do not use when**

- Sessions are deliberately stateless for privacy or compliance reasons.
- No reliable distillation step exists and the store would fill with noise.
- Users expect a fresh agent per session and persistent memory would surprise them.

## Known uses

- **ChatGPT Memory** — *Available*
- **Claude Projects + memory** — *Available*
- **Letta** — *Available*
- **Lindy memory** — *Available*

## Related patterns

- *complements* → [short-term-memory](short-term-memory.md)
- *alternative-to* → [memgpt-paging](memgpt-paging.md)
- *complements* → [session-isolation](session-isolation.md)

## References

- (blog) *OpenAI: Memory and new controls for ChatGPT*, 2024, <https://openai.com/index/memory-and-new-controls-for-chatgpt/>

**Tags:** memory, persistence, user
