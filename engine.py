"""
Policy evaluation engine – core logic for automated security compliance checks.
"""

import json
from pathlib import Path
from typing import Any

from evaluators import EVALUATORS


def load_policies(policies_dir: Path | str) -> list[dict]:
    """Load all JSON policy definitions from a directory."""
    path = Path(policies_dir)
    policies = []
    for f in sorted(path.glob("*.json")):
        with open(f) as fp:
            data = json.load(fp)
            policies.extend(data if isinstance(data, list) else [data])
    return policies


def get_applicable_policies(resource_type: str, policies: list[dict]) -> list[dict]:
    """Return policies that apply to the given resource type."""
    return [
        p
        for p in policies
        if resource_type in (p.get("resource_types") or [])
        or "*" in (p.get("resource_types") or [])
    ]


def evaluate_resource(
    resource: dict, policies: list[dict]
) -> tuple[bool, list[dict]]:
    """
    Evaluate a single resource against applicable policies.
    Returns (all_passed, list of {policy_id, passed, message}).
    """
    resource_type = resource.get("type", "unknown")
    applicable = get_applicable_policies(resource_type, policies)
    results = []
    all_passed = True

    for policy in applicable:
        control = policy.get("control")
        evaluator = EVALUATORS.get(control)
        if not evaluator:
            continue
        passed, message = evaluator(resource, policy)
        results.append(
            {
                "policy_id": policy.get("id"),
                "control": control,
                "passed": passed,
                "message": message,
            }
        )
        if not passed:
            all_passed = False

    return all_passed, results


def evaluate_resources(
    resources: list[dict], policies_dir: Path | str
) -> tuple[bool, list[dict]]:
    """
    Evaluate all resources against loaded policies.
    Returns (overall_passed, report per resource).
    """
    policies = load_policies(policies_dir)
    report = []
    overall = True

    for res in resources:
        rid = res.get("id", "unknown")
        passed, details = evaluate_resource(res, policies)
        report.append({"resource_id": rid, "passed": passed, "details": details})
        if not passed:
            overall = False

    return overall, report


def run_evaluation(resources: list[dict], policies_dir: Path | str) -> dict[str, Any]:
    """
    Main entry point: run full evaluation and return structured result.
    """
    passed, report = evaluate_resources(resources, policies_dir)
    return {
        "passed": passed,
        "report": report,
        "summary": {
            "total": len(report),
            "passed": sum(1 for r in report if r["passed"]),
            "failed": sum(1 for r in report if not r["passed"]),
        },
    }
