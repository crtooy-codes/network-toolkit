package com.zalexdev.stryker.ota;

import android.content.Context;
import android.content.SharedPreferences;

import org.json.JSONException;

import java.nio.charset.StandardCharsets;

public final class ManifestService {

    private static final int MAX_MANIFEST_BYTES = 512 * 1024;
    private static final int MAX_SIGNATURE_BYTES = 2048;
    private static final String KEY_CACHE = "manifest_cache_verified_v1";

    private ManifestService() {
    }

    public static RemoteManifest fetch(Context context) {
        SharedPreferences prefs = prefs(context);
        try {
            byte[] manifestBytes =
                    Net.getBytes(StrykerEndpoints.MANIFEST_URL, MAX_MANIFEST_BYTES);
            String signature = new String(
                    Net.getBytes(StrykerEndpoints.MANIFEST_SIGNATURE_URL, MAX_SIGNATURE_BYTES),
                    StandardCharsets.US_ASCII).trim();
            if (!ManifestVerifier.verify(manifestBytes, signature)) {
                return cached(context);
            }
            String json = new String(manifestBytes, StandardCharsets.UTF_8);
            RemoteManifest manifest = RemoteManifest.fromJson(json);
            prefs.edit().putString(KEY_CACHE, json).apply();
            return manifest;
        } catch (Exception e) {
            return cached(context);
        }
    }

    public static RemoteManifest cached(Context context) {
        String json = prefs(context).getString(KEY_CACHE, null);
        if (json == null || json.isEmpty()) {
            return null;
        }
        try {
            return RemoteManifest.fromJson(json);
        } catch (JSONException e) {
            return null;
        }
    }

    static SharedPreferences prefs(Context context) {
        return context.getApplicationContext()
                .getSharedPreferences(StrykerEndpoints.PREFS, Context.MODE_PRIVATE);
    }
}
