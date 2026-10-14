# Refusal

**Also known as:** Decline, Out-of-Scope Response

**Category:** Safety & Control  
**Status in practice:** mature

## Intent

Explicitly refuse requests that fall outside the agent's scope, capability, or policy boundaries.

## Context

A team runs an agent with a defined scope — customer support for a specific product, technical help in a specific domain, internal operations for a specific team — and real users will ask it things outside that scope: medical advice from a banking agent, legal interpretation from a coding assistant, competitor comparisons from a vendor's own bot. Some of these requests are simply off-topic; others are unsafe, regulated, or beyond what the model can reliably do.

## Problem

A helpful-by-default agent answers these out-of-scope questions anyway, producing plausible-sounding but unauthorised content: a stock pick from a system that has no business giving one, a dosage suggestion from a tool that is not a medical device, a confident wrong answer in a domain the model has not been validated against. Silently routing such requests through the model also strips the user of the signal that the agent has a boundary. Without an explicit, kind refusal at the named boundary, the agent drifts into territory that erodes trust and exposes the operator.

## Forces

- Over-refusal frustrates users.
- Under-refusal lands the agent in trouble.
- Refusal text quality matters; templated refusals feel insulting.

## Therefore

Therefore: trigger an explicit, specific refusal at the named boundary instead of trying to be helpful anyway, so that the agent stays inside its scope and the limit itself becomes visible to the user.

## Solution

Define refusal triggers (policy violation, out-of-scope, capability gap, regulatory boundary). Return a clear, kind, specific refusal that names the boundary and (when possible) suggests an alternative. Log refusals for review.

## Structure

```
Request --> Refusal trigger check (policy / out of scope / capability gap / regulatory) --none--> Handle normally | --hit--> Clear, specific refusal --> Suggest alternative + log refusal
```

## Diagram

```mermaid
flowchart TD
  Req[Request] --> T{Refusal trigger?}
  T -->|policy violation| Ref[Clear, kind refusal]
  T -->|out of scope| Ref
  T -->|capability gap| Ref
  T -->|regulatory| Ref
  T -->|none| Run[Handle normally]
  Ref --> Alt[Suggest alternative]
  Ref --> Log[(Refusal log)]
```

## Example scenario

A customer-service agent for a bank starts being asked for stock picks, legal advice, and competitor comparisons. Helpful-by-default, it answers and gets the bank into hot water. The team defines refusal triggers (regulatory boundary, out-of-scope, capability gap) and a kind, specific refusal template that names the boundary and points to a human team. Out-of-scope replies stop being plausible-sounding hallucinations and start being short, clear handoffs.

## Consequences

**Benefits**

- Trust improves: the agent has visible limits.
- Compliance posture is defensible.

**Liabilities**

- Calibration of triggers is empirical.
- Refusal-fatigue when triggers are wrong.

## Failure modes

- Refusal fatigue — triggers are set too broad, the agent refuses ordinary in-scope requests, and users stop trusting it.
- Vague refusal — the reply says 'cannot help' without naming the boundary or an alternative, and the user rephrases until something gets through.
- Missed trigger — an out-of-scope request does not match any trigger, and the agent answers it with confident, unauthorised content.

## What this pattern constrains

When triggers fire, the agent must refuse rather than attempt the task.

## Applicability

**Use when**

- Requests fall outside scope, capability, or policy and helpful-by-default would harm.
- Clear refusal triggers can be defined (policy violation, out-of-scope, regulatory boundary).
- Refusals can name the boundary and suggest an alternative when possible.

**Do not use when**

- The agent is a fully unrestricted research tool with no scope to defend.
- Refusal triggers are so vague they would block legitimate work.
- Logging refusals for review is not feasible and silent drops are unacceptable.

## Components

- Refusal-trigger detector — checks for policy, scope, capability, and regulatory hits
- Refusal surface — clear, kind message that names the boundary back to the user
- Alternative-suggester — optional pointer to a human team or other resource
- Refusal log — record of trigger, request shape, and surfaced message for later review

## Tools

- Scope classifier — categoriser that labels requests against the agent's defined domain
- Refusal-template library — vetted phrasings per trigger to avoid templated-feeling rejections

## Evaluation metrics

- Refusal precision — share of refusals reviewers agreed were warranted
- Refusal recall — share of out-of-scope requests the trigger detector caught
- Over-refusal rate — legitimate in-scope requests that triggered a refusal
- User-satisfaction post-refusal — survey or thumbs-rating on refusal interactions

## Known uses

- **OpenAI moderation API** _available_
- **Anthropic safety classifier (Claude)** _available_
- **Lakera Guard refusal flows** _available_
- **NVIDIA NeMo Guardrails** _available_

## Related patterns

- _uses_ **Constitutional Charter**
- _complements_ **Input/Output Guardrails**
- _conflicts-with_ **Code-Switching-Aware Agent**
- _complements_ **Policy-as-Code Gate**
- _complements_ **Typed Refusal Codes**
- _complements_ **Reflexive Metacognitive Agent**
- _alternative-to_ **Over-Helpfulness** — Refusal is the corrective: scoped requests that fail the capability gate are declined instead of attempted, which is exactly what over-helpfulness skips.
- _generalises_ **Scope-of-Practice Boundary Gate** — Refusal is the general act of declining out-of-scope requests on the model's judgment; this gate specialises it to a code-enforced boundary keyed to legally reserved professional acts.
- _alternative-to_ **Enforced Advisory Disclaimer** — Refusal declines the request; the enforced advisory answers it but frames the answer as information rather than professional advice.

## References

- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) — Bai et al., 2022
