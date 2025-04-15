"""Storage security – stakeholder requirements: no public access, encryption at rest."""


def evaluate_storage_public_access(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    Azure Storage Account must block public blob access.
    allowBlobPublicAccess=false means blocked.
    Returns (passed, message).
    """
    allow_public = resource.get("allowBlobPublicAccess", True)
    if allow_public:
        return False, "Public blob access must be blocked (allowBlobPublicAccess=false)"
    return True, "Public blob access blocked"


def evaluate_encryption(resource: dict, policy: dict) -> tuple[bool, str]:
    """
    Azure Storage and VM disks must use encryption at rest.
    Returns (passed, message).
    """
    encrypted = (
        resource.get("encryptionAtRest")
        or resource.get("encryption", {}).get("services", {}).get("blob", {}).get("enabled")
        or resource.get("requireInfrastructureEncryption")
    )
    if not encrypted:
        return False, "Encryption at rest required"
    return True, "Encryption enabled"
