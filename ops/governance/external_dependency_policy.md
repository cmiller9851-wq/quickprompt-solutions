# External Dependency and Acceptance Policy

QuickPrompt control truth is produced by repository-native validation, the independent read-only portfolio operator, authenticated evidence records, and the approved quote-to-cash controls. A third-party preview, deployment, hosting, analytics, or CI integration is not authoritative merely because it posts a status to GitHub.

## Acceptance boundary

A third-party status may be an advisory signal. It becomes a release gate only when the owner explicitly adopts it in the release record, documents the service, identifies its failure mode, and provides an independent fallback. A provider outage, account lock, deployment failure, expired integration, or missing provider credential must not invalidate repository validation, evidence controls, portfolio inventory, or financial-state reconciliation.

The QuickPrompt GO/NO-GO decision is based on the repository-native checklist, local independent operations receipt, deterministic deal validator, security scan, required tests, evidence completeness, rollback readiness, and reconciliation state. External preview comments and hosting deployment statuses are recorded separately as `advisory_external_status`.

## Independence requirements

Every external dependency used in production must have an owner, purpose, data boundary, credential owner, outage behavior, replacement or local fallback, and removal procedure. The independent operations lane must remain runnable with the owner-controlled GitHub read credential and must not require a provider-specific deployment account.

No external provider may be treated as proof of revenue, customer acceptance, settlement, ownership, legal authority, or financial balance. Those claims require authenticated external-primary evidence appropriate to the claim and the live/test environment boundary.

## Current repository posture

The repository contains no Vercel configuration and `main` has no required status checks configured. Vercel status contexts are therefore advisory external signals. They may be investigated separately, but they do not change the result of QuickPrompt-native operations validation or the independent 53-repository health control.
