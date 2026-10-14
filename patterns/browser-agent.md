# Browser Agent

**Also known as:** Web Agent, Browser Automation Agent

**Category:** Tool Use & Environment  
**Status in practice:** emerging

## Intent

Expose websites to the agent through a structured DOM/accessibility tree plus a small action vocabulary, sitting between raw HTML and pixel-level Computer Use.

## Context

A team needs an agent that operates websites end-to-end: filling forms, pulling competitive data, navigating multi-page checkouts, or running research across many sites. The target sites have no clean API the team can integrate with, and pixel-level screen control (the Computer Use approach) is too slow and brittle for routine web work.

## Problem

Raw HTML is full of inline scripts, tracking pixels, and minified CSS that overwhelm the context window before the agent reaches the actual content. Treating the browser as pure pixels and driving the mouse to coordinates is slow, breaks the moment the layout shifts, and burns vision tokens on every click. Without a stable, structured representation of the page the agent ends up reasoning over noise instead of intent.

## Forces

- DOM extraction needs a stable representation across sites.
- Action vocabulary completeness vs simplicity.
- Anti-bot measures break agent flows.

## Therefore

Therefore: expose the page as a numbered DOM / accessibility tree and a small action vocabulary, so that the agent reasons over stable structure instead of raw HTML or pixels.

## Solution

A library (Playwright-backed) exposes structured page state (numbered interactive elements, accessibility tree) and a compact action set (click, type, scroll, navigate). The agent reasons over the structured state and emits actions; the library executes them.

## Structure

```
Page --> Playwright library --> Accessibility tree + numbered elements --> Agent (reasons over structured state) --click / type / scroll / navigate--> Playwright library --> Page
```

## Diagram

```mermaid
flowchart TD
  P[Page] --> Lib[Playwright lib]
  Lib --> AT[A11y tree +<br/>numbered elements]
  AT --> Agent
  Agent -->|click/type/scroll| Lib
  Lib --> P
```

## Example scenario

A growth team builds an agent that scrapes competitor pricing pages. Feeding raw HTML overflows context with tracking scripts and inline CSS; pixel-level Computer Use is overkill for clicking through five filters. They settle on a Browser Agent surface: the page is reduced to a structured DOM/accessibility tree of interactable elements, and the agent emits actions from a small vocabulary like click(id) and type(id, text). The model spends its tokens on intent, not on parsing minified script tags.

## Consequences

**Benefits**

- Faster and more reliable than pixel-driven Computer Use on the web.
- Web-specific abstractions like 'fill form' compose naturally.

**Liabilities**

- Still struggles with heavily-dynamic JS apps.
- Anti-bot blocks; CAPTCHAs.

## Failure modes

- Dynamic page blindness — a heavy JavaScript app re-renders after the tree is read, and the numbered element the agent clicks no longer points at the same control.
- Bot wall — the site serves a CAPTCHA or blocks the automated browser, and the agent loops on a page it cannot get past.
- Missing element — the control the task needs is not in the accessibility tree, so the agent reasons over a page that looks complete but is not.
- Vocabulary gap — the task needs an action outside click, type, scroll, and navigate, and the agent cannot finish it within the allowed surface.

## What this pattern constrains

Actions are limited to the typed vocabulary; arbitrary JavaScript execution is not part of this surface.

## Applicability

**Use when**

- The agent must operate websites and a structured DOM/accessibility tree is available.
- Raw HTML is too noisy and pixel-level Computer Use is too slow or brittle for the web target.
- A small action vocabulary (click, type, scroll, navigate) suffices for the task.

**Do not use when**

- The site requires pixel-level interaction (canvas, custom drawing) that no DOM tree exposes.
- There is a clean API and using it is cheaper and more reliable than driving the UI.
- Anti-bot measures make programmatic browser control infeasible at the required scale.

## Components

- Agent — reasons over structured page state and emits compact actions
- Browser Driver (Playwright-backed) — executes click, type, scroll, and navigate against the live page
- Accessibility Tree Extractor — produces numbered interactive elements and the a11y tree from the DOM
- Action Vocabulary — small typed set (click, type, scroll, navigate) the agent can emit
- Page Snapshotter — captures the structured observation returned after each action

## Tools

- Playwright (or Puppeteer) — drives the browser and exposes accessibility-tree extraction
- DOM-to-a11y reducer — compresses raw HTML into a numbered element list that fits the context window

## Evaluation metrics

- Task success on web benchmarks (WebArena, Mind2Web) — headline capability on real sites
- Action-validity rate — fraction of emitted actions that resolve to a real element on the page
- Tokens per page observation — cost of the structured surface versus raw HTML
- Layout-shift recovery rate — share of runs that survive a DOM change between observation and action
- p95 step latency — time per click-or-type round trip including extraction

## Known uses

- **[browser-use (Python library)](https://github.com/browser-use/browser-use)** _available_
- **Playwright + LangChain** _available_
- **[OpenAI Operator](https://operator.chatgpt.com/)** _available_
- **[Browserbase](https://www.browserbase.com/)** _available_
- **Skyvern** _available_

## Related patterns

- _alternative-to_ **Computer Use**
- _specialises_ **Tool Use**
- _complements_ **Tool Output Poisoning Defense**
- _alternative-to_ **Mobile UI Agent**
- _generalises_ **Dual-System GUI Agent**
- _generalises_ **Policy-Localizer-Validator**
- _complements_ **Magentic-One Generalist Multi-Agent**
- _complements_ **Crawler Dispatcher**
- _alternative-to_ **Full-Desktop Computer Use**

## References

- [browser-use/browser-use](https://github.com/browser-use/browser-use)
