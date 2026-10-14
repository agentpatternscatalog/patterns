# Communicative Dehallucination

**Also known as:** Instructor-Reversal Clarification, Inter-Agent Clarifying Question

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

When an instructed agent would have to invent missing context to comply, have it reverse roles and ask the instructor for the missing detail before answering.

## Context

Two agents are communicating in an instructor-and-assistant shape — an orchestrator telling a coding sub-agent what to do, a planner handing work to an executor — and the instruction arrives with a decisive detail missing. The missing piece might be a specific class name, an API version, an ambiguous unit of measure, or which of several plausible interpretations the instructor actually meant.

## Problem

Without a way for the assistant to ask back, it complies by inventing a plausible value for the missing detail and proceeds as if it had been told. The fabricated choice gets baked into the next artefact and is hard to spot at the hand-off boundary, where it looks like a confident answer rather than a guess. By the time the wrong assumption surfaces — in a downstream failure or a user complaint — the trail back to the original gap is buried.

## Forces

- Speed of completion vs. fidelity of context.
- Adding a clarification round costs latency and tokens.
- Asking too eagerly degrades into chatter; not asking at all produces hallucinated outputs.

## Therefore

Therefore: when an instructed agent would have to invent a missing decisive fact, force it to reverse roles and ask one bounded question of the instructor first, so that fabrication is replaced by a scoped clarification round at the boundary.

## Solution

Define an explicit role-reversal protocol: when the assistant detects that the instruction is missing a deciding piece of context, it pivots and emits a focused question back to the instructor ("the precise name of the dependency, please"). The instructor answers, and only then does the assistant produce its conclusion. Bound the depth (one or two reversals) to prevent infinite ping-pong.

## Structure

```
Instructor -> instruction -> Assistant; if context_gap_detected: Assistant -> question -> Instructor -> answer -> Assistant -> conclusion.
```

## Diagram

```mermaid
sequenceDiagram
  participant Instr as Instructor
  participant Asst as Assistant
  Instr->>Asst: instruction (missing context)
  Asst->>Asst: detect missing piece
  Asst-->>Instr: focused question (role reversal)
  Instr-->>Asst: missing detail
  Asst-->>Instr: grounded answer
```

## Example scenario

An orchestrator agent tells a coding sub-agent 'add the new field to the user model'. The sub-agent doesn't know whether 'field' means database column, API contract, or both, but it would normally just pick one and start editing. Under Communicative Dehallucination, the sub-agent reverses roles and asks back: 'do you mean the database schema, the GraphQL type, or both?' Only after the orchestrator answers does it act, so the wrong choice never propagates downstream where it would be expensive to detect.

## Consequences

**Benefits**

- Targets the specific dehallucination point instead of after-the-fact verification.
- Cheaper than full multi-agent debate; the question is scoped.
- Produces a more faithful artefact at the next hand-off.

**Liabilities**

- Adds latency for every clarification round.
- Detecting the gap is itself a model judgement and can fail.
- Risk of infinite ping-pong without a depth bound.

## Failure modes

- Missed gap — the assistant does not notice the instruction is missing a deciding detail, invents a value, and carries on.
- Ping-pong — without a depth bound, assistant and instructor keep asking each other questions and never reach an answer.
- Over-asking — the assistant asks back on details it could have settled itself, and every hand-off pays an extra round of latency.
- Vague question — the clarifying question is broad, the instructor answers loosely, and the assistant still has to guess.

## What this pattern constrains

The assistant may not produce a final answer when a designated context slot is unfilled; it must instead emit a clarifying question.

## Applicability

**Use when**

- Multi-agent setups where the assistant otherwise fabricates missing context to comply with instructions.
- A reverse-direction question channel between agents can be implemented cleanly.
- Fabrications would propagate downstream and be hard to detect at the artefact boundary.

**Do not use when**

- The instructor cannot answer clarification questions in time (e.g. fully autonomous pipelines).
- The cost of an extra round-trip exceeds the cost of detecting and fixing fabrications later.
- Instructions are always complete by construction and missing-context fabrication never arises.

## Components

- Instructor agent — issues the original instruction and answers clarifying questions
- Assistant agent — detects context gaps and reverses roles to ask before answering
- Gap detector — judgement step that decides whether a deciding fact is missing
- Reversal-depth bound — hard cap on clarification rounds to prevent infinite ping-pong

## Tools

- LLM API — invoked on both sides of the reversal, often the same model
- ChatDev or equivalent multi-agent harness — supplies the assistant-instructor channel

## Evaluation metrics

- Clarification-question rate — share of instructions that triggered a reversal
- Fabrication-reduction rate — drop in invented details vs no-reversal baseline, sample-audited
- Reversal precision — share of clarifying questions humans agree were genuinely needed
- Added latency per task — extra wall-clock spent on clarification rounds
- Ping-pong incidents — runs that hit the reversal-depth bound without resolution

## Known uses

- **[ChatDev](https://github.com/OpenBMB/ChatDev)** _available_ — Original demonstration; assistant reverses to instructor role to request missing detail before delivering a conclusive response.

## Related patterns

- _specialises_ **Disambiguation** — Same shape, but agent-to-agent rather than agent-to-user.
- _alternative-to_ **Human-in-the-Loop**
- _alternative-to_ **Debate**
- _conflicts-with_ **Infinite Debate** — Requires a depth bound to avoid this anti-pattern.
- _uses_ **Inter-Agent Communication**

## References

- [ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) — Qian et al., 2023
