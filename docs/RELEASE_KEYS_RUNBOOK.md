# OpenLPS release keys runbook

This runbook describes how OpenLPS release keys must be created, stored and
used. It intentionally does not contain private keys, passwords or recovery
codes.

## Current state

- Public remote updates are disabled until `MANIFEST_PUBLIC_KEY_BASE64` is set
  in the Android app.
- Debug APKs are for laboratory testing only.
- The first public release requires two independent private keys:
  - Android APK release keystore;
  - Ed25519 manifest signing key.

## Rules

1. Never commit a private key, keystore, password, token or recovery code.
2. Keep the APK keystore and the manifest private key separate.
3. Keep at least two offline backups before the first public release.
4. Record hashes, file sizes, version names and version codes for every release.
5. If a private key is lost, do not publish a fake update path. Publish a new
   APK manually and document the key rotation.

## Offline key ceremony

Use a trusted computer, disconnected from untrusted remote sessions during key
creation. Create a temporary local folder outside the repository, for example:

```text
OpenLPS-release-secrets/
  apk/
    openlps-release.jks
    openlps-release-keystore-notes.txt
  manifest/
    manifest-ed25519-private.key
    manifest-ed25519-public.key
    manifest-ed25519-public-base64.txt
  recovery/
    release-record.md
```

The folder above is only an example. Do not place it inside this Git
repository.

## APK release keystore

Generate the Android release keystore with `keytool` from a Java 17
installation. Use a long unique password and keep it offline.

Example command shape:

```powershell
keytool -genkeypair -v -keystore openlps-release.jks -alias openlps-release -keyalg RSA -keysize 4096 -validity 10000
```

For GitHub Actions, store the keystore as a Base64 secret named
`OPENLPS_RELEASE_KEYSTORE_BASE64`. Store the passwords and alias in these
secrets:

```text
OPENLPS_RELEASE_STORE_PASSWORD
OPENLPS_RELEASE_KEY_ALIAS
OPENLPS_RELEASE_KEY_PASSWORD
```

The workflow decodes the keystore only on the temporary GitHub runner.

## Manifest Ed25519 key

The manifest key signs `server/public/v1/manifest.json`. The Android app stores
only the public key. The private key remains offline.

The release process must produce:

- private Ed25519 signing key;
- public Ed25519 verification key;
- Base64 public key for `MANIFEST_PUBLIC_KEY_BASE64`;
- Base64 signature file `manifest.json.sig`.

Before setting `MANIFEST_PUBLIC_KEY_BASE64`, verify a full update in the
laboratory with a signed manifest and a signed APK.

## First public release order

1. Create and back up the APK release keystore.
2. Create and back up the Ed25519 manifest key.
3. Add only the manifest public key to the Android source.
4. Bump `versionCode` and `versionName`.
5. Build and verify a signed release APK.
6. Upload the APK and reviewed core assets to a GitHub Release.
7. Create `manifest.json` from `server/manifest.template.json`.
8. Validate it with `server/scripts/validate_manifest.py`.
9. Sign the exact final manifest bytes.
10. Publish `manifest.json` and `manifest.json.sig` through GitHub Pages.
11. Test update detection and install on a laboratory device.

## Recovery

If the manifest is wrong, remove both live files:

```text
server/public/v1/manifest.json
server/public/v1/manifest.json.sig
```

The app fails closed when the manifest or signature is missing.

If the APK release key is compromised, publish a security notice and require a
manual reinstall signed by a new key. Android will not accept an in-place update
signed with a different certificate.
