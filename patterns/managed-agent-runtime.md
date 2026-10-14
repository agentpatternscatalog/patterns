# Managed Agent Runtime

**Also known as:** Agent Loop as a Service, Managed Agent Loop, Serverless Agent Runtime, Agent Harness Engineering, Harness Engineering

**Category:** Governance & Observability  
**Status in practice:** emerging

## Intent

Offer the agent loop itself as a managed cloud primitive so a caller supplies a model, system prompt, and tools and the platform runs the orchestration in an isolated, session-scoped runtime.

## Context

An organisation is shipping several agent products and every team has hand-rolled the same orchestration loop: the reason-act cycle, tool dispatch, session state, per-session isolation, identity for outbound calls, retries, and observability. Each loop is operated separately, drifts in behaviour, and carries its own on-call burden, while the cloud now exposes the loop as a service alongside memory, identity, and tracing.

## Problem

Re-implementing and operating the agent loop per team multiplies effort and risk. Each bespoke loop must solve session isolation, credential handling, resumability, and tracing on its own, and any one of them done weakly becomes a production incident. Sessions that share a process leak state into one another; outbound tool calls reach for ambient host credentials; a crash loses in-flight work because there was no checkpoint; and there is no uniform trace to debug across products. The loop is undifferentiated infrastructure that every team rebuilds and operates instead of consuming.

## Forces

- A bespoke loop gives full control over orchestration but multiplies operational surface across teams.
- Session-scoped isolation needs a sandbox per session, which adds cold-start latency.
- A managed runtime standardises identity, memory, and tracing but ties the deployment to a vendor contract.
- Built-in observability is uniform across products but constrained to what the platform emits.

## Therefore

Therefore: invoke the loop through a managed runtime that accepts model, system prompt, and tools per call and executes the orchestration in a session-scoped isolated sandbox with built-in memory, identity, and tracing, rather than operating a hand-rolled loop per team.

## Solution

The platform exposes a single invoke endpoint that takes a model reference, a system prompt, and a tool set, then runs the full reason-act loop on the caller's behalf. Each session executes inside its own isolated sandbox, commonly a microVM with filesystem and shell access, so concurrent sessions never share state. The runtime wires in managed memory for short- and long-term context, a managed identity service that mints scoped credentials for outbound tool calls, and observability that emits a uniform trace of every step. The caller owns prompt, tools, and policy; the platform owns the loop, isolation, and operations.

## Structure

```
Caller (model ref + system prompt + tools) --> Invoke API --> Session-scoped sandbox (microVM: fs + shell) --> Managed reason-act loop <--> Built-in memory + Managed identity (scoped credentials for tool calls) + Observability (uniform per-step trace) --> Result to caller
```

## Diagram

```mermaid
flowchart TD
  Caller[Caller: model + system prompt + tools] --> Invoke[Managed runtime: single invoke API]
  Invoke --> Session[Session-scoped sandbox<br/>microVM: fs + shell]
  Session --> Loop[Managed reason-act loop]
  Loop --> Mem[Built-in memory]
  Loop --> Id[Managed identity:<br/>scoped credentials]
  Loop --> Obs[Observability: uniform trace]
  Loop --> Result[Result to caller]
```

## Example scenario

A company runs a coding agent, a research agent, and a support agent, each on a separately operated loop, and a state leak between two concurrent support sessions causes one user to see another's data. The teams move to a managed agent runtime: each defines its model, system prompt, and tools and invokes a single API, and the platform runs every session in its own microVM with built-in identity and tracing. The cross-session leak becomes structurally impossible and the three teams stop carrying three on-call rotations for the same loop.

## Consequences

**Benefits**

- Teams stop rebuilding and operating the same loop; orchestration becomes a consumed primitive.
- Session-scoped sandboxing makes cross-session state leaks structurally hard.
- Identity, memory, and tracing are uniform across every agent product on the platform.

**Liabilities**

- The agent loop and its operational behaviour are tied to a vendor contract and pricing model.
- Per-session sandbox provisioning adds cold-start latency that a long-lived in-process loop avoids.
- Custom orchestration that the managed loop does not expose is hard or impossible to inject.

## Failure modes

- Cold-start latency — each new session waits for its sandbox to provision, and short interactive tasks feel slow compared with an in-process loop.
- Missing hook — a product needs custom orchestration the managed loop does not expose, and the team builds a workaround around the runtime that loses its isolation and trace.
- Vendor lock on the loop — pricing or behaviour of the managed loop changes, and every agent product on the platform is affected at once with no local fallback.
- Over-broad scoped credential — the identity service mints a credential with wider scope than the tool needs, so a misused tool call reaches more than intended.

## What this pattern constrains

Callers cannot run the orchestration loop in their own process; the loop runs only inside the platform's session-scoped sandbox, and each session is isolated rather than sharing a runtime.

## Applicability

**Use when**

- Several teams are each rebuilding and operating the same agent loop.
- Per-session isolation, identity, and tracing must be uniform across agent products.
- A cloud runtime that exposes the loop with session-scoped sandboxes is available.

**Do not use when**

- A single agent needs deep custom orchestration the managed loop cannot express.
- Vendor lock-in or per-session latency budgets rule out a hosted runtime.
- The workload is so simple that one in-process loop is cheaper to run than to outsource.

## Components

- Invoke API — single endpoint that accepts a model reference, system prompt, and tool set per call
- Managed Loop Engine — runs the reason-act cycle, tool dispatch, retries, and response generation on the caller's behalf
- Session Sandbox — per-session isolated runtime (commonly a microVM with filesystem and shell) so sessions never share state
- Managed Identity Service — mints scoped credentials for outbound tool calls instead of using ambient host secrets
- Built-in Memory Store — short-term per-session context and long-term memory that persists across sessions
- Observability Layer — emits a uniform per-step trace of every session for debugging and audit

## Tools

- Amazon Bedrock AgentCore (Harness + Runtime) — managed agent loop with microVM session isolation, identity, and observability
- Cloudflare Agents — serverless durable runtime for hosting agents on edge infrastructure
- Modal — serverless platform that provisions isolated sandboxes per workload with fast cold starts
- Firecracker microVM — isolation boundary used to give each session its own filesystem and shell
- OpenTelemetry — standardised telemetry format the runtime emits for cross-product tracing

## Evaluation metrics

- Per-session cold-start latency — time to provision the isolated sandbox before the loop runs
- Cross-session isolation incidents — confirmed state or credential leaks between concurrent sessions per million sessions
- Loop operational toil — on-call hours spent operating bespoke loops before versus after adoption
- Trace coverage — share of session steps captured in the uniform observability trace
- Resumability rate — fraction of interrupted sessions that resume from checkpoint without lost work

## Known uses

- **[Amazon Bedrock AgentCore (Harness + Runtime)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)** _available_ — Harness is a managed agent loop invoked with a single API call passing model, system prompt, and tools inline; each session runs in an isolated microVM with filesystem and shell access, with Runtime providing session isolation, built-in identity, and observability.
- **[Cloudflare Agents](https://developers.cloudflare.com/agents/)** _available_ — Serverless durable agent runtime that hosts the agent on Cloudflare infrastructure and connects chat, voice, email, and webhooks to it.
- **[Modal Sandboxes](https://modal.com/docs/guide)** _available_ — Serverless platform that spins up isolated, secure sandboxes per workload to execute agent-generated code with sub-second cold starts.

## Related patterns

- _uses_ **ReAct**
- _uses_ **Sandbox Isolation**
- _complements_ **Session Isolation**
- _complements_ **Agent Resumption**
- _uses_ **Channel-Decoupled Agent Core** — A managed runtime that fronts chat, voice, email, and webhooks is a hosted realization of this decoupling; the runtime uses channel adapters over a shared agent core.
- _complements_ **Harness-Native Rollout Capture** — That pattern makes the agent loop a managed platform primitive; this one says nothing about who operates the loop and only requires that whatever loop is already running expose a model-call boundary to tap.

## References

- [What is Amazon Bedrock AgentCore?](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Cloudflare Agents](https://developers.cloudflare.com/agents/)
- [Modal Guide](https://modal.com/docs/guide)
