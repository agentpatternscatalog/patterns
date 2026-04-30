# Computer Use

**Also known as:** Desktop Agent, GUI Agent, Screen Control

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Let the model drive a desktop end-to-end via screenshots plus virtual mouse/keyboard tool calls instead of bespoke per-app APIs.

## Context

Tasks that span multiple applications, legacy GUIs, or interfaces with no clean machine API; the agent must operate the same surfaces a human does.

## Problem

Most software has no clean API; agents need to operate GUIs visually, including ones the agent's vendor never integrated with.

## Forces

- Latency and reliability are open problems.
- Prompt injection via on-screen content is a real attack surface.
- Cost: every step pays vision tokens.

## Solution

The model receives screenshots (optionally augmented with accessibility-tree or set-of-mark annotations) and emits typed tool calls (move mouse, click, type, scroll, screenshot). A controller executes them against a real or virtual desktop. The loop is ReAct-shaped: screenshot → think → act → screenshot.

## Consequences

**Benefits**

- Universal coverage of GUI software.
- No per-app integration work.

**Liabilities**

- Slow and brittle on dynamic UIs.
- Screen content is now part of the prompt; injection becomes possible.

## What this pattern constrains

The agent operates the desktop only through the typed action vocabulary; arbitrary code execution is not part of this surface.

## Known uses

- **[Anthropic Computer Use (Claude 3.5+)](https://www.anthropic.com/news/3-5-models-and-computer-use)** — *Available*
- **OpenAI Operator** — *Available*

## Related patterns

- *alternative-to* → [browser-agent](browser-agent.md)
- *uses* → [react](react.md)
- *complements* → [input-output-guardrails](input-output-guardrails.md)
- *alternative-to* → [mobile-ui-agent](mobile-ui-agent.md)
- *generalises* → [dual-system-gui-agent](dual-system-gui-agent.md)
- *alternative-to* → [multilingual-voice-agent](multilingual-voice-agent.md)

## References

- (blog) Anthropic, *Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku*, 2024, <https://www.anthropic.com/news/3-5-models-and-computer-use>

**Tags:** environment, gui, vision
