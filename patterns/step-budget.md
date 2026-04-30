# Step Budget

**Also known as:** Max Steps, Iteration Cap, Loop Bound

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Cap the number of tool calls or loop iterations the agent is allowed within a single request.

## Context

Agent loops can run forever or wander; without a hard cap, runaway loops cost real money.

## Problem

Soft termination conditions (model says 'done') fail open; the agent never says done.

## Forces

- Cap too low cuts off legitimate work.
- Cap too high lets pathological runs burn budget.
- What to do when hit (return partial? error?) is its own design choice.

## Solution

Define a numeric cap (max_steps=N) in the agent loop. Increment per tool call or per loop iteration. When N is hit, terminate the loop and return the best partial answer with a note that the cap was reached.

## Consequences

**Benefits**

- Bounded worst-case cost per request.
- Surfaces pathological prompts as cap-hits.

**Liabilities**

- Can hide deeper bugs (the agent really should stop earlier).
- Choosing N is empirical.

## What this pattern constrains

The loop terminates after N iterations regardless of agent's own opinion.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. max_steps=4 in the agent lane.
- **Claude Code (max_turns)** — *Available*
- **OpenAI Agents SDK (max_iterations)** — *Available*

## Related patterns

- *complements* → [cost-gating](cost-gating.md)
- *complements* → [human-in-the-loop](human-in-the-loop.md)
- *alternative-to* → [infinite-debate](infinite-debate.md)
- *alternative-to* → [unbounded-loop](unbounded-loop.md)
- *complements* → [spec-driven-loop](spec-driven-loop.md)
- *complements* → [plan-and-execute](plan-and-execute.md)
- *generalises* → [stop-hook](stop-hook.md)
- *complements* → [stop-cancel](stop-cancel.md)
- *used-by* → [outer-inner-agent-loop](outer-inner-agent-loop.md)
- *complements* → [agent-as-tool-embedding](agent-as-tool-embedding.md)

## References

- (doc) *OpenAI Agents SDK*, <https://github.com/openai/openai-agents-python>
- (doc) *Anthropic: Building agents*, <https://docs.anthropic.com/en/docs/build-with-claude/tool-use>

**Tags:** safety, bound, loop
