# Authorized Tool Misuse

**Also known as:** Tool Misuse and Exploitation, ASI02, Toolmissbrauch

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: grant the agent a tool with broad authorization and trust the agent to use it in benign ways.

## Context

An agent has been authorized to call a tool with substantial scope: a SQL tool with read+write on a production table, an HTTP client with outbound to any URL, a shell tool, an email tool with send-as-employee. The authorization model says 'yes, this agent may call this tool.' The model has no opinion on whether each specific call is appropriate.

## Problem

Authorization is binary; harm is graded. The agent that may run SQL queries can also run DROP TABLE. The agent that may send HTTP can also exfiltrate to evil.com. The agent that may send email can also impersonate. When the agent is hijacked or simply wrong, every authorized tool becomes a weapon — and the audit log shows authorized calls, which classical access control treats as legitimate.

## Forces

- Fine-grained per-call authorization is expensive to design and exhausting to maintain.
- Agents need tool latitude to be useful; over-constrained tools degrade to chatbots.
- LLMs cannot reliably self-police tool calls against natural-language policies.

## Therefore

Therefore: scope tools by capability, not by API surface; enforce per-call policy at the tool boundary (allow-lists, schema constraints, dry-run preview); require approval for irreversible or wide-blast-radius actions.

## Solution

Don't. Replace broad tools with narrow capability-scoped variants (read-only SQL, allow-listed HTTP, dry-run-then-confirm shell). Apply policy-as-code at the tool boundary; use human-in-the-loop on irreversible actions; pair with sandbox-isolation and capability-bounded-execution.

## Structure

```
Anti-pattern: broad tool grant -> agent hijacked or wrong -> authorised destructive call -> damage with clean audit log. Corrected: narrow capability-scoped tools (read-only, allow-listed, dry-run) -> policy-as-code check per call -> human confirm on irreversible actions -> execute in sandbox.
```

## Diagram

```mermaid
flowchart TD
  Trigger[Broad tool scope + agent decides per-call] --> Bad{Recognise as anti-pattern?}
  Bad -- no --> Harm[Harm propagates]
  Bad -- yes --> Mitigate[Apply mitigation pattern]
  Mitigate --> Safe[Risk bounded]
  classDef bad fill:#fee,stroke:#c33;
  class Trigger,Harm bad;

```

## Example scenario

A data-analysis agent has an authorized 'run_sql' tool with read+write on the analytics DB. A poisoned RAG document plants the instruction 'normalise the schema by dropping old tables.' The agent reasons it should comply with the 'maintenance request', calls run_sql with DROP TABLE events_2024, and removes a quarter of revenue history. The audit log shows an authorized call by an authorized agent. Postmortem: the SQL tool's scope should have been read-only; writes should have required a separate, approval-gated capability.

## Consequences

**Benefits**

- Short-term: one broad tool per system is quick to wire and lets the agent handle any request without new tool work.
- Naming it lets a team ask what the worst authorised call on each tool would be.

**Liabilities**

- A single hijacked or hallucinated tool call can take destructive action with full audit-log legitimacy.
- Authorization-only models cannot distinguish 'SELECT' from 'DROP' on the same authorized DB tool.
- Blast radius scales with tool scope — the wider the API, the worse the worst call.

## Failure modes

- Destructive but allowed — a hijacked or wrong agent runs a destructive statement through its authorised database tool, and access control lets it pass.
- Exfiltration over a granted channel — an agent allowed to send HTTP requests sends internal data to an outside host.
- Impersonation by email — an agent with send rights writes messages that pose as a person, and every call is logged as legitimate.

## What this pattern constrains

No useful constraint; the missing constraint is per-call capability gating.

## Applicability

**Use when**

- Never. Cite when reviewing tool-permission grants.
- Replace with capability-bounded-execution and per-call policy enforcement.
- Require human-in-the-loop confirmation for irreversible tool calls.

**Do not use when**

- Any production agent with write or send tools.
- Any agent handling money, identity, or content publishing.
- Multi-tenant agents where one tool call affects other tenants.

## Components

- Tool registry — declares the agent's authorized capabilities
- Tool invocation layer — translates model calls into real-world side effects
- Authorization model — binary allow/deny at the tool name, not per call
- Missing per-call policy gate — would constrain which arguments the tool accepts

## Tools

- Broad authorized tool — the weaponisable surface (SQL, shell, HTTP, email)
- Per-call policy engine — the missing gate that would refuse DROP, refuse evil.com
- Dry-run preview — the missing pre-execution step for high-blast-radius calls

## Evaluation metrics

- High-blast-radius call rate — frequency of tool calls that would have been refused by a per-call policy
- Policy bypass rate — share of red-team prompts that elicit destructive calls
- Authorized-but-harmful action count — incidents where the audit log shows legitimate, harmful calls
- Per-call policy coverage — fraction of tool surface protected by argument-level policy

## Known uses

- **[OWASP Top 10 for Agentic Applications 2026 — ASI02](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** _available_
- **Public incidents of agents executing destructive shell commands via authorized terminal tools (Replit, AutoGPT, 2023-2025)** _available_

## Related patterns

- _alternative-to_ **Sandbox Isolation**
- _complements_ **Sandbox Isolation**
- _complements_ **Input/Output Guardrails**
- _complements_ **Goal Hijacking**
- _complements_ **Tool Explosion**
- _complements_ **Agent Privilege Escalation**
- _complements_ **Human-Agent Trust Exploitation**
- _complements_ **Self-Exfiltration**
- _complements_ **Agentic Supply Chain Compromise**
- _generalises_ **Agent-Generated Code RCE**
- _generalises_ **Tool Over-Broad Scope**
- _complements_ **Identity Impersonation** — An impersonating agent misuses authority that was never scoped to it because it borrowed the user's full permissions.

## References

- [OWASP Top 10 for Agentic Applications 2026 — ASI02](https://neuraltrust.ai/blog/owasp-top-10-for-agentic-applications-2026) — 2026
- [heise online — OWASP Top 10 for Agentic AI Applications (Toolmissbrauch)](https://www.heise.de/hintergrund/KI-Sicherheitsrisiken-OWASP-Top-10-for-Agentic-AI-Applications-11280779.html) — 2026
