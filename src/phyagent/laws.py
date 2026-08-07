from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .models import PhysicalProblem, VerificationFinding

ApplicabilityCheck = Callable[[PhysicalProblem], list[VerificationFinding]]


@dataclass(frozen=True)
class PhysicalLaw:
    law_id: str
    name: str
    domain: str
    assumptions: frozenset[str]
    description: str
    applicability_check: ApplicabilityCheck


def _classical_mechanics(problem: PhysicalProblem) -> list[VerificationFinding]:
    passed = problem.domain == "classical_mechanics"
    return [VerificationFinding(
        check="domain",
        passed=passed,
        message="Classical-mechanics domain confirmed." if passed else "Law requires classical mechanics.",
    )]


def _requires_isolated(problem: PhysicalProblem) -> list[VerificationFinding]:
    findings = _classical_mechanics(problem)
    ok = "isolated_system" in problem.assumptions
    findings.append(VerificationFinding(
        check="assumption:isolated_system",
        passed=ok,
        message="System is declared isolated." if ok else "Momentum conservation requires an isolated system.",
    ))
    return findings


LAW_REGISTRY: dict[str, PhysicalLaw] = {
    "newton_second_law": PhysicalLaw(
        law_id="newton_second_law",
        name="Newton's second law",
        domain="classical_mechanics",
        assumptions=frozenset({"inertial_frame"}),
        description="Net force equals mass times acceleration.",
        applicability_check=_classical_mechanics,
    ),
    "mechanical_energy": PhysicalLaw(
        law_id="mechanical_energy",
        name="Mechanical energy balance",
        domain="classical_mechanics",
        assumptions=frozenset(),
        description="Potential energy is converted into kinetic energy minus dissipative work.",
        applicability_check=_classical_mechanics,
    ),
    "linear_momentum": PhysicalLaw(
        law_id="linear_momentum",
        name="Conservation of linear momentum",
        domain="classical_mechanics",
        assumptions=frozenset({"isolated_system"}),
        description="Total linear momentum is conserved when external impulse is negligible.",
        applicability_check=_requires_isolated,
    ),
}
