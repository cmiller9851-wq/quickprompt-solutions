#!/usr/bin/env python3
"""Validate the QuickPrompt strategic-operations pack.

This is intentionally dependency-free so it can run locally and in CI.
It validates the presence of operating artifacts, KPI schema shape, required
control language, and accidental secret-like material in the operations pack.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = {
    "README.md",
    "governance/strategic_operations_charter.md",
    "evidence/evidence_control_policy.md",
    "release/production_release_checklist.md",
    "metrics/kpi_schema.json",
    "board/30_day_execution_board.md",
    "deals/deal_schema.json",
    "deals/validate_deal.py",
    "close_runbook.md",
}
SECRET_PATTERNS = [
    re.compile(r"sk_(?:live|test)_[A-Za-z0-9]+"),
    re.compile(r"whsec_[A-Za-z0-9]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
REQUIRED_TERMS = {
    "governance/strategic_operations_charter.md": ["decision rights", "operating cadence", "non-negotiable controls"],
    "evidence/evidence_control_policy.md": ["source_class", "reconciled", "redaction"],
    "release/production_release_checklist.md": ["rollback", "webhook", "no-go"],
    "board/30_day_execution_board.md": ["week 1", "week 2", "week 3", "week 4"],
    "close_runbook.md": ["three-way reconciliation", "segregation-of-duties", "Closed Won"],
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    missing = sorted(str(p) for p in REQUIRED_FILES if not (ROOT / p).is_file())
    if missing:
        fail("missing required files: " + ", ".join(missing))

    for relative, terms in REQUIRED_TERMS.items():
        text = (ROOT / relative).read_text(encoding="utf-8").lower()
        missing_terms = [term for term in terms if term.lower() not in text]
        if missing_terms:
            fail(f"{relative} missing required terms: {', '.join(missing_terms)}")

    try:
        schema = json.loads((ROOT / "metrics/kpi_schema.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid KPI schema: {exc}")
    metrics = schema.get("metrics")
    if schema.get("version") != "1.0" or not isinstance(metrics, list) or len(metrics) < 10:
        fail("KPI schema must be version 1.0 with at least 10 metrics")
    ids = [item.get("id") for item in metrics]
    if any(not item or not item.get("definition") or not item.get("source") for item in metrics):
        fail("every KPI must have id, definition, and source")
    if len(ids) != len(set(ids)):
        fail("KPI IDs must be unique")

    try:
        deal_schema = json.loads((ROOT / "deals/deal_schema.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid deal schema: {exc}")
    required = set(deal_schema.get("required", []))
    expected = {"deal_id", "environment", "owner", "customer", "quotes", "approvals", "acceptance", "billing", "settlement", "reconciliation", "exceptions", "audit_events"}
    if not expected.issubset(required):
        fail("deal schema is missing required quote-to-cash fields")

    import subprocess
    deal_validator = ROOT / "deals/validate_deal.py"
    result = subprocess.run([sys.executable, str(deal_validator)], capture_output=True, text=True)
    if result.returncode:
        fail("deal fixtures failed validation: " + result.stdout + result.stderr)

    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"secret-like material detected in {path.relative_to(ROOT)}")

    print(f"OPS_VALID: files={scanned} metrics={len(metrics)} deal_fixtures=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
