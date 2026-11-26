# 30-Day Execution Board

**North-star outcome:** One reproducible QuickPrompt paid-customer loop with evidence-backed operations.

## Week 1 — Control the portfolio

| Work item | Owner | Acceptance criterion |
|---|---|---|
| Adopt the five-repository Ship spine | Founder/Architect | Disposition map approved; no unowned production path |
| Freeze unsupported financial/legal claims from customer surfaces | Governance owner | Search and review completed; exceptions logged |
| Create environment matrix | Runtime owner | Test/live variables and data boundaries documented |
| Create incident contacts and escalation tree | Operations owner | Contact and severity matrix published |

## Week 2 — Make billing reproducible

| Work item | Owner | Acceptance criterion |
|---|---|---|
| Verify Atlas account, prices, and webhook configuration | Billing owner | Checklist evidence attached; test/live separated |
| Run checkout happy path | Billing + QA | Subscription and access state reconcile correctly |
| Run failed payment and retry path | Billing + QA | No access grant from failed state; recovery recorded |
| Run cancellation/refund path | Billing + QA | Correct entitlement and evidence state after cancellation/refund |

## Week 3 — Connect governance and evidence

| Work item | Owner | Acceptance criterion |
|---|---|---|
| Emit canonical event schema | Runtime + Governance | Tenant, actor, environment, source, time, evidence status present |
| Store redacted evidence references | Evidence owner | No secrets or unnecessary PII; hash/provenance recorded |
| Add reconciliation dashboard | Finance-control owner | Processor, payout, bank, and reconciled states distinct |
| Add release gate to CI/process | Release owner | No-go conditions block release |

## Week 4 — Prove repeatability

| Work item | Owner | Acceptance criterion |
|---|---|---|
| Run disaster/rollback rehearsal | Operations owner | Recovery completed within agreed target |
| Run security and dependency review | Security owner | Critical findings closed or formally excepted |
| Publish trust-center minimum content | Governance + Product | Controls, status, billing, privacy, and support pages ready |
| Review KPI baseline | Founder + owners | Dashboard has definitions, sources, owners, and first values |

## End-of-month go/no-go

Proceed to broader distribution only if the paid-customer loop is reproducible, all live/test boundaries are explicit, no critical security issue remains open, and every financial claim shown to customers links to primary evidence or is clearly labeled as provisional.
