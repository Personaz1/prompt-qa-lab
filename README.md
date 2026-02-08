# Prompt QA Lab

Prompt QA Lab is a lightweight toolkit for prompt/agent regression testing.

## Why
Prompt changes break quality silently. This project makes quality drift visible.

## Core idea
- Store prompt test cases as versioned fixtures
- Run deterministic checks (structure/constraints)
- Compare outputs across versions
- Generate a scorecard and diff report

## Planned MVP
- YAML/JSON test case format
- CLI: `pqalab run`
- Diff report (pass/fail + changes)
- Offline/mock mode (no paid API required)

## Who this is for
- AI builders shipping prompts weekly
- solo founders using agent workflows
- teams needing reproducible prompt QA

## Status
Scaffold released. Contributions welcome.



## Working scaffold CLI
```bash
python3 src/pqalab.py run --input examples/cases.json --out report.json
```


## Diff mode (regression gate)
```bash
python3 src/pqalab.py diff --old report-old.json --new report-new.json --fail-on-regression
```
Use exit code in CI to fail builds on quality regressions.
