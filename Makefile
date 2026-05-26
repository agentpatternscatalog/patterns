# Agentic Patterns Catalog — build orchestration.
#
# Source of truth: patterns-src/, compositions-src/, methodologies-src/, examples-src/.
# Everything else (patterns.json, patterns.graph.json, patterns.compositions.json, INDEX.md,
# dist/) is derived. This Makefile is the single entrypoint that builds the derived
# artifacts in dependency order, so the graph can never be built from a stale patterns.json.
#
#   make build    rebuild derived artifacts at repo root, from source
#   make lint     run the catalog linter
#   make drift    fail if committed INDEX.md is stale vs a clean rebuild
#   make check    lint + drift (what CI runs)
#   make publish  build the dist/ bundle for GitHub Pages
#   make clean    remove generated JSON artifacts and dist/

PY ?= python3
SCRIPTS := .github/scripts

.PHONY: build lint drift check publish clean

build:
	$(PY) $(SCRIPTS)/build_patterns_json.py .
	$(PY) $(SCRIPTS)/build_graph.py .
	$(PY) $(SCRIPTS)/build_pattern_compositions.py .
	$(PY) $(SCRIPTS)/build_index_md.py INDEX.md

lint:
	$(PY) $(SCRIPTS)/lint.py

drift:
	$(PY) $(SCRIPTS)/check_drift.py

check: lint drift

publish:
	$(PY) $(SCRIPTS)/build_patterns_json.py dist
	$(PY) $(SCRIPTS)/build_examples_json.py dist
	$(PY) $(SCRIPTS)/render_html.py dist

clean:
	rm -f patterns.json patterns.graph.json patterns.compositions.json
	rm -rf dist
