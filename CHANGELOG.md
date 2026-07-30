# Changelog

All notable OpenLPS changes are recorded here. The project is still in
pre-release development and has no stable public APK.

## 5.0.0-dev.4 — unreleased

### Security

- Pin the permanent 32-byte Ed25519 update-manifest public key after the
  verified offline ceremony.
- Record the public APK-certificate and manifest-key SHA-256 fingerprints.
- Store the encrypted private material in the KeePass primary and verified
  recovery vaults, without committing private keys or passwords.
- Add a hidden-prompt local signed-build helper that enforces the permanent
  APK-certificate fingerprint and clears process signing variables.
- Produce and independently verify the first optimized `dev.4` APK signed by
  the permanent RSA-4096 release certificate without installing or publishing
  it.

### Changed

- Advance the laboratory build to version code 503.
- Validate an in-place laboratory-device upgrade from `dev.3` after a
  hash-verified private-data backup, preserving the Android package UID,
  first-install timestamp and application state.
- Make the Windows key-ceremony assistant wait for network disconnection and
  report the active route instead of terminating immediately.

### Fixed

- Initialize the repository path after PowerShell establishes
  `$PSScriptRoot`, preserving compatibility with Windows PowerShell 5.1.

## 5.0.0-dev.3 — 2026-07-29

### Security

- Add offline release-key tooling for encrypted Ed25519 manifest keys and the
  independent RSA-4096 Android keystore, with repository/fixed-drive guards.
- Add an offline Windows ceremony wrapper with hidden confirmed prompts,
  removable-media checks, KeePass backup verification and file inventory.
- Add RFC 8032 verification tests and disposable end-to-end key-tool tests.
- Pin size and SHA-256 for temporary 32-bit and 64-bit upstream chroot
  bootstrap assets.
- Parse and restrict release, news, notification and image URLs to official
  HTTPS locations.
- Reject path traversal, encoded paths, query strings, URL fragments,
  lookalike domains and unexpected ports.
- Enforce a strict manifest contract, including duplicate-key and
  unknown-field rejection in the deployment validator.
- Add Java client tests and Python update-service contract tests.

### Changed

- Rename updater internals and release-signing variables to OpenLPS.
- Add security policy, contribution guide, code of conduct, release checklist,
  release-keys runbook and update-service operations guide.
- Define the Community and Official Services product strategy without
  restricting GPL-covered code.
- Add an authorized-use policy and a privacy-conscious access-review workflow
  for future official support, training and signed-build services.
- Rewrite the README around the OpenLPS continuation while preserving
  historical upstream credit.
- Extend GitHub Actions to test the update-service contract.
- Add a manual signed-release APK workflow for maintainers with configured
  GitHub secrets.

### Fixed

- Correct Terminal paths for the OpenLPS package.
- Complete the installer transition without leaving `Initializing…` visible.
- Derive the active IPv4 subnet from Android `LinkProperties`.
- Replace stale user-facing project links and promotional branding.

## 5.0.0-dev.2 — 2026-07-28

- Establish the independent `com.openlps.networktoolkit` package.
- Add OpenLPS identity, initial translations and authorized-use onboarding.
- Introduce the signed-manifest update architecture in disabled pre-release
  mode.
- Add GitHub Android CI and the static GitHub Pages update service.
