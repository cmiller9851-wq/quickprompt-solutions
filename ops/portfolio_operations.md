# Automated Portfolio Operations

The portfolio operator runs every six hours and on demand through GitHub Actions. It inventories both configured owners:

- `cmiller9851-wq`: expected 52 repositories.
- `corycardsmem-byte`: expected 1 repository.

The operator is read-only. It verifies repository counts, duplicate full names, default branches, and the required QuickPrompt operations controls. It writes a redacted `ops/reports/portfolio-health.json` artifact and marks the run `attention_required` when an expected repository or control path is missing.

For private-repository visibility beyond the workflow token, configure a repository secret named `PORTFOLIO_GITHUB_TOKEN` with the minimum read-only repository metadata/content scope needed for the two-account inventory. The workflow falls back to the standard GitHub Actions token for public and repository-local checks.

Run locally from the repository root:

```bash
python3 ops/portfolio_ops.py
```

A healthy run reports 53 observed repositories and zero errors. The workflow does not modify repositories, issue payments, change Stripe settings, or alter Workspace data.
