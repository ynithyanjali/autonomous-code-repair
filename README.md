# Autonomous Code Repair | Starter Prototype

[![Code Repair Tests](https://github.com/ynithyanjali/autonomous-code-repair/actions/workflows/tests.yml/badge.svg)](https://github.com/ynithyanjali/autonomous-code-repair/actions/workflows/tests.yml)

A small experiment in fixing bugs automatically, using tests to check the fix.

I wanted to see how far a simple, no-frills approach could go. The program finds an operator mistake in a small Python project (like - where + should be), tries swapping it, and keeps the change only if the tests pass.

This is a starting point, not an “AI engineer.” There’s no LLM, LangGraph, Docker, or multi-agent setup yet. The candidate generator is plain, deterministic code.

What it does today
Parses Python code and tries one-operator changes as repair candidates
Runs the tests before and after each candidate, using a temporary copy of the demo project
Accepts a fix only if the sample tests pass
Saves a diff, the fixed file, and a JSON report
Runs its own tests on GitHub Actions
Try it

You need Python 3.10+. No other packages.

bash
python main.py

On Windows, use py main.py.

You should see something like:

text
=== AUTONOMOUS CODE REPAIR: STARTER PROTOTYPE ===
Baseline passed: False
Candidates evaluated: 1
Verified patch found: True
Change: {'line': 6, 'from': 'Sub', 'to': 'Add'}
Saved: artifacts/proposed_fix.patch and artifacts/report.json

To run the project’s own tests:

bash
python -m unittest discover -s tests -v

The sample calculator.py has a bug on purpose, so the baseline tests are supposed to fail. The repair only counts as a success if a candidate makes them pass.

What’s where
text
repair_agent/             candidate generator + validation pipeline
sample_project/           a deliberately buggy calculator + its tests
tests/                    tests for the repair tool itself
.github/workflows/        CI
docs/architecture.md      design notes and limitations
main.py                   run this

Limitations
I’ve only tested it on one known, synthetic bug, so it says nothing about how it would do on real code.
Passing tests is good evidence, but it doesn’t prove a patch is correct.
It uses ast.unparse, which can change formatting and comments, so look over any patch before using it.
Tests run as plain local subprocesses, not in a sandbox. Don’t run this on code you don’t trust.
Your original source is never touched. Output goes to a separate folder.
What I’d like to do next
Run tests inside Docker with resource limits
Try a local LLM for generating candidates and compare it to this baseline
Add planning, review, and retries with clear logs
Benchmark on a range of licensed problems, tracking success rate, runtime, and how often it “fixes” things wrongly

More detail in docs/architecture.md.


