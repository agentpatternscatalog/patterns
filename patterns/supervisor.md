# Supervisor

**Also known as:** Multi-Agent Supervisor, Lane Supervisor

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

Place a coordinating agent above a set of specialised agents and route work to them.

## Context

A team is handling a mix of request types — billing questions, technical support, sales enquiries — and each type benefits from its own system prompt, its own tool palette, and possibly its own model. Each type is itself a multi-step interaction, not a single response, so routing alone is too coarse: the lanes want their own inner agent loop. This is distinct from orchestrator-workers, which dynamically decomposes a task into ad-hoc sub-tasks per request; supervisor routes work to a fixed set of pre-existing specialist agents.

## Problem

A single agent trying to handle every request type has either too few tools — which limits what it can actually do — or too many, in which case the model gets confused about which tool fits which request, the prompt balloons, and recall drops. The team cannot tune the agent for billing without making it worse at sales. A flat router that just dispatches to a one-shot specialist does not give each lane the multi-step loop it needs. Some coordinating layer above the specialists has to own dispatch and aggregation.

## Forces

- Adding a supervisor layer adds a model call.
- Inter-agent communication needs a protocol.
- Specialisation reduces transfer learning across requests.

## Therefore

Therefore: put a coordinating agent above a set of specialised lanes that each own their prompt, tools, and possibly model, and route requests by classification, so that capability grows by adding lanes rather than by enlarging one prompt.

## Solution

A supervisor classifies requests and dispatches them to a specialised agent. Each specialist has its own prompt, tools, and possibly its own model. The supervisor may receive results back and decide whether to escalate or respond.

## Structure

```
User request --> Supervisor (classify) --dispatch--> Specialist A | B | C (own prompt, tools, model) --result--> Supervisor --> [aggregate and respond | escalate]
```

## Diagram

```mermaid
flowchart TD
  Req[User request] --> Sup[Supervisor: classify + dispatch]
  Sup --> S1[Specialist A<br/>own prompt + tools + model]
  Sup --> S2[Specialist B]
  Sup --> S3[Specialist C]
  S1 --> Sup
  S2 --> Sup
  S3 --> Sup
  Sup --> Out[Aggregate or escalate]
```

## Example scenario

A customer-service platform routes incoming chats. A supervisor agent classifies each request: billing, technical, or sales. It dispatches each to the matching specialist agent, which has its own prompt, tool set, and ticket-system access. The supervisor doesn't try to be good at all three roles — it just routes and aggregates.

## Consequences

**Benefits**

- Each lane can be tuned and tested in isolation.
- Capability grows by adding lanes, not by enlarging one prompt.

**Liabilities**

- Multi-agent before simpler patterns are running is decoration.
- Coordination failures are often invisible until production.

## Failure modes

- Premature multi-agent — the team builds a supervisor and specialists before a single agent works, and the extra layer only adds failure points.
- Misclassification — the supervisor routes a billing request to the technical specialist, which answers it badly.
- Invisible coordination failure — a dispatch or aggregation bug only shows up under real production traffic.
- Scope creep — a specialist acts outside its declared scope, and the supervisor's aggregation now mixes overlapping answers.

## What this pattern constrains

Specialists may only act within their declared scope; the supervisor owns dispatch and aggregation.

## Applicability

**Use when**

- Different request types want their own loop, prompt, tools, and possibly model.
- A flat router would be too coarse because lanes need their own multi-step behaviour.
- A coordinating layer can dispatch and decide whether to escalate.

**Do not use when**

- A single agent already handles the workload without confusion.
- Routing alone (no inner loop per lane) suffices.
- Supervisor coordination cost outweighs the specialisation benefit.

## Components

- Supervisor agent — classifies incoming requests and dispatches to the right lane
- Lane specialist — pre-existing agent with its own prompt, tool palette, and possibly model
- Classifier step — supervisor's first move that picks the lane for each request
- Aggregation step — supervisor-side reconciliation of specialist output before responding
- Escalation rule — supervisor policy for handing back to user or to a different lane

## Tools

- LangGraph Supervisor — provides the supervisor-and-lanes scaffolding
- LLM API — supervisor uses one model, lanes may use heterogeneous models tuned per lane
- Per-lane tool palettes — billing tools, technical tools, sales tools scoped to their specialist

## Evaluation metrics

- Lane-routing accuracy — share of requests dispatched to the lane a human reviewer would pick
- Per-lane resolution rate — task-completion measured against single-agent monolith baseline
- Supervisor overhead — extra latency from the classify-and-dispatch step
- Escalation rate — share of requests the supervisor had to re-route or hand back
- Cross-lane interference — incidents where a tuning change in one lane degraded another

## Known uses

- **Bobbin (Stash2Go)** _available_ — agent_v2.py + supervisor.py implement the lane-supervisor pattern.
- **LangGraph Supervisor** _available_
- **[Sparrot](https://marco-nissen.com/sparrot/)** _available_ — A dispatcher routes requests to specialised internal lanes (chat, tick, MCP, voice) and coordinates across them, acting as the central traffic controller that the agent loop itself does not see.

## Related patterns

- _uses_ **Routing**
- _alternative-to_ **Orchestrator-Workers**
- _specialises_ **Hierarchical Agents**
- _alternative-to_ **Blackboard**
- _generalises_ **Lead Researcher**
- _complements_ **Inter-Agent Communication**
- _complements_ **Role Assignment**
- _alternative-to_ **Swarm**
- _alternative-to_ **Hero Agent**
- _alternative-to_ **Handoff**
- _complements_ **Mixture of Experts Routing**
- _alternative-to_ **Conversational Multi-Agent**
- _complements_ **SOP-Encoded Multi-Agent Workflow**
- _alternative-to_ **Chat Chain**
- _complements_ **Dynamic Expert Recruitment**
- _complements_ **Outer-Inner Agent Loop**
- _used-by_ **Cross-Domain Enterprise Agent Network**
- _complements_ **Actor-Model Agents**
- _generalises_ **Group-Chat Manager**
- _alternative-to_ **Role-Typed Subagents**
- _alternative-to_ **Orchestrator as Bottleneck**
- _generalises_ **Supervisor-Plus-Gate**
- _alternative-to_ **Contract Net Protocol**
- _complements_ **One Tool, One Agent**
- _complements_ **Magentic-One Generalist Multi-Agent**
- _alternative-to_ **Coalition Formation**
- _alternative-to_ **Joint Commitment Team**
- _alternative-to_ **Distributed Constraint Optimization**
- _alternative-to_ **Control-Loop-Mapped Agent Chain** — A supervising agent routes and arbitrates using a model; this pattern keeps the coordinating position but removes the model from it, because the priority answer already exists.

## References

- [LangGraph Multi-Agent Supervisor](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/)
