# Prompt Versioning

**Also known as:** Prompt-as-Artifact, Prompt Registry, Versioned Prompts

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Treat prompts as immutable, hashed, semver'd artefacts in a registry; deploy and roll back like code.

## Context

Production agents where prompt changes drive quality changes; ad-hoc prompt edits introduce silent regressions.

## Problem

Prompts edited inline in code are hard to audit; rolling back a prompt means rolling back a deployment; comparison across versions is bespoke.

## Forces

- Registry adds infrastructure.
- Prompt versioning must integrate with eval harness.
- Signed prompts vs editable prompts.


## Applicability

**Use when**

- Prompts are edited often and audit, rollback, or A/B comparison is required.
- Eval outcomes need to be tied to specific prompt versions.
- A registry can hold immutable, hashed, semver-tagged artefacts.

**Do not use when**

- Prompts are stable and rarely changed.
- No registry exists and the operational cost outweighs current churn.
- Inline prompts already work and there is no audit obligation.

## Solution

Prompts live in a registry as immutable, hashed, version-tagged artefacts. Code references prompts by name + version (semver). Deployments pin specific versions; rollback by version. Eval harness ties metric outcomes to prompt versions. Optionally signed for provenance.

## Example scenario

A team rolls a small wording change into a prompt at 14:00 and by 16:00 the agent's behaviour has shifted in ways nobody predicted. There is no clean rollback short of redeploying the entire service from a prior commit. They adopt prompt-versioning: prompts live in a registry as immutable, hashed, semver-tagged artefacts; code references them by name plus version; deployments pin a specific version; rollback is a one-line config change. Eval-harness metrics tie to prompt versions. The next bad-prompt incident is reverted in under a minute.

## Diagram

```mermaid
flowchart LR
  Ed[Author edits prompt] --> H[Hash + semver tag]
  H --> Reg[(Prompt registry<br/>immutable, signed)]
  Code[Application code] -->|name + version| Reg
  Reg --> Dep[Deployment]
  Dep --> Eval[Eval harness]
  Eval -.ties metrics to.-> Reg
```

## Consequences

**Benefits**

- Prompt rollback without redeploy.
- Eval results map to specific prompts.

**Liabilities**

- Registry infrastructure.
- Version-pinning means prompts stop tracking model upgrades automatically.

## What this pattern constrains

Production calls reference pinned prompt versions only; ad-hoc inline prompts are forbidden.

## Known uses

- **LangSmith Prompts** — *Available*
- **PromptLayer** — *Available*
- **Humanloop** — *Available*
- **Vellum** — *Available*
- **Helicone Prompts** — *Available*

## Related patterns

- *composes-with* → [lineage-tracking](lineage-tracking.md)
- *uses* → [eval-as-contract](eval-as-contract.md)
- *complements* → [shadow-canary](shadow-canary.md)

## References

- (doc) *LangSmith Prompts*, <https://docs.smith.langchain.com/prompt_engineering/concepts>
- (doc) *PromptLayer*, <https://docs.promptlayer.com>
- (doc) *Humanloop*, <https://humanloop.com>

**Tags:** governance, prompt, versioning
