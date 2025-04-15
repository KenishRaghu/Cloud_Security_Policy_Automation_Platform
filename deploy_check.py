#!/usr/bin/env python3
"""
Deployment gate – validates resources before provisioning (e.g., after Terraform plan).
Usage: python deploy_check.py <resources_json>
Exits with 0 if allowed, 1 if blocked (non-compliant).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine import run_evaluation


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: deploy_check.py <resources.json>", file=sys.stderr)
        return 2

    resources_path = Path(sys.argv[1])
    policies_dir = Path(__file__).parent / "policies"

    with open(resources_path) as f:
        resources = json.load(f)

    result = run_evaluation(resources, policies_dir)

    if result["passed"]:
        print("Deployment approved: all resources compliant")
        return 0

    print("Deployment BLOCKED: policy violations detected", file=sys.stderr)
    for item in result["report"]:
        if not item["passed"]:
            print(f"  {item['resource_id']}:", file=sys.stderr)
            for d in item["details"]:
                if not d["passed"]:
                    print(f"    - {d['policy_id']}: {d['message']}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
