# PhyAgent

**PhyAgent** is an early research prototype for *law-governed agentic physical reasoning*. It makes physical assumptions, law applicability, dimensional checks, invariants, and verification findings explicit instead of leaving them inside an opaque language-model trace.

> Status: MVP / research scaffold. This is not a universal physics solver and does not yet use an LLM.

## What the MVP demonstrates

- A structured Physical Reasoning Intermediate Representation (PRIR).
- Explicit provenance states: observed, provided, inferred, assumed, and unknown.
- An executable registry of physical laws and applicability checks.
- Physical proof obligations for assumptions, dimensions, feasibility, and energy balance.
- Deterministic solvers for ideal projectile motion and inclined-plane energy balance.
- Machine-readable reasoning reports with trace, findings, computed quantities, and acceptance status.
- Tests covering valid reasoning, missing assumptions, and dimensional inconsistency.

## Architecture

```text
JSON problem specification
        |
        v
PhysicalProblem / PRIR
        |
        v
Law selection -> applicability checks
        |
        v
Deterministic solver
        |
        v
Physical verifiers -> ReasoningReport
```

The current core is deliberately model-independent. A later agentic layer can use an LLM to compile natural language into `PhysicalProblem`, propose candidate plans, and repair failures, while the deterministic core remains the authority for executable checks.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
phyagent examples/inclined_plane.json
phyagent examples/projectile.json
```

The process exits with code `0` when all error-level proof obligations pass and `2` otherwise.

## Test

```bash
pytest
```

## Current scientific scope

The MVP covers a narrow subset of classical mechanics. It is intended to test the architecture, not to claim general physical reasoning. The next research increments are:

1. Natural-language-to-PRIR compilation with schema-constrained LLM output.
2. Candidate-plan generation and repair using verification feedback.
3. A richer law applicability engine with regimes and approximation boundaries.
4. Counterfactual parameter sweeps and uncertainty propagation.
5. Simulator adapters and a PhysAgentBench evaluation suite.

## Repository layout

```text
src/phyagent/models.py         PRIR data model
src/phyagent/laws.py           executable law registry
src/phyagent/verifiers.py      proof obligations
src/phyagent/engine.py         deterministic reasoning engine
src/phyagent/serialization.py  JSON adapter
src/phyagent/cli.py            command-line interface
examples/                      reproducible problem specifications
tests/                         unit tests
```

## License

No license has been selected yet. Until one is added, normal copyright restrictions apply.
