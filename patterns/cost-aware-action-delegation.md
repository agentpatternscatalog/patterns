# Cost-Aware Action Delegation

**Also known as:** Risk-Tiered Action Approval, Per-Action Autonomy

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Classify every agent action by risk/cost and route each tier to a different approval policy, bounding the autonomy surface per-action instead of by one global flag.

## Context

An agent has access to a mixed action surface: reading a file, calling a search API, sending an email, modifying a CRM record, refunding an order, terminating a cloud resource. A single 'auto-approve everything' flag treats sending an email the same as refunding $10,000. A single 'require approval for everything' flag turns the agent into a typing-assist tool.

## Problem

Without per-action risk tiering, the autonomy decision collapses to one global switch. Either the agent acts on dangerous things without checking, or it asks before every read. Approval fatigue kills the second mode within a week; trust incidents kill the first. The team has no vocabulary for 'this action is fine to do unsupervised, this one needs to confirm with the user, this one needs to escalate to a human reviewer'.

## Forces

- Risk varies by action type and sometimes by parameter value (refund $5 vs refund $5000).
- Approval fatigue dominates if every action requires confirmation.
- Trust incidents dominate if no action requires confirmation.
- Risk tiers must be a small enumeration that humans can reason about.

## Therefore

Therefore: classify each agent action by risk tier and route each tier to a fixed approval policy, so the autonomy surface is bounded per-action and per-parameter rather than by a single global flag.

## Solution

Tag every action with a risk tier (low / medium / high, or a richer scheme). Map each tier to an approval policy: low → auto-execute, medium → confirm with the user, high → require human reviewer with explicit sign-off. The tier can be conditional on parameters (refund > $1000 → high). The agent's action surface is the union of permitted (tier, policy) pairs; the runtime enforces the policy independently of the agent's reasoning. Make the classifier itself reviewable — actions and their tiers are configuration, not prompt content.

## Structure

```
Action requested --> Risk classifier (config, may read parameters) --low--> Auto-execute | --medium--> User confirms? --yes--> Execute | --high--> Reviewer signs off? --yes--> Execute; any no --> Skip
```

## Diagram

```mermaid
flowchart LR
  Act[Action requested] --> Cls[Risk classifier]
  Cls --> Low[Low: auto-execute]
  Cls --> Med[Medium: confirm with user]
  Cls --> Hi[High: human sign-off]
  Low --> Exec[Execute]
  Med --> UC{User confirms?}
  UC -- yes --> Exec
  UC -- no --> Skip[Skip]
  Hi --> HC{Reviewer signs off?}
  HC -- yes --> Exec
  HC -- no --> Skip
```

## Example scenario

A customer-ops agent has 30 actions. `search_orders` is low (auto). `update_shipping_address` is medium (confirm with the requesting customer-rep). `refund_order` is parameter-conditional: refunds under $100 are medium, refunds $100-1000 require manager sign-off, refunds over $1000 require both manager and finance approval. The agent's reasoning never gates the action; the runtime classifier does.

## Consequences

**Benefits**

- Autonomy decisions are per-action and per-parameter, not one switch.
- Approval fatigue collapses for low-tier actions while high-tier risk gets attention.
- Risk tier is auditable in traces; postmortems can ask why a high-tier action ran without sign-off.

**Liabilities**

- Tier assignment is a judgment call; misclassification (high marked as low) is a real attack surface.
- Parameter-conditional tiers add complexity to the classifier and to traces.
- Tier inflation — teams who get burned move actions up; over time the medium tier engulfs everything.

## Failure modes

- Mis-tiered action — a destructive action is tagged low, so it auto-executes with no confirmation, and an attacker learns to route through it.
- Tier inflation — after each incident more actions move up a tier, until the medium tier covers almost everything and approval fatigue returns.
- Parameter blind spot — the tier depends on an argument such as refund amount, and the classifier checks the tool name but not the argument.

## What this pattern constrains

An agent must not execute an action without consulting its risk tier; the approval policy for that tier must complete before the action proceeds.

## Applicability

**Use when**

- The agent's action surface spans actions of materially different blast radius.
- Operators need an audit trail of what risk class each executed action was in.
- Some actions are parameter-conditional and would be misclassified by a single tier per action.

**Do not use when**

- All actions are read-only or otherwise low-risk; a single tier suffices.
- Tier inflation pressure is so strong every action ends up high; gating is then theatre.
- The team cannot maintain the classifier — risk tier becomes stale.

## Components

- Action classifier — assigns each action (and parameters) a risk tier
- Policy table — per-tier approval policy (auto, confirm, sign-off)
- Runtime enforcer — gates execution on the policy outcome
- Audit log — records tier and approval result per action

## Tools

- Approval queue — used for human sign-off on high-tier actions
- Policy-engine — encodes the tier-to-policy mapping
- Risk-tier dashboard — surfaces current tier coverage to operators

## Evaluation metrics

- Tier-coverage — share of actions with explicit tier (target: 100%).
- Misclassification incidents — actions later found to belong in a higher tier.
- Approval cycle time per tier — confirms approval fatigue at medium and high.

## Known uses

- **[Designing Multi-Agent Systems (Dibia) — Cost-Aware Delegation UX principle](https://newsletter.victordibia.com/p/4-ux-design-principles-for-multi)** _available_
- **[Production agents with action-level risk classifiers (Anthropic computer-use, OpenAI Operator)](https://platform.claude.com/docs/en/docs/agents-and-tools/computer-use)** _available_

## Related patterns

- _uses_ **Approval Queue**
- _uses_ **Human-in-the-Loop**
- _composes-with_ **Policy-as-Code Gate**
- _composes-with_ **crawl-walk-run-automation-gating**
- _complements_ **Autonomy Slider**
- _complements_ **Two Human Touchpoints**
- _alternative-to_ **Agent Privilege Escalation**
- _composes-with_ **Progressive Delegation**
- _alternative-to_ **Risk-Tiered Action Autonomy** — Cost-aware delegation tiers by compute cost; risk-tiered autonomy tiers by financial materiality with an approver-distinct-from-initiator gate.
- _alternative-to_ **SLA-Aware Triage Scoring** — Cost-aware-action-delegation tiers an action by risk to choose an approval policy; this pattern tiers a queued ticket by SLA-impact to choose its position in the work order.
- _complements_ **Semantic Decision Node** — Classifying an action as read-only, reversible or destructive is a typical semantic decision node; the tiered approval policy is the code that consumes its answer.

## References

- [4 UX Design Principles for Multi-Agent Systems](https://newsletter.victordibia.com/p/4-ux-design-principles-for-multi) — Victor Dibia, 2025
- [Designing Multi-Agent Systems](https://multiagentbook.com/) — Victor Dibia, 2025
