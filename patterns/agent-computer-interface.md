# Agent-Computer Interface

**Also known as:** ACI, Agent-Friendly Tooling, SWE-Agent ACI

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Design the tool surface for an LLM agent specifically, with affordances different from human-facing CLIs.

## Context

Production coding agents and other domain agents that operate over file systems or APIs originally designed for humans.

## Problem

Tools designed for humans (full-buffer editors, full-page web views, generic shells) overwhelm agent context and provide poor signals; agents perform better against curated agent-friendly surfaces.

## Forces

- Agent-friendly tools require parallel implementations alongside human ones.
- Tool surface must balance agent ergonomics with capability completeness.
- Linter / type signal exposure helps but adds output volume.

## Solution

Design tools specifically for agents: file viewer that shows a windowed slice with line numbers, edit tool that re-runs linter and shows results, shell that returns structured stdout/stderr/exit-code, search tool that filters and ranks. Each tool's signature + return type optimised for the agent's context budget and reasoning shape.

## Consequences

**Benefits**

- Substantial accuracy gains over human-CLI tools at the same task.
- Inspectable design choices per tool.

**Liabilities**

- Two interface surfaces to maintain (agent + human).
- ACI design is empirical; iterations needed.

## What this pattern constrains

Agent tools follow a deliberate ACI design contract; raw human-CLI tools are not exposed as primary tools.

## Known uses

- **[SWE-Agent (Princeton)](https://github.com/princeton-nlp/SWE-agent)** — *Available*
- **Claude Code's curated tool set** — *Available*
- **Cursor's contextual file edit tools** — *Available*

## Related patterns

- *specialises* → [tool-use](tool-use.md)
- *complements* → [tool-loadout](tool-loadout.md)

## References

- (paper) Yang, Jimenez, Wettig, Lieret, Yao, Narasimhan, Press, *SWE-Agent: Agent-Computer Interfaces Enable Automated Software Engineering*, 2024, <https://arxiv.org/abs/2405.15793>

**Tags:** tool-use, aci, design
