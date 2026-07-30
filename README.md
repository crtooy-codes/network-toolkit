# OpenLPS Network Toolkit

OpenLPS Network Toolkit is an open-source Android toolkit for authorized
security research on rooted devices. It continues the historical StrykerOSS
codebase while moving the package, storage paths, update service and public
maintenance process to OpenLPS.

- Package: `com.openlps.networktoolkit`
- Current development version: `5.0.0-dev.3`
- Chroot path: `/data/local/openlps/release`
- Shared storage path: `/storage/emulated/0/OpenLPS`
- License: [GNU GPL v3.0](LICENSE)
- Official repository: <https://github.com/crtooy-codes/network-toolkit>
- Update service: <https://crtooy-codes.github.io/network-toolkit/>

OpenLPS is still in pre-release development. Debug APKs are for laboratory
testing only and are not public releases.

## Responsible Use

Use this software only on devices, applications, systems and networks that you
own or have explicit permission to test. The project is intended for education,
research and authorized security work. Users are responsible for complying with
applicable laws and engagement rules.

## Project Status

The current OpenLPS line has:

- OpenLPS application identity and parallel package name;
- OpenLPS chroot and shared-storage paths;
- initial English, Portuguese-BR, Spanish, Russian and Simplified Chinese
  resources;
- authorized-use onboarding;
- hardened update-client scaffold with HTTPS allowlisting, SHA-256 checks, size
  checks and Ed25519 manifest verification;
- GitHub Pages update-service scaffold;
- GitHub Actions checks for Android and update-service validation.

Remote updates intentionally remain disabled until the offline release keys are
created and the manifest public key is added to the app.

## Documentation

- [Status and management report](docs/RELATORIO_STATUS_E_GESTAO_OPENLPS_2026-07-28.md)
- [Product strategy](docs/PRODUCT_STRATEGY.md)
- [Authorized-use policy](docs/AUTHORIZED_USE_POLICY.md)
- [Official-service access workflow](docs/ACCESS_REQUEST_WORKFLOW.md)
- [Galaxy S10 smoke test](docs/DEVICE_SMOKE_TEST_SM-G973F_2026-07-28.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)
- [Release keys runbook](docs/RELEASE_KEYS_RUNBOOK.md)
- [Release-key ceremony status](docs/RELEASE_KEY_CEREMONY_STATUS_2026-07-29.md)
- [Update service operations](docs/UPDATE_SERVICE_OPERATIONS.md)
- [Security policy](SECURITY.md)
- [Contributing guide](CONTRIBUTING.md)
- [Code of conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)

## Capabilities

OpenLPS keeps the rooted Android/chroot model used by the original project. The
planned and partially migrated modules include:

- dashboard and core manager;
- built-in terminal;
- local-network and Nmap workflows;
- Wi-Fi adapter workflows for authorized lab testing;
- web scanning with Nuclei;
- Metasploit and other chroot tools;
- HID and USB gadget workflows where the kernel supports them;
- report, storage and utility modules inherited from the historical base.

Some screens still carry internal Java package names from the original project.
Those names are being migrated incrementally to reduce release risk.

## Requirements

- Rooted Android device, preferably Magisk or KernelSU.
- Enough internal storage for the chroot and tool assets.
- External monitor-mode USB Wi-Fi adapter for Wi-Fi laboratory workflows.
- Gadget-capable kernel for HID/USB Arsenal workflows.
- Java 17 and Android SDK for building from source.

## Build

From the repository root:

```powershell
.\gradlew.bat assembleDebug --stacktrace
```

Useful Gradle tasks:

```powershell
.\gradlew.bat build --stacktrace
.\gradlew.bat :app:testDebugUnitTest --stacktrace
.\gradlew.bat :app:assembleRelease --stacktrace
```

Debug APKs are written under:

```text
app/build/outputs/apk/debug/
```

Release APKs are written under:

```text
app/build/outputs/apk/release/
```

## Release Signing

Release signing uses environment variables or Gradle properties:

```properties
OPENLPS_RELEASE_STORE_FILE=/path/to/openlps-release.jks
OPENLPS_RELEASE_STORE_PASSWORD=...
OPENLPS_RELEASE_KEY_ALIAS=openlps-release
OPENLPS_RELEASE_KEY_PASSWORD=...
```

If these values are not set, release signing is skipped. This allows CI and
contributors to build the project without access to private release material.

The APK release key and the Ed25519 manifest key are separate. Private keys and
passwords must never be committed.

## Update Service

The update service is static and hosted through GitHub Pages. GitHub Releases
host large downloadable assets such as signed APKs and reviewed core archives.

Live service files:

```text
server/public/health.json
server/schema/manifest-v1.schema.json
server/public/v1/manifest.json
server/public/v1/manifest.json.sig
```

The manifest files are not published until the first signed release. When they
exist, the Pages workflow validates the JSON contract and signature envelope
before deployment.

## Project Layout

```text
app/                         Android application
server/                      Static update service, schema and validator
docs/                        Reports, release process and operations docs
.github/workflows/           CI, Pages deployment and manual release build
terminal/, Xorg/, NeoLang/   Historical support modules
```

## Contributing

Contributions should keep the authorized-use boundary clear, preserve GPL and
third-party notices, and avoid committing secrets or personal data. See
[CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and the
[authorized-use policy](docs/AUTHORIZED_USE_POLICY.md).

## Credits

OpenLPS Network Toolkit is derived from
[StrykerOSS](https://github.com/zalexdev/strykerapp), historically created and
maintained by zalexdev from 2021 to 2026. Copyright notices, GPL obligations and
third-party attributions are preserved. OpenLPS credits apply to new
continuation work from 2026 onward.

Bundled third-party components keep their own licenses. See
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) and the in-app open-source
license screen.
