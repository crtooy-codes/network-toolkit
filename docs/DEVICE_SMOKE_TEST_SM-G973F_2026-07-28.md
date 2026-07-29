# OpenLPS device smoke test — Galaxy S10 (SM-G973F)

Date: 2026-07-28  
Device OS: Android 15 / LineageOS userdebug  
Installed app: `com.openlps.networktoolkit` `5.0.0-dev.2` (`versionCode 501`)

This report intentionally excludes Wi-Fi names, IP addresses, MAC addresses,
device serials, and other local-network identifiers.

## Result

The installed APK starts and its main navigation is usable. Root access, the
Alpine chroot, required mounts, and the bundled base tools are operational.
One reproducible crash and three UI/integration defects were found and fixed in
source. The corrected APK builds successfully and was installed after a
verified backup. The Terminal, clean installer transition, and IPv4 subnet
fixes passed their on-device retests.

## Passed on device

- Dashboard startup after a force-stop and clean relaunch
- Root through Magisk
- Alpine chroot marker, `/usr`, and release metadata
- Chroot mounts for `/dev`, `/proc`, `/sys`, Android `/system`, and shared
  OpenLPS storage
- Base command availability/version checks for shell, Bash, BusyBox, Python,
  pip, curl, wget, Nmap, Aircrack-ng, macchanger, SQLite, and SSH
- Wi-Fi Networks screen and passive listing
- Handshakes screen with an empty state
- MAC Changer screen (no address was changed)
- Router Scan screen (scan was not started)
- WhisperPair authorization warning (BLE action was not accepted or run)
- Local Network screen and passive discovery
- Nmap screen (scan was not started)
- Arsenal hub and Database screens
- Web Scanner/Nuclei screen
- HID Tests screen and correct missing `/dev/hidg0` state
- Metasploit screen
- GeoMac screen
- VNC screen
- USB Arsenal screen and gadget/configfs capability detection
- Core Manager package inventory
- About and open-source license screens

## Defects found and fixed in source

1. Terminal crashed while creating its configuration directory because it used
   the former package path, `/data/data/com.zalexdev.stryker`. Terminal Kotlin
   configuration and its Android/chroot launcher scripts now use
   `/data/data/com.openlps.networktoolkit`.
2. The final installer screen restarted an already-active activity through a
   root shell command, which could leave the UI at `Initializing…`. It now
   performs a normal Android task restart using an explicit `Intent`.
3. Promo, About, Account, and Terminal links still used the old upstream
   branding/URLs. User-facing links and Portuguese promo text now point to the
   OpenLPS project. Upstream chroot download URLs were deliberately retained
   because they still provide the current core archive.
4. Local Network showed subnet `0.0.0.0` on modern Android because
   `DhcpInfo.netmask` is no longer reliable. It now derives the active IPv4
   network and CIDR prefix from `LinkProperties`.

## Corrected APK retest

- Complete private app-data backup created before uninstall
- Backup copied to the computer and verified against the device SHA-256
- Old APK removed; `/data/local/openlps/release/4.0` remained present with the
  same marker hash
- Corrected APK installed successfully
- Fresh setup completed and transitioned directly to the dashboard; it did not
  remain at `Initializing…`
- Terminal opened, created
  `files/usr/home/.terminal/color`, and produced no package crash
- Local Network displayed a valid IPv4 network in CIDR format rather than
  `0.0.0.0`
- About displayed the new OpenLPS project site and GitHub repository on the
  device; no external browser was opened
- Five historical database files and the small external app-data directory
  were restored from the verified backup
- Fresh configuration and executable files were retained to avoid
  reintroducing the former Terminal path
- Final crash buffer was empty after reopening both MainActivity and Terminal
- Final `/dev`, `/proc`, `/sys`, Android `/system`, and OpenLPS shared-storage
  mounts all passed

Backup:
`C:\Users\SilvaTech\OpenLPS_Next\device-backups\openlps-20260728-1300\openlps-appdata-20260728-1300.tar`

Backup SHA-256:
`52A1C86194542ABB11C382A278EA48E291E9D94D4732C4781E1C66F7382D821B`

## Build validation

Command: `gradlew.bat build --stacktrace`

- Result: success
- Unit tests: 2 executed, 0 failures, 0 errors, 0 skipped
- Debug APK:
  `app/build/outputs/apk/debug/app-debug.apk`
- SHA-256:
  `AA370FCF79FC7D278ECB9666DCE6D83FE1274D43799660A5F5B85F97F16F4099`

The project has existing non-blocking lint debt. Its Gradle configuration uses
`abortOnError false`; generated reports currently list issues in the app and
terminal modules. The changed functional files did not introduce a build
failure, but a separate lint-cleanup pass remains advisable.

## Not executed

No attack, exploitation, deauthentication, credential testing, HID payload,
USB profile change, MAC change, third-party scan, VNC installation, or large
optional module installation was performed. The optional Hydra, Nuclei,
Metasploit, SearchSploit, and ExploitDB components remain absent.

## Remaining follow-up

The corrected local APK now establishes the workstation's local debug
certificate on the device. Future locally built debug APKs can update it
without another uninstall. CI artifacts still need a stable signing key before
they can update this installation consistently.

The remaining project-level work is to introduce stable CI/release signing,
clean up the existing non-blocking lint debt, and optionally install/test the
large Hydra, Nuclei, Metasploit, SearchSploit, and ExploitDB modules.
