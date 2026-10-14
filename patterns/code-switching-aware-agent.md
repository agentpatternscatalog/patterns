# Code-Switching-Aware Agent

**Also known as:** Mixed-Language Input Handling, Hinglish-Tolerant Agent, Romanised-Indic Agent

**Category:** Structure & Data  
**Status in practice:** emerging

## Intent

Treat mixed-language input (e.g. Hinglish in Roman script) as the expected shape, and design tokenisation, language tagging, and tool routing to handle it natively without forcing the user to commit to one language.

## Context

A team is building a conversational agent for a market where users routinely blend two or more languages inside a single sentence, and often type one of those languages in a script that does not belong to it. A common example is Hinglish in India, where a user might type "book me a cab from Saket to Connaught Place jaldi" — English verbs, Hindi place names, and one Hindi adverb, all in the Latin alphabet because that is what the phone keyboard offers by default. The agent has to make sense of this mix without asking the user to commit to one language.

## Problem

A pipeline that assumes one language per turn fails this input in several distinct ways. A tokenizer tuned for English may split a Hindi word written in Latin letters into nonsense pieces; a language detector that runs on the whole utterance flips between turns or picks the wrong language and routes the request to a Natural Language Understanding stack that does not speak it; some systems give up entirely and ask the user to please pick one language, which is both a worse experience and a tacit refusal of how bilingual users actually talk. The team is then forced to choose between rejecting natural input and building a parallel pipeline per language pair.

## Forces

- Most off-the-shelf LLMs handle code-switching unevenly.
- Romanised Indic (Latin script) breaks naïve language detection.
- Tools and intents may be in one language while content is in another.
- Strict monolingual pipelines reject natural input.

## Therefore

Therefore: treat code-switched input as the default shape — tokenise script-agnostically, tag language at the clause level, and route tools off the tagged spans — so that the user never has to commit to one language.

## Solution

Adopt a three-part discipline. (1) Tokenise on Unicode + Latin without assuming a single script per turn. (2) Run language detection at clause level, not utterance level, so mixed-language tagging is preserved. (3) Choose models trained explicitly on code-switched corpora for the relevant language pair; if not available, prompt-engineer with code-switched few-shot examples. Tool slot extraction (entities like place names, times) must accept either script; normalise *after* extraction, not before.

## Structure

```
Utterance -> per-clause language tagger -> mixed-script aware extractor -> normalised slots -> tool call.
```

## Diagram

```mermaid
flowchart TD
  In[Mixed-language input] --> T[Tokenise on Unicode + Latin]
  T --> D[Clause-level<br/>language detection]
  D --> Tag[Per-clause language tags]
  Tag --> R[Route tools by tagged span]
  R --> Out[Response in user's mix]
```

## Example scenario

A consumer-finance assistant in India keeps mishandling messages like 'mera EMI kab due hai bhai?' — Roman-script Hindi mixed with English. A mono-language tokeniser splits 'EMI' awkwardly and the language detector flips between turns, sending replies to the wrong NLU pipeline. The team rebuilds the front of the agent as Code-Switching Aware: tokenisation handles Latin and Devanagari indistinguishably, each token gets a language tag, and tool routing uses the mixed signal directly. Users stop being asked to 'please use one language'.

## Consequences

**Benefits**

- Natural input is accepted as-is.
- Better recall for entities expressed in either language.
- Avoids the per-language refusal anti-pattern.

**Liabilities**

- Per-clause language detection is harder than utterance-level.
- Few foundation models are explicitly evaluated on code-switching.
- Eval sets need multilingual + code-switched coverage.

## Failure modes

- Utterance-level detection creeps back — a component tags the whole message with one language, and the clause in the other language is routed to a stack that cannot read it.
- Normalising too early — a place name in Latin script is converted before slot extraction, and the tool receives a mangled entity.
- Untested mix — the eval set covers each language alone but no code-switched turns, so regressions on mixed input ship unnoticed.
- Quiet downgrade — the agent does not refuse outright but answers mixed input with a shorter, less helpful reply than it gives single-language input.

## What this pattern constrains

The agent may not refuse or downgrade a request because the user mixed languages or scripts in one utterance; mixed-language input is in-spec.

## Applicability

**Use when**

- Real users mix languages within a single utterance (e.g. Hinglish, Spanglish, Singlish).
- Mono-language pipelines mis-tokenise or mis-detect the input.
- Models trained on code-switched corpora exist for the language pair in question.

**Do not use when**

- The user base reliably writes in one language per turn.
- No code-switched-trained model exists for the language pair and quality would regress.
- Forcing one language is acceptable in the deployment context (e.g. internal English-only tooling).

## Components

- Script-agnostic tokeniser — splits on Unicode and Latin without assuming a single script per turn
- Clause-level language detector — tags each clause rather than the whole utterance so mixed input is preserved
- Mixed-script slot extractor — pulls entities like place names and times from either script before normalisation
- Tool router — dispatches by tagged span so tools see content in the language they expect
- Slot normaliser — canonicalises extracted entities after extraction, never before

## Tools

- Code-switched-trained foundation model (e.g. Sarvam, IndicTrans, Krutrim) — primary inference for the relevant language pair
- Clause-level language identifier — replaces utterance-level langid that flips between turns
- Unicode-aware tokeniser — handles Latin and Devanagari (or other native script) indistinguishably

## Evaluation metrics

- Code-switched intent accuracy vs monolingual baseline — does treating mixed input as in-spec actually help
- Per-clause language-tag F1 — quality of the clause-level detector that the rest of the pipeline depends on
- Entity recall across scripts — fraction of place names / times correctly extracted whether typed in Latin or native script
- Refusal rate on mixed-language turns — should approach zero; the pattern's whole point is not refusing natural input
- Eval-set code-switching coverage — proportion of the held-out set that actually mixes languages, not just multilingual monolingual turns

## Known uses

- **[Sarvam (Indic LLMs and conversational agents)](https://www.sarvam.ai/)** _available_ — Models and pipelines explicitly trained for Indic-English code-switching.
- **AI4Bharat IndicTrans / IndicLLM family** _available_ — Indic-focused models with code-switching coverage.
- **Krutrim (Ola)** _available_ — Indic-first foundation model targeting mixed-language input.

## Related patterns

- _complements_ **Structured Output**
- _alternative-to_ **Translation Layer**
- _complements_ **Input/Output Guardrails**
- _complements_ **Multilingual Voice Agent Stack**
- _conflicts-with_ **Refusal**
- _complements_ **Liminal-State Detection**

## References

- [Sarvam AI](https://www.sarvam.ai/)
- [AI4Bharat](https://github.com/AI4Bharat)
