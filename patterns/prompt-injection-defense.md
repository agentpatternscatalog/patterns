# Prompt Injection Defense

**Also known as:** Instruction Hierarchy, Untrusted-Content Tagging

**Category:** Safety & Control  
**Status in practice:** emerging

## Intent

Tag user-supplied or tool-supplied content as untrusted and refuse to follow instructions found inside it.

## Context

Any agent that processes external content (documents, web pages, user uploads) where attackers can plant instructions intended to hijack the agent.

## Problem

LLMs cannot reliably distinguish their own instructions from instructions embedded in retrieved or user-supplied content.

## Forces

- Attackers control any document, page, email, or tool response that reaches the model; defense is probabilistic, not preventive.
- Egress channels (tool calls, image URLs, links) need their own controls; demoting tool output is necessary but not sufficient.
- Multi-turn payloads can hide instructions across messages, beyond per-turn tagging.

## Solution

Establish an instruction hierarchy: system prompts trusted, user prompts partially trusted, tool/document content untrusted. Wrap untrusted content in markers. Train or prompt the model to refuse instructions inside untrusted markers. Add output guardrails for known exfiltration patterns.

## Consequences

**Benefits**

- Reduces successful injections; not zero.
- Inspectable: which content was treated as untrusted.

**Liabilities**

- Adversarial inputs evolve.
- False positives on instruction-shaped legitimate content.
- Long context expands the injection surface; multi-turn injection bypasses single-turn tagging.

## What this pattern constrains

The agent must not follow instructions appearing inside untrusted-content markers; their effect is read-only context only.

## Known uses

- **OpenAI instruction hierarchy** — *Available*
- **Anthropic XML-tagged untrusted content guidance** — *Available*
- **Lakera Guard** — *Available*
- **NVIDIA NeMo Guardrails** — *Available*

## Related patterns

- *composes-with* → [input-output-guardrails](input-output-guardrails.md)
- *complements* → [session-isolation](session-isolation.md)
- *generalises* → [tool-output-poisoning](tool-output-poisoning.md)

## References

- (paper) Wallace, Xiao, Leike, Weng, Heidecke, Beutel, *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*, 2024, <https://arxiv.org/abs/2404.13208>

**Tags:** safety, injection, security
