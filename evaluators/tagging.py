"""Tagging compliance – stakeholder requirement: resources must be tagged for cost/audit."""

REQUIRED_TAGS = {"env", "team"}


def evaluate_tagging(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    Require resource to have env and team tags.
    Returns (passed, message).
    """
    tags = resource.get("tags") or {}
    missing = REQUIRED_TAGS - set(tags.keys())
    if missing:
        return False, f"Missing required tags: {sorted(missing)}"
    return True, "Tagging compliant"
