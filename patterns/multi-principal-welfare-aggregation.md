# Multi-Principal Welfare Aggregation

**Also known as:** Multi-Principal Assistance Game, Social-Choice Aggregation for Agents

**Category:** Governance & Observability  
**Status in practice:** experimental

## Intent

When an agent serves multiple humans with conflicting preferences, declare the aggregation rule explicitly rather than letting it be implicit in the prompt or fine-tune.

## Context

An agent serves a team, a household, a customer cohort, or an entire user base. The principals have conflicting preferences: different staff want different summary styles, different customers want different escalation defaults, different users in a shared workspace want different behaviours. Some preferences are zero-sum.

## Problem

Without an explicit aggregation rule the agent silently picks one principal — usually the loudest, the most recently heard, or the one whose preferences were fine-tuned in earliest. Gibbard's theorem says any aggregation rule that aggregates more than two principals' preferences is manipulable: principals can strategically misreport. Pretending there is no aggregation rule does not avoid this; it picks the implicit rule and hides it from review.

## Forces

- Multiple principals with conflicting preferences is the common case at scale.
- Every aggregation rule has trade-offs; none is uniformly best.
- Hidden aggregation is gameable and unaccountable.
- Explicit aggregation invites disputes that hidden aggregation avoided.

## Therefore

Therefore: declare the aggregation rule (sum-of-utilities, weighted welfare, collegial mechanism, role-priority order) explicitly and as configuration, so the trade-off is reviewable and operators can change it deliberately.

## Solution

When the agent's action space affects multiple principals, route the decision through an explicit aggregation function. Options: sum-of-utilities (utilitarian); weighted welfare (declared per-principal weights); collegial mechanism (each principal must be obtaining 'enough' reward through their own actions for their preferences to count); role-priority (some principals have veto). Surface the active rule in traces and documentation. Make it a configuration change, not a prompt change.

## Structure

```
Principal registry (principals + weights) --> Per-principal preference probes --> Aggregation function (sum / weighted / collegial / role-priority, set by configuration) --> Decision --> Decision logger (principals consulted, rule, weights, outcome)
```

## Diagram

```mermaid
flowchart TD
  P1[Principal 1 prefs] --> Agg[Aggregation rule]
  P2[Principal 2 prefs] --> Agg
  P3[Principal 3 prefs] --> Agg
  W[Declared weights / rule type] --> Agg
  Agg --> Dec[Decision]
  Dec --> Log[Trace records rule + weights]
```

## Example scenario

A household assistant must schedule shared resources (the family calendar, the thermostat). Two adults have conflicting work-from-home preferences. The product declares a weighted-welfare rule with declared weights and exposes them in settings. When the rule produces an outcome one adult dislikes, the dispute is about the weights and the rule, not about the agent's hidden disposition.

## Consequences

**Benefits**

- Aggregation choice becomes a deliberate policy, not an implicit accident.
- Disputes over agent behaviour have a vocabulary — they argue about the rule.
- Operators can switch rules without retraining or re-prompting.

**Liabilities**

- Explicit rules invite explicit attacks on them (strategic misreporting per Gibbard).
- Some rules require principal-weight assignment that itself becomes contested.
- Computational cost of welfare aggregation scales with the principal count.

## Failure modes

- Strategic misreporting — a principal overstates their preferences because the declared rule rewards it, and the aggregate tilts toward them.
- Contested weights — the weighted rule needs per-principal weights, and the fight over those weights replaces the fight over outcomes.
- Rule left in the prompt — the aggregation logic is still phrased inside the prompt, so the configured rule and the agent's real behaviour differ.
- Untraced decision — the trace records the outcome but not which rule and weights produced it, and a disputed decision cannot be explained.

## What this pattern constrains

An agent serving multiple principals must not aggregate their preferences implicitly; the aggregation rule is declared as configuration and surfaced in traces.

## Applicability

**Use when**

- Agent serves multiple principals whose preferences can conflict.
- Actions are zero-sum or rivalrous across principals.
- Operators or users need to understand and adjust how aggregation works.

**Do not use when**

- Single-principal agent where aggregation is trivially identity.
- Aggregation rule cannot be made legitimate by any choice; the agent should not arbitrate at all.
- Engineering complexity of explicit aggregation exceeds the welfare gain.

## Components

- Principal registry — declared list of principals and weights
- Per-principal preference probe — collects preferences as evidence
- Aggregation function — sum / weighted / collegial / role-priority
- Decision logger — records principals consulted, weights applied, and outcome

## Tools

- Weight config store — keyed per workspace or tenant
- Aggregation calculator — evaluates the rule on per-principal preferences
- Audit log — surfaces the rule and weights for each decision

## Evaluation metrics

- Principal-coverage — share of decisions that consulted all relevant principals
- Dispute rate — share of decisions that triggered principal pushback
- Manipulation indicators — Gibbard-style strategic-reporting signals

## Known uses

- **[Multi-Principal Assistance Games (Fickinger, Zhuang, Hadfield-Menell, Russell, 2020)](https://arxiv.org/abs/2007.09540)** _available_
- **Shared-workspace assistants needing per-user weight assignment** _available_

## Related patterns

- _complements_ **Preference-Uncertain Agent**
- _uses_ **Cooperative Preference Inference**
- _composes-with_ **Policy-as-Code Gate**
- _complements_ **Decision Log**
- _complements_ **Trust and Reputation Routing**

## References

- [Multi-Principal Assistance Games](https://arxiv.org/abs/2007.09540) — Fickinger, Zhuang, Hadfield-Menell, Russell, 2020
- [Human Compatible](https://www.penguinrandomhouse.com/books/566677/human-compatible-by-stuart-russell/) — Stuart Russell, 2019
