# Sandbox Escape Monitoring

**Also known as:** Sandbox Telemetry, Boundary Violation Alerts

**Category:** Governance & Observability  
**Status in practice:** emerging

## Intent

Treat sandbox boundary violations as telemetry; alert on syscalls, network egress, or filesystem writes outside expected scope.

## Context

A team runs an agent that executes generated code or manipulates files on behalf of users, inside an isolation boundary such as a container, microVM, or syscall-filtered sandbox. The boundary is designed to confine what the agent can read, write, and reach over the network. Real-world sandboxes have known escape vectors and zero-day vulnerabilities; isolation is necessary but not by itself sufficient.

## Problem

Treating the sandbox as a pure prevention mechanism means a successful escape, or even repeated escape attempts, can happen without anyone seeing them. A blocked network egress, an unexpected syscall, or a write outside the working directory will silently fail or succeed without any alert. The team is forced to choose between assuming the sandbox is impenetrable, which it is not, or learning about boundary violations from the downstream damage they cause.

## Forces

- Telemetry granularity vs cost.
- False positives on legitimate boundary-pushing operations.
- Egress patterns evolve faster than allowlists.


## Applicability

**Use when**

- The agent executes code or operates a filesystem inside a sandbox.
- Sandbox boundaries can be instrumented to log syscalls, egress, and writes.
- A safety telemetry pipeline and kill-switch already exist or are being built.

**Do not use when**

- There is no sandbox to monitor (escape monitoring without isolation is theatre).
- Telemetry volume would overwhelm the safety pipeline without thresholds.
- Alerts have no responder and would be ignored.

## Therefore

Therefore: instrument the sandbox to log every syscall, egress, and filesystem write outside the allowed set, stream to safety telemetry, and tie threshold breaches to the kill-switch, so that boundary violations become alertable signal rather than silent compromise.

## Solution

Instrument the sandbox: log every syscall outside the allowed set, every network egress not on the allowlist, every filesystem write outside the working directory. Stream to safety telemetry. Alert on threshold breaches. Pair with kill-switch for automatic halt on confirmed escape.

## Example scenario

A code-execution agent runs user-emitted Python in a container that should have no network. One day a contractor's prompt-injected payload triggers an outbound DNS request; sandbox-isolation alone would have allowed the egress to fail silently. With escape monitoring, the unexpected syscall and the blocked egress both stream to safety telemetry, an alert fires within seconds, and the team locks the offending tenant before any further attempts.

## Diagram

```mermaid
flowchart TD
  S[Sandbox] -->|syscall outside allowset| Tel[Telemetry stream]
  S -->|net egress not on allowlist| Tel
  S -->|fs write outside workdir| Tel
  Tel --> Det[Threshold detector]
  Det -->|alert| Op[Operators]
  Det -->|confirmed escape| KS[Kill-switch]
```

## Consequences

**Benefits**

- Detection of escape attempts and successes.
- Forensic trail when incidents occur.

**Liabilities**

- Telemetry volume.
- Alert fatigue if thresholds are mis-tuned.

## What this pattern constrains

Sandbox events outside the allowed set must be logged and inspectable; silent boundary violations are forbidden.

## Known uses

- **Production code-execution platforms (E2B, Modal sandbox monitoring)** — *Available*

## Related patterns

- *complements* → [sandbox-isolation](sandbox-isolation.md)
- *composes-with* → [kill-switch](kill-switch.md)
- *uses* → [provenance-ledger](provenance-ledger.md)

**Tags:** safety, sandbox, monitoring
