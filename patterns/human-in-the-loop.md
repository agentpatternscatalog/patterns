# Human-in-the-Loop

**Also known as:** HITL, Approval Gate, Confirmation Step, Risky Action Gate, Destructive Action Confirmation, Ask Before Risky Action

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Require explicit human approval at defined points before the agent performs an action.

## Context

An action is destructive, irreversible, or regulatory; the cost of being wrong exceeds the cost of waiting.

## Problem

Fully autonomous action at risky boundaries combines model confidence with consequence; the combination is unsafe.

## Forces

- Where to place the gate trades latency and friction for safety.
- Approval-fatigue: too many gates train users to click through.
- Asynchronous approval stalls the loop.


## Applicability

**Use when**

- Action consequences at a defined boundary are too costly to leave to the model alone.
- A human reviewer is reachable within the latency budget the workflow allows.
- Approve, reject, and resume semantics can be expressed cleanly in the agent loop.

**Do not use when**

- Decisions must be made in unattended or sub-second autonomous settings.
- Volume is too high for human review to keep up without becoming a rubber stamp.
- Risk per action is small enough that automated guardrails are sufficient.

## Solution

Identify the boundary. Pause the loop. Surface the proposed action with enough context for the human to decide. Require an explicit approve/reject. Resume on approve; abort or replan on reject. Log the decision.

## Example scenario

A finance ops agent automates supplier payments end to end. After an incident where it paid $42k to a typo-squatted vendor domain, the team installs human-in-the-loop at the payment-execution boundary: the agent prepares the full payment proposal, surfaces vendor name, amount, IBAN, and the source invoice, then pauses for an explicit approve or reject from the on-call operator. Reject sends the proposal back for replan. The decision and the operator id are logged. Auto-payments resume but the bad-vendor class of incident stops.

## Consequences

**Benefits**

- Risk drops to a level the system can defend.
- Decision log captures human judgement that can later train an automated gate.

**Liabilities**

- User experience friction.
- Synchronous gates break async agents.

## What this pattern constrains

The defined action class cannot proceed without an affirmative approval signal.

## Known uses

- **Knitting-DSL Pipeline (Stash2Go)** — *Available*. Opt-in fixer: user clicks to invoke.
- **Bobbin (Stash2Go)** — *Planned*. On destructive writes (project create, queue add, stash subtract).

## Related patterns

- *complements* → [step-budget](step-budget.md)
- *generalises* → [cost-gating](cost-gating.md)
- *generalises* → [approval-queue](approval-queue.md)
- *generalises* → [disambiguation](disambiguation.md)
- *complements* → [compensating-action](compensating-action.md)
- *alternative-to* → [conversation-handoff](conversation-handoff.md)
- *alternative-to* → [communicative-dehallucination](communicative-dehallucination.md)

## References

- (doc) *LangGraph: Human-in-the-Loop*, <https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/>

**Tags:** safety, approval, hitl
