# Cloud Security Policy Automation Platform

A minimal Python-based platform that automates security policy compliance checks and integrates with CI/CD and deployment workflows.

## Quick Start

```bash
pip install -r requirements.txt
python ci_check.py
```

## Project Statements → Implementation

### Statement 1: Scalable security enforcement platform

| Requirement | Implementation |
|-------------|----------------|
| Python-based | `engine.py` – policy loader, evaluator dispatch, result aggregation |
| Cloud technologies | Policy definitions for AWS resource types (S3, EC2, IAM); resource format aligns with IaC outputs |
| Automate compliance checks | `evaluators/` – programmatic checks for tagging, encryption, public access, IAM |
| Scalable | Policy-as-code (JSON) + pluggable evaluators; add policies without changing engine |

**Core flow:** Load policies → Match resources to policies → Run evaluators → Return pass/fail report.

### Statement 2: Cross-functional alignment – requirements → controls

| Stakeholder requirement | Policy ID | Technical control |
|-------------------------|-----------|-------------------|
| Resources must be tagged for cost/audit | POL-001 | `require_tags` – enforce `env`, `team` |
| Storage must not be public | POL-002 | `block_public_access` – S3 block public access |
| Sensitive data encrypted at rest | POL-003 | `require_encryption` – S3 SSE, EBS encryption |
| Least privilege – no broad permissions | POL-004 | `restrict_iam_wildcards` – disallow `*` in IAM actions |

**Product lifecycle enforcement:**

| Lifecycle stage | Script | Purpose |
|-----------------|--------|---------|
| CI/CD (pre-merge) | `ci_check.py` | Fail PR if IaC changes introduce non-compliant resources |
| Deployment (pre-provision) | `deploy_check.py` | Block deployment pipeline if resources violate policies |

## Structure

```
.
├── engine.py              # Policy evaluation engine
├── evaluators/            # Per-control evaluation logic
├── policies/              # Policy-as-code (JSON)
├── samples/resources.json # Example resource configs
├── ci_check.py            # CI integration
├── deploy_check.py        # Deployment gate
├── ARCHITECTURE.md        # Minimal architecture
└── README.md
```

## Usage

**CI (pre-merge):**
```bash
python ci_check.py path/to/planned_resources.json
# Exit 0 = compliant, 1 = violations (fail the pipeline)
```

**Deployment gate:**
```bash
python deploy_check.py path/to/resources.json
# Exit 0 = approve, 1 = block
```

## Adding a Policy

1. Add evaluator in `evaluators/` and register in `evaluators/__init__.py`
2. Create `policies/your_policy.json` with `control`, `resource_types`, `id`
