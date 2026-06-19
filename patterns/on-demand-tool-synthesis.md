# On-Demand Tool Synthesis

**Also known as:** Tool Creation, LLMs as Tool Makers

**Category:** Tool Use & Environment  
**Status in practice:** experimental

## Intent

When no available tool fits a subtask, have the agent write, validate, and register a new tool on the spot, separating the tool-creating role from the tool-using role.

## Context

An agent faces an open-ended task space, but its toolset is fixed at deployment. Sooner or later a subtask needs a capability no available tool provides — parse an unusual format, call an API with no wrapper, or run a computation the tools cannot express. The agent either gives up, fakes the result, or contorts existing tools into something brittle.

## Problem

A fixed toolset cannot cover an open task space, yet shipping every conceivable tool is impossible and bloats tool selection. When the agent hits a capability gap mid-task it has no clean way forward: hallucinating a tool fails, and forcing the wrong tool produces wrong results. The agent needs a way to manufacture the missing capability as a proper, callable tool, and to do so without blindly trusting code it just wrote.

## Forces

- A fixed toolset cannot cover an open task space, but shipping every possible tool bloats discovery and selection.
- Letting the agent author and run its own code adds an untrusted-code surface that needs validation and sandboxing.
- A tool created for one subtask is wasted effort unless it is registered for reuse, yet over-eager tool creation clutters the registry.

## Therefore

Therefore: when no tool matches, have one role synthesize a new tool (code plus an interface spec), validate it against a test, and register it, so a separate tool-using role can call it like any other.

## Solution

Split the work into a tool-creator and a tool-user. When the user role finds no tool fits the subtask, it hands the specification to the creator role, which writes the tool's code and interface, generates or runs a test to confirm it behaves, and registers it in the tool registry. The user role then calls the new tool exactly as it would a built-in one, and the tool persists for later reuse. Execution of synthesized code runs in a sandbox, and a tool that fails its validation check is discarded rather than registered.

## Structure

```
tool-user (no tool fits) -> tool-creator writes code + spec -> validate (test) -> pass: register; fail: discard -> tool-user calls registered tool
```

## Diagram

```mermaid
flowchart TD
  task[Subtask] --> fit{Existing tool fits?}
  fit -->|yes| call[Tool-user calls it]
  fit -->|no| make[Tool-creator writes code + spec]
  make --> val{Passes validation?}
  val -->|no| discard[Discard]
  val -->|yes| reg[Register in tool registry]
  reg --> call
```

*When no tool fits, a creator role writes and validates a new tool, which the user role then calls.*

## Example scenario

An agent answering data questions is asked to compute a Gini coefficient, but it has only a generic SQL tool and a calculator. No tool fits, so the creator role writes a small gini(values) function, runs it against a known example to confirm the output, and registers it. The user role then calls gini on the query result, and the tool stays available for the next inequality question.

## Consequences

**Benefits**

- The agent closes capability gaps mid-task instead of failing or faking a result.
- A small, fixed toolset can cover an open task space, since missing tools are made on demand.
- Validated tools accumulate, so the same gap is not re-synthesized next time.

**Liabilities**

- Generated, executable tools are an untrusted-code surface that must be sandboxed and reviewed.
- Validation is only as good as the test the agent writes for its own tool.
- Unchecked synthesis clutters the registry with near-duplicate or single-use tools.

## Failure modes

- Self-validating blind spot — the agent writes a test that its own buggy tool passes.
- Sandbox escape — synthesized code reaches resources it should not touch.
- Registry sprawl — many one-off tools accumulate and degrade later tool selection.

## What this pattern constrains

A synthesized tool may not be called until it has passed a validation check; untested generated code is never registered or invoked, and its execution is confined to a sandbox.

## Applicability

**Use when**

- The task space is open-ended and a fixed toolset will inevitably hit capability gaps.
- The agent can run code in a sandbox and write a check that validates a new tool before use.
- Synthesized tools are worth keeping because similar gaps recur.

**Do not use when**

- A small, stable toolset already covers the domain.
- Running agent-authored code cannot be safely sandboxed.
- Each gap is unique, so synthesized tools never get reused and only add risk.

## Components

- Tool-user — the role that selects and calls tools to make task progress
- Tool-creator — the role that writes a new tool's code and interface when no tool fits
- Validator — runs a test against the synthesized tool before it may be registered
- Sandbox — confines execution of generated tool code
- Tool registry — stores validated tools so the user role and later runs can call them

## Tools

- Code sandbox — executes synthesized and validated tool code in isolation
- Tool registry and dispatcher — registers new tools and routes calls to them
- Test runner — checks a freshly synthesized tool against an expected result

## Evaluation metrics

- Capability-gap resolution rate — fraction of no-tool-fits subtasks the agent closes by synthesis
- Synthesized-tool validation pass rate — how often generated tools survive their own check
- Tool reuse rate — how often a synthesized tool is called again rather than re-created
- Sandbox-violation count — attempts by generated code to exceed its confinement

## Known uses

- **[LATM (LLMs as Tool Makers)](https://arxiv.org/abs/2305.17126)** _pure-future_ — Decouples a tool-maker role from a tool-user role: the maker writes a reusable tool, the user calls it.
- **[CREATOR](https://arxiv.org/abs/2305.14318)** _pure-future_ — Transforms an abstract problem into a concrete Python tool, separating tool creation from decision making.
- **[Evolution of Tool Use in LLM Agents (survey)](https://arxiv.org/abs/2603.22862)** _available_ — Treats 'Autonomous Tool Expansion' (LATM, CREATOR, ToolMaker, RestGPT) as a distinct branch of the tool-use literature.
- **[ToolMaker](https://arxiv.org/abs/2502.11705)** _available_ — Agentic framework that autonomously transforms papers-with-code repositories into LLM-compatible tools, installing dependencies and using a closed-loop self-correction mechanism with unit tests before the tool is exposed for use.
- **[CRAFT](https://arxiv.org/abs/2309.17428)** _available_ — Creates a toolset of diverse, reusable, validated code-snippet tools and retrieves from it at inference, separating tool creation from tool use.
- **[Voyager](https://github.com/MineDojo/Voyager)** _available_ — Maintains an ever-growing skill library of executable code synthesized on demand as tools.
- **[ToolMaker (KatherLab/ToolMaker)](https://github.com/KatherLab/ToolMaker)** _available_ — Shipping implementation that autonomously generates and self-corrects executable tool code from a task description and repo URL.

## Related patterns

- _alternative-to_ **Skill Library** — Skill Library accumulates critic-gated skills over runs for long-term reuse; On-Demand Tool Synthesis fabricates a tool just-in-time to close a capability gap in the current task, with an explicit creator/user role split.
- _complements_ **Code-as-Action Agent** — Code-as-Action runs code as the answer; here the code is packaged and registered as a reusable, callable tool.
- _complements_ **Tool Discovery** — Discovery finds existing tools; synthesis creates one when discovery finds nothing that fits.

## References

- [Large Language Models as Tool Makers](https://arxiv.org/abs/2305.17126) — 2023
- [CREATOR: Tool Creation for Disentangling Abstract and Concrete Reasoning of Large Language Models](https://arxiv.org/abs/2305.14318) — 2023
- [The Evolution of Tool Use in LLM Agents](https://arxiv.org/abs/2603.22862) — 2026
- [LLM Agents Making Agent Tools (ToolMaker)](https://arxiv.org/abs/2502.11705) — Georg Wölflein, Dyke Ferber, Daniel Truhn, Ognjen Arandjelović, Jakob Nikolas Kather, 2025
- [CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets](https://arxiv.org/abs/2309.17428) — Lifan Yuan, Yangyi Chen, Xingyao Wang, Yi R. Fung, Hao Peng, Heng Ji, 2023
