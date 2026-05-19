# Darwin-Gödel Self-Rewrite

**Also known as:** DGM, Darwin-Gödel Machine, Archive-Sampled Self-Mutation, Stepping-Stone Self-Rewrite

**Category:** Verification & Reflection
**Status in practice:** experimental

## Intent

An agent rewrites its own source code, archives every successful variant, and samples mutation parents from the archive rather than from the latest version, using diversity in the archive as evolutionary stepping-stones to escape local optima.

## Context

Research and long-running agents that can read and rewrite their own implementation (prompt, tool-set, scaffolding, or code) and that have an objective measure (a benchmark, a task suite, a self-eval) by which a variant is judged successful. Naive self-modification loops mutate the latest version and quickly settle into a local optimum.

## Problem

Greedy self-rewrite gets stuck. If the agent always mutates the latest accepted version, it climbs the local hill and stops; the move that would unlock the next ridge is several mutations away from anything currently good. Throwing away non-best variants destroys the diversity that would have been the bridge. The agent needs a way to escape local optima that does not require an outside reset.

## Forces

- Greedy ascent from the latest variant converges to local optima quickly.
- Useful stepping-stone variants often score worse short-term than the current best.
- Throwing away history makes those stepping-stones permanently unreachable.
- Self-modification needs a safety gate so each variant is at least viable before it enters the archive.
- Archive growth must be bounded or sampling becomes diffuse and useless.

## Therefore

Therefore: keep an archive of every variant that passes a viability gate, sample the parent for the next mutation from the archive (weighted by diversity, not by score), and let the archive's diversity supply evolutionary stepping-stones so self-rewrite can escape local optima without an outside reset.

## Solution

The agent maintains a versioned archive of self-modifications. Each generation: (1) sample a parent variant from the archive using a diversity-aware policy (not strictly the current best); (2) propose a code or prompt mutation; (3) run the mutated variant through a viability gate (compiles, passes safety checks, runs end-to-end on a smoke test); (4) score it on the objective; (5) if viable, add it to the archive with its score and lineage. Selection from the archive is the key move — it lets a low-scoring but novel variant become the parent of a future high-scoring variant. The archive is bounded by a retention policy that favours diversity over raw score so stepping-stones are preserved.

## Structure

```
Archive (variants with score + lineage) -> sample parent (diversity-weighted) -> propose mutation -> viability gate -> score on objective -> if viable, add to archive. Outer loop iterates; archive is the memory of evolution, not just the leaderboard.
```

## Example scenario

A research agent rewrites its own coding scaffolding to maximise a benchmark score. The greedy version stalls at a plateau after twenty generations. Switching to an archive-sampled scheme, a worse-scoring variant from generation six becomes the parent for generation twenty-two; its odd tool-handling structure happens to combine well with a mutation that the greedy line never reached, and the score jumps. The archive stored that stepping-stone for sixteen generations before it paid off.

## Consequences

**Benefits**

- Escapes local optima that greedy self-rewrite cannot.
- Archive preserves lineage and makes regressions debuggable.
- Diversity-weighted sampling reuses old branches as starting points for new exploration.
- Viability gate keeps the archive populated with runnable variants only.

**Liabilities**

- Archive storage and bookkeeping grows with generations.
- Diversity metric is a design choice and a bad one biases the search the wrong way.
- Viability gate is a single point of failure — a bug there lets broken variants in.
- Self-modifying agents are inherently harder to audit and to safety-check than fixed ones.

## What this pattern constrains

Each proposed variant must pass the viability gate (compiles, safety-checks, smoke test) before entering the archive; the agent must not mutate or sample outside the archive; the archive must keep score and lineage for every variant and must not be silently pruned by score alone.

## Applicability

**Use when**

- The agent can rewrite its own implementation (code, prompt, scaffolding) safely.
- A clear objective score is available per variant.
- Greedy self-rewrite has empirically plateaued.

**Do not use when**

- Self-modification is out of scope or unsafe in the deployment.
- Storage and compute cannot support an archive plus repeated viability gating.
- Objective score is too noisy for variant-to-variant comparison to mean anything.

## Known uses

- **[Sakana AI Darwin-Gödel Machine](https://sakana.ai/dgm-jp/)** — *Available* — Self-improving agent that rewrites its own code, archives variants, and samples from the archive as evolutionary stepping-stones.

## Related patterns

- *alternative-to* → [self-refine](self-refine.md) — Self-refine rewrites once from the latest version; DGM samples from the archive instead.
- *alternative-to* → [reflexion](reflexion.md) — Reflexion writes verbal lessons; DGM rewrites the agent itself and archives the rewrites.
- *complements* → [inner-critic](inner-critic.md) — Inner-critic / self-modification diff gate can serve as the viability gate at the front of the archive.
- *complements* → [evaluator-optimizer](evaluator-optimizer.md) — Evaluator-optimizer scores variants; DGM adds an archive plus diversity-weighted sampling on top.

## References

- (blog) Sakana AI, *Darwin-Gödel Machine (Sakana AI)*, 2025, <https://sakana.ai/dgm-jp/>
- (blog) Sakana AI, *Sakana AI blog (May 30, 2025)*, 2025, <https://sakana.ai/>

**Tags:** self-modification, evolution, archive, stepping-stones, agentic-rl
