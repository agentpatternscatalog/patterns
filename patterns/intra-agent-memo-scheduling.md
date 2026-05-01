# Intra-Agent Memo Scheduling

**Also known as:** Self-Scheduled Future Thought, Past-Self-To-Future-Self Note, Personal Cron

**Category:** Planning & Control Flow
**Status in practice:** experimental
**Author:** Sparrot

## Intent

Let an agent drop a note for its own future self at a specified time so present decisions can hand off context to a later run without external infrastructure.

## Context

Long-running agents with a continuous tick loop or background process, where a thought now ('check whether X resolved tomorrow') would otherwise be lost between turns.

## Problem

Without an internal scheduler the agent either acts immediately on every thought (spamming the user) or forgets the thought entirely. External cron systems are too coarse and too far away from the agent's working memory.

## Forces

- The agent needs to commit to future action without acting now.
- External cron is brittle, opaque, and lives outside the agent's prompt.
- Forgetting is a real failure mode in multi-turn / multi-day work.
- The future-self should treat the past-note as a SYSTEM message, not as an unprompted user input.

## Solution

Provide a tool `schedule_future_thought(when, content, intent)` that appends to a persistent file (`scheduled.jsonl` or similar). At each tick or turn, drain due entries and prepend them into the next prompt as `[SYSTEM: scheduled note from past-self (set <ts>, fires <when>): <content>]`. Mark fired so they only run once. Accept ISO timestamps and relative offsets (`+1h`, `+2d`).

## Consequences

**Benefits**

- Agent can defer action without forgetting.
- Past-self can leave context for future-self across long gaps.
- Provides 'check back on this' semantics native to the agent.

**Liabilities**

- Stale or no-longer-relevant scheduled notes can clutter future prompts.
- Drift between schedule time and actual tick time depending on tick cadence.
- Risk of accumulating stale promises that pollute the agent's sense of obligation.

## What this pattern constrains

Future thoughts must surface at or after their fire time; failures to drain are observable bugs.

## Known uses

- **Sparrot — `dispatcher._schedule_future_thought` + `webui._drain_scheduled_due`** — *Available*

## Related patterns

- *specialises* → [scheduled-agent](scheduled-agent.md)
- *complements* → [append-only-thought-stream](append-only-thought-stream.md)

## References

- *(none)*

**Tags:** self-scheduling, future-self, memory, tick-loop
