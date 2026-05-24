#!/usr/bin/env python3
"""Generate patterns.compositions.json — reverse index from pattern_id to
the compositions that implement it.

Compositions already link to patterns via members[].pattern. This script
inverts that mapping so consumers can answer "which products / frameworks
implement pattern X?" without scanning every composition shard.

Run locally: python3 .github/scripts/build_pattern_compositions.py [out_dir]
Reads:  compositions-src/*.json
Writes: <out_dir>/patterns.compositions.json  (default: repo root)
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
COMPS_SRC = ROOT / "compositions-src"

ROLE_RANK = {
    "first-class": 0,
    "core": 1,
    "supporting": 2,
    "auxiliary": 3,
    "optional": 4,
}


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    if not COMPS_SRC.exists():
        print(f"no {COMPS_SRC} dir; skipping patterns.compositions.json")
        return

    index: dict[str, list[dict]] = defaultdict(list)
    total_links = 0

    for shard_path in sorted(COMPS_SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        for c in shard.get("compositions", []):
            for m in c.get("members", []):
                pid = m.get("pattern")
                if not pid:
                    continue
                index[pid].append(
                    {
                        "composition_id": c["id"],
                        "composition_name": c.get("name", c["id"]),
                        "kind": c.get("kind"),
                        "vendor": c.get("vendor"),
                        "role": m.get("role"),
                        "evidence_status": m.get("evidence_status"),
                        "note": m.get("note"),
                    }
                )
                total_links += 1

    for pid in index:
        index[pid].sort(
            key=lambda x: (
                ROLE_RANK.get(x.get("role") or "", 99),
                (x.get("composition_name") or "").lower(),
            )
        )

    out = {
        "$schema": "./patterns.compositions.schema.json",
        "updated": date.today().isoformat(),
        "license": "CC-BY-4.0",
        "source": "compositions-src/*.json members[]",
        "description": (
            "Reverse index from pattern_id to compositions that implement it. "
            "Sorted by role (first-class > core > supporting > ...) then by "
            "composition name."
        ),
        "total_patterns": len(index),
        "total_links": total_links,
        "patterns": dict(sorted(index.items())),
    }
    out_path = out_dir / "patterns.compositions.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    try:
        display = out_path.relative_to(ROOT)
    except ValueError:
        display = out_path
    print(f"wrote {display}  ({len(index)} patterns, {total_links} links)")


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    build(out_dir)


if __name__ == "__main__":
    main()
