import base64
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_manifest.py"
SPEC = importlib.util.spec_from_file_location("validate_manifest", SCRIPT)
validate_manifest = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validate_manifest)


def valid_manifest():
    return {
        "manifest_version": 1,
        "core": {
            "version": "4.0",
            "chroot64": {
                "url": (
                    "https://github.com/crtooy-codes/network-toolkit/"
                    "releases/download/v5.0.0/chroot64.tar.gz"
                ),
                "sha256": "a" * 64,
                "size": 58918734,
            },
        },
        "app": {
            "versionCode": 502,
            "versionName": "5.0.0-dev.3",
            "url": (
                "https://github.com/crtooy-codes/network-toolkit/"
                "releases/download/v5.0.0-dev.3/openlps.apk"
            ),
            "sha256": "b" * 64,
            "size": 28534177,
            "mandatory": False,
            "changelog": "Security hardening.",
        },
        "news": [
            {
                "id": 1,
                "title": "OpenLPS update",
                "description": "A signed preview is available.",
                "newsUrl": (
                    "https://crtooy-codes.github.io/network-toolkit/news/1"
                ),
            }
        ],
        "notifications": [
            {
                "id": 1,
                "title": "Preview",
                "body": "Open the official project page.",
                "url": "https://github.com/crtooy-codes/network-toolkit",
            }
        ],
    }


class ValidateManifestTest(unittest.TestCase):
    def test_accepts_valid_contract(self):
        validate_manifest.validate_manifest_object(valid_manifest())

    def test_rejects_unofficial_release_url(self):
        manifest = valid_manifest()
        manifest["app"]["url"] = "https://example.com/openlps.apk"
        with self.assertRaises(validate_manifest.ManifestError):
            validate_manifest.validate_manifest_object(manifest)

    def test_rejects_encoded_release_url_traversal(self):
        manifest = valid_manifest()
        manifest["app"]["url"] = (
            "https://github.com/crtooy-codes/network-toolkit/"
            "releases/download/%2e%2e/openlps.apk"
        )
        with self.assertRaises(validate_manifest.ManifestError):
            validate_manifest.validate_manifest_object(manifest)

    def test_rejects_unofficial_notification_url(self):
        manifest = valid_manifest()
        manifest["notifications"][0]["url"] = "https://example.com/phishing"
        with self.assertRaises(validate_manifest.ManifestError):
            validate_manifest.validate_manifest_object(manifest)

    def test_rejects_unknown_fields(self):
        manifest = valid_manifest()
        manifest["app"]["unexpected"] = True
        with self.assertRaises(validate_manifest.ManifestError):
            validate_manifest.validate_manifest_object(manifest)

    def test_rejects_duplicate_json_keys(self):
        duplicate = (
            '{"manifest_version":1,"manifest_version":1,'
            '"core":{},"app":{},"news":[],"notifications":[]}'
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(duplicate, encoding="utf-8")
            with self.assertRaises(validate_manifest.ManifestError):
                validate_manifest.load_and_validate_manifest(path)

    def test_signature_must_decode_to_64_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            valid_path = Path(directory) / "valid.sig"
            invalid_path = Path(directory) / "invalid.sig"
            valid_path.write_bytes(base64.b64encode(bytes(64)))
            invalid_path.write_bytes(base64.b64encode(bytes(63)))
            validate_manifest.validate_signature(valid_path)
            with self.assertRaises(validate_manifest.ManifestError):
                validate_manifest.validate_signature(invalid_path)

    def test_serialized_fixture_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(valid_manifest()), encoding="utf-8")
            parsed = validate_manifest.load_and_validate_manifest(path)
            self.assertEqual(502, parsed["app"]["versionCode"])


if __name__ == "__main__":
    unittest.main()
