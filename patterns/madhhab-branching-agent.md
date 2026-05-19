# Madhhab-Branching Agent

**Also known as:** Identity-Conditioned Multi-Answer, Plural-Authority Forking, مذهب-حسّاس, Multi-School Fork

**Category:** Routing & Composition
**Status in practice:** emerging

## Intent

When a query has multiple legally- or doctrinally-valid answers conditional on the user's identity, fork the reasoning per identity and return school-attributed answers rather than picking one as ground truth.

## Context

Domains where authoritative answers depend on the asker's affiliation rather than on any single ground truth: Islamic jurisprudence with multiple madhhabs, Christian or Jewish denominational practice, jurisdictional law (US federal vs state, EU member-state divergence), medical guidelines that differ between national bodies, accounting standards that differ between IFRS and US GAAP. The agent's role is to be correct for the user it is talking to, not to declare one school correct.

## Problem

Standard routing and disambiguation patterns assume the agent should converge on one answer. In plural-authority domains this is a category error: the answer 'what is the inheritance share of the daughter' has several simultaneously correct answers depending on which madhhab is consulted, and asking the user 'which madhhab are you' is sometimes appropriate but is itself a doctrinal claim about how identity binds practice. Picking one answer silently is worse — it imposes a school the user may not subscribe to. Most agent stacks have no first-class way to preserve plural valid answers.

## Forces

- Multiple authorities are simultaneously valid; only the user's identity (or the deployment's scope) determines which one applies.
- Silently picking one authority misrepresents the domain and the user.
- Always asking the user to declare an affiliation is intrusive and is itself a doctrinal claim.
- Surfacing all forks every time is verbose and can be confusing when one authority clearly dominates the deployment's audience.
- Citations must be authoritative per school, not a synthesised consensus.

## Therefore

Therefore: when the domain admits plural valid answers, fork the reasoning per recognised school or authority and present school-attributed answers in parallel, preserving non-convergence by design, while letting the user (or deployment) narrow to one school when appropriate.

## Solution

Detect plural-authority queries (a classifier or a router checks whether the domain admits identity-conditioned answers and whether the current query is in scope). For such queries, run a parallel reasoning pass per recognised school, each grounded in that school's own canonical sources. Present the answers side by side with explicit school attribution, citations from that school's authorities, and a note that the answers diverge by school of jurisprudence (or denomination, jurisdiction, etc.). Offer the user the option to filter to one school. Honour a deployment-level pin when the audience is monolithic (e.g. a Maliki-region deployment may default to Maliki but still expose the option to see other schools). Never present a single answer as 'the' answer when plural valid answers exist.

## Structure

```
User query --> Plural-authority detector --> {single-authority pipeline | multi-authority fork}. Multi-authority fork: spawn per-school reasoning {school_1 reasoning, school_2 reasoning, ...} --> Aggregator that preserves attribution and citations --> Side-by-side school-labelled response.
```

## Example scenario

A user asks an Islamic-jurisprudence assistant how a deceased person's estate should be divided. The plural-authority detector recognises that inheritance rules diverge meaningfully across Sunni madhhabs. The agent runs four parallel reasoning passes — Hanafi, Maliki, Shafi'i, Hanbali — each grounded in that school's canonical fiqh sources, and returns four labelled answers side by side with citations. The user is then offered the option to filter to one school; if the deployment is region-pinned to Maliki, that school is shown first by default but the other three remain accessible.

## Consequences

**Benefits**

- Faithfully represents domains where ground truth is plural by construction.
- Empowers users to see the landscape of valid answers and locate themselves.
- Citations remain per-authority and verifiable; nothing is averaged into a synthetic consensus.
- Generalises beyond religion to jurisdictional law, medical guidelines, accounting standards.

**Liabilities**

- Higher token and latency cost: each query may trigger N parallel reasoning passes.
- School-detection is itself a non-trivial classifier and a source of error.
- Designating which schools to fork over is a doctrinal/political call that must be made and documented.
- Presenting four answers when one is clearly relevant can degrade user experience; calibration matters.
- Deployments cannot use this pattern to evade local-authority obligations where a single authority is legally binding.

## What this pattern constrains

The LLM must not collapse plural valid answers into a single 'the' answer, must not strip per-school citations or paraphrase across schools, and must not silently adopt a school the user did not declare and the deployment did not configure.

## Applicability

**Use when**

- The domain has multiple recognised authorities that yield different valid answers (madhhabs, denominations, jurisdictions, specialty bodies).
- The user's identity or the deployment's scope determines which authority applies.
- Per-authority canonical sources are available and citation-quality is required.
- Imposing one authority silently would be a category error for the domain.

**Do not use when**

- The domain has a single binding authority (e.g. a single jurisdiction's statute) and pluralism would mislead.
- Per-authority sources are not available at citation quality; forking would produce shallow per-school answers.
- The added latency and verbosity is not justified by the audience's need for plural answers.

## Known uses

- **[QCRI Fanar-Sadiq](https://arxiv.org/abs/2603.08501)** — *Available* — Verified Islamic-law reasoning agent with explicit Sunni-school handling and per-school attribution.

## Related patterns

- *alternative-to* → [routing](routing.md) — Routing picks one branch; madhhab-branching preserves multiple branches by design when the domain admits plural valid answers.
- *complements* → [disambiguation](disambiguation.md) — Disambiguation asks the user to resolve ambiguity; madhhab-branching may follow when the user declines or when the deployment serves multiple identities.
- *alternative-to* → [parallelization](parallelization.md) — Parallelization aggregates parallel branches toward a single answer; madhhab-branching keeps the branches intentionally distinct.
- *alternative-to* → [voting-based-cooperation](voting-based-cooperation.md) — Voting drives consensus; madhhab-branching forbids consensus when authority is genuinely plural.

## References

- (paper) *Fanar-Sadiq: Verified Islamic-Law Reasoning Agent*, <https://arxiv.org/abs/2603.08501>
- (paper) Qatar Computing Research Institute, *Fanar 2.0 Technical Report*, <https://arxiv.org/abs/2603.16397>

**Tags:** routing, plural-authority, identity-conditioned, religious-llm, jurisdictional, multi-answer
