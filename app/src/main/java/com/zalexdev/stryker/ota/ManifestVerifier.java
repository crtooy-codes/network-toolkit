package com.zalexdev.stryker.ota;

import org.bouncycastle.crypto.params.Ed25519PublicKeyParameters;
import org.bouncycastle.crypto.signers.Ed25519Signer;
import org.bouncycastle.util.encoders.Base64;

/**
 * Verifies the exact downloaded manifest bytes before any URL is trusted.
 */
public final class ManifestVerifier {

    private static final int PUBLIC_KEY_BYTES = 32;
    private static final int SIGNATURE_BYTES = 64;

    private ManifestVerifier() {
    }

    public static boolean verify(byte[] manifest, String encodedSignature) {
        return verifyWithPublicKey(
                manifest,
                encodedSignature,
                OpenLpsEndpoints.MANIFEST_PUBLIC_KEY_BASE64);
    }

    static boolean verifyWithPublicKey(
            byte[] manifest,
            String encodedSignature,
            String encodedPublicKey) {
        if (manifest == null || manifest.length == 0
                || encodedSignature == null || encodedSignature.isEmpty()
                || encodedPublicKey == null || encodedPublicKey.isEmpty()) {
            return false;
        }
        try {
            byte[] publicKey = Base64.decode(encodedPublicKey);
            byte[] signature = Base64.decode(encodedSignature);
            if (publicKey.length != PUBLIC_KEY_BYTES || signature.length != SIGNATURE_BYTES) {
                return false;
            }
            Ed25519Signer verifier = new Ed25519Signer();
            verifier.init(false, new Ed25519PublicKeyParameters(publicKey, 0));
            verifier.update(manifest, 0, manifest.length);
            return verifier.verifySignature(signature);
        } catch (RuntimeException ignored) {
            return false;
        }
    }
}
