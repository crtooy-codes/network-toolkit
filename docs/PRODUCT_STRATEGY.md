# OpenLPS product strategy

## Mission

OpenLPS continues the historical StrykerOSS codebase so that the project
remains available to the security community, gains a maintainable release
process and is safer to operate in authorized laboratories.

The project has two complementary goals:

1. keep a useful GPL-3.0 community edition alive and auditable;
2. fund maintenance through official services that do not remove the freedoms
   granted by the GPL.

This document is a product and engineering direction. It is not legal advice.
The commercial model and final terms should be reviewed by qualified counsel
before money or personal data is accepted.

## Product structure

### OpenLPS Community

The community product is the GPL-covered Android application and its
corresponding source code. It includes:

- the public source repository and contribution process;
- community builds and documentation;
- the authorized-use onboarding and safety controls;
- the root/chroot engine and community modules that are part of the covered
  work;
- public security fixes and the source for distributed GPL binaries.

Recipients retain the rights granted by GPL-3.0, including studying, modifying
and redistributing the covered work under the same license.

### OpenLPS Official Services

The project may charge for work and services around the community product,
including:

- official APKs signed by the OpenLPS release key;
- a stable update channel and curated compatibility testing;
- priority support and installation assistance;
- training, laboratory exercises and documentation packages;
- compatibility certification for devices, kernels and adapters;
- managed services that run separately from the Android application.

Payment is for the official delivery, service, assurance or support. It must
not be described as purchasing permission to test systems owned by someone
else.

### Separately developed modules

A future module may use a different commercial model only after a written
license and architecture review confirms that it is an independent work and
does not create an incompatible derivative of GPL-covered code.

Until that review exists:

- do not place a paywall around an existing GPL-covered module;
- do not add restrictions that contradict GPL rights;
- do not copy GPL-covered implementation into a proprietary component;
- do not promise exclusivity for code that recipients may lawfully
  redistribute.

When separation is unclear, the module remains part of OpenLPS Community.

## Access and authorization

OpenLPS may review applications before providing official paid services. That
review protects the project relationship and helps screen obvious misuse, but
it has clear limits:

- project approval is not legal authorization to test a target;
- the customer must obtain target-specific written permission;
- a payment, account or license token does not replace a rules-of-engagement
  document;
- project disclaimers do not automatically remove duties imposed by law.

The operational review is defined in
[ACCESS_REQUEST_WORKFLOW.md](ACCESS_REQUEST_WORKFLOW.md). Expected behavior is
defined in [AUTHORIZED_USE_POLICY.md](AUTHORIZED_USE_POLICY.md).

## Product principles

1. **Fail closed:** updates and privileged actions stop safely when trust or
   authorization data is missing.
2. **Local first:** ordinary community use should not require an OpenLPS
   account or permanent network connection.
3. **Minimal data:** collect only information required for a requested paid
   service, security response or support case.
4. **Transparent trust:** official APKs and manifests are cryptographically
   signed, and source obligations remain visible.
5. **Laboratory default:** examples, tests and documentation use isolated
   targets owned by the tester.
6. **No hidden remote control:** the update service announces reviewed assets;
   it does not execute arbitrary commands on user devices.
7. **Incremental modernization:** preserve working behavior while replacing
   historical branding, paths and unsafe assumptions module by module.

## Suggested roadmap

### Phase 1: trustworthy community preview

- finish the release-key ceremony and offline backups;
- produce the first signed preview APK;
- publish the corresponding source and notices;
- test install and update on dedicated laboratory devices;
- finish high-risk branding, path and updater cleanup;
- publish a compatibility matrix and known limitations.

### Phase 2: community operations

- add issue and pull-request governance;
- define stable and preview update channels;
- expand automated and device testing;
- add clear risk labels and confirmation screens to sensitive modules;
- create reproducible test laboratories and reporting templates.

### Phase 3: official services pilot

- obtain legal review of terms, privacy notice and GPL compliance;
- select a private support and access-request channel;
- pilot manual approval with minimal data and no automatic payment;
- offer support, training and signed preview access to a small group;
- record service quality, abuse reports and operational cost.

### Phase 4: managed commercial service

Only after the manual pilot is understood:

- choose an identity and billing provider;
- build a separate service backend with audit logging and role separation;
- publish privacy, retention, refund and incident procedures;
- automate entitlements for services, not GPL freedoms;
- conduct an independent security review before public launch.

GitHub Pages is suitable for the current static update service. It is not an
account, payment or approval backend. A future commercial service needs a
separate managed backend and its own threat model.

## Decisions before implementation

The maintainers must decide and document:

- which support or training services will be offered first;
- which countries and customer types can be served;
- who reviews applications and appeals;
- the minimum personal data and retention period;
- the support response time and refund policy;
- how suspected abuse is investigated and access to official services is
  suspended;
- whether any proposed paid module is technically and legally separate.

No payment or identity collection should be implemented until these decisions,
the privacy notice and the legal review are complete.
