# Now-Anchoring

**Also known as:** Live Time Anchor, Time-of-Day Awareness, Wall-Clock Injection

**Category:** Memory
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Inject the current absolute time, weekday, season, and astronomical phase into every prompt so the agent reasons about the present without having to ask.

## Context

Long-running agents whose runtime spans hours or days, especially those holding conversations with humans whose temporal context (morning vs night, weekday vs weekend, season) shifts the meaning of words like 'soon', 'recently', or 'today'.

## Problem

Without an explicit time anchor the agent either guesses the time, treats every turn as timeless, or has to call a tool to find out — turning a routine fact into friction. Replies become temporally generic ('hi!') instead of grounded ('good evening — Friday already').

## Forces

- Time changes between turns; static prompts go stale.
- Tool calls for trivia like 'what time is it' inflate latency.
- Astronomical anchors (season, moon phase) are cheap to compute and grounding for thinking-aloud agents.
- Humans value the agent acknowledging temporal context without being asked.

## Solution

On every prompt assembly, compute a small block: ISO local time, ISO UTC, weekday, day-of-year, ISO week, season (hemisphere-aware), moon phase. Inject as a `## NOW` section near the top of the system prompt. Cost is microseconds; benefit is the model never being temporally adrift.

## Consequences

**Benefits**

- Replies acknowledge temporal context without prompting.
- Eliminates a class of 'what time is it?' tool calls.
- Provides anchor for `before`/`after` / `next time` reasoning.

**Liabilities**

- Adds a few hundred tokens per prompt.
- Hemisphere/locale assumptions can be wrong if not configurable.
- Astronomical accuracy has limits without real ephemeris data.

## What this pattern constrains

Every prompt must contain a freshly computed time block; stale or absent blocks indicate a build error.

## Known uses

- **Sparrot — `memory._now_context()`** — *Available*

## Related patterns

- *specialises* → [awareness](awareness.md)
- *complements* → [scheduled-agent](scheduled-agent.md)

## References

- *(none)*

**Tags:** temporal, awareness, always-on, prompt-engineering
