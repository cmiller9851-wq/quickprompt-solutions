# QuickPrompt Solutions Strategic Operations Charter

**Owner:** Cory Miller — Founder and Architect  
**Version:** 1.0  
**Operating mode:** Evidence-first, read-only against external systems unless an action is separately authorized

## Mission

Turn QuickPrompt Solutions into a globally distributable AI-workflow platform with measurable customer value, reliable billing, auditable operations, and disciplined governance.

## Operating spine

- **QuickPrompt Solutions:** commercial brand, customer experience, pricing, documentation, and distribution.
- **Atlas:** Stripe Checkout, subscriptions, webhooks, and paid-state reconciliation.
- **Astera:** runtime orchestration, integrations, jobs, feature flags, and observability.
- **Aegis:** policy, access control, approval workflows, risk classification, and audit events.
- **Settlement Reconciliation Monitor:** evidence vault, provenance, payment-state reconciliation, and finance controls.
- **GlobalLink / Sovereign Safe:** isolated testnet and security research until independently audited and production-approved.

## Decision rights

| Decision | Accountable owner | Required evidence |
|---|---|---|
| Product scope and release priority | Founder/Architect | Customer problem, acceptance criteria, owner, KPI |
| Production release | Release owner | Checklist, tests, security review, rollback plan |
| Billing configuration | Billing owner | Stripe account/price/webhook verification and test evidence |
| Security exception | Security owner | Threat model, compensating control, expiry date |
| Financial recognition | Finance-control owner | Primary processor/bank/accounting evidence |
| Legal/title/trust assertion | Legal reviewer | External primary authority; internal documents are insufficient |
| Customer-impacting incident | Incident commander | Timeline, containment, customer communication, postmortem |

## Non-negotiable controls

1. No repository constant is treated as a live balance.
2. No document, declaration, generated narrative, or repeated corpus assertion is treated as settlement proof.
3. Processor success, payout initiation, and bank settlement remain separate states.
4. Production claims require a source object, timestamp, environment, owner, and evidence status.
5. Research and testnet systems cannot silently become production payment rails.
6. Secrets stay in deployment secret stores and never in repositories, logs, reports, or tickets.
7. Every production change has an owner, reviewer, rollback path, and verification step.

## Operating cadence

- **Daily:** incident review, failed payments, deployment health, critical security alerts.
- **Weekly:** KPI review, release board, evidence exceptions, customer feedback, repository drift.
- **Monthly:** access review, dependency review, financial reconciliation review, portfolio disposition review.
- **Quarterly:** strategy reset, pricing review, disaster recovery exercise, independent control review.

## First success condition

A customer can discover QuickPrompt, activate a paid plan through Atlas, receive access only after a correctly reconciled paid state, use the product, cancel successfully, and receive an auditable record of every material event.
