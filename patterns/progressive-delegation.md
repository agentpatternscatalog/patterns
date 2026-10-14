# Progressive Delegation

**Also known as:** Trust-Graded Handoff, Permission Ratchet

**Category:** Multi-Agent  
**Status in practice:** emerging

## Intent

Stage the human-to-agent handoff over time: the agent starts producing drafts a human always reviews; its autonomy expands action-by-action as measured trust accrues.

## Context

A team is introducing an agent that will eventually take over parts of a human workflow — drafting code review comments, triaging support tickets, scheduling meetings. The end state is fully autonomous on routine cases; the starting state is human-supervised because trust has not been built.

## Problem

One-shot deployment swings between two failure modes. Going fully autonomous on day one yields trust incidents because the team has no measured basis for confidence. Going fully supervised forever yields no learning — the team never accumulates the success-rate data that would justify expansion, and the agent's value is capped at 'faster drafter'. Without a per-action ratchet, autonomy decisions are calendar-driven, not evidence-driven.

## Forces

- Trust must be earned per action class, not per agent.
- The success-rate window per action must be long enough to be evidence.
- Demotion when a class regresses must be cheap and visible.
- Multiple action classes can be at different trust levels simultaneously.

## Therefore

Therefore: ratchet the agent's autonomy per action class as a function of measured historical success, so trust accrues from evidence and a regression in one class only demotes that class.

## Solution

Tag each action class with a current autonomy level (draft -> assisted-send -> autonomous). For each class the runtime tracks a rolling success-rate window. Promotion fires automatically when the window clears a bar over enough samples; demotion fires when it drops below. The promotion mechanism is the policy of record, not a verbal decision in standup. The same agent runs many action classes at different levels simultaneously.

## Structure

```
Action class at level Draft --success window clears bar--> Assisted --success window clears bar--> Autonomous; regression in window --> demote one level; each action class tracked separately
```

## Diagram

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Assisted : success window clears
  Assisted --> Autonomous : success window clears
  Autonomous --> Assisted : regression in window
  Assisted --> Draft : regression in window
```

## Example scenario

A meeting-scheduling agent runs three action classes: propose-times (autonomous from day one), send-invite (assisted: drafts an invite, human clicks send), and reschedule (autonomous after 200 successful proposals without complaint). After two months reschedule reaches its bar and promotes; a complaint a month later demotes it back automatically.

## Consequences

**Benefits**

- Autonomy decisions become a function of evidence rather than calendar.
- Different action classes can sit at different levels honestly.
- Trust incidents demote only the affected class, not the whole agent.

**Liabilities**

- Promotion gates can be cheaply gamed if the success metric is weak.
- Demotion thrashing on small windows can yank capabilities away noisily.
- Per-class bookkeeping is overhead that small teams underinvest in.

## Failure modes

- Gamed promotion — the success metric is weak, so an action class clears the bar without being trustworthy and goes autonomous.
- Demotion thrash — a small window lets one or two bad outcomes demote a class, and capabilities flip back and forth.
- Skipped bookkeeping — a small team stops tracking per-class success rates, and promotion falls back to a verbal decision.
- Whole-agent promotion — the team promotes the agent as a unit, and a weak action class gains autonomy along with the strong ones.

## What this pattern constrains

Agent autonomy on an action class must not be promoted by calendar or seniority; promotion requires the documented success-rate window to clear the bar.

## Applicability

**Use when**

- Multiple action classes with materially different risk.
- Per-class success can be measured online with reasonable delay.
- Stakeholders want autonomy to be a measurement, not a meeting decision.

**Do not use when**

- Only one action class exists — a simple [[autonomy-slider]] or [[crawl-walk-run-automation-gating]] suffices.
- No reliable per-class success signal can be measured.
- The agent will live for too short to accumulate evidence per class.

## Components

- Action-class registry — maps actions to their current autonomy level
- Rolling success-rate window — per-class measured signal
- Promotion gate — automatic ratchet up when window clears bar
- Demotion gate — automatic ratchet down on regression

## Tools

- Per-class telemetry — feeds the rolling window
- Approval queue — used at draft and assisted levels
- Audit log — records promotions and demotions

## Evaluation metrics

- Per-class promotion lag — days from passing bar to promotion.
- Per-class demotion rate — promotions later reversed.
- Class coverage — fraction of action classes with a ratchet vs hardcoded level.

## Known uses

- **[Building Applications with AI Agents (Albada) — Progressive Delegation in human-agent collaboration](https://www.oreilly.com/library/view/building-applications-with/9781098176495/ch13.html)** _available_
- **Production code-review agents promoting suggest→commit per file class** _available_

## Related patterns

- _complements_ **crawl-walk-run-automation-gating** — Three-tier ramp; progressive-delegation is the per-action ratchet.
- _complements_ **Autonomy Slider**
- _composes-with_ **Cost-Aware Action Delegation**
- _uses_ **Approval Queue**
- _complements_ **Shadow Canary**
- _uses_ **Human-in-the-Loop**
- _complements_ **Risk-Tiered Action Autonomy** — Ratchets on track record; risk-tiering keys the ceiling on materiality.
- _alternative-to_ **Attenuating Delegation Chain** — That pattern widens an agent's autonomy across runs as a human observes measured performance; this one forbids widening within a single call tree. They operate on different axes and are usually combined.
- _alternative-to_ **Monotonic Privilege Confinement** — Stages the human-to-agent handoff upward across deployments as measured trust accrues; here the ratchet runs downward inside one execution and can never widen on its own evidence.

## References

- [Building Applications with AI Agents](https://www.oreilly.com/library/view/building-applications-with/9781098176495/ch13.html) — Michael Albada, 2025
