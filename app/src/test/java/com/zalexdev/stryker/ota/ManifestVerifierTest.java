package com.zalexdev.stryker.ota;

import org.junit.Test;

import java.util.Base64;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class ManifestVerifierTest {

    /*
     * RFC 8032, section 7.1, test vector 2: Ed25519 signature of a one-byte
     * message. This confirms that the app accepts the raw 32-byte public-key
     * representation emitted by the offline release tool.
     */
    private static final byte[] PUBLIC_KEY = hex(
            "3d4017c3e843895a92b70aa74d1b7ebc"
                    + "9c982ccf2ec4968cc0cd55f12af4660c");
    private static final byte[] SIGNATURE = hex(
            "92a009a9f0d4cab8720e820b5f642540"
                    + "a2b27b5416503f8fb3762223ebdb69da"
                    + "085ac1e43e15996e458f3613d0f11d8c"
                    + "387b2eaeb4302aeeb00d291612bb0c00");

    @Test
    public void acceptsKnownEd25519Vector() {
        assertTrue(ManifestVerifier.verifyWithPublicKey(
                new byte[]{0x72},
                Base64.getEncoder().encodeToString(SIGNATURE),
                Base64.getEncoder().encodeToString(PUBLIC_KEY)));
    }

    @Test
    public void rejectsChangedManifest() {
        assertFalse(ManifestVerifier.verifyWithPublicKey(
                new byte[]{0x73},
                Base64.getEncoder().encodeToString(SIGNATURE),
                Base64.getEncoder().encodeToString(PUBLIC_KEY)));
    }

    @Test
    public void rejectsWrongKeyOrSignatureSize() {
        assertFalse(ManifestVerifier.verifyWithPublicKey(
                new byte[]{0x72},
                Base64.getEncoder().encodeToString(new byte[63]),
                Base64.getEncoder().encodeToString(PUBLIC_KEY)));
        assertFalse(ManifestVerifier.verifyWithPublicKey(
                new byte[]{0x72},
                Base64.getEncoder().encodeToString(SIGNATURE),
                Base64.getEncoder().encodeToString(new byte[31])));
    }

    private static byte[] hex(String value) {
        int length = value.length();
        byte[] output = new byte[length / 2];
        for (int index = 0; index < length; index += 2) {
            output[index / 2] = (byte) Integer.parseInt(
                    value.substring(index, index + 2), 16);
        }
        return output;
    }
}
