# KRITIS Auditable Decision Artifact

**Also known as:** Run-ID + Modell-Digest + Policy-Hash Triple, KRITIS Audit Triple, Re-Executable Decision Record, AI-Act Article-12 Triple

**Category:** Governance & Observability
**Status in practice:** emerging

## Intent

For every agent action in regulated or critical-infrastructure contexts, emit a WORM-stored triple of run-id, model-digest, and policy-hash so each decision is independently re-verifiable against the exact code, weights, and policy version that produced it.

## Context

Agents operating in domains subject to EU AI Act, NIS2, BSI KRITIS, AIC4, or sectoral equivalents, where regulators or internal auditors must be able to replay any individual decision and prove it was produced by a specific, declared version of the model and the policy stack. Generic action logs and reasoning traces do not satisfy this bar because they do not pin the executable artifacts.

## Problem

An action log says what the agent did. A reasoning trace says what it claimed to be thinking. Neither lets an auditor re-execute the decision against the exact weights and rules that produced it months earlier, by which time the model has been updated and the policy has been revised many times. Regulators in critical-infrastructure and high-risk AI regimes increasingly require not just observability but re-verifiability: a decision is auditable only if the artifacts that produced it can be reconstructed from the log.

## Forces

- Auditors need re-executability, not just observability.
- Models, policies, and agent code drift on independent release cadences; a decision must pin all three.
- Storage must be tamper-evident; a mutable log is not an audit artifact.
- Cryptographic digests must be stable across re-execution; non-deterministic build inputs break replay.
- Hot-path logging cost must remain bounded; the triple must be compact and computable cheaply.
- Regulatory references (AI Act Art. 12, NIS2, BSI AIC4) explicitly tie obligations to artifact identity, not narrative summaries.

## Therefore

Therefore: for each agent decision, emit and store an immutable triple of (run-id, model-digest, policy-hash) — together with the input fingerprint and the verdict — in a WORM medium, so that the decision can be re-executed against the exact pinned artifacts and an auditor can verify the result.

## Solution

Establish a build pipeline that computes a content digest over the model weights (and tokenizer, system prompt, scaffolding) and a content hash over the policy bundle. Both digests are published, signed, and retained. At runtime, every agent decision is wrapped to emit a record containing run-id, model-digest, policy-hash, input fingerprint, decision verdict, and timestamp. Records are written to WORM storage (object-lock S3, immutable ledger, append-only DB) under a retention horizon set by the governing regulation. The model and policy artifacts themselves are retained for the same horizon, addressable by their digests, so any record can be replayed against its pinned versions. The triple is cited in user-facing audit responses and in regulator submissions.

## Structure

```
Agent decision --> Wrapper --> {run-id, model-digest, policy-hash, input-fingerprint, verdict, ts} --> WORM ledger. Model registry: model-digest --> weights+tokenizer+prompt blob. Policy registry: policy-hash --> rules bundle. Auditor: pick a record --> fetch pinned artifacts by digest --> re-execute --> compare verdict.
```

## Example scenario

A German energy operator runs an agent that helps dispatch grid-balancing actions. Each decision the agent makes is wrapped: the wrapper writes a record with the run-id, the digest of the deployed model weights, the hash of the active policy bundle, a fingerprint of the input situation, and the chosen action, into an immutable object-lock store retained for the regulatory horizon. Six months later BSI auditors pick a specific record, fetch the pinned model and policy by digest from the registry, replay the decision, and confirm the agent's verdict matches what was logged.

## Consequences

**Benefits**

- Every decision is re-executable against its pinned artifacts.
- Tamper-evident storage gives the log evidentiary weight.
- Maps cleanly onto AI Act Article 12 (record-keeping) and Article 14 (human oversight) obligations and onto BSI AIC4 audit criteria.
- Cross-version regression analysis becomes possible: compare decisions on the same inputs across model-digest changes.

**Liabilities**

- Retaining old weights and policy bundles for the full regulatory horizon is a real storage and security cost.
- Model non-determinism (sampling, hardware, kernel versions) can break replay unless seeds and inference environments are also pinned.
- Hot-path emission of the triple adds latency and a hard dependency on the WORM medium.
- Pinning is necessary but not sufficient: a decision can be 'auditable' and still wrong.
- Privacy obligations on the input fingerprint require careful design; raw inputs may not be retainable.

## What this pattern constrains

The LLM-driven decision path must not emit an action without producing the (run-id, model-digest, policy-hash) triple, must not write decision records to mutable storage, and must not allow model or policy updates to overwrite the artifacts referenced by retained records.

## Applicability

**Use when**

- The deployment is in scope of EU AI Act high-risk, NIS2, BSI KRITIS, AIC4, or analogous regimes.
- Auditors or regulators have or may acquire the right to replay individual decisions.
- Model and policy artifacts can be content-addressed and retained for the regulatory horizon.
- Decisions have material consequences (financial, safety, legal) and a narrative log alone is not enough.

**Do not use when**

- The deployment is non-regulated and a standard action log meets the bar.
- Model artifacts cannot be retained (e.g. third-party API with no version-pinning guarantee) and no equivalent pinning is achievable.
- Inference is intrinsically non-deterministic and replay cannot be approximated, removing the value of pinning.

## Known uses

- **[German KRITIS / regulated-enterprise agent deployments](https://www.heise.de/hintergrund/Agentic-AIOps-KI-Agenten-in-kritischen-Infrastrukturen-11267508.html)** — *Planned* — Emerging reference architectures described in heise's Agentic AIOps coverage couple agent action logs with model and policy version pins under BSI/NIS2 obligations.

## Related patterns

- *specialises* → [provenance-ledger](provenance-ledger.md) — Specialises a generic action/audit log by adding the cryptographic pinning of model and policy versions and the WORM retention requirement.
- *complements* → [decision-log](decision-log.md) — A decision log captures reasoning; the KRITIS triple captures the executable identity of model and policy at decision time. Both are needed in regulated contexts.
- *complements* → [model-card](model-card.md) — A model card documents the model in the abstract; model-digest in the triple identifies the specific deployed instance.
- *complements* → [eval-as-contract](eval-as-contract.md) — Eval-as-contract validates the model against a contract before release; the audit triple proves which validated version actually produced a given decision.
- *uses* → [policy-as-code-gate](policy-as-code-gate.md) — Policy-as-code naturally produces the policy-hash component of the triple.

## References

- (blog) *Agentic AIOps: KI-Agenten in kritischen Infrastrukturen*, <https://www.heise.de/hintergrund/Agentic-AIOps-KI-Agenten-in-kritischen-Infrastrukturen-11267508.html>
- (spec) *Regulation (EU) 2024/1689 (Artificial Intelligence Act), Articles 12 and 14*, 2024, <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>
- (spec) Bundesamt für Sicherheit in der Informationstechnik, *BSI AIC4 — AI Cloud Service Compliance Criteria Catalogue*, <https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/AIC4/aic4_node.html>

**Tags:** governance, audit, ai-act, kritis, nis2, bsi, worm, observability, re-executability
