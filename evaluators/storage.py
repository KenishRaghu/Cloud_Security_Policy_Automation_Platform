"""Storage security – stakeholder requirements: no public access, encryption at rest."""


def evaluate_storage_public_access(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    S3/storage must block public access.
    Returns (passed, message).
    """
    block_public = resource.get("block_public_access", True)
    if not block_public:
        return False, "Public access must be blocked"
    return True, "Public access blocked"


def evaluate_encryption(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    Storage and compute volumes must use encryption at rest.
    Returns (passed, message).
    """
    encrypted = resource.get("encrypted", resource.get("server_side_encryption"))
    if not encrypted:
        return False, "Encryption at rest required"
    return True, "Encryption enabled"
