# OpenLPS authorized-use policy

Effective status: draft for project review

Applies to: OpenLPS-operated services, official support channels and official
signed distributions

## Purpose

OpenLPS is intended for education, defensive research and security testing
performed with clear authority. This policy establishes the minimum conditions
for using project-operated services and receiving official support.

The GPL-3.0 license governs copyright permissions for the covered software.
This policy does not replace or reduce rights granted by that license. It
governs project-operated services and expected conduct in project spaces.

This draft is not legal advice and is not a substitute for customer-specific
legal review or a written penetration-testing agreement.

## Required authorization

Before using a security-testing function, the operator must have one of the
following:

- ownership of the target device, application, account, system or network; or
- explicit authorization from an owner or authorized representative.

For work performed for another person or organization, authorization should be
written and should identify:

- the legal owner or authorizing representative;
- the operator and, when applicable, the operator's employer;
- the exact targets and environments in scope;
- allowed techniques and prohibited techniques;
- the start and end time;
- data-handling and reporting requirements;
- emergency and stop contacts.

Approval by the OpenLPS project, payment for a service, possession of an APK or
acceptance of an in-app notice does not create target authorization.

## Permitted use

Examples of permitted use include:

- a personal or organization-owned isolated laboratory;
- defensive validation of systems explicitly placed in scope;
- capture-the-flag exercises and intentionally vulnerable training systems;
- classroom or supervised research with permission;
- compatibility testing on devices owned by the tester;
- incident-response work performed under documented authority.

The operator must use the least disruptive technique that can meet the
authorized objective and stop when scope or safety becomes uncertain.

## Prohibited use in OpenLPS services

OpenLPS-operated services and support must not be used to assist:

- access to systems, accounts or data without authorization;
- credential theft, phishing, extortion, stalking or harassment;
- persistence, evasion or destructive activity outside an approved lab;
- interception of third-party communications without lawful authority;
- denial-of-service activity against public or third-party infrastructure;
- deployment of malware or payloads to non-consenting parties;
- concealment, resale or publication of unlawfully obtained data;
- bypass of a provider's rules solely to avoid abuse controls.

Do not send credentials, private keys, real victim data, production dumps or
unredacted customer identifiers to public issues or support channels.

## Operator responsibilities

The operator is responsible for:

- verifying authority and staying inside the written scope;
- following applicable law and contractual rules;
- obtaining backups and a recovery plan before disruptive tests;
- protecting collected data and deleting it when no longer required;
- maintaining an activity log sufficient to explain what was tested;
- stopping immediately when unintended impact or out-of-scope access occurs;
- reporting vulnerabilities responsibly and securely.

Sensitive actions should be tested first in an isolated laboratory. A warning
or confirmation screen is a safety control, not evidence of legal permission.

## Project response

The project may refuse or suspend access to official services when an
application is incomplete, authority cannot be reasonably explained, there is
credible evidence of prohibited use, payment fraud is suspected or continued
support would create an unacceptable safety risk.

When practical, the project will:

1. preserve a minimal decision record;
2. tell the applicant which policy category caused the decision;
3. allow corrected information or an appeal;
4. avoid publishing personal or investigative details;
5. report an incident when required by applicable law.

Suspending an OpenLPS-operated service does not revoke copyright rights that a
recipient already has under GPL-3.0.

## Reporting concerns

Security vulnerabilities should follow [../SECURITY.md](../SECURITY.md).
Sensitive abuse reports should use a private maintainer-designated channel, not
a public issue. The permanent private contact method will be published before
official paid services open.

## Policy changes

Material changes should be versioned, dated and announced before taking effect.
The project should retain prior versions so that users can identify the policy
that applied to a particular service decision.
