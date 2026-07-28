package com.zalexdev.stryker.ota;

public final class StrykerEndpoints {

    public static final String GITHUB_REPO =
            "https://github.com/crtooy-codes/network-toolkit";

    public static final String MANIFEST_URL =
            "https://crtooy-codes.github.io/network-toolkit/v1/manifest.json";

    public static final String MANIFEST_SIGNATURE_URL =
            "https://crtooy-codes.github.io/network-toolkit/v1/manifest.json.sig";

    /*
     * Raw 32-byte Ed25519 public key encoded with standard Base64.
     * Intentionally empty during development: remote updates remain disabled
     * until the offline release key is created and its public half is pinned.
     */
    public static final String MANIFEST_PUBLIC_KEY_BASE64 = "";

    public static final String FALLBACK_CHROOT_64 =
            "https://github.com/zalexdev/strykerapp/releases/download/chroot-main/chroot64.tar.gz";

    public static final String FALLBACK_CHROOT_32 =
            "https://github.com/zalexdev/strykerapp/releases/download/chroot-main/chroot32.tar.gz";

    public static final String PREFS = "openlps_ota";

    public static boolean isAllowedReleaseUrl(String url) {
        return url != null && url.startsWith(GITHUB_REPO + "/releases/download/");
    }

    private StrykerEndpoints() {
    }
}
