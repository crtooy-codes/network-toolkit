# OpenLPS official-service access workflow

Status: operational draft; no paid service is open yet

## Scope

This workflow is for requests to buy or receive an OpenLPS-operated service,
such as an official signed build, support, training or managed laboratory
access.

It is not a license to attack a target and does not control the GPL rights in
copies of the community software already received.

## Before opening applications

Maintainers must first publish:

- the exact service description and price;
- the service terms, refund policy and support level;
- the authorized-use policy;
- a privacy notice with purpose, legal basis, retention and contact details;
- a private request channel;
- the countries and customer types that can be served;
- the names or roles allowed to approve, deny and audit requests.

Do not collect payments, government identity documents or target credentials
while these items are missing.

## Minimum request form

Collect the least information necessary:

```text
Request identifier:
Applicant name:
Organization, if applicable:
Contact email:
Country or region:
Requested OpenLPS service:
Intended use:
Target type (do not include secrets or live IP addresses):
Who owns the target:
How authorization will be obtained:
Laboratory or production environment:
Expected testing period:
Data that may be processed:
Agreement to the authorized-use policy: yes/no
Agreement that OpenLPS approval is not target authorization: yes/no
```

Do not ask an applicant to email passwords, private keys, customer databases,
exploit results or full target inventories. If stronger verification becomes
necessary, design a separate protected process after privacy and security
review.

## Review procedure

Use two-person review for unusual, high-risk or production-facing requests.

1. Assign a random request identifier.
2. Check that required fields are complete.
3. Confirm that the intended use fits
   [AUTHORIZED_USE_POLICY.md](AUTHORIZED_USE_POLICY.md).
4. Ask only the minimum clarification needed.
5. Classify the request as:
   - `approved`;
   - `approved-with-conditions`;
   - `needs-information`;
   - `denied`;
   - `suspended`;
   - `closed`.
6. Record a short reason category without storing unnecessary sensitive
   details.
7. Send the decision through the private channel.
8. Create a service entitlement only after approval and successful payment.

Suggested reason categories:

- incomplete request;
- authority not sufficiently explained;
- use outside policy;
- unsupported country or customer type;
- service unavailable or capacity reached;
- suspected fraud or identity inconsistency;
- approved standard laboratory use;
- approved documented professional engagement.

## Approval conditions

An approval message should state:

- the exact service and validity period;
- any technical or support limits;
- that target-specific written authorization remains the operator's duty;
- that access is personal or organizational as defined by the service terms;
- that suspicious use may suspend the service;
- how to request support or appeal a decision.

Do not claim that the project has legally certified the customer's engagement.

## Decision templates

### Needs information

```text
Subject: OpenLPS request [ID] needs more information

We received your request for [service]. Before a decision, please clarify:
[minimal questions].

Do not send passwords, private keys, customer data or live target details.
OpenLPS service approval does not replace written authorization from the target
owner.
```

### Approved

```text
Subject: OpenLPS request [ID] approved

Your request for [service] is approved [with these conditions: ...].
Validity: [period].

This approval covers only the OpenLPS-operated service. You remain responsible
for written target authorization, scope, applicable law and safe operation.
Next step: [payment or onboarding instructions].
```

### Denied

```text
Subject: OpenLPS request [ID] decision

We cannot provide [service] for this request.
Reason category: [category].

You may reply with corrected information or an appeal. Do not send secrets,
credentials or private target data.
```

## Records and privacy

Until a reviewed retention schedule exists, use a conservative temporary
baseline:

- separate access-request records from public GitHub issues;
- restrict access to named reviewers;
- enable multi-factor authentication;
- retain the minimum decision and transaction record required for operations
  and law;
- delete unnecessary attachments and clarification messages promptly;
- never place request data, credentials or payment data in the source
  repository;
- use a payment provider rather than storing card data directly.

The final retention period must be defined in the privacy notice for each
jurisdiction. This draft deliberately does not invent a universal period.

## Revocation and incident handling

If credible misuse or account compromise is reported:

1. suspend only the affected official service when safe to do so;
2. preserve minimal relevant evidence with restricted access;
3. notify the account contact through the verified private channel;
4. review the event against the policy;
5. restore, condition, close or deny the service;
6. document the reason and appeal path;
7. follow legal reporting duties where applicable.

Service suspension must not be represented as revoking GPL rights in software
copies already conveyed.

## Technical boundary

The current GitHub Pages update service is public and static. It must not store
applications, approvals, payment status or personal information.

A future automated system requires a separate backend with:

- authenticated staff roles and least privilege;
- encrypted transport and protected storage;
- auditable decisions without secret logging;
- rate limiting and abuse monitoring;
- backup, recovery and incident response;
- data export and deletion procedures;
- separation between billing, support and release-signing authority.

Release private keys remain offline and are never exposed to the access system.
