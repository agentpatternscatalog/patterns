# Stigmergic Coordination

**Also known as:** Trace-Mediated Coordination, Environment-as-Channel, Indirect Coordination

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

Agents coordinate indirectly by leaving and reading marks in a shared environment (files, queues, scratchpads, world model) so that one agent's trace stimulates another's next action, with no direct messaging.

## Context

Multiple agents share an environment — a workspace directory, a task queue, a shared scratchpad, a vector store. The environment is the only thing they all see; direct point-to-point messaging is either expensive (per-message coordination overhead), unreliable, or simply unavailable across agent boundaries (different processes, different products, different time windows).

## Problem

Forcing every coordination event through direct messaging adds overhead and creates an N×N communication graph. Agents must know each other's identities and protocols. Asynchronous coordination across time windows (one agent finishing a task hours before the next picks it up) needs persistence the messaging layer doesn't have. Without environment-mediated coordination, multi-agent systems either over-couple through direct chatter or fail to coordinate at all when direct channels aren't available.

## Forces

- Direct messaging assumes liveness and identity that may not hold.
- Environment is the natural shared state agents already touch.
- Traces in the environment must be readable by other agents without prior agreement on a protocol.
- Traces decay over time; agents must handle stale marks.

## Therefore

Therefore: have each agent leave structured traces in the shared environment as the side-effect of its action, and have other agents read the environment as input, so coordination emerges from the environment without direct messaging.

## Solution

Define a structured trace format the environment carries — a TODO file, a queue of jobs, status markers in a scratchpad, named entries in a vector store. Each agent's action writes a trace; each agent's next decision reads traces left by others. Traces include enough context that a fresh agent can act on them. Traces decay or are explicitly cleared. No direct messaging is required. Inspired by stigmergy in social insects (ants follow pheromone trails; termites build mounds via local rules).

## Structure

```
Agent 1 --write structured trace--> Shared environment (TODO file, job queue, scratchpad, store) --read trace--> Agent 2 --act, write trace--> Shared environment --read trace--> Agent 3; traces decay or are cleared
```

## Diagram

```mermaid
flowchart LR
  A1[Agent 1] -->|write trace| Env[(Shared environment)]
  Env -->|read trace| A2[Agent 2]
  A2 -->|write trace| Env
  Env -->|read trace| A3[Agent 3]
  A3 -->|write trace| Env
```

## Example scenario

Three coding agents work on the same repository across different sessions. The first writes a TODO file noting which tasks it started and didn't finish. The second reads the TODO, picks up incomplete tasks, and updates it. The third, opening hours later, reads the same TODO and continues. No direct messages pass between them; the TODO file is the coordination channel.

## Consequences

**Benefits**

- Coordination across time, processes, and product boundaries.
- No N×N direct-message graph; the environment is the channel.
- Audit comes for free: the environment is the trace log.

**Liabilities**

- Stale or conflicting traces produce wrong-direction stimulation.
- Traces designed for one agent can mislead another that reads them differently.
- Latency is bounded by how often agents poll the environment.

## Failure modes

- Stale trace — a TODO marker is never cleared after the work is done, and another agent picks it up and repeats the task.
- Conflicting traces — two agents leave opposite markers on the same item, and the next agent acts on whichever it reads first.
- Misread trace — a trace written with one agent's conventions is read differently by another, which then moves in the wrong direction.
- Polling lag — agents check the environment rarely, so a trace waits a long time before anyone acts on it.

## What this pattern constrains

Multi-agent coordination must not require point-to-point direct messaging when the environment can carry traces; agents read and write structured traces in the shared environment.

## Applicability

**Use when**

- Agents share an environment they all read and write.
- Coordination crosses time windows or process boundaries direct messaging cannot.
- Trace format can be made readable by future agents without prior protocol agreement.

**Do not use when**

- Real-time tight coordination is needed; polling latency is unacceptable.
- Agents have no shared environment to mediate through.
- Stale traces would mislead more often than fresh traces help.

## Components

- Shared environment — files, queue, scratchpad, world model
- Trace writer — leaves structured marks per action
- Trace reader — consumes marks as input
- Trace lifecycle — decay or explicit clear policy

## Tools

- Trace schema — readable by any future agent
- Environment storage layer — file system, vector DB, queue, etc.
- Polling or event hook — surfaces new traces to subscribers

## Evaluation metrics

- Trace-pickup latency — time from write to first other-agent read
- Stale-trace incidents — actions driven by outdated marks
- Coordination effectiveness — task success vs direct-message baseline

## Known uses

- **[Claude Code session files (TODO list, plan files) coordinating sequential agents](https://code.claude.com/docs/en/overview)** _available_
- **[Multiagent Systems (Weiss) — Coordination via environment](https://mitpress.mit.edu/9780262731317/multiagent-systems/)** _available_
- **[Insect-colony coordination (canonical biological reference)](https://en.wikipedia.org/wiki/Stigmergy)** _available_

## Related patterns

- _specialises_ **Blackboard**
- _complements_ **World Model as Tool**
- _alternative-to_ **Actor-Model Agents**
- _complements_ **Event-Driven Agent**
- _alternative-to_ **Performative Message**
- _alternative-to_ **Distributed Constraint Optimization**
- _alternative-to_ **Joint Commitment Team**
- _complements_ **Co-Tenant Interference Profiling** — Coordination through the environment used deliberately; the same channel here is unintended, which is why it has to be measured rather than designed.

## References

- [Multiagent Systems, 2nd ed.](https://mitpress.mit.edu/9780262731317/multiagent-systems/) — Gerhard Weiss (ed.), 2013
- [Stigmergy](https://en.wikipedia.org/wiki/Stigmergy)
