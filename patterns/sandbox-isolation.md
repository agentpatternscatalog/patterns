# Sandbox Isolation

**Also known as:** Code Sandbox, Container Isolation, Restricted Execution

**Category:** Tool Use & Environment  
**Status in practice:** mature

## Intent

Run agent-emitted code or actions in a contained environment with restricted filesystem, network, and process privileges.

## Context

Agents that execute code or operate the filesystem; ungated execution is a security and stability hazard.

## Problem

An agent with full host access can damage the host (delete files, exfiltrate data, install malware) intentionally or accidentally.

## Forces

- Sandbox setup adds latency.
- Strict sandboxes block legitimate work.
- Escape vulnerabilities are real and ongoing.

## Solution

Run code in a container, microVM, WASM runtime, or restricted subprocess with minimal privileges. Filesystem is read-only or scoped to a working directory. Network is allowlisted or blocked. Resource limits cap CPU/memory/time. Persistent state is ephemeral by default.

## Consequences

**Benefits**

- Blast radius is contained.
- Same sandbox image is reproducible across runs.

**Liabilities**

- Some workflows need network or filesystem access the sandbox forbids.
- Sandbox tech (Docker, gVisor, Firecracker, WASM) is its own engineering.

## What this pattern constrains

Code may only access resources granted by the sandbox policy; outbound network and host filesystem are forbidden by default.

## Known uses

- **OpenAI Code Interpreter sandbox** — *Available*
- **E2B sandboxes** — *Available*
- **Claude Code's project-level write boundaries** — *Available*

## Related patterns

- *complements* → [code-execution](code-execution.md)
- *composes-with* → [input-output-guardrails](input-output-guardrails.md)
- *composes-with* → [subagent-isolation](subagent-isolation.md)
- *complements* → [sandbox-escape-monitoring](sandbox-escape-monitoring.md)
- *used-by* → [todo-list-driven-agent](todo-list-driven-agent.md)
- *generalises* → [wasm-skill-runtime](wasm-skill-runtime.md)
- *used-by* → [code-as-action](code-as-action.md)

## References

- (doc) *E2B Sandboxes*, <https://e2b.dev/docs>

**Tags:** sandbox, safety, execution
