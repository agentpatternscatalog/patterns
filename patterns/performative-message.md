# Performative Message

**Also known as:** Speech-Act Message, KQML Performative, Typed Agent Message

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

Inter-agent messages are typed by communicative intent (request, inform, propose, accept, refuse, query) rather than by free-form prose, so receivers can dispatch on act type.

## Context

A multi-agent system exchanges messages across agents. The default in LLM-agent deployments is free-form natural language: agent A writes a paragraph that agent B reads as a paragraph. The communicative act — is this a request? a proposal? an answer? — is implicit in the text.

## Problem

Untyped messages collapse in several ways. Receivers must classify the act before dispatching, which is itself an error-prone LLM call. Audit and orchestration tools cannot tell who requested what from whom. Negotiation, query, and information-sharing protocols cannot be enforced because the protocol's state machine has no typed transitions to track. Without typing, multi-agent communication is prose all the way down and the system has no language for 'A proposed X to B, B accepted, C is querying about it'.

## Forces

- Receivers benefit from explicit act type for dispatching.
- Protocol state machines need typed transitions to enforce contracts.
- Free-form payloads are still needed for the act content.
- Type vocabulary must be small and stable across agents.

## Therefore

Therefore: type every inter-agent message with a performative drawn from a small fixed vocabulary, so receivers can dispatch on act type and protocols can be enforced as state machines.

## Solution

Define a small fixed set of performatives — request, inform, propose, accept, refuse, query, agree, cancel — drawn from the KQML (Knowledge Query and Manipulation Language) and FIPA-ACL (FIPA Agent Communication Language) tradition. Every inter-agent message carries an explicit performative plus the act content. Receivers dispatch on performative. Protocol state machines (negotiation, query-then-answer, contract-net) become enforceable because the transitions are typed. Free-form natural language remains the content payload; the typing is a metadata layer the LLM sees and produces.

## Structure

```
Sender --message = (performative: request | inform | propose | accept | refuse | query | ...) + content--> Receiver --dispatch on performative--> handler --> protocol state machine advances on typed transition (logged for audit)
```

## Diagram

```mermaid
sequenceDiagram
  participant A as Agent A
  participant B as Agent B
  A->>B: (propose: deliver by Friday at $500)
  B->>A: (counter-propose: deliver by Friday at $700)
  A->>B: (accept: $700)
  Note over A,B: Typed performatives enable<br/>protocol enforcement + audit
```

## Example scenario

A negotiation protocol between two agents uses {propose, counter-propose, accept, refuse, withdraw}. Agent A sends `(propose: deliver-by Friday at $500)`. Agent B sends `(counter-propose: deliver-by Friday at $700)`. Agent A sends `(accept: $700)`. The orchestrator's audit log shows the typed exchange; no classification of free-form prose is needed.

## Consequences

**Benefits**

- Receivers can dispatch without an additional classification call.
- Protocol state machines are enforceable, not advisory.
- Audit and orchestration tools have typed events to reason over.

**Liabilities**

- Choosing the performative is one more output the model can get wrong.
- Performative vocabulary can drift or fragment across teams without governance.
- Type-checking adds overhead on each message exchange.

## Failure modes

- Wrong act type — the model labels a counter-offer as 'accept', and the receiver closes a negotiation that was still open.
- Vocabulary drift — two teams add their own performatives, and agents from one team cannot dispatch messages from the other.
- Label-content mismatch — the performative says 'inform' but the content asks for an action, and the receiver ignores the real request.
- Per-message overhead — type-checking every message slows high-volume exchanges.

## What this pattern constrains

Inter-agent messages must not be untyped natural-language blobs; every message carries an explicit performative drawn from the fixed vocabulary.

## Applicability

**Use when**

- Multi-agent communication has recognisable communicative acts.
- Protocols (negotiation, query, contract-net) are run between agents.
- Receivers benefit from typed dispatch.

**Do not use when**

- Communication is purely free-form discussion with no protocol structure.
- Performative vocabulary cannot be standardised across the agents involved.
- Single-agent system with no inter-agent messaging.

## Components

- Performative vocabulary — fixed set of types (request, inform, propose, accept, refuse, query, agree, cancel)
- Message envelope — typed header plus free-form content payload
- Dispatcher — routes messages by performative
- Protocol state machine — typed transitions per protocol

## Tools

- Schema registry — defines the performative vocabulary
- Message bus — carries typed messages between agents
- Audit log — typed events for review

## Evaluation metrics

- Performative misclassification rate — incorrect typing by the sender
- Protocol completion rate — share of started protocols that reach a terminal state
- Message volume per performative — operational visibility into the communication mix

## Known uses

- **[KQML / FIPA-ACL classical agent communication languages](https://en.wikipedia.org/wiki/Knowledge_Query_and_Manipulation_Language)** _available_
- **[Modern MCP / A2A message schemas (typed call/response)](https://modelcontextprotocol.io/specification/2025-11-25/basic)** _available_
- **[Multiagent Systems (Weiss) — Agent communication chapter](https://mitpress.mit.edu/9780262731317/multiagent-systems/)** _available_

## Related patterns

- _complements_ **Agent Adapter**
- _uses_ **Contract Net Protocol**
- _complements_ **Tool Use**
- _complements_ **MCP Bidirectional Bridge**
- _uses_ **Structured Output**
- _complements_ **Actor-Model Agents**
- _alternative-to_ **Stigmergic Coordination**

## References

- [Multiagent Systems, 2nd ed.](https://mitpress.mit.edu/9780262731317/multiagent-systems/) — Gerhard Weiss (ed.), 2013
- [KQML — Knowledge Query and Manipulation Language](https://en.wikipedia.org/wiki/Knowledge_Query_and_Manipulation_Language)
