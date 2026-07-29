# OpenLPS release checklist

Use this checklist only after the permanent APK and manifest keys have been
created, backed up and tested. Debug APKs are never public releases.

## 1. Prepare

- [ ] Work from a clean release branch based on the approved `main`
- [ ] Choose a unique tag and release name
- [ ] Increase `versionCode`
- [ ] Set the intended `versionName`
- [ ] Update changelog and user documentation
- [ ] Confirm no remote-update key or release secret changed unexpectedly

## 2. Validate source

- [ ] Review the complete diff
- [ ] Search for secrets and personal identifiers
- [ ] Run the full Gradle build
- [ ] Run update-service Python tests
- [ ] Review lint reports and justify remaining baseline issues
- [ ] Test supported Android versions where available
- [ ] Test root, chroot, Terminal and storage on a laboratory device

## 3. Build the release APK

- [ ] Load the OpenLPS release keystore from its controlled offline location
- [ ] Build the release variant
- [ ] Verify that the APK is signed
- [ ] Verify that its certificate matches the previous public release
- [ ] Record exact file size
- [ ] Record SHA-256
- [ ] Install as an update over the previous release on a laboratory device
- [ ] Confirm app data, core and settings remain compatible

## 4. Prepare assets

- [ ] Create a GitHub pre-release
- [ ] Upload the signed APK
- [ ] Upload only reviewed core/module assets
- [ ] Confirm every asset URL belongs to the official OpenLPS Release
- [ ] Record size and SHA-256 for every downloadable asset

## 5. Prepare and sign the manifest

- [ ] Copy `server/manifest.template.json` to a temporary release workspace
- [ ] Replace every placeholder
- [ ] Keep `mandatory` false unless a documented security decision requires it
- [ ] Validate the contract with `server/scripts/validate_manifest.py`
- [ ] Sign the exact final UTF-8 bytes using the offline Ed25519 manifest key
- [ ] Do not reformat or rewrite the manifest after signing
- [ ] Verify the signature independently

## 6. Publish the update

- [ ] Add `manifest.json` and `manifest.json.sig` under `server/public/v1/`
- [ ] Merge through an approved pull request
- [ ] Confirm the OpenLPS Update Service workflow succeeds
- [ ] Confirm Pages serves both exact files
- [ ] Confirm the app accepts the signature and offers the intended version
- [ ] Download through the app and verify installation

## 7. Promote or roll back

- [ ] Keep the GitHub release as pre-release during staged testing
- [ ] Promote only after successful laboratory updates
- [ ] If defective, remove both live manifest files to fail closed
- [ ] Fix forward with a higher `versionCode`; do not publish a downgrade
- [ ] Preserve build records, hashes and test evidence
