# Evidence and Financial-Control Policy

## Evidence classes

| Class | Examples | Permitted use |
|---|---|---|
| A — Primary live evidence | Stripe API object, signed webhook, bank/broker statement, chain receipt, registrar record | Financial, operational, or legal conclusion within scope |
| B — Reproducible implementation | Tested source, CI result, deployment log, schema, signed release | Capability and configuration claims |
| C — Documentary | Contract, Workspace document, statement copy, declaration, research note | Document-existence and reported-history claims |
| D — Narrative/generated | Manifest, dossier, internal ledger, generated JSON, copied assertion | Hypothesis, backlog, or research only |

## Required evidence record

Every material claim must record:

- `claim_id`
- `claim_text`
- `source_class`
- `source_reference`
- `environment`
- `observed_at`
- `owner`
- `status`: `verified`, `contradicted`, `unverifiable`, or `pending`
- `redaction_status`
- `next_evidence_required`

## Financial state machine

`reported -> expected -> initiated -> processor_succeeded -> processor_failed -> payout_pending -> bank_confirmed -> reconciled -> disputed`

No state may skip directly from `reported` or `processor_succeeded` to `reconciled` without the required source evidence.

## Redaction standard

Exclude secrets, API keys, webhook secrets, private keys, wallet addresses, bank/routing details, card numbers, unnecessary object IDs, and full personal data. Reports should use context aliases and last-four identifiers only when operationally necessary.

## Evidence gates

- **Revenue:** active customer transaction, payment status, amount, currency, account, and corresponding accounting record.
- **Payout:** processor payout record plus external bank confirmation where bank settlement is claimed.
- **Crypto:** chain/network, transaction hash, block/finality, token contract, sender/recipient control, and independent query.
- **Legal/title:** registrar, court, trustee, custodian, or other authoritative primary record.
- **Production capability:** tested code, deployment state, configuration, monitoring, and rollback evidence.

## Escalation rule

If evidence conflicts, preserve both records, mark the claim `contradicted` or `unverifiable`, open an exception, and do not resolve by repetition, narrative confidence, or larger document counts.
