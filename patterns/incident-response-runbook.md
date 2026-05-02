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

## Applicability

**Use when**

- An agent is in production where PII leaks, tool exploits, or mass false actions are possible.
- Detection signals exist but no coordinated response procedure does.
- Regulatory or customer obligations require documented containment and notification steps.

**Do not use when**

- The agent is purely experimental with no production blast radius.
- No alerting infrastructure exists yet to trigger runbook entries.
- Severity, on-call, and forensic responsibilities are not yet assignable to anyone.

## Solution

Maintain a runbook covering: severity levels, on-call paths, containment steps (kill-switch invocation, traffic rerouting), forensic preservation (pin traces beyond normal retention), compensating actions, customer communication templates, regulator notification procedures, and post-mortem template. Tie alerts from kill-switch/sandbox-escape-monitoring/cost-observability to runbook entries.

## Example scenario

A multi-tenant chat platform discovers at 02:14 that an agent has been emailing one customer's support transcripts to another customer's address for the past nine hours. The on-call has alerts but no plan, and the first hour goes to arguing about whether to kill the service. After the post-mortem the team writes an incident-response-runbook covering severity levels, kill-switch invocation, trace pinning beyond normal retention, customer-notification templates, and regulator timelines. The next incident is contained in eight minutes.

## Diagram

```mermaid
flowchart TD
  Alert[Alert: kill-switch / sandbox-escape / cost spike] --> Sev{Severity}
  Sev --> OnCall[Page on-call]
  OnCall --> Cont[Containment: kill-switch / reroute]
  Cont --> Pres[Pin traces beyond retention]
  Pres --> Comp[Compensating actions]
  Comp --> Comm[Customer + regulator comms]
  Comm --> PM[Post-mortem]
```

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
