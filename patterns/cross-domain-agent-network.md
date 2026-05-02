# Cross-Domain Enterprise Agent Network

**Also known as:** Domain-Specialised Agent Mesh, Joule-Style Agent Collaboration, Per-Function Agent Network

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Decompose enterprise agency into a set of domain-specialised agents (finance, supply chain, HR, service), each grounded in its own system of record, and orchestrate cross-functional workflows by routing artefacts between them through a standardised inter-agent protocol.

## Context

Large enterprises whose business processes already live across many backing systems (ERP, CRM, HR, ticketing) and where end-to-end workflows (e.g. dispute → cash collection → finance close) cross domain boundaries.

## Problem

A single mega-agent grounded against every system has bad recall, no clear ownership, and no domain-specific guardrails; flat tool-use agents over a flat tool catalogue degrade as the catalogue grows.

## Forces

- Each domain has its own data model, vocabulary, and compliance rules.
- End-to-end workflows must cross domains.
- A single agent over all systems blows up the tool catalogue and the prompt.
- Domain teams want ownership and lifecycle of their own agents.

## Solution

Build one specialised agent per business domain, each with its own grounded data, tool palette, and acceptance criteria. Define a standardised inter-agent protocol for handoffs (e.g. A2A, MCP). When a task crosses domains, the source agent routes to the target via the protocol, passing a typed artefact. An optional supervisor or role-based assistant fronts the user and dispatches to the right entry agent.

## Structure

```
User -> Role Assistant -> Domain Agent A (own data + tools) -- protocol message --> Domain Agent B -- ... --> outcome.
```

## Consequences

**Benefits**

- Each domain agent stays small, grounded, and ownable.
- Cross-domain workflows are auditable per agent.
- Domain teams ship and update their agents independently.

**Liabilities**

- Protocol design is the core engineering problem; bad protocol fossilises mistakes.
- Routing decisions become a second-order problem (who does what).
- Failure attribution across the chain is harder than for a monolith.

## What this pattern constrains

An agent may only call across domains via the standardised protocol; ad-hoc backdoor integrations between domain agents are forbidden.

## Applicability

**Use when**

- Enterprise agency spans multiple domains (finance, supply chain, HR, service) each with its own system of record.
- A standardised inter-agent protocol (A2A, MCP) is available or can be adopted.
- Each domain benefits from its own grounded data, tool palette, and acceptance criteria.

**Do not use when**

- All work happens in one domain and a single specialised agent suffices.
- No inter-agent protocol is in place and the integration cost dominates the benefit.
- Domains share so much context that a single mega-agent is actually simpler.

## Known uses

- **[SAP Joule](https://www.sap.com/products/artificial-intelligence/ai-agents.html)** — *Available*. Per-domain Joule Agents (finance, HR, supply chain, service) collaborating via SAP's collaborative agent architecture; A2A and MCP support announced 2025.
- **ServiceNow Now Assist** — *Available*. Comparable pattern in ITSM/HR/CSM domain agents.

## Related patterns

- *uses* → [supervisor](supervisor.md)
- *uses* → [handoff](handoff.md)
- *uses* → [inter-agent-communication](inter-agent-communication.md)
- *uses* → [mcp](mcp.md)
- *uses* → [role-assignment](role-assignment.md)
- *alternative-to* → [hero-agent](hero-agent.md)

## References

- (blog) *Joule Agents: How SAP Uniquely Delivers AI Agents That Truly Mean Business*, <https://news.sap.com/2025/02/joule-sap-uniquely-delivers-ai-agents/>

**Tags:** multi-agent, enterprise, germany-origin, sap, joule
