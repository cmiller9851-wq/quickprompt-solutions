#!/usr/bin/env python3
"""Run QuickPrompt operations without GitHub Actions.

This is a local, read-only control plane. It deliberately fails closed when
portfolio visibility is incomplete and writes a redacted execution receipt.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "ops" / "reports"
RECEIPT = REPORT_DIR / "independent-operations-receipt.json"


def run(command: list[str]) -> dict[str, object]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, env={**os.environ, "GH_PROMPT_DISABLED": "1", "GH_FORCE_TTY": "0", "NO_COLOR": "1"})
    return {"command": " ".join(command), "returncode": proc.returncode, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-2000:]}


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    results = [
        run([sys.executable, "ops/validate_operations.py"]),
        run([sys.executable, "ops/portfolio_ops.py"]),
    ]
    finished = datetime.now(timezone.utc).isoformat()
    payload = {
        "started_at": started,
        "finished_at": finished,
        "mode": "independent_local_read_only",
        "git_sha": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip(),
        "results": results,
        "status": "healthy" if all(item["returncode"] == 0 for item in results) else "attention_required",
        "control_rule": "portfolio visibility and operations validation must pass; no financial writes are performed",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["receipt_sha256"] = hashlib.sha256(canonical).hexdigest()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "receipt": str(RECEIPT), "receipt_sha256": payload["receipt_sha256"]}))
    return 0 if payload["status"] == "healthy" else 1


if __name__ == "__main__":
    raise SystemExit(main())
