# Autonomous Code Repair | Starter Prototype

[![Code Repair Tests](https://github.com/ynithyanjali/autonomous-code-repair/actions/workflows/tests.yml/badge.svg)](https://github.com/ynithyanjali/autonomous-code-repair/actions/workflows/tests.yml)

A small, reproducible **test-guided program repair prototype** that locates a simple operator error in a synthetic Python project, proposes candidate changes, and validates them against automated tests.

> **Status:** Working starter demonstration, not a production autonomous AI engineer. The candidate generator is deterministic and does not yet use an LLM, LangGraph, Docker, or multi-agent orchestration.

## What works now

- Parses Python code and generates single-operator repair candidates.
- Runs baseline and candidate unit tests using a temporary copy of the bundled demo.
- Accepts a repair only when the sample test suite passes.
- Exports a unified diff, proposed fixed file, and machine-readable JSON report.
- Runs its own tests through GitHub Actions.

## Quick start

Requires **Python 3.10+**. No third-party packages are needed.

```bash
python main.py
```

On Windows you can use `py main.py` instead of `python main.py`.

Expected output looks like:

```text
=== AUTONOMOUS CODE REPAIR: STARTER PROTOTYPE ===
Baseline passed: False
Candidates evaluated: 1
Verified patch found: True
Change: {'line': 6, 'from': 'Sub', 'to': 'Add'}
Saved: artifacts/proposed_fix.patch and artifacts/report.json
```

To run the prototype's own tests:

```bash
python -m unittest discover -s tests -v
```

**Note:** The sample `calculator.py` intentionally contains a bug, so its baseline tests are supposed to fail. The repair workflow succeeds only if a candidate passes them.

## Project layout

```text
repair_agent/             mutation generator + validation pipeline
sample_project/           deliberately buggy calculator + tests
tests/                    tests for the repair system
.github/workflows/        automated CI checks
docs/architecture.md      architecture and limitations
main.py                   runnable demonstration
```

## Evaluation and limitations

This demo checks **one known synthetic bug**, not thousands of real-world issues. A passing test suite is useful evidence, but not proof that a patch is universally correct. The patch engine uses `ast.unparse`, which may alter formatting/comments; inspect any generated patch before using it.

The sample tests execute as local subprocesses, **not** in a sandbox; never run this against code you do not trust. Source code remains unmodified, and artifacts are written separately.

## Roadmap (not implemented)

1. Isolate test execution in Docker with resource limits.
2. Generate patch candidates with a local LLM and compare against the deterministic baseline.
3. Add agent-style planning, review, and retries with transparent logging.
4. Benchmark on diverse, licensed test problems with success rate, runtime, and false-fix rate.

See [docs/architecture.md](docs/architecture.md) for a more detailed overview.
