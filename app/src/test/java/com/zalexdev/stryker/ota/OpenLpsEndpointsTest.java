package com.zalexdev.stryker.ota;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

public class OpenLpsEndpointsTest {

    @Test
    public void acceptsOfficialReleaseAsset() {
        assertTrue(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com/crtooy-codes/network-toolkit/"
                        + "releases/download/v5.0.0/openlps.apk"));
    }

    @Test
    public void rejectsReleaseUrlSpoofingAndTraversal() {
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "http://github.com/crtooy-codes/network-toolkit/"
                        + "releases/download/v5.0.0/openlps.apk"));
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com.evil.example/crtooy-codes/network-toolkit/"
                        + "releases/download/v5.0.0/openlps.apk"));
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com/crtooy-codes/network-toolkit/"
                        + "releases/download/../openlps.apk"));
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com/crtooy-codes/network-toolkit/"
                        + "releases/download/%2e%2e/openlps.apk"));
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com/crtooy-codes/network-toolkit/"
                        + "releases/download/v5.0.0/openlps.apk?redirect=evil"));
        assertFalse(OpenLpsEndpoints.isAllowedReleaseUrl(
                "https://github.com/crtooy-codes/network-toolkit/releases/download/"));
    }

    @Test
    public void acceptsOnlyOfficialContentUrls() {
        assertTrue(OpenLpsEndpoints.isAllowedContentUrl(
                "https://github.com/crtooy-codes/network-toolkit/issues/1"));
        assertTrue(OpenLpsEndpoints.isAllowedContentUrl(
                "https://crtooy-codes.github.io/network-toolkit/news/1"));
        assertFalse(OpenLpsEndpoints.isAllowedContentUrl(
                "https://example.com/openlps"));
        assertFalse(OpenLpsEndpoints.isAllowedContentUrl(
                "https://github.com/another-owner/network-toolkit"));
    }

    @Test
    public void fallbackChrootsHavePinnedIntegrityMetadata() {
        assertTrue(OpenLpsEndpoints.FALLBACK_CHROOT_64_SIZE > 0);
        assertTrue(OpenLpsEndpoints.FALLBACK_CHROOT_32_SIZE > 0);
        assertTrue(OpenLpsEndpoints.FALLBACK_CHROOT_64_SHA256
                .matches("[0-9a-f]{64}"));
        assertTrue(OpenLpsEndpoints.FALLBACK_CHROOT_32_SHA256
                .matches("[0-9a-f]{64}"));
    }
}
