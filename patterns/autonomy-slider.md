# Autonomy Slider

**Also known as:** Autonomy Dial, Continuous Autonomy Control

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Expose agent autonomy as a continuous adjustable parameter so the same codebase can span scripted assistant to fully autonomous worker without re-architecting.

## Context

A product team owns one agent codebase but several deployment contexts: a free tier that should not act unsupervised, a paid tier where the user has opted into automation, an internal beta where engineers want full autonomy to stress-test. Hard-coding the autonomy level per build forks the codebase or branches the prompt.

## Problem

Binary 'workflow vs agent' framings collapse the design space to two points. Most real deployments want a position between — autonomous on some axes (information gathering), supervised on others (irreversible action). Without a control surface for autonomy, each new context forces an ad-hoc fork in code or in prompt, and the team loses the ability to dial the same agent across users, contexts, or risk profiles.

## Forces

- Different users and contexts justify different default autonomy.
- Autonomy is multidimensional — read vs write, internal vs external, reversible vs not.
- The control must be runtime-mutable so it can dial without redeploy.
- Operators need to inspect and audit the current setting.

## Therefore

Therefore: model autonomy as a runtime-mutable parameter that the agent and runtime consult on each action, so one codebase covers the full workflow-to-autonomous span by configuration rather than code.

## Solution

Define an autonomy parameter (scalar or vector) the runtime consults before each action. At one end the agent only emits suggestions a human acts on; at the other it acts directly and reports. Intermediate values gate by action type, confidence, or user opt-in. Persist the setting per-tenant or per-user. Surface the current value in the UI so users and operators see at a glance how autonomous the agent currently is.

## Structure

```
Operator or user --set--> Autonomy parameter (per tenant / per user); Agent proposes action --> Runtime gate (checks action against level) --authorised--> Execute | --not authorised--> Demote to suggestion for a human
```

## Diagram

```mermaid
flowchart LR
  Cfg[Autonomy parameter] --> Rt[Runtime gate]
  Act[Agent proposes action] --> Rt
  Rt --> P{Authorised at this level?}
  P -- yes --> Exec[Execute]
  P -- no --> Sug[Demote to suggestion]
  Op[Operator] -.-> Cfg
  User -.-> Cfg
```

## Example scenario

A coding-assistant product ships with an autonomy slider: at 0, the agent only suggests; at 1, it edits files; at 2, it runs tests; at 3, it commits and pushes. New users default to 1; power users opt into 3 per repository. A bug-bash mode drops the entire fleet to 1 within a release while the team investigates a regression.

## Consequences

**Benefits**

- One codebase serves many autonomy contexts.
- Per-tenant or per-user tuning without redeploy.
- Operators can dial autonomy down quickly in response to incidents.

**Liabilities**

- A continuous knob invites micro-tuning that has no clear meaning.
- Multidimensional autonomy is hard to render as a single slider; teams collapse to a slider that loses information.
- Users may not know what setting they are on if the UI hides it.

## Failure modes

- Meaningless notch — operators nudge the setting by small steps that change no real behaviour, and nobody can say what a given value allows.
- Flattened axes — a single slider hides that the agent should be free to read but gated on irreversible writes, so one value is wrong for one of them.
- Invisible setting — the UI does not show the current level, and a user assumes suggestion mode while the agent is acting directly.

## What this pattern constrains

The agent must not act at an autonomy level the runtime parameter does not currently authorise; autonomy is decided by the parameter, not by the agent's own reasoning.

## Applicability

**Use when**

- One agent codebase needs to serve materially different autonomy contexts.
- Operators need to dial autonomy down quickly without redeploy.
- Users should be able to opt into higher autonomy explicitly.

**Do not use when**

- The product has a single autonomy level for everyone forever.
- A discrete tier vocabulary (Crawl/Walk/Run) is what stakeholders ask for.
- Multidimensional autonomy cannot honestly compress to a single slider without misleading users.

## Components

- Autonomy parameter — runtime-mutable scalar or vector
- Runtime gate — consults the parameter before each action
- Persistence layer — stores per-tenant or per-user setting
- UI surface — exposes current setting to user and operator

## Tools

- Config store — keyed per tenant/user, low-latency read on every action
- Audit log — records autonomy-setting changes
- Dashboard — shows distribution of autonomy across the user base

## Evaluation metrics

- Setting distribution — histogram across users
- Time-at-max-autonomy — total time spent at the highest setting
- Demotion incidents — operator-triggered cuts in autonomy and their causes

## Known uses

- **[Building Applications with AI Agents (Albada, O'Reilly 2025) — Autonomy Slider UX pattern](https://www.oreilly.com/library/view/building-applications-with/9781098176495/ch03.html)** _available_
- **[Cursor / Claude Code agent-mode toggles](https://www.anthropic.com/engineering/claude-code-auto-mode)** _available_

## Related patterns

- _alternative-to_ **crawl-walk-run-automation-gating** — Three discrete tiers; this is the continuous version.
- _complements_ **Cost-Aware Action Delegation**
- _complements_ **Progressive Delegation**
- _complements_ **Approval Queue**
- _complements_ **Human-in-the-Loop**
- _complements_ **Kill Switch**
- _complements_ **Risk-Tiered Action Autonomy** — A continuous knob versus a discrete per-action partition with a release gate.
- _complements_ **Velocity-and-Magnitude Governor** — The governor's beyond-threshold deviation is what drives the slider down from human-on-the-loop to human-in-the-loop; the slider expresses the autonomy level, the governor decides when to lower it.

## References

- [Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/) — Michael Albada, 2025
