# OpenLPS in-place update smoke test - Galaxy S10 (SM-G973F)

Date: 2026-07-30

Device OS: Android 15 / LineageOS userdebug

Package: `com.openlps.networktoolkit`

Update: `5.0.0-dev.3` (`versionCode 502`) to
`5.0.0-dev.4` (`versionCode 503`)

This report intentionally excludes Wi-Fi names, IP addresses, MAC addresses,
the device serial number and other local-network identifiers.

## Result

The development APK updated the existing package in place with
`adb install -r`. Android preserved the package UID, application data
directory, first-install timestamp and visible application state. The
dashboard started normally, Magisk granted root to the existing package, and
no application fatal exception or ANR was observed during the launch check.

The permanent Ed25519 update-manifest public key is present in this build. No
live remote manifest was published or fetched during this test.

## Pre-update verification

- Connected device identity matched the laboratory Galaxy S10.
- Magisk root returned `uid=0(root)`.
- Installed package reported `5.0.0-dev.3` / `versionCode 502`.
- Target APK reported `5.0.0-dev.4` / `versionCode 503`.
- Target APK SHA-256 matched the previously verified build:
  `D91BA9DC6E3B85A26BCEFECDDD435D776F84A1CB9F665527026C0AE13B715A8F`.
- Target and installed APK certificate SHA-256 values matched, allowing a
  safe development-signature update without uninstalling.

## Recovery backup

Before installation, OpenLPS was force-stopped and three recovery artifacts
were copied to the computer outside the Git repository:

- credential-protected app data: 137 archive entries, SHA-256
  `240896D76EE7780718D343D38FC9E0413CAB767C163B83A3BC0E333B48C724E5`;
- device-protected app data: 4 archive entries, SHA-256
  `B8C44DC10FF9461DB0ABCCCB03FB583566E7159B2A7C2A8216F1F56F0A944A6A`;
- installed `dev.3` APK: SHA-256
  `675B2A4F040A60EF01B82A8217D6C2FC0A73A086E7FABA83E50ABB358285A378`.

The data-archive hashes were calculated independently on the phone and
computer and matched. The temporary phone-side archives were removed only
after that comparison passed.

Local backup directory:
`C:\Users\SilvaTech\OpenLPS_Next\device-backups\pre-dev4-20260730-115707`

## Post-update verification

- `adb install -r` returned `Success`.
- Package version became `5.0.0-dev.4` / `versionCode 503`.
- The first-install timestamp remained `2026-07-28 13:01:17`.
- Package UID and application data directory remained unchanged.
- The credential-protected directory contained 86 files after launch.
- The device-protected directory contained 1 file after launch.
- `MainActivity` completed a cold start in 1.23 seconds.
- The OpenLPS process remained active with `MainActivity` at the top.
- The dashboard retained the prior summary of 9 devices in the last scan.
- Magisk displayed a successful superuser-access notification.
- The launch log contained no OpenLPS fatal exception or ANR.

## Build validation

Debug build and unit tests:

```powershell
.\gradlew.bat :app:assembleDebug :app:testDebugUnitTest --no-daemon --console=plain
```

- Result: success
- Debug APK SHA-256:
  `D91BA9DC6E3B85A26BCEFECDDD435D776F84A1CB9F665527026C0AE13B715A8F`
- APK Signature Scheme v2: verified

Optimized unsigned release build:

```powershell
.\gradlew.bat :app:assembleRelease :app:testDebugUnitTest --no-daemon --console=plain
```

- Result: success
- Output: `app/build/outputs/apk/release/app-release-unsigned.apk`
- ZIP alignment: verified
- SHA-256:
  `99C6AD7B723C5CCC4646E95FE34CDF8323FB4FB11551C4E80E429D2F6694BD93`

The unsigned artifact is an intermediate build only. It must not be
distributed.

Permanent-signature release validation:

- Hidden-prompt local signing helper result: success
- Package: `com.openlps.networktoolkit`
- Version: `5.0.0-dev.4` / `versionCode 503`
- ZIP alignment: verified
- APK Signature Scheme v2: verified
- Signer count: 1
- Certificate SHA-256:
  `50fc73ceb72d4c446ebac3c24f30b45f37772e34b1fe734db0d9f13e1ac92dc9`
- Certificate matched the permanent public release-key record.
- Signed APK SHA-256:
  `B6494D8C9E936A9B80E97FDDEFAAC700C8334065B6916ED1F55437019E56BB4A`
- Local artifact:
  `C:\Users\SilvaTech\OpenLPS_Next\OpenLPS-Network-Toolkit-5.0.0-dev.4-release-signed.apk`

The permanent-signature APK was not installed over the development-signature
package because Android correctly treats them as different signing
identities. It was not uploaded or published.

## Not executed

No uninstall, data reset, remote-update publication, attack, exploitation,
deauthentication, credential testing, third-party scan, MAC change, HID
payload, USB profile change or optional large-module installation was
performed.
