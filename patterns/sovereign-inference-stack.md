# Sovereign Inference Stack

**Also known as:** On-Premise Agent Stack, Data-Residency Agent Architecture, Sovereign AI

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Run the entire agent stack (model weights, inference, tool layer, vector stores, logs) inside a jurisdictional and operational boundary the operator controls, so no request, prompt, or output crosses into a third-party API.

## Context

Public administration, regulated industry (banking, defense, health), or critical infrastructure operators where data egress to a foreign-cloud LLM provider is forbidden by policy or law (e.g. EU AI Act high-risk systems, BSI C5, NIS2, sectoral data-protection regimes).

## Problem

Hosted-API agents leak prompts, tool inputs, and outputs to a third party; for regulated workloads this is a non-starter regardless of contractual assurances.

## Forces

- Frontier hosted models offer the best capability per dollar.
- Regulators forbid data egress for protected categories.
- Self-hosting demands GPU capex and MLOps competence the operator may lack.
- Sovereign deployments must still reach acceptable model quality to be useful.


## Applicability

**Use when**

- Regulated workload forbids data egress to a foreign-cloud LLM provider.
- Permissively licensed or sovereign-licensed models meet quality requirements.
- The operator can run inference on-prem or in a controlled jurisdiction.

**Do not use when**

- Data egress to a hosted API is allowed and frontier capability matters more.
- Self-hosted operations cost or complexity exceeds the regulatory benefit.
- Available open-weight models cannot meet quality targets for the workload.

## Therefore

Therefore: place every load-bearing component (weights, inference, tools, memory, logs, eval) inside one operator-controlled jurisdictional boundary and forbid any agent path that crosses it, so that no prompt or output ever reaches a third-party API.

## Solution

Choose models with permissive weights or commercial sovereign licensing. Run inference on-prem or in a jurisdictionally controlled cloud region with the operator holding the keys. Place all auxiliary services (vector store, tool gateway, audit log, evaluation harness) inside the same boundary. Document the boundary as part of the system's compliance posture (model card, data-flow diagram). Treat the boundary as load-bearing: any new tool or model call has to be reviewed for boundary impact before merge.

## Example scenario

A bank wants an internal coding assistant but legal flatly forbids any source-code or prompt leaving the bank's controlled boundary, regardless of vendor contractual language. The team picks a permissively-licensed open-weights model, runs inference in their own datacentre, places the vector store and trace logs inside the same boundary, and holds the keys themselves. No request, prompt, or output ever crosses to a third-party API; the assistant ships under regulator review.

## Structure

```
Boundary { Inference + Tools + Memory + Logs + Eval } -- only public artefacts (UI responses) leave.
```


## Diagram

```mermaid
flowchart TB
  subgraph Boundary[Operator-controlled boundary]
    Inf[On-prem inference]
    Tools[Tool gateway]
    Vec[(Vector store)]
    Logs[(Audit log)]
    Eval[Eval harness]
  end
  U[User UI] --> Inf
  Inf --> Tools
  Tools --> Vec
  Inf --> Logs
  Inf -.never crosses.-x Ext[Third-party API]
  Inf --> U
```

## Consequences

**Benefits**

- Compliant with data-residency and sectoral regulations.
- Auditable end-to-end; no opaque third-party API.
- Operator retains negotiating power over model upgrades and pricing.

**Liabilities**

- Capex and operational complexity (GPU fleet, ops team).
- Capability gap vs. frontier hosted models is real and ongoing.
- Each new model upgrade is a procurement project, not an API key swap.

## What this pattern constrains

No prompt, tool input, tool output, or memory entry may leave the operator-controlled boundary; agent components that require a third-party hosted call are forbidden by construction.

## Known uses

- **[Aleph Alpha PhariaAI](https://docs.aleph-alpha.com/phariaai-home/latest/index.html)** — *Available*. End-to-end stack (Pharia models, PhariaEngine WebAssembly skill runtime, on-prem deployable) marketed for sovereign / explainable enterprise and government use.
- **Mistral on-prem ("Le Chat Enterprise" / private deployment)** — *Available*. Self-hostable European model option used for similar sovereignty requirements.
- **SAP Joule with private grounding** — *Available*. Tenant-isolated agent stack with customer data residency commitments.

## Related patterns

- *complements* → [session-isolation](session-isolation.md)
- *complements* → [model-card](model-card.md)
- *uses* → [lineage-tracking](lineage-tracking.md)
- *complements* → [secrets-handling](secrets-handling.md)
- *complements* → [constitutional-charter](constitutional-charter.md)
- *complements* → [open-weight-cascade](open-weight-cascade.md)

## References

- (doc) *PhariaAI Documentation*, <https://docs.aleph-alpha.com/phariaai-home/latest/index.html>
- (doc) *Aleph Alpha — Sovereign AI Solutions*, <https://aleph-alpha.com/>

**Tags:** safety, compliance, germany-origin, sovereignty, eu-ai-act
