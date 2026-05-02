# Provenance Ledger

**Also known as:** Audit Trail, Action Log

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Log every agent decision and state change with enough metadata to explain or reverse it later.

## Context

Long-running or regulated agents need to answer 'why did the agent do X on day Y?' months later.

## Problem

Without provenance, agent behaviour is post-hoc inscrutable; audit and rollback become impossible.

## Forces

- Auditability vs storage cost of every event.
- Schema rigidity vs evolvability over the agent's lifetime.
- PII in events: redaction at write time vs read time.


## Applicability

**Use when**

- Agent decisions and state changes must be explainable or reversible after the fact.
- An immutable, append-only log can be operated and queried.
- Each event can carry timestamp, actor, action, target, and justification fields.

**Do not use when**

- The agent has no consequential state changes worth logging.
- Storage and review cost of immutable logs are unjustified by risk.
- No queryable store is available to make the ledger useful.

## Solution

Append events to an immutable log with: timestamp, actor, action, target, justification (link to thought or decision), diff hash. Enable rollback by id. Reject events that lack the required fields.

## Example scenario

A regulator asks an insurance-claims agent why it rejected a specific claim three months ago. The team can show the final decision but not the chain of reasoning, the retrieved policy clauses, or which model version answered — the audit trail is partial. They add a provenance-ledger: every decision and state change appends an immutable event with timestamp, actor, action, target, justification link, and diff hash. Rollback by event id becomes trivial; the next regulator question is answered with a full reconstruction.

## Consequences

**Benefits**

- Audit and rollback become tractable.
- Pattern of failures becomes visible across time.

**Liabilities**

- Log volume can dominate other storage.
- Justification fields require the agent to write them; lazy agents skip.

## What this pattern constrains

Self-edits and other recorded actions are rejected if they lack a valid justification reference.

## Known uses

- **Sparrot** — *Available*. ledger.jsonl with {ts, file, diff_hash, thought_id, justification}; orphan writes rejected.
- **Langfuse traces** — *Available*
- **OpenTelemetry GenAI semantic conventions** — *Available*
- **Datadog LLM Observability** — *Available*

## Related patterns

- *composes-with* → [append-only-thought-stream](append-only-thought-stream.md)
- *specialises* → [decision-log](decision-log.md)
- *used-by* → [compensating-action](compensating-action.md)
- *complements* → [lineage-tracking](lineage-tracking.md)
- *complements* → [model-card](model-card.md)
- *alternative-to* → [black-box-opaqueness](black-box-opaqueness.md)
- *used-by* → [sandbox-escape-monitoring](sandbox-escape-monitoring.md)
- *complements* → [memo-as-source-confusion](memo-as-source-confusion.md)
- *used-by* → [emotional-state-persistence](emotional-state-persistence.md)
- *complements* → [world-model-separation](world-model-separation.md)

## References

- (doc) *OpenTelemetry GenAI semantic conventions*, 2024

**Tags:** audit, provenance, rollback
