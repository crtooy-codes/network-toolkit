package com.zalexdev.stryker.config;

import com.zalexdev.stryker.BuildConfig;

/**
 * Canonical paths and identifiers for the OpenLPS generation.
 *
 * Feature code must not create new /data/data or /data/local paths by hand.
 */
public final class OpenLpsPaths {

    public static final String PACKAGE_NAME = BuildConfig.APPLICATION_ID;
    public static final String APP_DATA = "/data/data/" + PACKAGE_NAME;
    public static final String APP_FILES = APP_DATA + "/files";

    public static final String CHROOT_ROOT = "/data/local/openlps";
    public static final String CHROOT_RELEASE = CHROOT_ROOT + "/release";

    public static final String SHARED_ROOT = "/storage/emulated/0/OpenLPS";

    private OpenLpsPaths() {
    }
}
