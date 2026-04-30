# Orchestrator-Workers

**Also known as:** Dynamic Decomposition, Orchestrator-Subagents

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

An orchestrator dynamically breaks a task into subtasks at runtime and delegates each to a worker LLM, then synthesises results.

## Context

The subtasks needed are not known in advance and depend on the task; coding tasks where the number of files to change varies are the canonical example.

## Problem

Static decomposition (Plan-and-Execute, Prompt Chaining) cannot handle tasks whose shape is data-dependent.

## Forces

- The orchestrator must reason at a higher level than any worker.
- Workers should not have to know they are workers.
- Synthesis must reconcile conflicting worker outputs.

## Solution

Orchestrator agent receives the task, decides at runtime what subtasks to spawn, hands each to a worker (often via tool call), collects results, and synthesises the final output. Worker count and roles can vary per task.

## Consequences

**Benefits**

- Handles tasks with data-dependent decomposition.
- Workers stay simple; complexity lives in the orchestrator.

**Liabilities**

- Orchestrator failure is unrecoverable without retry logic.
- Token cost scales with worker count; budget awareness matters.

## What this pattern constrains

Workers see only their assigned subtask; only the orchestrator has the global view.

## Known uses

- **Anthropic Building Effective Agents (Workflow #4)** — *Available*
- **Claude Code subagents** — *Available*
- **Anthropic Multi-Agent Research** — *Available*
- **OpenAI Deep Research** — *Available*

## Related patterns

- *alternative-to* → [supervisor](supervisor.md)
- *alternative-to* → [plan-and-execute](plan-and-execute.md)
- *generalises* → [subagent-isolation](subagent-isolation.md)
- *generalises* → [lead-researcher](lead-researcher.md)
- *complements* → [inter-agent-communication](inter-agent-communication.md)
- *generalises* → [hierarchical-agents](hierarchical-agents.md)
- *complements* → [dynamic-expert-recruitment](dynamic-expert-recruitment.md)
- *generalises* → [agent-as-tool-embedding](agent-as-tool-embedding.md)

## References

- (blog) *Anthropic: Building Effective Agents*, 2024, <https://www.anthropic.com/research/building-effective-agents>

**Tags:** multi-agent, orchestrator
