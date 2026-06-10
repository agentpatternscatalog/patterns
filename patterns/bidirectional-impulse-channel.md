# Bidirectional Impulse Channel

**Also known as:** Two-Way Chat, User-and-Agent-Initiated Communication

**Category:** Streaming & UX  
**Status in practice:** experimental

## Intent

Let the user inject impulses into the agent and let the agent push messages to the user, both through one channel.

## Context

A team is running an agent that does not sit idle between user turns. It might be a personal assistant running a continuous reasoning loop, a monitoring agent watching a system, or any process that has internal activity the user would sometimes want to interrupt or hear about. The user is at a chat or command-line surface, occasionally typing, occasionally absent for hours.

## Problem

A pure request-and-response chat interface fits this poorly: the agent has nothing to say when nothing is asked, and the user has no way to inject a correction without phrasing it as a new question for the model to interpret. A pure notification firehose in the other direction is worse, because it trains the user to mute the channel within a day. The team has to choose between an agent that goes silent until prompted and an agent that becomes background noise, with no obvious middle ground.

## Forces

- Push hygiene: too many messages train users to ignore the channel.
- Inverse: starvation when the agent waits forever.
- Authority: not every user-typed line should be a command.

## Therefore

Therefore: pair sigil-prefixed user commands that bypass the model with salience-gated agent pushes on one channel, so that both sides can interrupt without spamming the other.

## Solution

A single CLI/chat surface where the user can send sigil-prefixed commands (e.g. `!<verb> ...`) that bypass the model and write directly to memory, while the agent can push messages when salience clears a threshold (insight, stuck focus, contradiction, goal complete). Hygiene rule: at most one unsolicited message per window.

## Variants

- **Command-prefix channel** — User commands begin with a sigil (e.g. `!`) that bypasses the model and writes directly to memory; the agent pushes inline messages.
- **Out-of-band push** — User and agent share the same chat for prompts, but the agent sends salience-triggered pushes through a separate notification surface (toast, email).
- **Always-on REPL channel** — User and agent both type into a shared REPL with the agent running a continuous loop; both can interrupt the other.

## Example scenario

A user has asked their personal agent to monitor a slow scientific computation overnight and 'tell me when it's interesting'. Pure request/response would force the user to keep polling; pure push notifications wake them for trivia. They build a bidirectional impulse channel: the agent can send messages at any time, but the user can also reach in mid-run with 'stop watching the temperature, watch the residual'. The agent picks up the impulse on its next tick and changes what it pushes.

## Diagram

```mermaid
sequenceDiagram
  participant User
  participant Channel as CLI / Chat
  participant Mem as Memory
  participant Agent
  User->>Channel: !&lt;verb&gt; ... (sigil-prefixed command)
  Channel->>Mem: write directly (bypass model)
  Agent->>Mem: read salient context
  Agent->>Channel: push message on salience spike
  Channel-->>User: notification
```

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

- **Author's long-running personal agent (single private deployment)** — *Available* — Single-source evidence: one private deployment by the catalog author; no independently documented use yet.

## Related patterns

- *uses* → [salience-triggered-output](salience-triggered-output.md)
- *complements* → [streaming-typed-events](streaming-typed-events.md)

## References

- (paper) Liu, Fang, Shi, Wu, Igarashi, Chen, *Proactive Conversational Agents with Inner Thoughts*, 2024, <https://arxiv.org/abs/2501.00383>

**Tags:** ux, long-running, agent-initiated
