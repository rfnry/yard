---
name: stock-check
description: SKU lookup with full self-evolving loop. Auto-consolidation + eval-gate enforcement + calibration alerts. Human approval is bypassed by design.
refining:
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

# Stock check (self-evolving)

Self-evolving demo tier. Mirrors `task-reasoning` for inputs but enables the full v5 closed loop:

- **mode: self_evolving** — engine validator enforces `level=4` + `approval.required=false` + `eval_gate.required=true` + `auto_consolidation` present.
- **eval_gate.required: true** — every promotion is replayed against a trial snapshot and must not regress any seeded eval case in `data/{scope}/tasks/stock-check/eval/cases/`.
- **min_eval_cases: 3** — `Agent.turn` raises `RefiningError` until at least 3 eval cases are extracted (use `Agent.extract_eval_case` from low-quality outcomes).
- **auto_consolidation.threshold: 5** — auto-consolidates after every 5 outcomes, with a 1-hour cooldown.

Calibration verdicts of `overconfident` or `uncorrelated` automatically suppress promotion (existing v3 behavior) and additionally fire `SelfEvolvingCalibrationAlertEvent` so the host can notice. Promoted lessons flow straight into `learned/_index.md` and the next boot bundle.

To enable: seed at least 3 eval cases via `Agent.extract_eval_case(...)`, then drive normal turns. The first successful turn fires `SelfEvolvingActivatedEvent` carrying the live case count and current calibration verdict.
