#!/usr/bin/env python3
"""Deterministic quote-to-cash state and evidence-gate validator."""
from __future__ import annotations

import json
import sys
from pathlib import Path

STATES = {
    "Draft", "Qualified", "Approval Pending", "Approved to Send", "Sent",
    "Accepted/Signed", "Invoice Issued", "Payment Confirmed/Settled", "Closed Won",
    "Rejected", "Expired", "Canceled", "Void", "Failed", "Disputed", "Refunded",
    "Uncollectible", "Reconciliation Exception",
}
ALLOWED = {
    "Draft": {"Qualified", "Rejected", "Canceled"},
    "Qualified": {"Approval Pending", "Rejected", "Canceled"},
    "Approval Pending": {"Approved to Send", "Rejected", "Canceled"},
    "Approved to Send": {"Sent", "Expired", "Canceled"},
    "Sent": {"Accepted/Signed", "Rejected", "Expired", "Void", "Canceled"},
    "Accepted/Signed": {"Invoice Issued", "Canceled", "Void"},
    "Invoice Issued": {"Payment Confirmed/Settled", "Failed", "Uncollectible", "Canceled", "Reconciliation Exception"},
    "Payment Confirmed/Settled": {"Closed Won", "Disputed", "Refunded", "Reconciliation Exception"},
    "Closed Won": {"Disputed", "Refunded", "Reconciliation Exception"},
    "Rejected": set(), "Expired": set(), "Canceled": set(), "Void": set(),
    "Failed": {"Invoice Issued", "Canceled", "Reconciliation Exception"},
    "Disputed": {"Refunded", "Closed Won", "Reconciliation Exception"},
    "Refunded": {"Reconciliation Exception"}, "Uncollectible": {"Reconciliation Exception"},
    "Reconciliation Exception": {"Invoice Issued", "Payment Confirmed/Settled", "Closed Won", "Refunded", "Canceled"},
}


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    for key in ("deal_id", "environment", "owner", "customer", "quotes", "approvals", "acceptance", "billing", "settlement", "reconciliation", "audit_events"):
        if key not in record:
            errors.append(f"missing top-level field: {key}")
    if errors:
        return errors

    history = record.get("state_history", [])
    if not history:
        errors.append("state_history is required for transition validation")
    else:
        for event in history:
            source, target = event.get("from_state"), event.get("to_state")
            if source not in STATES or target not in STATES:
                errors.append(f"unknown state transition: {source} -> {target}")
            elif target not in ALLOWED[source]:
                errors.append(f"illegal state transition: {source} -> {target}")
        if history[0].get("from_state") != "Draft":
            errors.append("state history must begin at Draft")

    quotes = record.get("quotes", [])
    approvals = record.get("approvals", [])
    acceptance = record.get("acceptance", {})
    latest = max(quotes, key=lambda q: q.get("quote_version", 0), default={})
    matching_approval = [a for a in approvals if a.get("decision") == "approved" and a.get("approved_quote_version") == latest.get("quote_version") and a.get("approved_content_hash") == latest.get("content_hash")]
    if any(e.get("to_state") in {"Approved to Send", "Sent", "Accepted/Signed", "Invoice Issued", "Payment Confirmed/Settled", "Closed Won"} for e in history) and not matching_approval:
        errors.append("no approval matching the operative quote version and content hash")

    if any(e.get("to_state") in {"Accepted/Signed", "Invoice Issued", "Payment Confirmed/Settled", "Closed Won"} for e in history):
        if acceptance.get("status") != "accepted":
            errors.append("customer acceptance is required before invoicing")
        if acceptance.get("accepted_quote_version") != latest.get("quote_version") or acceptance.get("accepted_content_hash") != latest.get("content_hash"):
            errors.append("customer acceptance does not match the operative quote version and content hash")
        if not acceptance.get("signer_authority_evidence") or not acceptance.get("evidence_uri"):
            errors.append("acceptance authority and evidence URI are required")

    billing = record.get("billing", {})
    if any(e.get("to_state") in {"Invoice Issued", "Payment Confirmed/Settled", "Closed Won"} for e in history) and billing.get("invoice_state") not in {"issued", "paid"}:
        errors.append("invoice state must be issued or paid after Invoice Issued")
    if any(e.get("to_state") in {"Payment Confirmed/Settled", "Closed Won"} for e in history) and billing.get("payment_state") != "succeeded":
        errors.append("payment state must be succeeded before settlement")

    settlement = record.get("settlement", {})
    reconciliation = record.get("reconciliation", {})
    if any(e.get("to_state") == "Closed Won" for e in history):
        if settlement.get("state") not in {"processor_confirmed", "bank_settled"}:
            errors.append("settlement evidence is required before Closed Won")
        if reconciliation.get("state") not in {"matched", "cleared"}:
            errors.append("reconciliation must be matched or cleared before Closed Won")
        if reconciliation.get("duplicate_check") != "clear":
            errors.append("duplicate check must be clear before Closed Won")

    owner_id = record.get("owner", {}).get("user_id")
    approval_ids = {a.get("approver_id") for a in approvals if a.get("decision") == "approved"}
    if owner_id and owner_id in approval_ids:
        errors.append("segregation-of-duties conflict: owner also approved the deal")
    if any(e.get("to_state") in {"Payment Confirmed/Settled", "Closed Won"} for e in history) and not record.get("reconciliation", {}).get("reviewer_id"):
        errors.append("independent reconciliation reviewer is required")

    audit_ids = [e.get("event_id") for e in record.get("audit_events", [])]
    if not audit_ids or len(audit_ids) != len(set(audit_ids)):
        errors.append("audit event IDs must be present and unique")
    return errors


def main() -> int:
    paths = [Path(arg) for arg in sys.argv[1:]]
    if not paths:
        paths = sorted(Path(__file__).parent.glob("examples/*.json"))
    failures = 0
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        errors = validate(record)
        expected = record.get("_expected", "valid")
        passed = (not errors) if expected == "valid" else bool(errors)
        print(f"DEAL_{'VALID' if passed else 'INVALID'}: {path.name}")
        if not passed:
            failures += 1
            for error in errors:
                print(f"  - {error}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
