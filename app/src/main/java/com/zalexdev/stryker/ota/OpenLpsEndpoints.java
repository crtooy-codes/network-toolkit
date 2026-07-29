package com.zalexdev.stryker.ota;

import java.net.URI;
import java.net.URISyntaxException;

public final class OpenLpsEndpoints {

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

    /*
     * Temporary StrykerOSS bootstrap assets. Size and GitHub-provided SHA-256
     * were pinned on 2026-07-28. Any upstream replacement must fail closed
     * until a maintainer deliberately reviews and updates both values.
     */
    public static final String FALLBACK_CHROOT_64 =
            "https://github.com/zalexdev/strykerapp/releases/download/chroot-main/chroot64.tar.gz";
    public static final String FALLBACK_CHROOT_64_SHA256 =
            "2ad21f1445102913c52099bcb86ab380f9520c9e4d7771e6a951f634451068ac";
    public static final long FALLBACK_CHROOT_64_SIZE = 58_918_734L;

    public static final String FALLBACK_CHROOT_32 =
            "https://github.com/zalexdev/strykerapp/releases/download/chroot-main/chroot32.tar.gz";
    public static final String FALLBACK_CHROOT_32_SHA256 =
            "faa4b256819818360945d8fecc8f05f0f158a76e6a61feb8eff66308c32b3341";
    public static final long FALLBACK_CHROOT_32_SIZE = 140_633_600L;

    public static final String PREFS = "openlps_ota";

    public static boolean isAllowedReleaseUrl(String url) {
        URI uri = parseHttps(url);
        String releasePrefix =
                "/crtooy-codes/network-toolkit/releases/download/";
        return uri != null
                && "github.com".equalsIgnoreCase(uri.getHost())
                && uri.getPath() != null
                && uri.getPath().startsWith(releasePrefix)
                && uri.getPath().length() > releasePrefix.length()
                && uri.getQuery() == null
                && uri.getFragment() == null;
    }

    public static boolean isAllowedContentUrl(String url) {
        URI uri = parseHttps(url);
        if (uri == null || uri.getQuery() != null || uri.getFragment() != null) {
            return false;
        }
        String host = uri.getHost();
        String path = uri.getPath();
        if ("github.com".equalsIgnoreCase(host)) {
            return path != null && (path.equals("/crtooy-codes/network-toolkit")
                    || path.startsWith("/crtooy-codes/network-toolkit/"));
        }
        return "crtooy-codes.github.io".equalsIgnoreCase(host)
                && path != null
                && (path.equals("/network-toolkit")
                || path.startsWith("/network-toolkit/"));
    }

    private static URI parseHttps(String url) {
        if (url == null || url.isEmpty()) {
            return null;
        }
        try {
            URI uri = new URI(url);
            if (!"https".equalsIgnoreCase(uri.getScheme())
                    || uri.getHost() == null
                    || uri.getUserInfo() != null
                    || uri.getPort() != -1
                    || !uri.normalize().equals(uri)
                    || uri.getRawPath() == null
                    || uri.getRawPath().contains("%")
                    || hasTraversalSegment(uri.getPath())) {
                return null;
            }
            return uri;
        } catch (URISyntaxException ignored) {
            return null;
        }
    }

    private static boolean hasTraversalSegment(String path) {
        if (path == null) {
            return true;
        }
        for (String segment : path.split("/")) {
            if (".".equals(segment) || "..".equals(segment)) {
                return true;
            }
        }
        return false;
    }

    private OpenLpsEndpoints() {
    }
}
