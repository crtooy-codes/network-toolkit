# OpenLPS static update service

This directory is the source for the live GitHub Pages service at
`https://crtooy-codes.github.io/network-toolkit/`.
GitHub Releases will hold the large APK and core assets; Pages only publishes
small manifests, signatures and documentation.

The Pages workflow publishes only `server/public/` plus the public JSON schema.
If a manifest is added later, the workflow requires both `manifest.json` and
`manifest.json.sig`, rejects placeholders, parses the JSON and checks that the
signature decodes to exactly 64 bytes. It also runs the strict contract
validator in `scripts/validate_manifest.py`, which rejects duplicate keys,
unknown fields, unofficial URLs, invalid sizes/hashes and malformed
news/notifications. The app still performs the authoritative Ed25519
verification. The status endpoint is `health.json`.

GitHub Pages is configured to use GitHub Actions. Every push to `main` that
changes the public service redeploys it without requiring this development
computer to remain online.

## Security gate

Remote updates are intentionally disabled while
`MANIFEST_PUBLIC_KEY_BASE64` is empty. Before the first preview release:

1. create an Ed25519 signing key on an offline machine;
2. back up the private key outside the repository;
3. copy only the raw 32-byte public key, Base64 encoded, into the app;
4. replace every placeholder in `manifest.template.json`;
5. validate the JSON against `schema/manifest-v1.schema.json`;
6. sign the exact UTF-8 bytes without rewriting the file afterward;
7. publish `manifest.json` and its Base64 signature as `manifest.json.sig`.

The APK release key and manifest key must be different. A private key, token,
keystore password or signing secret must never be committed.

## Publication layout

```text
public/
  v1/
    manifest.json
    manifest.json.sig
schema/
  manifest-v1.schema.json
```

Do not publish the template as a live manifest.

## Upstream core bootstrap

Development builds can bootstrap from the historical StrykerOSS chroot release
while the first OpenLPS core asset is being prepared. Both fallback assets have
their exact current GitHub size and SHA-256 pinned in `OpenLpsEndpoints`; the
download is rejected if the upstream file changes.

Before the first public OpenLPS release, publish a reviewed core asset in the
official OpenLPS GitHub Release and reference it from the signed manifest.
