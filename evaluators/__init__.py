"""Policy evaluators – one per security control type."""

from .tagging import evaluate_tagging
from .storage import evaluate_storage_public_access, evaluate_encryption
from .iam import evaluate_iam_least_privilege

EVALUATORS = {
    "require_tags": evaluate_tagging,
    "block_public_access": evaluate_storage_public_access,
    "require_encryption": evaluate_encryption,
    "restrict_iam_wildcards": evaluate_iam_least_privilege,
}
