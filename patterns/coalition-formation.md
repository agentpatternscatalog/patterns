# Coalition Formation

**Also known as:** Ad-Hoc Team Formation, Cooperative Subgroup

**Category:** Multi-Agent  
**Status in practice:** experimental

## Intent

Agents form temporary subgroups around a task because the coalition can achieve more value than the sum of its members acting alone, with explicit rules for who joins and how payoff or credit is shared.

## Context

A multi-agent system holds many agents with overlapping capabilities. Some tasks are super-additive — three agents working as a coalition deliver more than they would individually. Other tasks are sub-additive. Without a coalition-formation step, agents act in isolation and the super-additive value is left on the floor.

## Problem

Static team rosters do not match the problem. Some problems need three specialists, others need eight generalists, others need only the agent who already holds context. Either there is a fixed multi-agent topology that wastes capacity on small problems and underprovisions for large ones, or there is no coordination and the agents work alone. Worse, when a coalition does form ad hoc, the credit/payoff allocation is implicit and political: contributors who did the heaviest lifting do not get the credit, and over time agents stop volunteering.

## Forces

- Coalition value depends on the problem and on which agents join.
- Joining is a cost — at least the coordination overhead — that the joining agent must expect to recover.
- Credit / payoff sharing must be principled or contributors disengage.
- Coalition dissolution must be clean — agents return to the pool.

## Applicability

**Use when**

- Agents have heterogeneous capabilities and tasks vary in shape.
- Some tasks are super-additive in agent contribution.
- Reputation or payoff matters for agent engagement.

**Do not use when**

- All tasks fit a single fixed team — no benefit from per-task formation.
- Coordination cost dominates task value.
- No principled value/payoff function can be defined for the domain.

## Therefore

Therefore: form coalitions per-task using an explicit value function and a declared payoff-allocation rule, so the team shape matches the problem and contributors are compensated proportionally.

## Solution

Define a value function v(S) for any subset S of agents on a given task. A coalition-formation protocol enumerates candidate coalitions, scores them, and chooses the one with the best value/cost ratio. A payoff-allocation rule (Shapley value, equal split, proportional to contribution, weighted by reputation) determines how the coalition's reward is split. Coalitions are temporary: once the task is done, the coalition dissolves and agents return to the pool. For LLM agents this can be lighter — a coordinator picks a few agents per task based on heuristics rather than full optimisation.

## Example scenario

A document-analysis platform holds 15 specialist agents. A new task arrives: 'review this 60-page contract'. The coordinator forms a coalition of the legal-clause specialist, the entity-extractor, and the redline-comparator (skipping the design-review agent). Payoff (compute budget, reputation credit) is split per Shapley value on a small holdout eval. After the task the three return to the pool.

## Diagram

```mermaid
flowchart TD
  Task[New task] --> Eval[Score candidate coalitions]
  Pool[Agent pool] --> Eval
  Eval --> Pick[Pick best v(S)/cost]
  Pick --> Form[Form coalition]
  Form --> Work[Coalition executes]
  Work --> Pay[Allocate payoff per rule]
  Pay --> Diss[Dissolve back to pool]
```

## Consequences

**Benefits**

- Team shape matches problem shape.
- Super-additive tasks unlock value that solo or fixed-team operation misses.
- Explicit payoff rule keeps contributors engaged.

**Liabilities**

- Enumerating coalitions is exponential in agent count without heuristics.
- Payoff allocation rules each have failure modes; no rule is universal.
- Coalition-formation overhead can exceed the task value for small problems.

## What this pattern constrains

Multi-agent teams must not be static when task shape varies; coalitions form per-task with an explicit value function and a declared payoff-allocation rule.

## Known uses

- **Multiagent Systems (Weiss, MIT Press) — Coalition formation chapter (Sandholm)** — *Available* — <https://mitpress.mit.edu/9780262731317/multiagent-systems/>
- **Game-theoretic multi-agent platforms (Shapley-value calculators in MAS toolkits)** — *Available*

## Related patterns

- *complements* → [contract-net-protocol](contract-net-protocol.md) — CNP allocates one task; coalition formation chooses a sub-team for the task.
- *alternative-to* → [supervisor](supervisor.md)
- *complements* → [trust-and-reputation-routing](trust-and-reputation-routing.md)
- *complements* → [vickrey-auction-allocation](vickrey-auction-allocation.md)
- *uses* → [world-model-as-tool](world-model-as-tool.md)
- *composes-with* → [joint-commitment-team](joint-commitment-team.md)

## References

- (book) *Multiagent Systems, 2nd ed.*, Gerhard Weiss (ed.), 2013, <https://mitpress.mit.edu/9780262731317/multiagent-systems/>
- (doc) *Cooperative game theory*, <https://en.wikipedia.org/wiki/Cooperative_game_theory>

**Tags:** multi-agent, cooperation, game-theory
