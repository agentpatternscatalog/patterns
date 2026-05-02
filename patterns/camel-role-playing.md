# CAMEL Role-Playing

**Also known as:** Inception Prompting, AI-User AI-Assistant

**Category:** Multi-Agent  
**Status in practice:** experimental

## Intent

Have two agents role-play a user-assistant interaction to autonomously complete a task neither could solve alone.

## Context

Tasks where a user-style agent and an assistant-style agent productively elaborate a task through their interaction.

## Problem

Single agents miss the turn-taking dynamics that human collaboration relies on; pure debate is adversarial when collaboration is what is wanted.

## Forces

- Roles drift toward sameness without inception prompting.
- Conversation length must be bounded.
- Tasks need to be specified as something the role-play can converge on.

## Solution

Use inception prompts to instantiate two agents (AI-User and AI-Assistant) with their roles fixed and the task specified. They converse until the task is completed or budget exhausted. The output is the final assistant message; the conversation log is debugging artefact.

## Example scenario

A research team wants an agent to design and prototype a small data-pipeline tool, but a single agent loop keeps drifting between requirements and implementation. They cast it as a CAMEL role-play: a 'product owner' agent and a 'developer' agent autonomously play out a user-assistant dialogue, with the product owner stating goals and constraints and the developer iterating. Neither alone could keep the conversation grounded; the role pairing produces working scaffolding without a human in the loop.

## Diagram

```mermaid
sequenceDiagram
  participant Sys as Inception Prompts
  participant U as AI-User
  participant A as AI-Assistant
  Sys->>U: role: user, task fixed
  Sys->>A: role: assistant, task fixed
  loop until task complete or budget
    U->>A: instruction
    A-->>U: action / output
  end
  A-->>Sys: trajectory
```

## Consequences

**Benefits**

- Synthetic task-solving without human-in-the-loop.
- Useful for generating training data.

**Liabilities**

- Cost: 2x inference per task.
- Role drift over long conversations.

## What this pattern constrains

The AI-User role may only ask, never answer; AI-Assistant may only answer, never ask user-style questions.

## Applicability

**Use when**

- The task benefits from explicit user-assistant turn-taking that a single agent loop misses.
- Inception prompts can fix the two roles and the task tightly enough to keep the conversation on-track.
- A budget caps the conversation length so unproductive loops terminate.

**Do not use when**

- A single agent already solves the task without turn-taking dynamics.
- Adversarial debate (not collaborative role-play) is what the task actually wants.
- Roles cannot be specified tightly enough and the conversation drifts off-task.

## Known uses

- **CAMEL framework** — *Available*

## Related patterns

- *alternative-to* → [autogen-conversational](autogen-conversational.md)
- *specialises* → [role-assignment](role-assignment.md)

## References

- (paper) Li, Hammoud, Itani, Khizbullin, Ghanem, *CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society*, 2023, <https://arxiv.org/abs/2303.17760>

**Tags:** multi-agent, role-play
