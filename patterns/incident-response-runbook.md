# Incident Response Runbook

**Also known as:** IR Runbook, Agent Failure Playbook, Agent Incident Procedure

**Category:** Governance & Observability  
**Status in practice:** mature

## Intent

Maintain pre-written response procedures for agent failures (PII leak, tool exploit, mass false action) so detected incidents trigger known steps.

## Context

Production agents at organisations with safety controls (kill-switch, sandbox-escape-monitoring, provenance-ledger) that detect events nobody knows how to respond to.

## Problem

Without a runbook, detection produces alerts that wake the on-call but do not lead to coordinated containment, compensation, communication, or post-mortem.

## Forces

- Severity classification must be agreed upfront.
- Containment vs forensic preservation tension.
- Communication clocks for regulators (GDPR 72h, EU AI Act serious incident) constrain runbook latency.

## Solution

Maintain a runbook covering: severity levels, on-call paths, containment steps (kill-switch invocation, traffic rerouting), forensic preservation (pin traces beyond normal retention), compensating actions, customer communication templates, regulator notification procedures, and post-mortem template. Tie alerts from kill-switch/sandbox-escape-monitoring/cost-observability to runbook entries.

## Consequences

**Benefits**

- Detection produces coordinated response, not panic.
- Regulator timelines are met.

**Liabilities**

- Runbook drift: scenarios evolve faster than the doc.
- Runbook fatigue if drilled too rarely or too often.

## What this pattern constrains

Detected incidents must trigger a documented runbook step; ad-hoc response without runbook is a process failure to be flagged in post-mortem.

## Known uses

- **Standard SRE practice transferred to agent platforms** — *Available*
- **Frontier-lab safety teams** — *Available*

## Related patterns

- *complements* → [kill-switch](kill-switch.md)
- *complements* → [sandbox-escape-monitoring](sandbox-escape-monitoring.md)
- *uses* → [provenance-ledger](provenance-ledger.md)
- *uses* → [compensating-action](compensating-action.md)

## References

- (book) *Site Reliability Engineering (Google, ch. 14 Managing Incidents)*, 2016
- (book) *Site Reliability Engineering (Google) — Managing Incidents*, 2016, <https://sre.google/sre-book/managing-incidents/>

**Tags:** governance, incident-response, safety
