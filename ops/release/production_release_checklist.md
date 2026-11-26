# Production Release Checklist

## Release identity

- [ ] Release ID and commit SHA recorded
- [ ] Scope and customer impact documented
- [ ] Owner, reviewer, and incident contact assigned
- [ ] Environment identified as test or live

## Application quality

- [ ] Unit, integration, and end-to-end tests pass
- [ ] Database migrations are backward compatible
- [ ] Error paths and retries are tested
- [ ] Idempotency is verified
- [ ] Logs contain correlation IDs but no secrets or payment data
- [ ] Health check and dependency checks pass

## Atlas billing gate

- [ ] Intended Stripe account verified
- [ ] Live/test mode verified
- [ ] Product and price IDs verified for currency, amount, interval, and active state
- [ ] Webhook endpoint is enabled and signature validation tested
- [ ] Event account matching tested
- [ ] Duplicate webhook replay tested
- [ ] Successful checkout tested
- [ ] Failed payment tested
- [ ] Cancellation and renewal behavior tested
- [ ] Refund handling documented
- [ ] No live payment is made without separate explicit authorization

## Aegis and evidence gate

- [ ] Role and tenant boundaries tested
- [ ] Audit events emitted for material changes
- [ ] Evidence status is assigned and immutable after finalization
- [ ] Processor success is not mislabeled as bank settlement
- [ ] Export contains provenance and redaction metadata
- [ ] Security review completed

## Quote-to-cash control gate

- [ ] Deal record contains customer legal entity, owner, environment, quote versions, hashes, approvals, acceptance, billing, settlement, reconciliation, exceptions, and audit events
- [ ] Threshold routing and ordered approvals tested with segregation-of-duties checks
- [ ] Discount, amount, scope, legal-term, or billing-term changes create a new quote version and require reapproval
- [ ] Unauthorized signer, expired document, void document, and acceptance/version mismatch are negative-path no-go tests
- [ ] Invoice cannot issue without exact customer acceptance tied to the approved quote hash
- [ ] Payment failure, dispute, refund, reversal, credit hold, duplicate transaction, and uncollectible paths are tested
- [ ] Processor confirmation is not labeled bank settlement
- [ ] Three-way reconciliation matches quote/invoice, payment, and settlement independently
- [ ] Webhook replay, duplicate event, out-of-order event, signature failure, integration outage, pause/resume, and cancellation are tested
- [ ] Amendments and reconciliation exceptions preserve the original evidence and produce a new audit trail
- [ ] Audit-log completeness, event idempotency, retry latency, and integration failure alerts are measured

## Operations gate

- [ ] Monitoring dashboard available
- [ ] Alert thresholds configured
- [ ] On-call owner assigned
- [ ] Rollback artifact available
- [ ] Backup/restore check completed
- [ ] Customer communication prepared if behavior changes

## Go / no-go

- **GO:** every mandatory gate is checked, evidence references are attached, and rollback is rehearsed.
- **NO-GO:** any secret exposure, account mismatch, untested payment path, missing rollback, unresolved critical vulnerability, or ambiguous financial state.
- **NO-GO:** missing approval, signer-authority evidence, quote-hash mismatch, failed/disputed/refunded payment, duplicate transaction, credit hold, open reconciliation exception, or incomplete audit trail.

## Rollback

1. Freeze the release and record the incident ID.
2. Disable the affected feature flag or route.
3. Restore the last known-good artifact.
4. Verify billing/webhook/event processing in the affected environment.
5. Preserve logs and evidence before cleanup.
6. Notify impacted users when required.
7. Complete a postmortem with corrective actions and an owner for each action.
