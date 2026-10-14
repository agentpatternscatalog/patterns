# CAMEL Role-Playing

**Also known as:** Inception Prompting, AI-User AI-Assistant

**Category:** Multi-Agent  
**Status in practice:** experimental

## Intent

Have two agents role-play a user-assistant interaction to autonomously complete a task neither could solve alone.

## Context

A team wants an autonomous system to carry out a task that, if done by humans, would unfold as a collaboration between someone stating goals and someone executing — a product owner working with a developer, an instructor working with a learner. There is no real user in the loop; both sides need to be played by agents, and the work has to converge through their interaction.

## Problem

A single-agent loop has no opposite voice to clarify or push back, and tends to mix goal-setting and execution in the same prompt until both blur. An adversarial debate setup is the wrong shape when what is actually wanted is collaborative role-play, not winning an argument. Without fixed roles and a bounded conversation, two free-form agents drift toward sameness, repeat themselves, and never converge on a working artefact.

## Forces

- Roles drift toward sameness without inception prompting.
- Conversation length must be bounded.
- Tasks need to be specified as something the role-play can converge on.

## Therefore

Therefore: instantiate two role-fixed agents — AI-User and AI-Assistant — with inception prompts and let them converse against a bounded budget, so that turn-taking collaboration runs to a task neither could solve alone.

## Solution

Use inception prompts to instantiate two agents (AI-User and AI-Assistant) with their roles fixed and the task specified. They converse until the task is completed or budget exhausted. The output is the final assistant message; the conversation log is debugging artefact.

## Structure

```
Task + inception prompts --> user-agent (fixed role: instructs) --instruction--> assistant-agent (fixed role: acts) --output--> user-agent --> [loop until task complete or budget] --> final assistant message (log kept for debugging)
```

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

## Example scenario

A research team wants an agent to design and prototype a small data-pipeline tool, but a single agent loop keeps drifting between requirements and implementation. They cast it as a CAMEL role-play: a 'product owner' agent and a 'developer' agent autonomously play out a user-assistant dialogue, with the product owner stating goals and constraints and the developer iterating. Neither alone could keep the conversation grounded; the role pairing produces working scaffolding without a human in the loop.

## Consequences

**Benefits**

- Synthetic task-solving without human-in-the-loop.
- Useful for generating training data.

**Liabilities**

- Cost: 2x inference per task.
- Role drift over long conversations.

## Failure modes

- Role drift — over a long chat the user-agent starts answering its own instructions, and the two agents collapse into one voice.
- Echo loop — the assistant repeats the same output and the user-agent repeats the same instruction until the budget runs out.
- Premature finish — the user-agent declares the task done after a plausible but incomplete answer, and no outside check catches it.
- Doubled cost for easy tasks — a task one agent could finish alone still pays for two models per turn.

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

## Components

- AI-User agent — role-locked to issuing instructions, never answering
- AI-Assistant agent — role-locked to executing and returning artefacts
- Inception prompts — fixed system prompts that pin both roles and the task description
- Conversation budget — hard cap on turns to prevent runaway role-play loops

## Tools

- LLM API — two invocations per round, one per role
- CAMEL framework — provides role templates and the inception-prompting harness
- Trajectory logger — captures the dialogue for downstream training data extraction

## Evaluation metrics

- Task-completion rate inside budget — share of role-plays that finish before turn cap
- Role-drift incidents — turns where AI-User answers or AI-Assistant asks user-style questions
- Convergence speed — turns to a satisfying final assistant message
- Training-data yield — usable trajectories per session for downstream fine-tuning
- Per-task token cost — total spend at two LLM calls per turn

## Known uses

- **[CAMEL framework](https://www.camel-ai.org/)** _available_

## Related patterns

- _alternative-to_ **Conversational Multi-Agent**
- _specialises_ **Role Assignment**
- _alternative-to_ **Agent Persona Profile**
- _complements_ **Simulated-User Rollout Evaluation** — Same two-model conversational structure aimed at completing a task rather than measuring one: the AI-User there cooperates toward an artefact, while the simulated user here withholds information and its counterpart is the subject of the score.

## References

- [CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society](https://arxiv.org/abs/2303.17760) — Li, Hammoud, Itani, Khizbullin, Ghanem, 2023
