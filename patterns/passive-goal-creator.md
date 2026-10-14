# Passive Goal Creator

**Also known as:** Dialogue Goal Extractor, Goal Refinement from Prompts

**Category:** Planning & Control Flow  
**Status in practice:** emerging

## Intent

Analyse the user's articulated prompts and accompanying context to derive a precise, actionable goal before any planning or tool use begins.

## Context

A team runs an agent behind a dialogue interface — a chatbot, a coding assistant, a personal-assistant surface — where users type short, conversational prompts. Those prompts are often under-specified relative to what the agent has to do: the user says "book me a flight Thursday" and leaves the destination, the time of day, and the preferences implicit. Other relevant context (recent conversation, stored preferences, prior tasks) lives in memory but does not arrive automatically with the prompt.

## Problem

If the planner reads the raw user prompt directly it inherits all of that under-specification. It then either guesses (producing confidently wrong work the user has to correct) or fails on a missing field. Pushing the clarification work into every downstream component spreads the same problem across many places. The team needs one early step that turns a thin dialogue prompt plus retrieved memory into a precise, structured goal that the planner can act on.

## Forces

- Underspecification: users rarely articulate complete context or precise constraints.
- Efficiency: users expect quick responses, so the goal-clarification step must be cheap.
- Reasoning uncertainty: ambiguous goal information propagates into the plan.

## Therefore

Therefore: before planning, route the user's prompt through a goal-creator component that inspects the prompt together with retrieved memory (recent tasks, conversation history, examples) and emits a refined, structured goal, so that downstream planning has a precise target.

## Solution

A dedicated component receives the user's prompt via the dialogue interface, retrieves related context from memory (recent tasks, conversation history, positive/negative examples), and produces a refined goal handed to the planner. In multi-agent setups, the same component can receive goals via API from a coordinator instead of directly from a user.

## Structure

```
User → Dialogue interface → Passive goal creator (uses Memory) → Goal → Planner / Prompt-response optimiser.
```

## Diagram

```mermaid
flowchart TD
  U[User] -->|prompt| D[Dialogue interface]
  D --> P[Passive goal creator]
  P <-->|retrieve context| M[Memory]
  P -->|refined goal| PL[Planner]

```

*Passive Goal Creator refines a dialogue prompt into a planner-ready goal.*

## Example scenario

A user types: "book me a flight Thursday". A passive goal creator pulls recent conversation (the user mentioned Tokyo last week), checks memory (the user prefers morning departures), and emits a refined goal: "book a morning flight from the user's home airport to Tokyo on the next Thursday". The planner now has something concrete to plan against, instead of the original eight-word prompt.

## Consequences

**Benefits**

- Interactivity: a familiar dialogue surface for users.
- Goal-seeking: downstream components plan against an explicit goal, not a raw prompt.
- Efficiency: pushes the lightweight clarification work to a single early component.

**Liabilities**

- Reasoning uncertainty when the prompt is too ambiguous to refine reliably.
- Becomes a single point of misinterpretation if the goal extraction is wrong.

## Failure modes

- Wrong goal, clean plan — the goal creator misreads the prompt, and the planner builds a correct plan for the wrong task.
- Forced refinement — the prompt is too ambiguous to refine, but the component still emits a precise-looking goal by filling gaps with guesses.
- Raw-prompt bypass — a downstream component reads the user's raw prompt instead of the refined goal, and the two disagree.
- Stale memory — retrieved past tasks or examples no longer match the current request, and they pull the goal toward an old intent.

## What this pattern constrains

Downstream planning components must consume the refined goal, not the raw user prompt.

## Applicability

**Use when**

- Users interact with the agent through free-form dialogue and prompts are often under-specified.
- Goal context lives in memory or recent history that the planner does not naturally see.
- A single early step can replace many downstream clarifications.

**Do not use when**

- Inputs are already structured (form fields, API calls) and need no refinement.
- Multimodal context capture is essential — use Proactive Goal Creator instead.

## Components

- Dialogue interface — receives the user's free-form prompt
- Memory retriever — pulls recent conversation, prior tasks, and stored preferences
- Goal creator — synthesises prompt plus retrieved context into a structured goal
- Refined goal artefact — schema-typed handoff to the planner

## Tools

- LLM API — drives the goal-synthesis step
- Memory store — recent conversation, task history, and user preferences
- Structured-output schema — defines the refined-goal contract for downstream planning

## Evaluation metrics

- Goal-precision lift over raw-prompt baseline — downstream planning success rate
- Missing-field rate in the refined goal — fields the synthesis could not fill
- Goal-misinterpretation rate — refined goals the user later corrects
- Latency cost of the refinement step — extra turn-time before planning begins
- Memory-retrieval hit rate — fraction of refinements that pulled relevant context

## Known uses

- **[HuggingGPT](https://huggingface.co/spaces/microsoft/HuggingGPT)** _available_ — Cited by Liu et al. (2025) §4.1 — user requests with complex intents are interpreted as the intended goal before task planning.

## Related patterns

- _alternative-to_ **Proactive Goal Creator**
- _complements_ **Disambiguation**
- _used-by_ **Prompt/Response Optimiser**
- _complements_ **Plan-and-Execute**
- _alternative-to_ **Socratic Questioning Agent**

## References

- [Agent design pattern catalogue: A collection of architectural patterns for foundation model based agents](https://doi.org/10.1016/j.jss.2024.112278) — Yue Liu, Sin Kit Lo, Qinghua Lu, Liming Zhu, Dehai Zhao, Xiwei Xu, Stefan Harrer, Jon Whittle, 2025
