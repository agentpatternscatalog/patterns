# Hallucinated Tools

**Also known as:** Phantom Tool Calls, Imagined Functions

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: trust the model to invoke only the tools it has been given, then debug calls to functions that do not exist.

## Context

The agent is given a tool palette, but the host accepts whatever the model emits without validation.

## Problem

The model invents tool names. The host either crashes, silently drops the call, or worse, dispatches to a similar-named real tool.

## Forces

- Validation feels redundant when providers offer typed tool calls.
- Provider-side validation is not always strict.
- Logging fails to surface 'tool does not exist' as a first-class event.

## Solution

Don't trust. Validate every tool call against the registered palette before dispatch. Reject unknown names with a typed error the agent can react to. See tool-use, structured-output.

## Consequences

**Liabilities**

- Silent failures.
- Wrong actions executed by similar-named tools.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Common in pre-2024 agent integrations** — *Available*

## Related patterns

- *alternative-to* → [tool-use](tool-use.md)
- *alternative-to* → [structured-output](structured-output.md)

**Tags:** anti-pattern, tool-use
