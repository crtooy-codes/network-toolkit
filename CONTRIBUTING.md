# Contributing to OpenLPS

OpenLPS welcomes improvements that preserve the GPL-3.0 license, upstream
attribution and the authorized-use safety boundary.

All contributors are expected to follow the project
[code of conduct](CODE_OF_CONDUCT.md) and
[authorized-use policy](docs/AUTHORIZED_USE_POLICY.md).

## Development flow

1. Create a branch from `main`.
2. Keep each change focused and explain its user-visible effect.
3. Do not add secrets, personal data, captured credentials or real target
   identifiers.
4. Add or update tests for changed behavior.
5. Run the build and relevant tests locally.
6. Open a pull request and wait for required CI checks.
7. Do not publish release assets or update manifests from a feature branch.
8. Do not add paywalls or usage restrictions to GPL-covered functionality
   without a documented license and architecture review.

Suggested branch names:

- `feature/short-description`
- `fix/short-description`
- `docs/short-description`
- `release/version`

## Local validation

Windows:

```powershell
.\gradlew.bat build --stacktrace
```

Linux/macOS:

```bash
./gradlew build --stacktrace
```

The update-service contract tests run in CI with:

```bash
python3 -m unittest discover -s server/tests -p 'test_*.py'
```

Root/device behavior must also be tested on a dedicated laboratory device.
Never point active scans, wireless actions, payloads or exploitation modules at
third-party systems.

## Versioning

- `versionCode` must always increase for every distributed APK.
- `versionName` should identify development, preview, release-candidate or
  stable status.
- Only maintainers with access to the offline release process may produce an
  official signed APK or manifest.
- Release maintainers should follow
  [docs/RELEASE_KEYS_RUNBOOK.md](docs/RELEASE_KEYS_RUNBOOK.md) and
  [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).

## Pull-request checklist

- [ ] Scope and risk are described
- [ ] Build succeeds
- [ ] Relevant automated tests pass
- [ ] Device test is documented when root/chroot behavior changes
- [ ] No secret or personal identifier is present
- [ ] User-facing text and documentation are updated
- [ ] GPL/upstream attribution is preserved
