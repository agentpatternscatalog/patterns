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

## Solution

Maintain a markdown document at a known location with sections: intended use, out-of-scope use, training/data lineage, evaluation results, limitations, risks, contact. Versioned alongside the agent.

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
