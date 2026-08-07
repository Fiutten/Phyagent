from __future__ import annotations

import json
from pathlib import Path

from .models import EvidenceStatus, PhysicalEntity, PhysicalProblem, Quantity, ReasoningReport


def load_problem(path: str | Path) -> PhysicalProblem:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    entities = []
    for item in raw["entities"]:
        properties = {
            key: Quantity(
                value=float(value["value"]),
                unit=value["unit"],
                status=EvidenceStatus(value.get("status", "provided")),
            )
            for key, value in item.get("properties", {}).items()
        }
        entities.append(PhysicalEntity(item["entity_id"], item["entity_type"], properties))
    return PhysicalProblem(
        problem_id=raw["problem_id"],
        domain=raw["domain"],
        goal=raw["goal"],
        entities=entities,
        assumptions=set(raw.get("assumptions", [])),
        context=raw.get("context", {}),
    )


def report_to_dict(report: ReasoningReport) -> dict:
    return {
        "problem_id": report.problem_id,
        "accepted": report.accepted,
        "selected_laws": report.selected_laws,
        "computed": {
            key: {"value": value.value, "unit": value.unit}
            for key, value in report.computed.items()
        },
        "findings": [
            {
                "check": finding.check,
                "passed": finding.passed,
                "severity": finding.severity,
                "message": finding.message,
                "evidence": finding.evidence,
            }
            for finding in report.findings
        ],
        "trace": report.trace,
    }
