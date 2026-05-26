#!/usr/bin/env python3
"""Drift gate: assert the committed catalog matches a clean rebuild from source.

The gitignored JSON artifacts (patterns.json, patterns.graph.json, …) are rebuilt fresh in
CI, so they can't drift in what ships. But two things CAN drift:

  1. Committed derived files — INDEX.md is checked into the repo and read directly on
     GitHub. If a pattern is added straight to a derived artifact instead of patterns-src/
     (a "phantom"), INDEX.md and the source disagree.
  2. The build itself — build_graph rejects related[] edges that resolve to neither a
     pattern nor a methodology, so a clean rebuild surfaces dangling cross-references.

This script rebuilds every derived artifact from source into a temp dir, then diffs the
regenerated INDEX.md against the committed copy. Exit non-zero on any drift.

Run locally:  python3 .github/scripts/check_drift.py
Fix drift:    make build   (regenerates INDEX.md and the JSON artifacts), then commit.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / ".github" / "scripts"


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        # These raise SystemExit / non-zero on dangling refs or duplicate ids.
        try:
            run([sys.executable, str(SCRIPTS / "build_patterns_json.py"), str(out)])
            run([sys.executable, str(SCRIPTS / "build_graph.py"), str(out)])
            run([sys.executable, str(SCRIPTS / "build_pattern_compositions.py"), str(out)])
        except subprocess.CalledProcessError as e:
            return e.returncode or 1

        # Committed-artifact drift: INDEX.md must equal a fresh render from source.
        regen = out / "INDEX.md"
        run([sys.executable, str(SCRIPTS / "build_index_md.py"), str(regen)])
        committed = ROOT / "INDEX.md"
        if not committed.exists():
            failures.append("INDEX.md is missing")
        elif committed.read_text() != regen.read_text():
            failures.append(
                "INDEX.md is stale — it does not match a rebuild from patterns-src/.\n"
                "  This usually means a pattern was added to a derived artifact (or INDEX.md\n"
                "  directly) instead of a patterns-src/ shard. Run `make build` and commit."
            )

    if failures:
        print("\nDRIFT DETECTED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nno drift: committed catalog matches a clean rebuild from source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
