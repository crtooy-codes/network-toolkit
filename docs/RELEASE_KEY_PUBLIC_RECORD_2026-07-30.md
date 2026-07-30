# OpenLPS public release-key record

This record contains public verification metadata only. It contains no private
key, keystore, password or recovery code.

## APK signing certificate

- Ceremony date: 2026-07-30
- Alias: `openlps-release`
- Key algorithm: RSA 4096
- Signature algorithm: SHA256withRSA
- Certificate SHA-256:
  `50fc73ceb72d4c446ebac3c24f30b45f37772e34b1fe734db0d9f13e1ac92dc9`
- Certificate validity UTC: 2026-07-30 through 2053-12-15

Every official release APK must report this certificate SHA-256. A different
certificate must fail the release gate and must not be distributed as an
in-place OpenLPS update.

First local signing validation:

- Version: `5.0.0-dev.4` / `versionCode 503`
- APK Signature Scheme v2: verified
- Signer count: 1
- APK SHA-256:
  `B6494D8C9E936A9B80E97FDDEFAAC700C8334065B6916ED1F55437019E56BB4A`
- Status: local validation only; not installed, uploaded or published

## Update-manifest key

- Algorithm: Ed25519
- Raw public-key size: 32 bytes
- Raw public-key SHA-256:
  `4a619ddca87a28500781ac51eab5f7f398e68313db9c350d3c2e9824d5628ae2`
- Public key pinned in:
  `app/src/main/java/com/zalexdev/stryker/ota/OpenLpsEndpoints.java`

The corresponding private key must remain encrypted outside the repository.
The app must reject a manifest whose signature does not verify with this
pinned public key.

## Custody status

- Primary encrypted KeePass database: removable USB media.
- Encrypted recovery KeePass database: OneDrive recovery folder.
- Recovery database opened successfully and its 4 APK attachments and 5
  manifest attachments were confirmed.
- A second independent offline medium is still recommended before the first
  public release.
