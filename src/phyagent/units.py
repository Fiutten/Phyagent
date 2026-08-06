from __future__ import annotations

from dataclasses import dataclass


Dimension = tuple[int, int, int]  # mass, length, time


@dataclass(frozen=True)
class UnitDefinition:
    symbol: str
    dimension: Dimension
    to_si: float = 1.0


UNITS: dict[str, UnitDefinition] = {
    "1": UnitDefinition("1", (0, 0, 0)),
    "kg": UnitDefinition("kg", (1, 0, 0)),
    "g": UnitDefinition("g", (1, 0, 0), 1e-3),
    "m": UnitDefinition("m", (0, 1, 0)),
    "cm": UnitDefinition("cm", (0, 1, 0), 1e-2),
    "s": UnitDefinition("s", (0, 0, 1)),
    "m/s": UnitDefinition("m/s", (0, 1, -1)),
    "m/s^2": UnitDefinition("m/s^2", (0, 1, -2)),
    "N": UnitDefinition("N", (1, 1, -2)),
    "J": UnitDefinition("J", (1, 2, -2)),
    "kg*m/s": UnitDefinition("kg*m/s", (1, 1, -1)),
    "deg": UnitDefinition("deg", (0, 0, 0)),
}


def dimension(unit: str) -> Dimension:
    try:
        return UNITS[unit].dimension
    except KeyError as exc:
        raise ValueError(f"Unsupported unit: {unit}") from exc


def to_si(value: float, unit: str) -> float:
    try:
        return value * UNITS[unit].to_si
    except KeyError as exc:
        raise ValueError(f"Unsupported unit: {unit}") from exc


def compatible(left: str, right: str) -> bool:
    return dimension(left) == dimension(right)
