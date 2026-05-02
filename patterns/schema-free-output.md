# Schema-Free Output

**Also known as:** Free-Form Tool Call, String-Parsing the Model

**Category:** Anti-Patterns  
**Status in practice:** deprecated

## Intent

Anti-pattern: parse free-form model output for downstream code instead of using structured output.

## Context

An agent emits text that downstream code parses with regex, string splits, or 'is the word yes in there?'.

## Problem

The model invents punctuation, formatting, and field names. Parsers fail in non-obvious ways. Errors are mis-attributed to the model when they are parser bugs.

## Forces

- Structured output adds setup cost and provider lock-in.
- Some providers offered structured output later than tool use.
- Free-form feels flexible until it breaks.


## Applicability

**Use when**

- Never use this; downstream code parsing free-form model text is brittle and silently corrupts state.
- Use structured-output (JSON Schema, Pydantic, function calling) instead.
- If a provider lacks structured output, validate with strict post-parse and retry.

**Do not use when**

- Downstream code depends on typed fields.
- Parser failure would propagate as a model bug and waste debugging time.
- Structured output or tool calling is available on the chosen provider.

## Solution

Don't. Use structured-output (JSON Schema, Pydantic, function calling). See structured-output, tool-use.

## Example scenario

A team ships an agent whose downstream consumes free-form model output by regex-parsing 'looks like JSON.' Edge cases (smart quotes, missing commas, surprise prose preamble) fail in non-obvious ways, and post-mortems blame the model when most failures are parser bugs. They stop doing this and switch to structured output with a JSON Schema, validating against it and retrying on parse failure. The 'flaky model' framing dissolves into a parser-bug fix.

## Consequences

**Liabilities**

- Brittle parsing.
- Silent corruption of downstream state.
- Debugging blames the model when the parser is at fault.

## What this pattern constrains

By definition, this anti-pattern imposes no useful constraint; the missing constraint is the failure mode.

## Known uses

- **Pre-2024 LangChain agents** — *Available*

## Related patterns

- *alternative-to* → [structured-output](structured-output.md)
- *alternative-to* → [tool-use](tool-use.md)

**Tags:** anti-pattern, parsing, schema
