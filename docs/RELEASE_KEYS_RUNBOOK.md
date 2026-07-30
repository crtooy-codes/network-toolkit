# OpenLPS release keys runbook

This runbook describes how OpenLPS release keys must be created, stored and
used. It intentionally does not contain private keys, passwords or recovery
codes.

## Current state

- The Ed25519 public key is pinned in `MANIFEST_PUBLIC_KEY_BASE64`.
- Do not publish a live update manifest until the signed APK and complete
  update flow pass on a laboratory device.
- Debug APKs are for laboratory testing only.
- The permanent release identity uses two independent private keys:
  - Android APK release keystore;
  - Ed25519 manifest signing key.
- Public fingerprints from the completed ceremony are recorded in
  `RELEASE_KEY_PUBLIC_RECORD_2026-07-30.md`.

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

The repository includes `server/scripts/release_key_tool.py`. It uses OpenSSL
and Java `keytool`, refuses output inside the repository, refuses a fixed
Windows drive by default, and never accepts passwords in command-line
arguments. Use `--allow-fixed-drive` only on a dedicated trusted computer that
is offline and has encrypted storage.

Set long, unique passwords in the current offline shell without writing them
to a script or shell-history command:

```text
OPENLPS_RELEASE_STORE_PASSWORD
OPENLPS_RELEASE_KEY_PASSWORD
OPENLPS_MANIFEST_KEY_PASSWORD
```

Do not enter real release passwords in CI, chat, issues or repository files.

On Windows, `server/scripts/run_release_key_ceremony.ps1` provides the
interactive permanent ceremony. It:

- requires the computer to be offline;
- reports active default-route interfaces and waits until they are disconnected;
- verifies that the primary and recovery KeePass databases are identical;
- accepts the three KeePass-generated passwords through hidden prompts;
- confirms every password twice and requires them to be different;
- invokes `release_key_tool.py` without putting values on the command line;
- generates both permanent identities on removable media;
- signs and verifies a disposable manifest;
- records SHA-256 for every generated file;
- clears the three process environment variables before closing.

Run this wrapper only after creating and saving these KeePass entries:

```text
APK Keystore - Store Password
APK Keystore - Key Password
Manifest Ed25519 Password
```

The generated `Pending-Key-Import` folder remains encrypted by the JKS and PEM
passwords, but it is temporary. Attach its private files and records to the
appropriate KeePass entries, verify the recovery copy, then securely remove
the loose temporary folder.

For a local signed-build check, extract only `openlps-release.jks` from the
KeePass attachment to a temporary directory outside the repository. Then run:

```powershell
.\server\scripts\build_local_signed_release.ps1 `
  -KeystorePath 'X:\temporary-signing\openlps-release.jks' `
  -JavaHome 'C:\path\to\jdk-17' `
  -AndroidSdk 'C:\path\to\AndroidSDK'
```

The helper requests the store and key passwords through hidden prompts,
verifies the permanent public certificate fingerprint before and after the
build, and clears all signing variables from its process. Remove the temporary
JKS after verifying the resulting APK. Never install the permanent-signature
APK over a development-signature installation.

## APK release keystore

Generate the Android release keystore with `keytool` from a Java 17
installation. Use a long unique password and keep it offline.

Example command shape:

```powershell
keytool -genkeypair -v -keystore openlps-release.jks -alias openlps-release -keyalg RSA -keysize 4096 -validity 10000
```

Preferred tool command:

```powershell
python server/scripts/release_key_tool.py generate-apk `
  --output-dir E:\OpenLPS-release-secrets\apk
```

The two APK passwords must be different. The tool creates a JKS keystore,
exports its public certificate and records the certificate SHA-256 without
recording either password.

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

Preferred tool command:

```powershell
python server/scripts/release_key_tool.py generate-manifest `
  --output-dir E:\OpenLPS-release-secrets\manifest
```

The private Ed25519 key is encrypted with AES-256-CBC. Sign and independently
verify exact manifest bytes with:

```powershell
python server/scripts/release_key_tool.py sign-manifest `
  --private-key E:\OpenLPS-release-secrets\manifest\manifest-ed25519-private.pem `
  --manifest C:\release-workspace\manifest.json `
  --signature C:\release-workspace\manifest.json.sig

python server/scripts/release_key_tool.py verify-manifest `
  --public-key E:\OpenLPS-release-secrets\manifest\manifest-ed25519-public.pem `
  --manifest C:\release-workspace\manifest.json `
  --signature C:\release-workspace\manifest.json.sig
```

Before setting `MANIFEST_PUBLIC_KEY_BASE64`, verify a full update in the
laboratory with a signed manifest and a signed APK.

## Backup acceptance gate

Do not enable remote updates until all of these are true:

- the primary secret set is stored offline outside the repository;
- two encrypted offline backup copies exist on separate media;
- both backups have been read back and their file hashes match the primary;
- the passwords are stored separately from the media and recovery was tested;
- the APK certificate and raw manifest public-key fingerprints are recorded;
- no private file appears in `git status` or Git history.

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
