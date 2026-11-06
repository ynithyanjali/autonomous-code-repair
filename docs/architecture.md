# Architecture and safety notes

The demonstration runs **only the bundled synthetic calculator example**. It performs:

1. Baseline validation: run Python's `unittest` suite in a temporary copy.
2. Diagnosis (limited): inspect Python's abstract syntax tree for mutation sites.
3. Candidate generation: propose one small operator change at a time.
4. Validation: re-run the sample tests on each candidate.
5. Reporting: save a diff, candidate code, and structured JSON report if tests pass.

No original input files are overwritten. Tests run as ordinary local Python subprocesses,
not in a security sandbox. **Do not use this prototype on untrusted code.**

This is a demonstration of *test-guided program repair*. The candidate generator is
rules-based. It does not use LLM inference, LangGraph, FastAPI, Docker, multi-agent
collaboration, or external code hosting integrations.

## Future extensions

- Container-isolated validation with time and resource limits.
- A local language model to propose candidate patches.
- Function-level patches that preserve comments and formatting.
- Differential tests on multiple public, licensed benchmark cases.
- An API and observable metrics, added only after reliable evaluations.
