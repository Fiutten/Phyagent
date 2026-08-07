from __future__ import annotations

import argparse
import json

from .engine import PhysicalReasoningEngine
from .serialization import load_problem, report_to_dict


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PhyAgent deterministic reasoning MVP.")
    parser.add_argument("problem", help="Path to a JSON physical-problem specification")
    args = parser.parse_args()
    report = PhysicalReasoningEngine().solve(load_problem(args.problem))
    print(json.dumps(report_to_dict(report), indent=2))
    raise SystemExit(0 if report.accepted else 2)


if __name__ == "__main__":
    main()
