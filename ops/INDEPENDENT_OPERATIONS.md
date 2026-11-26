# Independent Operations Lane

QuickPrompt portfolio health does not depend on GitHub-hosted Actions. The canonical local operator is `ops/independent_ops.py`. It runs the dependency-free operations validator and the read-only 53-repository portfolio operator, then writes a redacted execution receipt to `ops/reports/independent-operations-receipt.json`.

Run it from any controlled host with the GitHub CLI authenticated to both portfolio owners:

```bash
gh auth status
python3 ops/independent_ops.py
```

The operator uses the active `gh` credential or `GH_TOKEN`; it never stores a token in the repository and never prints one. The credential must be able to read 52 repositories under `cmiller9851-wq` and 1 repository under `corycardsmem-byte`. If fewer than 53 are visible, the run returns `attention_required` and does not claim portfolio health.

## Durable scheduling

On a Linux host that belongs to the owner, use a user-level systemd timer or cron. The host is the execution authority; GitHub Actions is only an optional duplicate observer.

Example cron entry, adjusted to the checked-out path and authenticated user:

```cron
17 */6 * * * cd /srv/quickprompt-solutions && /usr/bin/python3 ops/independent_ops.py >> /var/log/quickprompt-operations.log 2>&1
```

For a stronger deployment, run the command through a systemd service with a restricted service account, read-only repository access, no shell secrets in unit files, and log rotation. Keep the receipt outside public artifacts if it contains operational metadata that should remain private.

## Independence controls

The local lane is read-only. It does not create invoices, collect payments, create subscriptions, send customer messages, issue refunds, or alter settlement records. It fails closed on incomplete repository visibility, missing operations artifacts, duplicate repository names, missing default branches, or validator errors.

The six-hour Manus schedule may continue as a second observer. GitHub Actions can remain enabled for hosted evidence, but a GitHub billing lock, Actions outage, or repository-secret administration bottleneck no longer prevents the owner-controlled lane from running the portfolio control.
