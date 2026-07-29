package com.zalexdev.stryker.ota;

import android.content.Context;

public final class CoreDownloader {

    private CoreDownloader() {
    }

    public static RemoteManifest.Asset resolve(Context context, boolean is64Bit) {
        RemoteManifest manifest = ManifestService.fetch(context);
        if (manifest != null) {
            RemoteManifest.Asset asset = is64Bit ? manifest.chroot64 : manifest.chroot32;
            if (asset != null && asset.isUsable()) {
                return asset;
            }
        }
        if (is64Bit) {
            return new RemoteManifest.Asset(
                    OpenLpsEndpoints.FALLBACK_CHROOT_64,
                    OpenLpsEndpoints.FALLBACK_CHROOT_64_SHA256,
                    OpenLpsEndpoints.FALLBACK_CHROOT_64_SIZE);
        }
        return new RemoteManifest.Asset(
                OpenLpsEndpoints.FALLBACK_CHROOT_32,
                OpenLpsEndpoints.FALLBACK_CHROOT_32_SHA256,
                OpenLpsEndpoints.FALLBACK_CHROOT_32_SIZE);
    }
}
