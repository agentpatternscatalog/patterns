# Conversation Handoff to Human

**Also known as:** Escalation, Live-Agent Handoff, Human Takeover

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Transfer the entire conversation thread from agent to human operator, with state transfer and return primitive.

## Context

Customer-facing agent products where some conversations exceed agent capability or require regulatory accountability.

## Problem

Human-in-the-loop gates approve or reject discrete actions; this pattern transfers ownership of the whole conversation, which is structurally different.

## Forces

- Handoff loses context fidelity.
- Sticky routing (return to same operator on follow-up) needs auth + session plumbing.
- Return primitive (back to agent) requires re-grounding.

## Solution

On escalation trigger (low confidence, explicit user request, policy violation), the agent emits a structured handoff envelope with conversation summary, ticket number, and human operator queue assignment. Operator takes ownership; agent disengages. On return, agent resumes with operator's note in context.

## Consequences

**Benefits**

- Hard cases reach humans.
- Customer experience preserved across the boundary.

**Liabilities**

- Operator queue capacity bounds scale.
- State transfer has fidelity loss.

## What this pattern constrains

Once handed off, the agent does not generate to the user; the operator owns the thread until explicit return.

## Applicability

**Use when**

- Some triggers (low confidence, policy violation, explicit user request) demand transferring ownership of the whole thread, not just one action.
- A human operator queue exists with the capacity to take over conversations.
- A return primitive is needed so the agent can resume after the operator hands back.

**Do not use when**

- Discrete-action approval is sufficient and full thread transfer is overkill (use approval-queue).
- No human operator queue exists to hand the conversation to.
- The agent must remain the sole user-facing interface for compliance reasons.

## Known uses

- **Sierra agent escalations** — *Available*
- **Intercom Fin handoffs** — *Available*
- **Zendesk AI handoffs** — *Available*

## Related patterns

- *alternative-to* → [human-in-the-loop](human-in-the-loop.md)
- *complements* → [approval-queue](approval-queue.md)
- *specialises* → [handoff](handoff.md)

## References

- (doc) *Intercom Fin: Human handoff*, <https://www.intercom.com/help/en/articles/8362236-fin-handover>
- (doc) *Sierra agent escalations*, <https://sierra.ai>

**Tags:** safety, escalation, handoff
