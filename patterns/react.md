# ReAct

**Also known as:** Reason+Act, Think-Act-Observe Loop

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Interleave a single thought, a single tool call, and a single observation per step so the agent reasons over fresh evidence.

## Context

The task requires looking things up or acting on the world; the answer cannot be produced by pure thinking.

## Problem

Pure chain-of-thought hallucinates facts; pure tool-blasting wastes calls on the wrong things.

## Forces

- Tool calls are expensive (latency, cost, side effects).
- Observations change the right next step.
- The loop must terminate.

## Solution

On each step the agent emits Thought (private reasoning), Action (one tool call), Observation (the tool's result). Repeat until the agent decides to answer. A step budget bounds the loop.

## Structure

```
[Thought_i, Action_i, Observation_i] for i in 1..N, then Answer.
```

## Consequences

**Benefits**

- Lowest-overhead path for simple lookups and single-field updates.
- Easy to inspect and debug step by step.

**Liabilities**

- Sequential by nature; long traces are slow and expensive.
- No global plan; the agent can wander.

## What this pattern constrains

Each step the model may call exactly one tool; reasoning between calls is not actuated.

## Known uses

- **Bobbin (Stash2Go)** — *Available*. observe node + route_after_observe edge in LangGraph.
- **LangChain AgentExecutor (default)** — *Available*
- **Claude Code** — *Available*
- **Cursor** — *Available*
- **GitHub Copilot agent** — *Available*
- **Devin** — *Available*

## Related patterns

- *alternative-to* → [plan-and-execute](plan-and-execute.md)
- *uses* → [tool-use](tool-use.md)
- *used-by* → [agentic-rag](agentic-rag.md)
- *alternative-to* → [planner-executor-observer](planner-executor-observer.md)
- *used-by* → [lats](lats.md)
- *used-by* → [computer-use](computer-use.md)
- *specialises* → [self-ask](self-ask.md)
- *composes-with* → [code-execution](code-execution.md)
- *generalises* → [code-as-action](code-as-action.md)

## References

- (paper) Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao, *ReAct: Synergizing Reasoning and Acting in Language Models*, 2022, <https://arxiv.org/abs/2210.03629>

**Tags:** react, loop, tool-use
