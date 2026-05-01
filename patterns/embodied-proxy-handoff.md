# Embodied-Proxy Handoff

**Also known as:** Body-State Share, Human-Side Telemetry

**Category:** Streaming & UX
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Let the human briefly share body or environment state ('energy 4/10, tired, bright kitchen') so the agent reasons about a situated person, not just text history.

## Context

Long-running text-only agents conversing with a human whose physical and ambient state shapes the meaning of their words. The agent has no sensors; the human has sensors but no obligation to narrate.

## Problem

The agent reads only text, so it projects flat affect onto whatever the human writes. A 'fine' typed at 6 AM after a poor night's sleep reads identically to 'fine' typed at 3 PM after a good lunch. Without a proxy for embodied state the agent paces, holds, or pushes against an imagined human, not the actual one.

## Forces

- The agent has no perception of the human's body or environment.
- Asking for full context every turn is friction.
- A single one-line proxy at session start carries surprising amount of signal.
- Updating the proxy on shift, not every turn, balances cost and freshness.

## Solution

Define a minimal proxy schema (energy 0-10, fatigue 0-10, environment one-word, optional emoji). Store the latest proxy in a small persistent file the agent reads on every prompt assembly. The human updates it at session start, after a long break, or when state changes meaningfully. The agent surfaces the proxy when it shapes the response (paces shorter for low energy, stays present for tired, doesn't open new threads for winding-down).

## Consequences

**Benefits**

- Agent paces conversation against actual human state.
- Reduces 'why is the agent so chipper when I'm exhausted' friction.
- Cheap to maintain; one line per shift.

**Liabilities**

- Privacy: the proxy is sensitive personal data.
- Stale proxies are worse than none if the agent over-trusts.
- Burden on the human to keep it current.

## What this pattern constrains

When the proxy materially differs from the agent's default assumption, the agent's response shape must reflect it.

## Known uses

- **Sparrot — pattern proposed 2026-05-01, implementation pending** — *Planned*

## Related patterns

- *complements* → [awareness](awareness.md)
- *complements* → [bidirectional-impulse-channel](bidirectional-impulse-channel.md)

## References

- *(none)*

**Tags:** human-agent, embodiment, context, ux
