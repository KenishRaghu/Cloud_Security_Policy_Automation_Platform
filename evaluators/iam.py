"""IAM least privilege – stakeholder requirement: avoid overly broad permissions."""


def evaluate_iam_least_privilege(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    IAM policies must not use wildcard (*) in actions.
    Returns (passed, message).
    """
    statements = resource.get("statement", [])
    for stmt in statements:
        actions = stmt.get("action", []) or stmt.get("Action", [])
        if isinstance(actions, str):
            actions = [actions]
        for act in actions:
            if "*" in str(act):
                return False, f"Wildcard action not allowed: {act}"
    return True, "No wildcard actions"
