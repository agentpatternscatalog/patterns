# Business + LLM Microservice Split

**Also known as:** CPU/GPU Tier Split, Inference-Service Decoupling

**Category:** Structure & Data  
**Status in practice:** mature

## Intent

Split an LLM application into a CPU-bound business microservice (retrieval, prompt assembly, orchestration) and a GPU-bound LLM microservice (only model.generate behind REST), so each tier scales on its own hardware budget.

## Context

A production LLM application bundles retrieval, prompt assembly, post-processing, business logic, and the LLM inference call into a single service. The service autoscales as a unit. The LLM call needs GPU; the rest does not. The unified deployment pays GPU prices to autoscale the CPU-only parts.

## Problem

Bundled deployments waste expensive hardware. As traffic grows, the autoscaler adds whole GPU pods to handle CPU-bound spikes in prompt assembly and retrieval, while genuine GPU-bound spikes drag the entire service. Maintenance is coupled: bumping the model means redeploying the business logic; bumping the retrieval code means restarting GPU pods. The single service is a strict generalisation that loses on cost, scaling, and deploy velocity.

## Forces

- LLM inference needs GPU; retrieval and prompt assembly do not.
- Independent scaling axes (RPS, token throughput) have different load shapes.
- Coupled deploys slow both teams; decoupled deploys let model and business iterate independently.
- REST boundary adds one network hop per request — a measurable latency cost.

## Therefore

Therefore: split the application into a CPU business service (retrieval, prompt assembly, orchestration) and a GPU LLM service exposing only model.generate over REST, so each tier scales on its own hardware budget and is deployed on its own cadence.

## Solution

Define the LLM microservice's contract as a single REST endpoint: generate(prompt, params) → completion. Run it on GPU autoscaling on token-throughput metrics. Run everything else — retrieval, prompt templating, business logic, orchestration, output post-processing — in the CPU business service that calls the LLM service over REST. Bound the LLM service's tail latency with batching, queueing, and admission control. The business service can use multiple LLM service instances (different models, different providers) behind the same contract.

## Structure

```
User request -> CPU business service (retrieval via vector DB/cache, prompt assembly, orchestration) --REST generate(prompt, params)--> GPU LLM service (batching, queueing, admission control; scales on token throughput) --completion--> business service (post-processing) -> response
```

## Diagram

```mermaid
flowchart LR
  U[User request] --> Biz[CPU business service<br/>retrieval, prompt, orchestration]
  Biz -->|REST: generate| LLM[GPU LLM service<br/>model.generate]
  LLM --> Biz
  Biz --> U
  Biz -.-> VDB[(Vector DB)]
  Biz -.-> Cache[(Cache)]
```

## Example scenario

A RAG support platform deploys a CPU FastAPI business service handling retrieval (Qdrant), prompt assembly, and tenant routing, plus a separate GPU LLM service hosting a fine-tuned model behind TGI. Traffic spike: CPU pods scale 5x for retrieval load, GPU pods scale 2x for inference load. A model swap (Llama-3-8B to Llama-3-70B) is a deploy in the LLM service only; the business service is unchanged.

## Consequences

**Benefits**

- GPU pods size to GPU-bound load only; CPU pods to CPU-bound load only.
- Model swaps and business-logic changes deploy independently.
- Multiple LLM providers can sit behind one contract without business-service changes.

**Liabilities**

- One extra network hop per LLM call — latency cost.
- Two services to operate, deploy, monitor.
- Cross-service tracing required to make end-to-end latency visible.

## Failure modes

- Leaky contract — business logic such as prompt templating creeps into the GPU service, and a retrieval change once again forces a GPU redeploy.
- Hop latency pile-up — an orchestration step calls the LLM service many times in sequence, and the extra network hop per call adds up to a slow response.
- Blind spot between services — without cross-service tracing, a slow request cannot be pinned on retrieval, queueing or generation.
- Unbounded queue — the LLM service has no admission control, a traffic spike fills its queue, and tail latency climbs for every caller.

## What this pattern constrains

An LLM application must not bundle GPU inference with CPU business logic in one service when scaling and deploy cadence diverge; the LLM call lives behind its own service contract.

## Applicability

**Use when**

- LLM inference and business logic have diverging scaling profiles.
- Model swaps should not force business-logic redeploys.
- Multiple LLM providers may sit behind one contract.

**Do not use when**

- Very low traffic — one service is simpler and within budget.
- Latency budget cannot absorb one network hop.
- Team has no capacity to operate two services and cross-service tracing.

## Components

- Business service — CPU-bound retrieval, prompt assembly, orchestration
- LLM service — GPU-bound model.generate behind REST
- REST contract — generate(prompt, params) -> completion
- Cross-service tracing — propagates request IDs for end-to-end visibility

## Tools

- LLM serving runtime (TGI, vLLM, SageMaker)
- REST framework for business service (FastAPI, Express)
- OpenTelemetry — cross-service tracing

## Evaluation metrics

- GPU utilisation — share of GPU pod time on real inference
- Cross-service tail latency — added ms from the network hop
- Deploy decoupling — independent deploy frequency per service

## Known uses

- **[LLM Engineer's Handbook (Iusztin, Labonne, Packt 2024) — Twin business/inference services](https://www.packtpub.com/en-us/product/llm-engineers-handbook-9781836200079)** _available_
- **[Hugging Face TGI / vLLM / SageMaker deployments as standalone LLM services](https://huggingface.co/docs/text-generation-inference/en/index)** _available_
- **[Most production LLM platforms (Anthropic, OpenAI) — model inference behind API](https://platform.claude.com/docs/en/api/overview)** _available_

## Related patterns

- _composes-with_ **FTI LLM Pipeline Split**
- _complements_ **Agent Adapter**
- _complements_ **Augmented LLM**
- _complements_ **Prompt Caching**
- _uses_ **Rate Limiting**
- _complements_ **Channel-Decoupled Agent Core** — Both split an agent system along a boundary so each side evolves on its own: that pattern splits CPU business logic from GPU inference, this splits the channel-agnostic core from per-channel adapters.

## References

- [LLM Engineer's Handbook](https://www.packtpub.com/en-us/product/llm-engineers-handbook-9781836200079) — Paul Iusztin, Maxime Labonne, 2024
- [Architect scalable and cost-effective LLM & RAG inference pipelines](https://www.decodingai.com/p/architect-scalable-and-cost-effective)
