# Perma-Beta

**Also known as:** Forever Beta, Eval Vacuum

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: ship the agent in 'beta' indefinitely so that quality regressions are someone else's problem.

## Context

An agent is launched without an eval harness and stays in beta because removing the label would create accountability for quality.

## Problem

Beta becomes a permanent excuse. Without an eval harness, quality is a guess and regressions are invisible.

## Forces

- Eval harnesses cost time to build.
- GA promises commit to quality bars.
- Beta lets product move fast.


## Applicability

**Use when**

- Never use this; treat indefinite beta as a smell and exit it deliberately.
- Build an eval harness so quality regressions are visible (see eval-harness).
- Pair eval-harness with llm-as-judge and shadow-canary to gate releases.

**Do not use when**

- Any agent serving real users where regressions matter.
- Any product where 'beta' is being used as an excuse for missing evaluation.
- Any team that has the resources to build an eval harness but has not.

## Solution

Don't. Build the eval harness and exit beta. See eval-harness, llm-as-judge, shadow-canary.

## Example scenario

A startup launches its agent product as 'beta' and uses the label as a blanket excuse for any quality complaint. Eighteen months later the agent is still beta, there is no eval harness, and customers have started churning to a competitor that ships GA. The team names the failure perma-beta and forces an exit: build the eval suite, set quality gates, fix the regressions blocking GA, and remove the beta label. The label was hiding the fact that nobody actually knew whether the product was getting better or worse.

## Consequences

**Liabilities**

- Trust erosion.
- No SLA defensibility.
- Quality stagnates without measurement.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Many AI products since 2023** — *Available*

## Related patterns

- *alternative-to* → [eval-harness](eval-harness.md)
- *alternative-to* → [shadow-canary](shadow-canary.md)
- *conflicts-with* → [eval-as-contract](eval-as-contract.md)

## References

- (repo) *ai-standards/ai-design-patterns (Perma-Beta)*, <https://github.com/ai-standards/ai-design-patterns>

**Tags:** anti-pattern, release, beta
