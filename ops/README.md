# QuickPrompt Solutions Strategic Operations

This directory is the operating system for the QuickPrompt Solutions platform spine.

- `governance/strategic_operations_charter.md` — mission, decision rights, cadence, and controls.
- `evidence/evidence_control_policy.md` — evidence classes, financial states, redaction, and evidence gates.
- `release/production_release_checklist.md` — release, billing, governance, operations, and rollback gates.
- `metrics/kpi_schema.json` — machine-readable KPI definitions.
- `board/30_day_execution_board.md` — first-month execution board.
- `deals/deal_schema.json` — machine-readable quote-to-cash control record.
- `deals/validate_deal.py` — deterministic transition and evidence-gate validator.
- `deals/examples/` — redacted positive and negative validation fixtures.
- `close_runbook.md` — corporate close, settlement, reconciliation, retention, and decision-rights procedure.

The operating spine is QuickPrompt (commercial), Atlas (billing), Astera (runtime), Aegis (governance), and Settlement Reconciliation Monitor (evidence and finance controls).

Run `python3 validate_operations.py` and `python3 deals/validate_deal.py` before opening a pull request. The deal validator is intentionally dependency-free and treats missing acceptance, version mismatch, failed or disputed payment, duplicate transactions, credit hold, segregation-of-duties conflicts, and reconciliation breaks as no-go conditions.
