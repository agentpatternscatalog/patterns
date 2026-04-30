# Black-Box Opaqueness

**Also known as:** Opaque Agent, No-Trace Agent

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: ship an agent without traces, decision logs, or provenance, then debug from user reports.

## Context

Schedule pressure or framework defaults push the agent into production with no observability hooks.

## Problem

When (not if) the agent does something wrong, there is no record of why; debugging is reduced to reproduction attempts.

## Forces

- Observability has a cost (storage, dev time).
- Frameworks differ in trace quality.
- Privacy and trace coverage tension.

## Solution

Don't. Add traces, decision logs, and provenance from day one. See provenance-ledger, decision-log, lineage-tracking.

## Consequences

**Liabilities**

- Debugging time stretches to weeks.
- Compliance posture is unanswerable.
- Stakeholder trust erodes.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Default state of un-instrumented LangChain projects circa 2023** — *Available*

## Related patterns

- *alternative-to* → [provenance-ledger](provenance-ledger.md)
- *alternative-to* → [decision-log](decision-log.md)
- *alternative-to* → [lineage-tracking](lineage-tracking.md)

## References

- (repo) *ai-standards/ai-design-patterns (Black-Box Opaqueness)*, <https://github.com/ai-standards/ai-design-patterns>

**Tags:** anti-pattern, observability
