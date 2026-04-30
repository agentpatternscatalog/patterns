# Secrets Handling

**Also known as:** Tool-Side Credential Injection, Model-Never-Sees-Secrets

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Ensure the model never receives secrets in plaintext; tools resolve credentials from references at runtime.

## Context

Agents with tools that need authentication (API keys, OAuth tokens, DB credentials, service accounts).

## Problem

Any secret that reaches the model is now in the chat log, the trace store, the eval harness, and likely the third-party model provider. Leaks are then everywhere.

## Forces

- Tool authors prefer simple credential passing.
- Reference-based credential resolution adds tool runtime complexity.
- Some integrations require credentials in URL or header (cannot avoid).

## Solution

Tool runtime resolves credentials from typed references the agent emits (e.g., `{auth: 'github_token_for_user_42'}`). Credential values are injected outside the model context. Input/output guards reject any payload matching credential signatures. Provenance ledger and traces are scrubbed at write time.

## Consequences

**Benefits**

- Secrets never appear in agent context, logs, or traces.
- Compliance posture improves.

**Liabilities**

- Tool runtime complexity rises.
- Credential reference scheme must be maintained.

## What this pattern constrains

The model may emit credential references but never plaintext secrets; runtime injects values out-of-context.

## Known uses

- **Anthropic Claude with workspace credentials** — *Available*
- **MCP servers with server-side OAuth** — *Available*
- **Production agent gateways (Portkey, Helicone)** — *Available*

## Related patterns

- *complements* → [pii-redaction](pii-redaction.md)
- *composes-with* → [input-output-guardrails](input-output-guardrails.md)
- *complements* → [mcp](mcp.md)
- *complements* → [session-isolation](session-isolation.md)
- *complements* → [sovereign-inference-stack](sovereign-inference-stack.md)
- *complements* → [wasm-skill-runtime](wasm-skill-runtime.md)

## References

- (doc) *MCP authentication*, <https://modelcontextprotocol.io/specification>

**Tags:** safety, secrets, credentials
