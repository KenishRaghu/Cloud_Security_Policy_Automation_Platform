"""Azure RBAC least privilege – stakeholder requirement: avoid overly broad permissions."""


def evaluate_iam_least_privilege(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    Azure role definitions must not use wildcard (*) in actions.
    Returns (passed, message).
    """
    permissions = resource.get("permissions", [])
    for perm in permissions:
        actions = perm.get("actions", []) or perm.get("Actions", [])
        if isinstance(actions, str):
            actions = [actions]
        for act in actions:
            if "*" in str(act):
                return False, f"Wildcard action not allowed: {act}"
    return True, "No wildcard actions"
