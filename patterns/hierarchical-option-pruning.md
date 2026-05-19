# Hierarchical Option Pruning

**Also known as:** Two-Stage Tool Routing, Coarse-then-LLM Routing, Filtrado Jerárquico, Banking Routing Agent

**Category:** Routing & Composition
**Status in practice:** emerging

## Intent

Pre-filter a large catalog of tools or operations with a coarse classifier down to a small candidate set before letting the LLM make the final selection, mitigating function-calling accuracy collapse at scale.

## Context

Production agents whose action surface has grown into the hundreds of tools or operations (banking back-office, ERP, ticketing, internal platforms). The full catalog cannot be presented to the LLM in a single call without degrading function-calling accuracy and inflating token cost, but the catalog is largely stable and known in advance.

## Problem

When the LLM is given a single-step choice over a large, mostly-stable tool inventory, function-calling accuracy degrades sharply (it picks plausible-looking but wrong tools, hallucinates argument shapes, or fails to pick at all). Static per-task subsets (loadouts) are too brittle when the same agent serves many user intents. Lazy schema fetching by semantic query helps when the catalog is huge and dynamic, but does not solve the accuracy collapse for a fixed inventory where the bottleneck is the size of the choice set, not the missing schemas. The agent needs a way to first reduce the choice set with a cheap, well-calibrated classifier and only then let the LLM choose.

## Forces

- Function-calling accuracy collapses as the number of candidate tools grows.
- Token cost grows linearly with the number of fully-described tools exposed to the LLM.
- Static per-task loadouts cannot anticipate the diversity of real user queries.
- The catalog is stable enough to train a coarse classifier offline.
- Coarse classifiers are cheaper and faster than LLM tool selection.
- End-users do not care which stage made the decision; they care that the right tool fired with the right arguments.

## Therefore

Therefore: insert a coarse classifier between the user query and the LLM's tool-call step that prunes the full catalog to a small candidate set (typically five to six), and let the LLM perform final selection and argument filling over that pruned set.

## Solution

Train (or compile, or rule-author) a coarse classifier that maps the user query and minimal context to a short ranked list of candidate tools or operations from the full inventory. At runtime, the classifier runs first, returns the top-k candidates (commonly k=5 or k=6), and only those candidates' schemas are presented to the LLM. The LLM then performs final intent verification, picks one, and fills arguments. If the LLM cannot pick from the candidates (confidence below threshold, schema mismatch), fall back to a broader candidate set or escalate to disambiguation. The classifier is trained on labelled query/tool pairs and re-trained on production traffic; precision at top-k is the headline metric. The pruned set is logged so misroutes are diagnosable as classifier errors or LLM errors.

## Structure

```
User query --> Coarse classifier --> Top-k candidate tools --> LLM (sees only k schemas) --> Final tool pick + arguments --> Dispatch. Logging: (query, classifier top-k, LLM pick) for offline evaluation.
```

## Example scenario

A bank's customer assistant exposes more than 150 distinct back-office operations — transfers, card actions, KYC updates, dispute filings, mortgage queries. Presenting all 150 to the LLM at once collapses function-calling accuracy and burns tokens. A coarse routing classifier is trained on historical query/operation pairs and runs first: for any incoming utterance it returns five to six candidate operations. Only those candidates' schemas are passed to the LLM, which verifies intent, picks one, and fills arguments. Production accuracy stays high; misroutes are traced back to either the classifier (right answer missing from top-k) or the LLM (right answer present but wrong choice) and each stage is improved on its own metric.

## Consequences

**Benefits**

- Function-calling accuracy stays high because the LLM chooses from a small set.
- Token cost is proportional to k, not to the full catalog size.
- The classifier and the LLM stage are independently observable and improvable.
- Coarse classifier training data accumulates naturally from production traffic.
- Scales to inventories where lazy semantic search is overkill and static loadouts are too brittle.

**Liabilities**

- Misroutes by the coarse classifier are invisible to the LLM; if the right tool is not in the top-k, the LLM cannot recover.
- Two-stage pipelines require two evaluation harnesses and two monitoring surfaces.
- The classifier becomes a hidden dependency on training-data freshness; concept drift in the inventory or in user phrasing degrades it silently.
- Choosing k is a calibration knob between accuracy and recall; mis-set, it hurts one or the other.
- Does not address the case where the catalog itself is dynamic at runtime (a different pattern fits there).

## What this pattern constrains

The LLM must not be presented with the full tool catalog when the inventory exceeds the size at which function-calling accuracy collapses, must not silently expand the candidate set beyond the classifier's top-k without logging the fallback, and must not pick a tool outside the pruned candidate set without an explicit fallback path.

## Applicability

**Use when**

- The tool or operation inventory is large enough (tens to hundreds) that exposing all of it to the LLM degrades function-calling accuracy.
- The inventory is stable enough to train and maintain a coarse classifier.
- Labelled query/tool data is available or can be bootstrapped from production traffic.
- Misroutes are diagnosable and tolerable in the deployment's risk envelope.

**Do not use when**

- The inventory is small enough that a single-step LLM choice is accurate.
- The inventory is highly dynamic at runtime and a trained classifier would be perpetually stale; lazy semantic search fits better.
- There is no labelled data and no realistic path to bootstrap it.
- The risk of a top-k miss (right tool not in the candidate set) is unacceptable and there is no escalation path.

## Known uses

- **[BBVA AI Factory routing agent](https://www.bbvaaifactory.com/the-routing-agent-a-key-component-for-agentic-ai-assistants/)** — *Available* — Production banking assistants collapse a catalog of more than 150 banking operations to a 5-6 candidate set via a coarse routing classifier before LLM selection.

## Related patterns

- *specialises* → [routing](routing.md) — Specialises single-step intent routing by inserting a coarse-then-LLM pruning stage instead of a single classifier-picks-one decision.
- *alternative-to* → [tool-loadout](tool-loadout.md) — Tool loadout selects a static per-task subset up front; hierarchical option pruning selects dynamically per query.
- *alternative-to* → [tool-search-lazy-loading](tool-search-lazy-loading.md) — Lazy-loading fetches schemas on demand by semantic query, suited to huge or dynamic inventories; hierarchical pruning suits stable inventories where a trained classifier is cheaper and more precise.
- *complements* → [multi-model-routing](multi-model-routing.md) — Multi-model routing picks the model; hierarchical option pruning picks the tool. They compose.
- *alternative-to* → [mixture-of-experts-routing](mixture-of-experts-routing.md) — MoE routes among expert agents; hierarchical option pruning routes among tools within a single agent.
- *complements* → [disambiguation](disambiguation.md) — When the classifier's top-k is low-confidence or the LLM cannot pick, fall back to a clarifying question.

## References

- (blog) BBVA AI Factory, *The Routing Agent: A Key Component for Building Agentic AI Assistants at Scale*, <https://www.bbvaaifactory.com/the-routing-agent-a-key-component-for-agentic-ai-assistants/>
- (blog) BBVA AI Factory, *From Message to Action: How Specialized Agents Operate in a Multi-Agent AI Assistant*, <https://www.bbvaaifactory.com/specialized-ai-agents-in-an-ai-assistant/>

**Tags:** routing, tool-selection, two-stage, function-calling, scalability, banking
