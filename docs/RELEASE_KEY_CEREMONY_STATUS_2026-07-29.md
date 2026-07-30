# OpenLPS release-key ceremony status

Date: 2026-07-29

Base commit at start: `c8a6f07`

Permanent-key status: **not created**

## Safety decision

The maintainer authorized preparation of the permanent OpenLPS release keys.
The machine was inspected before generation. Only the fixed Windows `C:` drive
was mounted; no removable offline media was available.

The permanent ceremony was therefore stopped before creating private material.
This follows the project rule that private release material must have verified
offline backups before remote updates are enabled.

## Prepared and validated

The project now has an offline helper at
`server/scripts/release_key_tool.py`. It:

- creates an encrypted Ed25519 manifest private key;
- extracts the exact raw 32-byte public-key format accepted by the app;
- signs exact manifest bytes and writes a 64-byte signature as Base64;
- verifies the signature independently with OpenSSL;
- creates an independent RSA-4096 Android JKS release key;
- exports and records the public APK certificate fingerprint;
- refuses release-key output inside the Git repository;
- refuses a fixed Windows drive unless an offline operator explicitly
  overrides the guard;
- receives passwords only through environment variables, not command-line
  arguments.

The Android verifier now has RFC 8032 test-vector coverage for the same raw
Ed25519 public-key format.

## Test evidence

- Java: Microsoft OpenJDK 17.0.19
- OpenSSL: 3.5.7
- Disposable key-tool tests: approved
- Ed25519 disposable generation/sign/verify: approved
- Disposable Android RSA-4096 keystore generation: approved
- Update-service Python tests: 13 approved
- Android debug unit tests: 7 approved
- Full Gradle build: approved

All disposable private material was created under the operating-system
temporary directory and removed by the test cleanup.

## Current trust state

- `MANIFEST_PUBLIC_KEY_BASE64` remains empty.
- Remote updates remain disabled and fail closed.
- No permanent APK or manifest private key was created.
- No keystore, PEM private key or real release password is present in the
  repository.
- No GitHub release-signing secret was configured.

## Required next session

Before resuming the permanent ceremony:

1. connect two trusted removable drives with enough free space;
2. make sure they do not contain the only copy of personal files;
3. disconnect remote-support sessions and untrusted applications;
4. disconnect the ceremony computer from the network;
5. choose how the three long passwords will be stored separately from the key
   media;
6. generate the primary set, copy it to the second medium and compare every
   file hash;
7. test reading both copies before adding only the manifest public key to the
   app.

The first signed preview and live manifest must not be published until the
backup acceptance gate in `RELEASE_KEYS_RUNBOOK.md` is complete.
