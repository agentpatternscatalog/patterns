# Role Assignment

**Also known as:** Persona Roles, Agent Crew, Specialist Roles

**Category:** Multi-Agent  
**Status in practice:** mature

## Intent

Assign each agent a named role (researcher, writer, critic, planner) with a role-specific prompt, tool palette, and acceptance criteria.

## Context

A team is running several agents that contribute to a shared workflow — a content pipeline with a researcher, a writer, and a critic; a coding crew with a planner, a coder, and a reviewer — and the user, the reviewer, and the team itself need to know who produced what. Each role has its own work to do and its own definition of done.

## Problem

When the agents share a generic prompt and an open tool palette, they drift toward sameness: the researcher starts writing prose, the writer starts critiquing, the critic starts proposing rewrites, and the outputs all sound alike. Contributions blur together in the transcript, review cannot focus on the right thing, and disagreement between roles — which is the signal the team wanted — never surfaces because every agent agrees with every other agent. Without explicit roles backed by scoped prompts, tools, and acceptance criteria, the multi-agent setup gives no benefit over a single agent.

## Forces

- Role definitions can ossify into bureaucracy.
- Cross-role handoffs need typed contracts.
- Role count multiplies prompt-engineering effort.


## Applicability

**Use when**

- Multiple agents collaborate and the user needs to reason about who did what.
- Different parts of the workflow have distinct responsibilities, tools, and acceptance criteria.
- Generic agents have been observed drifting toward similarity or duplicating effort.

**Do not use when**

- A single agent with one prompt already handles the workflow well.
- Roles would be artificial and add prompt overhead without separating concerns.
- The team cannot articulate distinct responsibilities and acceptance criteria per role.

## Therefore

Therefore: give each agent a named role with a scoped prompt, a scoped tool palette, and explicit acceptance criteria for its outputs, so that contributions are attributable and review focuses on the role boundary.

## Solution

Define each role with a system prompt naming its responsibility and constraints, a tool palette scoped to its role, and acceptance criteria for outputs it produces. Workflow assigns tasks to roles. Outputs are evaluated against the role's acceptance criteria.

## Example scenario

A multi-agent content pipeline with three identical generic agents keeps producing similar bland outputs and reviewers cannot tell whose work to trust. The team gives each agent a named role with role-specific prompt and a scoped tool palette: researcher (search-only), writer (draft tools), critic (lint and policy tools). Outputs become identifiable, review focuses on the role boundary, and disagreement between writer and critic surfaces as a productive signal rather than confusion.

## Diagram

```mermaid
classDiagram
  class Role {
    +name
    +system_prompt
    +tool_palette
    +acceptance_criteria
  }
  class Researcher
  class Writer
  class Critic
  class Planner
  Role <|-- Researcher
  Role <|-- Writer
  Role <|-- Critic
  Role <|-- Planner
```

## Consequences

**Benefits**

- Outputs are attributable and reviewable per role.
- Specialisation improves quality on each role's task.

**Liabilities**

- Bureaucratic overhead.
- Role drift over long sessions.

## What this pattern constrains

An agent operates only within its role's constraints and tool palette; cross-role action is forbidden.

## Known uses

- **CrewAI** — *Available*
- **AutoGen named agents** — *Available*

## Related patterns

- *complements* → [supervisor](supervisor.md)
- *alternative-to* → [inner-committee](inner-committee.md)
- *complements* → [handoff](handoff.md)
- *complements* → [mixture-of-experts-routing](mixture-of-experts-routing.md)
- *complements* → [autogen-conversational](autogen-conversational.md)
- *generalises* → [camel-role-playing](camel-role-playing.md)
- *used-by* → [sop-encoded-multi-agent](sop-encoded-multi-agent.md)
- *specialises* → [dynamic-expert-recruitment](dynamic-expert-recruitment.md)
- *used-by* → [cross-domain-agent-network](cross-domain-agent-network.md)

## References

- (doc) *CrewAI docs*, <https://docs.crewai.com>
- (paper) Yue Liu, Sin Kit Lo, Qinghua Lu, Liming Zhu, Dehai Zhao, Xiwei Xu, Stefan Harrer, Jon Whittle, *Agent design pattern catalogue: A collection of architectural patterns for foundation model based agents* (2025) — https://doi.org/10.1016/j.jss.2024.112278

**Tags:** multi-agent, roles, crew
