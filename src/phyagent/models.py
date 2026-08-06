from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EvidenceStatus(StrEnum):
    OBSERVED = "observed"
    PROVIDED = "provided"
    INFERRED = "inferred"
    ASSUMED = "assumed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str
    status: EvidenceStatus = EvidenceStatus.PROVIDED


@dataclass
class PhysicalEntity:
    entity_id: str
    entity_type: str
    properties: dict[str, Quantity] = field(default_factory=dict)


@dataclass
class PhysicalProblem:
    problem_id: str
    domain: str
    goal: str
    entities: list[PhysicalEntity]
    assumptions: set[str] = field(default_factory=set)
    context: dict[str, Any] = field(default_factory=dict)

    def entity(self, entity_id: str) -> PhysicalEntity:
        for item in self.entities:
            if item.entity_id == entity_id:
                return item
        raise KeyError(f"Unknown entity: {entity_id}")


@dataclass(frozen=True)
class VerificationFinding:
    check: str
    passed: bool
    message: str
    severity: str = "error"
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningReport:
    problem_id: str
    selected_laws: list[str]
    findings: list[VerificationFinding]
    computed: dict[str, Quantity]
    trace: list[str]

    @property
    def accepted(self) -> bool:
        return all(f.passed or f.severity != "error" for f in self.findings)
