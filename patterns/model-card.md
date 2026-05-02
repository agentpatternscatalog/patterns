# Model Card

**Also known as:** System Card

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Maintain a structured document describing the model/agent's intended use, limitations, evaluation results, and risks.

## Context

Regulated, high-stakes, or public-facing agents where stakeholders (legal, compliance, users) need to understand what the system does and where it fails.

## Problem

Agent capabilities and limitations are tribal knowledge; without a card, every stakeholder reinvents understanding.

## Forces

- Cards age fast in fast-moving systems.
- Truthful disclosure conflicts with marketing pressure.
- Card depth vs maintainability.


## Applicability

**Use when**

- Multiple stakeholders need a shared understanding of agent capabilities and limits.
- Intended use, out-of-scope use, and known risks are stable enough to document.
- Evaluation results exist or can be produced periodically.

**Do not use when**

- The agent is an internal experiment with one consumer and no governance need.
- Capabilities change so fast that a card would be stale before publication.
- No team can own keeping the card current.

## Solution

Maintain a markdown document at a known location with sections: intended use, out-of-scope use, training/data lineage, evaluation results, limitations, risks, contact. Versioned alongside the agent.

## Example scenario

A new product manager joins and has to explain to a regulator what the underwriting agent does, what data it was trained on, and where it is known to fail. The institutional knowledge lives in three engineers' heads and a Slack thread. The team writes a model-card: intended use, out-of-scope use, training data lineage, evaluation results by demographic slice, known limitations, contact owner. It lives at /docs/agents/underwriter-card.md, is versioned with the agent, and is the canonical reference for the next regulator question.

## Consequences

**Benefits**

- Stakeholder alignment.
- Regulatory and audit defensibility.

**Liabilities**

- Maintenance burden.
- Card drift when not enforced in PRs.

## What this pattern constrains

Production releases require a current card; missing or stale cards block deployment.

## Known uses

- **Anthropic system cards** — *Available*
- **Google Model Cards** — *Available*

## Related patterns

- *complements* → [lineage-tracking](lineage-tracking.md)
- *complements* → [eval-harness](eval-harness.md)
- *complements* → [provenance-ledger](provenance-ledger.md)
- *generalises* → [awareness](awareness.md)
- *alternative-to* → [hidden-mode-switching](hidden-mode-switching.md)
- *complements* → [sovereign-inference-stack](sovereign-inference-stack.md)
- *complements* → [attention-manipulation-explainability](attention-manipulation-explainability.md)

## References

- (paper) Mitchell, Wu, Zaldivar, Barnes, Vasserman, Hutchinson, Spitzer, Raji, Gebru, *Model Cards for Model Reporting*, 2018, <https://arxiv.org/abs/1810.03993>

**Tags:** governance, documentation
