from __future__ import annotations

import math

from .models import PhysicalEntity, Quantity, VerificationFinding
from .units import dimension, to_si


def verify_positive(entity: PhysicalEntity, property_name: str) -> VerificationFinding:
    quantity = entity.properties[property_name]
    return VerificationFinding(
        check=f"positive:{entity.entity_id}.{property_name}",
        passed=quantity.value > 0,
        message=f"{property_name} is positive." if quantity.value > 0 else f"{property_name} must be positive.",
        evidence={"value": quantity.value, "unit": quantity.unit},
    )


def verify_dimension(quantity: Quantity, expected: tuple[int, int, int], label: str) -> VerificationFinding:
    actual = dimension(quantity.unit)
    return VerificationFinding(
        check=f"dimension:{label}",
        passed=actual == expected,
        message=f"{label} has the expected physical dimension." if actual == expected else f"{label} has dimension {actual}, expected {expected}.",
        evidence={"unit": quantity.unit},
    )


def verify_energy_balance(
    initial_energy_j: float,
    final_energy_j: float,
    dissipated_j: float = 0.0,
    tolerance: float = 1e-6,
) -> VerificationFinding:
    residual = initial_energy_j - final_energy_j - dissipated_j
    scale = max(abs(initial_energy_j), 1.0)
    passed = math.isclose(residual, 0.0, rel_tol=tolerance, abs_tol=tolerance * scale)
    return VerificationFinding(
        check="invariant:energy_balance",
        passed=passed,
        message="Energy balance closes within tolerance." if passed else "Energy balance is violated.",
        evidence={"residual_j": residual, "tolerance": tolerance},
    )


def si(quantity: Quantity) -> float:
    return to_si(quantity.value, quantity.unit)
