# Disambiguation

**Also known as:** Clarifying Questions, Confirmation Loop, Ask About Ambiguity

**Category:** Planning & Control Flow  
**Status in practice:** mature

## Intent

Have the agent ask a clarifying question before acting on an ambiguous request.

## Context

User requests are often underspecified; acting on the wrong interpretation costs more than asking.

## Problem

Agents that always act produce confidently wrong results on ambiguous inputs.

## Forces

- Asking too often is annoying.
- Asking too rarely produces wrong work.
- The model must detect ambiguity, which is itself hard.

## Solution

Detect ambiguity via low-confidence intent classification or explicit ambiguity rubric. When detected, ask one focused question and wait for the answer before acting. Phrase the question with the most-likely interpretation as a default.

## Consequences

**Benefits**

- Quality improvement on ambiguous inputs.
- User feels in control.

**Liabilities**

- Latency penalty.
- Conversational drag if overused.

## What this pattern constrains

Below the confidence threshold the agent must ask; it is forbidden to guess.

## Applicability

**Use when**

- Ambiguous user requests would otherwise produce confidently wrong agent actions.
- Ambiguity can be detected (low-confidence intent, explicit rubric, multiple plausible parses).
- A focused clarifying question, with a default interpretation, is acceptable UX.

**Do not use when**

- The deployment is non-interactive and clarification questions cannot be asked.
- Asking for clarification is more disruptive than acting on the most-likely interpretation.
- Ambiguity detection is unreliable and most clarifications would be unnecessary.

## Known uses

- **Cursor / Claude Code clarifying questions** — *Available*
- **Production support chatbots** — *Available*
- **ChatGPT clarifying questions** — *Available*
- **Claude clarifying questions** — *Available*

## Related patterns

- *uses* → [routing](routing.md)
- *specialises* → [human-in-the-loop](human-in-the-loop.md)
- *complements* → [confidence-reporting](confidence-reporting.md)
- *generalises* → [communicative-dehallucination](communicative-dehallucination.md)

## References

- (paper) Aliannejadi, Zamani et al., *ClariQ: Asking Clarification Questions in Conversational Information Seeking*, 2020, <https://arxiv.org/abs/2009.11352>

**Tags:** ux, clarification
