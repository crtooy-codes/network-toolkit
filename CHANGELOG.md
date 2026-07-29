# Changelog

All notable OpenLPS changes are recorded here. The project is still in
pre-release development and has no stable public APK.

## 5.0.0-dev.3 — unreleased

### Security

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
