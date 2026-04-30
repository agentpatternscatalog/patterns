# Tool Output Poisoning Defense

**Also known as:** Indirect Prompt Injection (Tools), Untrusted Tool Output

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Treat tool output as untrusted content and apply instruction-stripping plus per-tool trust labels.

## Context

Agents that consume tool output where the tool itself is untrusted (browser-agent, MCP server with unknown providers, search results, document parsers, third-party APIs).

## Problem

A compromised or hijacked tool can return content with embedded instructions that hijack the agent. Tool-output is the largest unstructured untrusted surface modern agents ingest.

## Forces

- Tool trust is heterogeneous: a typed DB query is high-trust, a web fetch is low-trust.
- Instruction-stripping has false positives on legitimate instruction-shaped content.
- Egress channels (tool calls, image URLs, links) are exfiltration vectors.

## Solution

Typed `ToolResult` envelope with `trust: low|medium|high` and content-type discriminator. Apply instruction-stripping on `low` results. Forbid tool-output-driven follow-up tool calls without re-validation against the user's original intent. Pair with input/output guardrails.

## Consequences

**Benefits**

- Reduces successful indirect injection from compromised tools.
- Trust labels are inspectable in traces.

**Liabilities**

- False positives strip legitimate instruction-shaped content.
- New injection vectors emerge faster than defenses.

## What this pattern constrains

Tool output is treated as untrusted by default; instructions inside tool responses do not have authority over the agent's behaviour.

## Known uses

- **Anthropic XML-tagged untrusted-content guidance** — *Available*
- **Lakera Guard tool-output filtering** — *Available*

## Related patterns

- *specialises* → [prompt-injection-defense](prompt-injection-defense.md)
- *composes-with* → [input-output-guardrails](input-output-guardrails.md)
- *complements* → [mcp](mcp.md)
- *complements* → [browser-agent](browser-agent.md)
- *alternative-to* → [tool-output-trusted-verbatim](tool-output-trusted-verbatim.md)

## References

- (paper) Greshake et al., *Not what you've signed up for: Compromising Real-World LLM-Integrated Apps with Indirect Prompt Injection*, 2023, <https://arxiv.org/abs/2302.12173>

**Tags:** safety, injection, tool-trust
