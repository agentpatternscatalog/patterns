# Bidirectional Impulse Channel

**Also known as:** Two-Way Chat, User-and-Agent-Initiated Communication

**Category:** Streaming & UX  
**Status in practice:** experimental

## Intent

Let the user inject impulses into the agent and let the agent push messages to the user, both through one channel.

## Context

Long-running agents (cognitive loops, monitoring agents) that have continuous internal activity the user might want to influence or be informed of.

## Problem

Pure request/response chat misses the long-running case; pure push notifications are intrusive without a back-channel.

## Forces

- Push hygiene: too many messages train users to ignore the channel.
- Inverse: starvation when the agent waits forever.
- Authority: not every user-typed line should be a command.

## Solution

A single CLI/chat surface where the user can send commands (`!rule ...`, `!goal ...`, `!forget ...`) that bypass the model and write directly to memory, while the agent can push messages when salience clears a threshold (insight, stuck focus, contradiction, goal complete). Hygiene rule: at most one unsolicited message per window.

## Consequences

**Benefits**

- User feels the agent is alive without being noisy.
- Direct memory edits are auditable and reversible.

**Liabilities**

- Salience threshold tuning is empirical.
- Direct memory edits bypass the LLM and can encode wrong rules.

## What this pattern constrains

The agent may push at most one unsolicited message per window; user commands beginning with `!` bypass the model entirely.

## Applicability

**Use when**

- The agent runs long enough that pure request-response chat misses the point.
- Users want to inject commands or facts that bypass the model and write directly to memory.
- Salience signals exist that justify agent-initiated push messages without spamming the user.

**Do not use when**

- Interactions are bounded turn-pairs with no need for a back-channel.
- Push notifications are always intrusive in the deployment context (e.g. shared work surface).
- There is no salience function and the agent would push noise.

## Known uses

- **Sparrot** — *Available*. CLI as bidirectional impulse channel.

## Related patterns

- *uses* → [salience-triggered-output](salience-triggered-output.md)
- *complements* → [streaming-typed-events](streaming-typed-events.md)

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** ux, long-running, agent-initiated
