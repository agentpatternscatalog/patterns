# Swarm

**Also known as:** Society of Mind, Peer Agents, Decentralised Multi-Agent

**Category:** Multi-Agent  
**Status in practice:** experimental

## Intent

Run many peer agents that interact directly without a central supervisor, achieving emergent coordination.

## Context

Tasks where centralised coordination is a bottleneck or where the problem benefits from many independent attempts (simulation, exploration).

## Problem

Centralised supervisors become bottlenecks at scale; some tasks (negotiation, simulation, exploration) need agent-to-agent dynamics.

## Forces

- Emergent behaviour can surprise designers; debugging is hard.
- Communication topology (broadcast? gossip? pub/sub?) is a design choice.
- Termination is non-trivial without a supervisor.

## Solution

Agents interact via a shared message bus, chat, or environment. Each agent has its own goals and policies. No central coordinator; convergence is emergent. Termination conditions are environment-level (time budget, consensus threshold, external trigger).

## Consequences

**Benefits**

- Scales horizontally.
- Suits negotiation, market simulation, exploration.

**Liabilities**

- Hard to debug; emergent failures are global.
- Cost can balloon without supervision.

## What this pattern constrains

Agents communicate only via the shared channel; out-of-band coordination is forbidden.

## Known uses

- **OpenAI Swarm (deprecated; succeeded by OpenAI Agents SDK)**
- **Stanford Generative Agents simulation** — *Available*

## Related patterns

- *specialises* → [debate](debate.md)
- *alternative-to* → [supervisor](supervisor.md)
- *complements* → [blackboard](blackboard.md)

## References

- (repo) *openai/swarm*, <https://github.com/openai/swarm>

**Tags:** multi-agent, swarm, emergent
