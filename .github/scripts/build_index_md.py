#!/usr/bin/env python3
"""Generate INDEX.md from patterns-src/ — the human-browsable catalog index.

INDEX.md is committed to the repo (consumers read it directly on GitHub), so unlike the
gitignored JSON artifacts it can drift from source. This generator is tracked CI infra so
check_drift.py can regenerate it and fail the build if the committed copy is stale.

Patterns are sorted alphabetically by name within each category. The category order below
is the canonical presentation order.

Run locally: python3 .github/scripts/build_index_md.py [out_path]
Reads:  patterns-src/*.json
Writes: <out_path>  (default: repo-root INDEX.md)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PAT_SRC = ROOT / "patterns-src"

# Canonical presentation order. Every pattern category must appear here.
CAT_LABEL = {
    "reasoning": "Reasoning",
    "planning-control-flow": "Planning & Control Flow",
    "tool-use-environment": "Tool Use & Environment",
    "retrieval": "Retrieval & RAG",
    "memory": "Memory",
    "multi-agent": "Multi-Agent",
    "verification-reflection": "Verification & Reflection",
    "safety-control": "Safety & Control",
    "routing-composition": "Routing & Composition",
    "governance-observability": "Governance & Observability",
    "structure-data": "Structure & Data",
    "streaming-ux": "Streaming & UX",
    "cognition-introspection": "Cognition & Introspection",
    "anti-patterns": "Anti-Patterns",
}


def render() -> str:
    by_cat: dict[str, list[dict]] = {c: [] for c in CAT_LABEL}
    total = 0
    for path in sorted(PAT_SRC.glob("*.json")):
        for p in json.loads(path.read_text())["patterns"]:
            cat = p["category"]
            if cat not in CAT_LABEL:
                raise SystemExit(
                    f"{path.name}: pattern {p['id']} has category {cat!r} "
                    f"not in CAT_LABEL — add it to build_index_md.py"
                )
            by_cat[cat].append(p)
            total += 1
    for cat in by_cat:
        by_cat[cat].sort(key=lambda p: p["name"].lower())

    populated = [c for c in CAT_LABEL if by_cat[c]]
    lines = ["# Pattern Index", "", f"{total} patterns across {len(populated)} categories.", ""]
    for slug in CAT_LABEL:
        if not by_cat[slug]:
            continue
        lines.append(f"## {CAT_LABEL[slug]}")
        lines.append("")
        for p in by_cat[slug]:
            aliases = p.get("aliases") or []
            ak = f" *(a.k.a. {', '.join(aliases)})*" if aliases else ""
            lines.append(f"- [{p['name']}](patterns/{p['id']}.md){ak} — {p['intent']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "INDEX.md"
    text = render()
    out_path.write_text(text)
    total = text.split("\n", 3)[2]
    print(f"wrote {out_path}  ({total})")


if __name__ == "__main__":
    main()
