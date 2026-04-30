# Self-Modification Diff Gate

**Also known as:** Diff Reviewer, Self-Mod Gate, Inner Critic

**Category:** Verification & Reflection  
**Status in practice:** experimental

## Intent

Gate the agent's edits to its own code or rules through a separate critic persona that reviews the diff before it lands.

## Context

A self-modifying agent can edit its own source, prompts, or rules; without a gate, recursive self-editing can drift into incoherence or unsafe behaviour.

## Problem

Self-edits applied directly bypass review; the agent can corrupt its own future behaviour irreversibly.

## Forces

- Critic and modifier may share blind spots if they share a model.
- Strict critics block legitimate improvements.
- Lax critics defeat the gate.

## Solution

Every self-edit goes through a critic step: a separate prompt (and optionally a separate model) reviews the proposed diff against criteria (safety, charter compliance, test passing). Edits land only on critic approval. Rejected edits are logged for later human review. The critic must run on a frozen checkpoint (separate process or sandbox) so a malformed self-edit cannot corrupt the critic before it votes; recursion guard is required when the critic itself is in the edit scope.

## Consequences

**Benefits**

- Recursive self-improvement becomes survivable in practice.
- Audit trail of what was rejected is itself learning signal.

**Liabilities**

- Critic prompt is a load-bearing artefact; bad critics are worse than no critic.
- Two-step pipeline doubles per-edit latency.

## What this pattern constrains

No write to self-modifiable files succeeds without a passing critic review.

## Known uses

- **Sparrot** — *Available*. src/sparrot/*.py edits gated by critic.py.

## Related patterns

- *used-by* → [skill-library](skill-library.md)
- *uses* → [constitutional-charter](constitutional-charter.md)
- *generalises* → [inner-committee](inner-committee.md)
- *complements* → [quorum-on-mutation](quorum-on-mutation.md)

## References

- (blog) *Marco Nissen, Working with the models*, 2026

**Tags:** self-modification, critic, safety
