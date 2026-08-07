import math

from phyagent.engine import PhysicalReasoningEngine
from phyagent.models import PhysicalEntity, PhysicalProblem, Quantity


def test_frictionless_inclined_plane_energy_balance():
    problem = PhysicalProblem(
        problem_id="p1",
        domain="classical_mechanics",
        goal="speed",
        assumptions={"uniform_gravity"},
        context={"task": "inclined_plane", "entity_id": "block", "gravity": 9.80665},
        entities=[PhysicalEntity("block", "rigid_body", {
            "mass": Quantity(2.0, "kg"),
            "height": Quantity(1.0, "m"),
        })],
    )
    report = PhysicalReasoningEngine().solve(problem)
    assert report.accepted
    assert math.isclose(
        report.computed["terminal_speed"].value,
        math.sqrt(2 * 9.80665),
        rel_tol=1e-9,
    )


def test_projectile_requires_inertial_frame():
    problem = PhysicalProblem(
        problem_id="p2",
        domain="classical_mechanics",
        goal="range",
        assumptions=set(),
        context={"task": "projectile", "entity_id": "projectile", "angle_deg": 45.0},
        entities=[PhysicalEntity("projectile", "point_mass", {
            "initial_speed": Quantity(10.0, "m/s"),
        })],
    )
    report = PhysicalReasoningEngine().solve(problem)
    assert not report.accepted
    assert any(
        finding.check == "assumption:inertial_frame" and not finding.passed
        for finding in report.findings
    )


def test_rejects_dimensionally_invalid_speed():
    problem = PhysicalProblem(
        problem_id="p3",
        domain="classical_mechanics",
        goal="range",
        assumptions={"inertial_frame"},
        context={"task": "projectile", "entity_id": "projectile", "angle_deg": 45.0},
        entities=[PhysicalEntity("projectile", "point_mass", {
            "initial_speed": Quantity(10.0, "kg"),
        })],
    )
    report = PhysicalReasoningEngine().solve(problem)
    assert not report.accepted
    assert any(
        finding.check == "dimension:initial_speed" and not finding.passed
        for finding in report.findings
    )
