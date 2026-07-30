import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "release_key_tool.py"
SPEC = importlib.util.spec_from_file_location("release_key_tool", SCRIPT)
release_key_tool = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(release_key_tool)


def executable(name):
    located = shutil.which(name)
    if located:
        return located
    if os.name == "nt" and name == "openssl":
        fallback = Path(r"C:\Program Files\Git\usr\bin\openssl.exe")
        if fallback.is_file():
            return str(fallback)
    return None


class ReleaseKeyToolUnitTest(unittest.TestCase):
    def test_extracts_raw_ed25519_public_key(self):
        raw = bytes(range(32))
        self.assertEqual(
            raw,
            release_key_tool.raw_ed25519_public_key(
                release_key_tool.ED25519_SPKI_PREFIX + raw
            ),
        )

    def test_rejects_unexpected_public_key_encoding(self):
        with self.assertRaises(release_key_tool.ReleaseKeyError):
            release_key_tool.raw_ed25519_public_key(bytes(44))

    def test_rejects_output_inside_repository(self):
        output = release_key_tool.REPOSITORY_ROOT / "release-secrets"
        with self.assertRaises(release_key_tool.ReleaseKeyError):
            release_key_tool.validate_new_output(output, True)

    def test_requires_long_password(self):
        with mock.patch.dict(
            os.environ,
            {release_key_tool.MANIFEST_PASSWORD_ENV: "too-short"},
            clear=False,
        ):
            with self.assertRaises(release_key_tool.ReleaseKeyError):
                release_key_tool.require_password(
                    release_key_tool.MANIFEST_PASSWORD_ENV
                )


@unittest.skipUnless(
    executable("openssl") and executable("keytool"),
    "OpenSSL and Java keytool are required for integration testing",
)
class ReleaseKeyToolIntegrationTest(unittest.TestCase):
    def test_disposable_keys_sign_and_verify(self):
        password_environment = {
            release_key_tool.MANIFEST_PASSWORD_ENV:
                "temporary-manifest-test-password-2026",
            release_key_tool.APK_STORE_PASSWORD_ENV:
                "temporary-store-test-password-2026",
            release_key_tool.APK_KEY_PASSWORD_ENV:
                "temporary-key-test-password-2026",
        }
        with mock.patch.dict(os.environ, password_environment, clear=False):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                manifest_keys = root / "manifest"
                apk_keys = root / "apk"
                manifest = root / "manifest.json"
                signature = root / "manifest.json.sig"
                manifest.write_bytes(b'{"manifest_version":1}\n')

                release_key_tool.generate_manifest_key(
                    manifest_keys, executable("openssl"), True
                )
                release_key_tool.sign_manifest(
                    manifest_keys / "manifest-ed25519-private.pem",
                    manifest,
                    signature,
                    executable("openssl"),
                    False,
                )
                release_key_tool.verify_manifest(
                    manifest_keys / "manifest-ed25519-public.pem",
                    manifest,
                    signature,
                    executable("openssl"),
                )
                release_key_tool.generate_apk_key(
                    apk_keys,
                    executable("keytool"),
                    release_key_tool.DEFAULT_ALIAS,
                    release_key_tool.DEFAULT_DNAME,
                    True,
                )

                self.assertEqual(
                    44,
                    len(
                        (
                            manifest_keys
                            / "manifest-ed25519-public-base64.txt"
                        ).read_text(encoding="ascii").strip()
                    ),
                )
                self.assertEqual(
                    88,
                    len(signature.read_text(encoding="ascii").strip()),
                )
                self.assertTrue((apk_keys / "openlps-release.jks").is_file())
                self.assertTrue(
                    (apk_keys / "openlps-release-certificate.pem").is_file()
                )


if __name__ == "__main__":
    unittest.main()
