#!/usr/bin/env python3
"""Automated read-only health check for the QuickPrompt GitHub portfolio."""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "ops" / "reports" / "portfolio-health.json"
OWNERS = {"cmiller9851-wq": 52, "corycardsmem-byte": 1}
REQUIRED_QUICKPROMPT_PATHS = [
    "ops/validate_operations.py",
    "ops/metrics/kpi_schema.json",
    "ops/release/production_release_checklist.md",
    ".github/workflows/operations-validation.yml",
]
ANSI = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def command_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update({"GH_PROMPT_DISABLED": "1", "GH_FORCE_TTY": "0", "NO_COLOR": "1"})
    return env


def gh_json(args: list[str]) -> object:
    result = subprocess.run(["gh", *args], cwd=ROOT, env=command_env(), text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(f"gh command failed: {args[0]}")
    output = ANSI.sub("", result.stdout).strip()
    return json.loads(output)


def fetch_repositories(owner: str) -> list[dict[str, object]]:
    payload = gh_json([
        "repo", "list", owner, "--limit", "100",
        "--json", "nameWithOwner,name,isArchived,defaultBranchRef",
    ])
    if not isinstance(payload, list):
        raise RuntimeError(f"unexpected repository response for {owner}")
    return payload


def remote_path_exists(owner: str, repo: str, path: str) -> bool:
    result = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}/contents/{path}", "--jq", ".name"],
        cwd=ROOT, env=command_env(), text=True, capture_output=True, timeout=60,
    )
    return result.returncode == 0 and bool(ANSI.sub("", result.stdout).strip())


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    errors: list[str] = []
    owner_results: dict[str, object] = {}
    all_repos: list[dict[str, object]] = []

    for owner, expected in OWNERS.items():
        try:
            repos = fetch_repositories(owner)
            names = sorted(str(repo.get("name")) for repo in repos)
            missing_branch = sorted(str(repo.get("nameWithOwner")) for repo in repos if not repo.get("defaultBranchRef"))
            owner_results[owner] = {
                "expected": expected,
                "observed": len(repos),
                "names": names,
                "archived": sum(bool(repo.get("isArchived")) for repo in repos),
                "default_branch_missing": missing_branch,
            }
            if len(repos) != expected:
                errors.append(f"{owner}: expected {expected}, observed {len(repos)}")
                owner_results[owner]["count_gap"] = expected - len(repos)
                owner_results[owner]["visibility_gap"] = True
            if missing_branch:
                errors.append(f"{owner}: repository missing default branch")
            all_repos.extend(repos)
        except Exception as exc:  # noqa: BLE001
            owner_results[owner] = {"expected": expected, "error": type(exc).__name__}
            errors.append(f"{owner}: GitHub inventory failed ({type(exc).__name__})")

    full_names = sorted(str(repo.get("nameWithOwner")) for repo in all_repos)
    if len(full_names) != len(set(full_names)):
        errors.append("portfolio: duplicate full repository names")
    if len(full_names) != sum(OWNERS.values()):
        errors.append(f"portfolio: expected {sum(OWNERS.values())}, observed {len(full_names)}")

    quickprompt_paths: dict[str, bool] = {}
    for path in REQUIRED_QUICKPROMPT_PATHS:
        try:
            quickprompt_paths[path] = remote_path_exists("cmiller9851-wq", "quickprompt-solutions", path)
        except Exception:
            quickprompt_paths[path] = False
        if not quickprompt_paths[path]:
            errors.append(f"quickprompt-solutions: missing remote operations path {path}")

    report = {
        "generated_at": now,
        "mode": "read_only",
        "owners": owner_results,
        "portfolio": {
            "expected_total": sum(OWNERS.values()),
            "observed_total": len(full_names),
            "unique_total": len(set(full_names)),
            "repository_names_redacted_to_metadata_only": True,
        },
        "quickprompt_controls": quickprompt_paths,
        "errors": errors,
        "status": "healthy" if not errors else "attention_required",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "expected_total": 53, "observed_total": len(full_names), "errors": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
