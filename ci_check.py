#!/usr/bin/env python3
"""
CI/CD integration – runs policy checks on infra-as-code changes before merge.
Usage: python ci_check.py [path/to/resources.json]
Exits with 0 if compliant, 1 if violations found.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import run_evaluation


def main() -> int:
    resources_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "samples" / "resources.json"
    policies_dir = Path(__file__).parent / "policies"

    with open(resources_path) as f:
        resources = json.load(f)

    result = run_evaluation(resources, policies_dir)

    for item in result["report"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['resource_id']}")
        for d in item["details"]:
            print(f"  - {d['policy_id']}: {d['message']}")
        if not item["passed"]:
            print()

    print(f"\nSummary: {result['summary']['passed']}/{result['summary']['total']} resources compliant")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
