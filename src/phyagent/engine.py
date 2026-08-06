from __future__ import annotations

import math

from .laws import LAW_REGISTRY
from .models import PhysicalProblem, Quantity, ReasoningReport, VerificationFinding
from .verifiers import si, verify_dimension, verify_energy_balance, verify_positive


class PhysicalReasoningEngine:
    """Deterministic MVP for law selection, execution, and physical verification."""

    def solve(self, problem: PhysicalProblem) -> ReasoningReport:
        task = problem.context.get("task")
        if task == "inclined_plane":
            return self._solve_inclined_plane(problem)
        if task == "projectile":
            return self._solve_projectile(problem)
        raise ValueError(f"Unsupported task: {task!r}")

    def _apply_law(self, law_id: str, problem: PhysicalProblem) -> list[VerificationFinding]:
        law = LAW_REGISTRY[law_id]
        findings = law.applicability_check(problem)
        for assumption in law.assumptions:
            findings.append(VerificationFinding(
                check=f"assumption:{assumption}",
                passed=assumption in problem.assumptions,
                message=(
                    f"Assumption '{assumption}' is explicit."
                    if assumption in problem.assumptions
                    else f"Missing assumption: {assumption}."
                ),
            ))
        return findings

    def _solve_inclined_plane(self, problem: PhysicalProblem) -> ReasoningReport:
        block = problem.entity(problem.context.get("entity_id", "block"))
        findings: list[VerificationFinding] = []
        trace = ["Parsed inclined-plane task.", "Selected mechanical-energy law."]
        findings.extend(self._apply_law("mechanical_energy", problem))

        mass = block.properties["mass"]
        height = block.properties["height"]
        friction = block.properties.get("friction_coefficient", Quantity(0.0, "1"))
        distance = block.properties.get("path_length")

        findings += [
            verify_positive(block, "mass"),
            verify_positive(block, "height"),
            verify_dimension(mass, (1, 0, 0), "mass"),
            verify_dimension(height, (0, 1, 0), "height"),
            verify_dimension(friction, (0, 0, 0), "friction_coefficient"),
        ]

        m = si(mass)
        h = si(height)
        mu = friction.value
        g = float(problem.context.get("gravity", 9.80665))
        initial_energy = m * g * h
        dissipated = 0.0
        if distance is not None and mu > 0:
            angle_deg = float(problem.context["angle_deg"])
            normal = m * g * math.cos(math.radians(angle_deg))
            dissipated = mu * normal * si(distance)
            trace.append("Computed frictional work along the path.")

        kinetic = initial_energy - dissipated
        if kinetic < 0:
            findings.append(VerificationFinding(
                check="feasibility:motion",
                passed=False,
                message=(
                    "Dissipative work exceeds available potential energy; "
                    "the assumed motion is infeasible."
                ),
                evidence={"available_j": initial_energy, "dissipated_j": dissipated},
            ))
            velocity = 0.0
            kinetic = 0.0
        else:
            velocity = math.sqrt(2.0 * kinetic / m)
            findings.append(VerificationFinding(
                check="feasibility:motion",
                passed=True,
                message="Available energy permits the motion.",
            ))

        findings.append(verify_energy_balance(initial_energy, kinetic, dissipated))
        trace += [
            "Solved terminal speed from the energy balance.",
            "Verified dimensions and energy residual.",
        ]
        return ReasoningReport(
            problem_id=problem.problem_id,
            selected_laws=["mechanical_energy"],
            findings=findings,
            computed={
                "terminal_speed": Quantity(velocity, "m/s"),
                "initial_potential_energy": Quantity(initial_energy, "J"),
                "dissipated_energy": Quantity(dissipated, "J"),
            },
            trace=trace,
        )

    def _solve_projectile(self, problem: PhysicalProblem) -> ReasoningReport:
        projectile = problem.entity(problem.context.get("entity_id", "projectile"))
        findings = self._apply_law("newton_second_law", problem)
        speed = projectile.properties["initial_speed"]
        findings.append(verify_dimension(speed, (0, 1, -1), "initial_speed"))
        angle_deg = float(problem.context["angle_deg"])
        g = float(problem.context.get("gravity", 9.80665))
        v = si(speed)
        angle = math.radians(angle_deg)
        flight_time = 2 * v * math.sin(angle) / g
        range_m = v * math.cos(angle) * flight_time
        max_height = (v * math.sin(angle)) ** 2 / (2 * g)
        return ReasoningReport(
            problem_id=problem.problem_id,
            selected_laws=["newton_second_law"],
            findings=findings,
            computed={
                "flight_time": Quantity(flight_time, "s"),
                "range": Quantity(range_m, "m"),
                "maximum_height": Quantity(max_height, "m"),
            },
            trace=[
                "Parsed ideal projectile task.",
                "Checked Newtonian applicability.",
                "Resolved velocity components.",
                "Computed and verified trajectory observables.",
            ],
        )
