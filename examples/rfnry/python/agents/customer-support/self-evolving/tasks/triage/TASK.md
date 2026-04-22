---
name: triage
description: Self-evolving triage with full v5 closed loop. Auto-consolidation + eval-gate enforcement + calibration alerts per org_id scope. Human approval is bypassed by design; eval cases are the source of truth.
reflection:
  mode: self_evolving
  level: 4
  approval:
    required: false
  promotion:
    min_occurrences: 1
    min_quality: 0.6
    eval_gate:
      required: true
      block_regression: true
      regression_tolerance: 0.05
  auto_consolidation:
    trigger: outcomes
    threshold: 5
    cooldown_hours: 1
    only_when_idle: true
  min_eval_cases: 3
---

# Triage (self-evolving)

Multi-tenant: scoped by `org_id` so each organization's learnings stay isolated. The full self-evolving loop runs per-org: auto-consolidation fires after every 5 outcomes for that org, the eval gate blocks any candidate learning that would regress a seeded eval case under that org's scope, and calibration verdicts of `overconfident`/`uncorrelated` halt promotion + emit `SelfEvolvingCalibrationAlertEvent`.

Seed at least 3 eval cases per org via `Agent.extract_eval_case(task="triage", scope={"org_id": "..."}, ...)` before turning the agent loose for that org — until then `Agent.turn` raises `ReflectionError`.
