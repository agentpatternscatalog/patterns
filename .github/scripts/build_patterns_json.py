#!/usr/bin/env python3
"""Concatenate patterns-src/<category>.json shards into a single patterns.json.

Used by .github/workflows/pages.yml to publish the consolidated catalog.
Run locally: python3 .github/scripts/build_patterns_json.py [out_dir]
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "patterns-src"
SCHEMA = ROOT / "schema.json"


def build(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    patterns: list[dict] = []
    seen: set[str] = set()
    for shard_path in sorted(SRC.glob("*.json")):
        shard = json.loads(shard_path.read_text())
        cat = shard["category"]
        for p in shard["patterns"]:
            if p["category"] != cat:
                raise SystemExit(
                    f"{shard_path.name}: pattern {p['id']} has category "
                    f"{p['category']!r}, expected {cat!r}"
                )
            if p["id"] in seen:
                raise SystemExit(f"duplicate pattern id: {p['id']}")
            seen.add(p["id"])
            patterns.append(p)

    patterns.sort(key=lambda p: (p["category"], p["id"]))

    out = {
        "$schema": "./schema.json",
        "license": "CC-BY-4.0",
        "patterns": patterns,
    }
    (out_dir / "patterns.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )
    shutil.copy(SCHEMA, out_dir / "schema.json")

    for extra in (
        "framework-coverage.json",
        "framework-coverage.schema.json",
        "recipes.json",
        "recipes.schema.json",
        "glossary.json",
        "glossary.schema.json",
    ):
        src = ROOT / extra
        if src.exists():
            shutil.copy(src, out_dir / extra)

    print(f"built {out_dir/'patterns.json'} with {len(patterns)} patterns")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    build(target)
