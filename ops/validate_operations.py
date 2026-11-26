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

    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"secret-like material detected in {path.relative_to(ROOT)}")

    print(f"OPS_VALID: files={scanned} metrics={len(metrics)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
