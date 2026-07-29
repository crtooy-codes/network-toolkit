# OpenLPS update service operations

OpenLPS does not currently use a VPS. The update service is a small static
service hosted with GitHub infrastructure:

- GitHub repository: source code, workflows and documentation;
- GitHub Actions: build, tests and Pages deployment;
- GitHub Pages: public `health.json`, schema and signed manifests;
- GitHub Releases: signed APK and reviewed core assets.

This static service is not an account, payment or access-approval backend. It
must never contain application forms, entitlement records, personal data,
payment data or private release keys. The boundary for a future official
service is described in
[ACCESS_REQUEST_WORKFLOW.md](ACCESS_REQUEST_WORKFLOW.md).

## Public endpoints

```text
https://crtooy-codes.github.io/network-toolkit/
https://crtooy-codes.github.io/network-toolkit/health.json
https://crtooy-codes.github.io/network-toolkit/schema/manifest-v1.schema.json
https://crtooy-codes.github.io/network-toolkit/v1/manifest.json
https://crtooy-codes.github.io/network-toolkit/v1/manifest.json.sig
```

`manifest.json` and `manifest.json.sig` remain unpublished until the first
signed release.

## Daily management

Use GitHub Issues and pull requests for changes. Every functional change should
land through `main`, pass Android CI and keep the update-service contract tests
green.

For a normal app update:

1. create a release branch;
2. change code and documentation;
3. bump `versionCode` and `versionName`;
4. run local tests when possible;
5. merge to `main`;
6. build the signed APK from the approved source;
7. publish the APK to GitHub Releases;
8. publish a signed manifest through GitHub Pages.

For a news-only update:

1. edit the manifest news or notifications;
2. validate the manifest;
3. sign the final manifest bytes;
4. publish both manifest files.

## What can be changed remotely

The signed manifest can announce:

- a new app version;
- core asset URLs, hashes and sizes;
- news shown in the app;
- notifications shown in the app.

The manifest cannot safely change arbitrary code. New app behavior still
requires a signed APK release.

## Failure handling

- Bad manifest: remove both live manifest files so clients fail closed.
- Bad APK: remove or mark the GitHub Release as broken, then publish a higher
  `versionCode`.
- Lost manifest key: ship a new APK containing a new public key.
- Lost APK key: users must manually reinstall a build signed by a new key.

## Monitoring

Check these after every deployment:

- Android CI workflow result;
- OpenLPS Update Service workflow result;
- `health.json` status;
- schema URL;
- manifest URL and signature URL when remote updates are enabled.
