# OpenLPS security policy

## Supported versions

OpenLPS is currently in pre-release development. No build is yet declared a
stable, publicly supported release. Security fixes are applied to the latest
commit on the maintained branch and will be included in the next signed
preview.

## Reporting a vulnerability

Do not publish credentials, signing material, private network identifiers,
personal data, or a working exploit against a real third-party target in a
public issue.

For a sensitive vulnerability, use GitHub's private **Report a vulnerability**
option in the repository Security tab when it is available. Include:

- affected commit/version and Android version;
- device/root environment when relevant;
- minimal reproduction in an isolated, authorized laboratory;
- expected and observed result;
- crash log with secrets and personal identifiers removed;
- likely impact and any safe mitigation.

Ordinary non-sensitive bugs can be reported through GitHub Issues.

## Release and update trust

OpenLPS uses two independent identities:

1. the Android APK release signing key;
2. the Ed25519 key that signs the update manifest.

Private keys, keystores, passwords, tokens, recovery codes and raw user data
must never be committed. Release keys are generated and backed up offline. The
repository contains only public keys and cryptographic hashes.

The update client rejects:

- unsigned or incorrectly signed manifests;
- unsupported manifest versions;
- non-HTTPS or unofficial release URLs;
- APK/core assets with an unexpected size or SHA-256;
- malformed or oversized manifests and signatures.

Until the first release keys are created, remote updates remain disabled.
The key creation and backup process is documented in
[`docs/RELEASE_KEYS_RUNBOOK.md`](docs/RELEASE_KEYS_RUNBOOK.md).

## Authorized-use boundary

Security testing must be limited to devices, applications, systems and
networks owned by the tester or covered by explicit authorization. Reports
must not contain stolen credentials, third-party private data or instructions
whose purpose is unauthorized access.

The project-wide expectations and future official-service review process are
documented in
[`docs/AUTHORIZED_USE_POLICY.md`](docs/AUTHORIZED_USE_POLICY.md) and
[`docs/ACCESS_REQUEST_WORKFLOW.md`](docs/ACCESS_REQUEST_WORKFLOW.md).

## Dependency and upstream assets

Every downloadable core/module asset must have a pinned size and SHA-256 or be
declared in a valid signed manifest. A changed upstream asset is rejected until
its new digest has been independently reviewed and deliberately updated.
