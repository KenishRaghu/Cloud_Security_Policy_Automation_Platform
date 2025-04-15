# Cloud Security Policy Automation Platform – Minimal Architecture

## Overview

A lightweight policy-as-code platform that evaluates cloud resource configurations against security policies and integrates into CI/CD and deployment workflows.

## Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Policy Automation Platform                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌─────────────────────┐    ┌─────────────────┐ │
│  │   Policies   │───▶│   Policy Engine     │◀───│  Resource       │ │
│  │  (JSON)      │    │   (engine.py)       │    │  Configs        │ │
│  └──────────────┘    └──────────┬──────────┘    └─────────────────┘ │
│                                 │                                    │
│                                 ▼                                    │
│                    ┌─────────────────────┐                           │
│                    │  Evaluation Result   │                           │
│                    │  (pass/fail, report) │                           │
│                    └──────────┬──────────┘                           │
│                               │                                      │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
┌───────────────────┐                         ┌───────────────────┐
│   CI/CD Stage     │                         │ Deployment Stage  │
│   (pre-merge)     │                         │ (pre-provision)   │
│   ci_check.py     │                         │ deploy_check.py   │
└───────────────────┘                         └───────────────────┘
```

## Data Flow

1. **Policy definitions** (JSON) capture stakeholder security requirements as declarative rules.
2. **Resource configs** (JSON/dict) represent planned or existing cloud resources (e.g., from IaC output).
3. **Policy engine** loads policies, selects evaluators, and runs checks on each resource.
4. **Results** are returned as structured pass/fail with remediation guidance.
5. **Integrations** run the engine at CI (validate before merge) and deployment (validate before provision).

## Lifecycle Touchpoints

| Stage       | Trigger               | Purpose                              |
|-------------|-----------------------|--------------------------------------|
| CI/CD       | PR / merge request    | Block non-compliant IaC from merging |
| Deployment  | Pre-provision / plan  | Block non-compliant resources from deploy |
