# Cultural Alignment Guard

**Also known as:** حارس الاتساق الثقافي, Two-Axis Safety Filter, Locale-Norm Guard, Cultural Misalignment Score

**Category:** Safety & Control
**Status in practice:** emerging

## Intent

Score model output along two independent axes — universal harmlessness and locally-specific cultural-norm violation — so deployments can set independent thresholds per axis and overlay locale-specific norms on top of a generic safety baseline.

## Context

LLM deployments that serve a culturally-defined audience (religious community, regional locale, age group, school) where content can be technically harmless in the global sense yet violate community-specific norms (dietary, modesty, ritual, denominational, age-appropriateness). The deployer is closer to the community than the model vendor and must be able to tune cultural sensitivity without weakening the universal-harm filter.

## Problem

Most safety classifiers project all undesirable outputs onto a single normative axis, so the only knob is 'safer' or 'less safe'. This collapses two genuinely different judgments — is this universally harmful, and does this violate the deploying community's norms — into one number. A deployer cannot, for example, keep the universal-harm threshold strict while raising sensitivity to alcohol references for a Muslim audience, or to non-kosher food imagery for an Orthodox audience, or to denominational specifics for a Hasidic deployment. Trying to express these as a single combined score either over-blocks the universal channel or under-protects the cultural one.

## Forces

- Universal harm and cultural-norm violation are independent judgments; collapsing them loses information.
- The deployer is closer to the community than the model vendor and must own the cultural threshold.
- Cultural norms are plural and contradictory across deployments; no single global threshold fits.
- A scoring head must be calibrated on community-annotated data, not on a generic safety corpus.
- Over-blocking the cultural axis silently degrades utility; under-blocking erodes community trust.

## Therefore

Therefore: emit two independent scores from the safety layer — one for universal harmlessness, one for cultural-norm alignment relative to a named locale or community — and let the deployer set each threshold separately, so the cultural overlay can be tuned without weakening the universal filter.

## Solution

The safety classifier exposes two regression or classification heads sharing an encoder: a universal-harm head trained on broad harmfulness labels, and a cultural-alignment head trained on community-annotated norm-violation labels tagged with a locale or community id. At inference, both heads score every output. The deploying application configures two thresholds (universal_harm_max, cultural_violation_max) and, optionally, which community label to evaluate against. Outputs failing either threshold are blocked or rewritten by a downstream rewriter. Threshold pairs are part of the deployment manifest and ship with the application, not with the base model. Community-specific evaluation sets are versioned so changes in cultural calibration are auditable.

## Structure

```
Generated output --> Shared encoder --> {universal-harm head, cultural-alignment head[locale]} --> (score_h, score_c) --> Threshold check (universal_harm_max, cultural_violation_max) --> {pass | block | route-to-rewriter}.
```

## Example scenario

A Gulf-region search assistant runs on top of a multilingual model. Its operators need the assistant to behave well by global standards and additionally to respect locally-prevalent Muslim norms in user-facing text and image prompts. The safety layer emits two scores per output: a universal-harm score and a cultural-alignment score relative to a Gulf-Arabic community label. The deployment sets a strict universal-harm threshold and a separate, tighter cultural-alignment threshold; a generic-audience sibling deployment uses the same model with the cultural threshold relaxed. When a user's query elicits a recipe involving alcohol, the universal-harm head passes it but the cultural head flags it, and the assistant offers a halal substitution instead of refusing outright.

## Consequences

**Benefits**

- Deployers can tighten cultural sensitivity without touching the universal-harm threshold.
- Cultural calibration is a per-deployment configuration, not a fork of the base model.
- Failure modes are diagnosable: an audit can distinguish 'blocked for universal harm' from 'blocked for cultural violation in locale X'.
- Plural deployments (different communities) share one model and differ only in the two thresholds and the community label.

**Liabilities**

- Requires community-annotated training data, which is hard to source and harder to keep balanced.
- Two heads doubles the calibration and evaluation burden and the surface for distribution shift.
- Naming and scoping a 'community' is itself political; over-coarse labels misrepresent the community.
- A two-axis filter does not solve cultural-norm conflicts between an output and the user's actual identity if that identity is not the configured community.

## What this pattern constrains

The LLM must not collapse universal harm and cultural-norm violation into a single score, must not allow the cultural threshold to weaken the universal-harm filter, and must not apply a community's cultural overlay to a deployment that has not declared that community as its audience.

## Applicability

**Use when**

- The deployment serves a culturally-defined audience whose norms diverge from a generic safety baseline.
- The deployer is responsible to that audience and must own the cultural threshold independently of the model vendor.
- Community-annotated training or evaluation data for the cultural axis can be obtained.
- Plural deployments share a base model but differ in audience.

**Do not use when**

- The audience is generic and a single universal-harm classifier already meets the bar.
- Community-annotated data cannot be sourced; the cultural head would be uncalibrated.
- The deployer is unwilling or unable to name and bound the community whose norms are being applied.

## Known uses

- **[QCRI FanarGuard](https://arxiv.org/abs/2511.18852)** — *Available* — Two-axis safety classifier for Arabic-language LLMs; separates universal harmfulness from culturally-misaligned content using community-annotated data.

## Related patterns

- *specialises* → [input-output-guardrails](input-output-guardrails.md) — Specialises content-filtering guardrails by splitting the normative axis into universal and cultural channels.
- *complements* → [refusal](refusal.md) — Refusal is the action; the two-axis guard decides which axis triggered it and how to phrase the refusal.
- *complements* → [constitutional-charter](constitutional-charter.md) — A constitutional charter can encode the universal axis; the cultural overlay sits beside it as a separate threshold.
- *complements* → [pii-redaction](pii-redaction.md) — Both are protective filters but on orthogonal axes; PII redaction concerns data identity, cultural-alignment concerns norm fit.

## References

- (paper) *FanarGuard: A Culturally-Aware Safety Classifier for Arabic LLMs*, 2025, <https://arxiv.org/abs/2511.18852>
- (paper) Qatar Computing Research Institute, *Fanar 2.0 Technical Report*, <https://arxiv.org/abs/2603.16397>

**Tags:** safety-control, cultural-alignment, localisation, two-axis-classifier, guardrails, regional-llms
