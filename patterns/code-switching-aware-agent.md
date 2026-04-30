# Code-Switching-Aware Agent

**Also known as:** Mixed-Language Input Handling, Hinglish-Tolerant Agent, Romanised-Indic Agent

**Category:** Structure & Data  
**Status in practice:** emerging

## Intent

Treat mixed-language input (e.g. Hinglish — Hindi-English code-switching, often in Roman script) as the expected input shape, not an error, and design tokenisation, language tagging, and tool routing to handle it natively without forcing the user to commit to one language.

## Context

Conversational agents in markets where users routinely mix languages and scripts within a single utterance ("book me a cab from Saket to Connaught Place jaldi"); romanised Indic typing is the norm because Latin keyboards dominate.

## Problem

Mono-language pipelines mis-tokenise, mis-detect, or refuse mixed-language input; forcing the user to pick a language degrades UX and discriminates against real-world bilingual usage.

## Forces

- Most off-the-shelf LLMs handle code-switching unevenly.
- Romanised Indic (Latin script) breaks naïve language detection.
- Tools and intents may be in one language while content is in another.
- Strict monolingual pipelines reject natural input.

## Solution

Adopt a three-part discipline. (1) Tokenise on Unicode + Latin without assuming a single script per turn. (2) Run language detection at clause level, not utterance level, so mixed-language tagging is preserved. (3) Choose models trained explicitly on code-switched corpora for the relevant language pair; if not available, prompt-engineer with code-switched few-shot examples. Tool slot extraction (entities like place names, times) must accept either script; normalise *after* extraction, not before.

## Structure

```
Utterance -> per-clause language tagger -> mixed-script aware extractor -> normalised slots -> tool call.
```

## Consequences

**Benefits**

- Natural input is accepted as-is.
- Better recall for entities expressed in either language.
- Avoids the per-language refusal anti-pattern.

**Liabilities**

- Per-clause language detection is harder than utterance-level.
- Few foundation models are explicitly evaluated on code-switching.
- Eval sets need multilingual + code-switched coverage.

## What this pattern constrains

The agent may not refuse or downgrade a request because the user mixed languages or scripts in one utterance; mixed-language input is in-spec.

## Known uses

- **[Sarvam (Indic LLMs and conversational agents)](https://www.sarvam.ai/)** — *Available*. Models and pipelines explicitly trained for Indic-English code-switching.
- **AI4Bharat IndicTrans / IndicLLM family** — *Available*. Indic-focused models with code-switching coverage.
- **Krutrim (Ola)** — *Available*. Indic-first foundation model targeting mixed-language input.

## Related patterns

- *complements* → [structured-output](structured-output.md)
- *alternative-to* → [translation-layer](translation-layer.md)
- *complements* → [input-output-guardrails](input-output-guardrails.md)
- *complements* → [multilingual-voice-agent](multilingual-voice-agent.md)
- *conflicts-with* → [refusal](refusal.md)

## References

- (doc) *Sarvam AI*, <https://www.sarvam.ai/>
- (doc) *AI4Bharat*, <https://ai4bharat.iitm.ac.in/>

**Tags:** structure-data, multilingual, india-origin, code-switching
