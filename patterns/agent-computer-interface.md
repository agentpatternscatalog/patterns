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

## Example scenario

An engineering team wires their agent to the standard bash and a desktop-grade text editor. Every diff balloons into a 4000-line buffer, output gets truncated mid-stack-trace, and the agent burns turns scrolling. They replace the surface with an Agent-Computer Interface: a file_view tool that returns numbered windows with elision markers, an edit tool that takes line ranges, and a run tool that streams the last 200 lines plus exit code. Task success rates rise sharply on the same model.

## Consequences

**Benefits**

- Substantial accuracy gains over human-CLI tools at the same task.
- Inspectable design choices per tool.

**Liabilities**

- Two interface surfaces to maintain (agent + human).
- ACI design is empirical; iterations needed.

## What this pattern constrains

Agent tools follow a deliberate ACI design contract; raw human-CLI tools are not exposed as primary tools.

## Applicability

**Use when**

- Off-the-shelf human tools (shells, editors, web pages) overwhelm the agent's context with noise.
- You can curate a small, agent-specific tool surface (windowed file viewer, structured shell, ranked search).
- You measure agent performance and want the tool layer to be a tunable variable.

**Do not use when**

- The agent must use unmodified human tools verbatim (e.g. legal or audit constraint).
- Tool surface changes faster than you can re-curate agent-friendly wrappers.
- The agent runs against one-off APIs where building a curated surface is not worth the effort.

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
