# Stakeholder Requirements → Security Controls

How cross-functional security requirements are translated into technical policies and enforced.

## Mapping Table

| Stakeholder requirement | Source (e.g. security review, compliance) | Policy ID | Control | Implementation |
|-------------------------|-------------------------------------------|-----------|---------|----------------|
| Resources must be tagged for cost allocation and audit | Finance, audit | POL-001 | require_tags | Enforce `env`, `team` tags on compute/storage |
| Storage must not be publicly accessible | Security, data protection | POL-002 | block_public_access | Require S3 block_public_access |
| Sensitive data must be encrypted at rest | Compliance (e.g. PCI/SOC2) | POL-003 | require_encryption | S3 SSE, EBS encryption |
| Access must follow least privilege | Security, IAM governance | POL-004 | restrict_iam_wildcards | Disallow `*` in IAM action lists |

## Product Lifecycle Enforcement

| Stage | When | Mechanism | Outcome |
|-------|------|-----------|---------|
| CI/CD | Pre-merge (IaC PR) | `ci_check.py` in pipeline | PR blocked if violations |
| Deployment | Pre-provision (plan/apply) | `deploy_check.py` as gate | Deployment blocked if violations |

## Adding New Requirements

1. Capture stakeholder requirement (e.g. "RDS must use encrypted connections").
2. Define policy JSON with `control`, `resource_types`, `severity`.
3. Implement evaluator in `evaluators/` and register in `EVALUATORS`.
4. Policies apply automatically at CI and deployment stages.
