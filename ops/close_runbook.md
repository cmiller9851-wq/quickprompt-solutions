# Corporate Quote-to-Cash Close Runbook

This runbook is the operating procedure for converting a legitimate QuickPrompt commercial opportunity into an evidence-backed close. It applies separately to `test` and `live` environments. A test record can exercise the workflow, but it cannot be reported as revenue, settlement, owner income, or customer payment.

## 1. Commercial stages and required controls

A deal moves through the controlled state machine below. Every transition emits an immutable audit event with an actor, timestamp, correlation ID, prior state, next state, and metadata hash.

`Draft → Qualified → Approval Pending → Approved to Send → Sent → Accepted/Signed → Invoice Issued → Payment Confirmed/Settled → Closed Won`

The side states are `Rejected`, `Expired`, `Canceled`, `Void`, `Failed`, `Disputed`, `Refunded`, `Uncollectible`, and `Reconciliation Exception`. Side states do not bypass evidence gates. A failed, disputed, refunded, duplicate, or unreconciled transaction is not Closed Won.

Qualification records the customer legal entity, jurisdiction, business need, owner, expected value, currency, environment, and credit status. Approval routing is threshold-based and ordered. The commercial owner cannot approve their own deal, and a reconciliation reviewer cannot be the payment initiator for the same transaction.

## 2. Quote and approval control

Each quote version is immutable after approval. The record stores the exact quote version, content hash, currency, amount, discount, creation time, and status. Any amount, discount, scope, legal term, billing term, or customer-entity change creates a new version and returns the deal to Approval Pending.

The approval record must name the independent approver, decision, threshold basis, approved version, approved content hash, and decision time. No quote may be sent until the approval matches the operative version and hash. A missing approval, stale approval, or segregation-of-duties conflict is a no-go.

## 3. Customer acceptance

Acceptance must be tied to the approved quote version and content hash. Store the acceptance method, signer identity, signer-authority evidence, evidence URI, and acceptance timestamp. An unsigned order form, unauthorized signer, expired or voided document, or version mismatch blocks invoicing.

DocuSign, Ironclad, portal, and order-form integrations are evidence providers, not substitutes for checking signer authority and exact-version identity. Processor status is not bank settlement.

## 4. Invoice, payment, and settlement

Invoice issuance requires accepted customer evidence and an approved quote. Record the invoice ID, provider account reference in redacted form, amount, currency, issue time, invoice state, and payment state. The payment state must distinguish pending, succeeded, failed, canceled, disputed, and refunded.

A successful processor response supports `processor_confirmed`; it does not by itself prove `bank_settled`. Settlement requires an independent provider or bank evidence reference with amount and currency. A chargeback, reversal, refund, duplicate transaction, credit hold, or failed payment moves the deal to the appropriate side state or Reconciliation Exception.

No payment, invoice finalization, subscription creation, refund, or customer communication is executed from a draft record. The exact live payload and action require explicit owner authorization at the point of execution.

## 5. Three-way reconciliation

The independent reviewer matches three records: approved quote/invoice, payment-provider transaction, and settlement or bank evidence. The match checks customer, invoice, amount, currency, transaction identity, settlement date, and duplicate status. The reconciliation record stores `matched`, `partial_match`, `exception`, or `cleared`, plus reviewer, review time, and exception reason.

A deal can reach Closed Won only when invoice-to-payment and payment-to-settlement matches are true, duplicate check is clear, no critical exception is open, and the reviewer is independent. Exceptions are retained until resolved, waived by an authorized decision-maker, or rolled back with a reason.

## 6. Webhooks and integrations

All inbound events are idempotent by provider event ID and deal correlation ID. Replay, duplicate, out-of-order, delayed, malformed, and signature-invalid events are tested. Out-of-order events are held until prerequisites exist; they never advance a deal past a missing gate. Integration outage and retry exhaustion create an exception and alert the owner.

Every material integration failure records provider, event ID, first-seen time, last-attempt time, retry count, latency, and resolution. Secrets and payment details are excluded from logs.

## 7. Retention and reporting

Retain the approved quote versions, approval records, acceptance evidence, invoice and payment references, settlement evidence, reconciliation review, exceptions, rollback records, and audit events according to the applicable legal and accounting retention policy. Redact secrets, card data, bank details, wallet addresses, and unnecessary personal identifiers from operational exports.

Revenue, capital, settlement, and owner-earned-income reporting uses only live, reconciled records supported by authenticated external-primary evidence. Internal ledgers, code constants, generated narratives, and repeated corpus language are not financial proof.

## 8. Owner decision rights

The owner may approve commercial strategy, designate deal owners, authorize a specific live financial action, and accept or reject an exception resolution. The owner does not self-approve a deal, override missing customer acceptance, waive a reconciliation break without an auditable authorization, or classify processor success as settlement. The system preserves the owner’s decision and the independent control evidence separately.
