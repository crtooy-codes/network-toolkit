#!/usr/bin/env python3
"""Validate the OpenLPS v1 release manifest before GitHub Pages deployment."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

MAX_MANIFEST_BYTES = 512 * 1024
MAX_SIGNATURE_BYTES = 2048
MAX_ASSET_BYTES = 4 * 1024 * 1024 * 1024
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
RELEASE_PREFIX = "/crtooy-codes/network-toolkit/releases/download/"
CONTENT_GITHUB_PREFIX = "/crtooy-codes/network-toolkit"
CONTENT_PAGES_PREFIX = "/network-toolkit"


class ManifestError(ValueError):
    pass


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{name} must be an object")
    return value


def _require_exact_keys(
    value: dict[str, Any], required: set[str], optional: set[str], name: str
) -> None:
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing:
        raise ManifestError(f"{name} missing keys: {', '.join(sorted(missing))}")
    if extra:
        raise ManifestError(f"{name} has unknown keys: {', '.join(sorted(extra))}")


def _require_string(
    value: Any, name: str, *, minimum: int = 0, maximum: int
) -> str:
    if not isinstance(value, str) or not minimum <= len(value) <= maximum:
        raise ManifestError(
            f"{name} must be a string with length {minimum}..{maximum}"
        )
    return value


def _require_int(value: Any, name: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ManifestError(f"{name} must be an integer")
    if not minimum <= value <= maximum:
        raise ManifestError(f"{name} must be in range {minimum}..{maximum}")
    return value


def _is_clean_https_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
        decoded_path = unquote(parsed.path)
        return (
            parsed.scheme == "https"
            and parsed.hostname is not None
            and parsed.username is None
            and parsed.password is None
            and parsed.port is None
            and not parsed.query
            and not parsed.fragment
            and "%" not in parsed.path
            and "." not in decoded_path.split("/")
            and ".." not in decoded_path.split("/")
        )
    except ValueError:
        return False


def is_allowed_release_url(url: str) -> bool:
    if not _is_clean_https_url(url):
        return False
    parsed = urlsplit(url)
    return (
        parsed.hostname == "github.com"
        and parsed.path.startswith(RELEASE_PREFIX)
        and len(parsed.path) > len(RELEASE_PREFIX)
    )


def is_allowed_content_url(url: str) -> bool:
    if not _is_clean_https_url(url):
        return False
    parsed = urlsplit(url)
    if parsed.hostname == "github.com":
        return parsed.path == CONTENT_GITHUB_PREFIX or parsed.path.startswith(
            CONTENT_GITHUB_PREFIX + "/"
        )
    if parsed.hostname == "crtooy-codes.github.io":
        return parsed.path == CONTENT_PAGES_PREFIX or parsed.path.startswith(
            CONTENT_PAGES_PREFIX + "/"
        )
    return False


def _validate_optional_content_url(value: Any, name: str) -> None:
    url = _require_string(value, name, maximum=2048)
    if url and not is_allowed_content_url(url):
        raise ManifestError(f"{name} is not an allowed OpenLPS URL")


def _validate_asset(value: Any, name: str) -> None:
    asset = _require_object(value, name)
    _require_exact_keys(asset, {"url", "sha256", "size"}, set(), name)
    url = _require_string(asset["url"], f"{name}.url", minimum=1, maximum=2048)
    if not is_allowed_release_url(url):
        raise ManifestError(f"{name}.url is not an official OpenLPS release URL")
    sha256 = _require_string(
        asset["sha256"], f"{name}.sha256", minimum=64, maximum=64
    )
    if not SHA256_RE.fullmatch(sha256):
        raise ManifestError(f"{name}.sha256 must contain 64 hexadecimal characters")
    _require_int(asset["size"], f"{name}.size", 1, MAX_ASSET_BYTES)


def _validate_news(value: Any, index: int) -> None:
    name = f"news[{index}]"
    item = _require_object(value, name)
    required = {"id", "title", "description"}
    optional = {
        "pin",
        "pinned",
        "newsDate",
        "newsUrl",
        "imageUrl",
        "actionbutton1",
        "actionbutton2",
        "actionbutton1text",
        "actionbutton2text",
        "actionbutton1url",
        "actionbutton2url",
    }
    _require_exact_keys(item, required, optional, name)
    _require_int(item["id"], f"{name}.id", 1, 2_147_483_647)
    _require_string(item["title"], f"{name}.title", minimum=1, maximum=160)
    _require_string(
        item["description"], f"{name}.description", minimum=1, maximum=4000
    )
    for field in ("pin", "pinned", "actionbutton1", "actionbutton2"):
        if field in item and not isinstance(item[field], bool):
            raise ManifestError(f"{name}.{field} must be a boolean")
    for field, maximum in (
        ("newsDate", 32),
        ("actionbutton1text", 80),
        ("actionbutton2text", 80),
    ):
        if field in item:
            _require_string(item[field], f"{name}.{field}", maximum=maximum)
    for field in (
        "newsUrl",
        "imageUrl",
        "actionbutton1url",
        "actionbutton2url",
    ):
        if field in item:
            _validate_optional_content_url(item[field], f"{name}.{field}")


def _validate_notification(value: Any, index: int) -> None:
    name = f"notifications[{index}]"
    item = _require_object(value, name)
    _require_exact_keys(item, {"id", "title", "body"}, {"url"}, name)
    _require_int(item["id"], f"{name}.id", 1, 2_147_483_647)
    _require_string(item["title"], f"{name}.title", minimum=1, maximum=160)
    _require_string(item["body"], f"{name}.body", maximum=2000)
    if "url" in item:
        _validate_optional_content_url(item["url"], f"{name}.url")


def validate_manifest_object(root: Any) -> None:
    manifest = _require_object(root, "manifest")
    _require_exact_keys(
        manifest,
        {"manifest_version", "core", "app", "news", "notifications"},
        set(),
        "manifest",
    )
    if manifest["manifest_version"] != 1:
        raise ManifestError("manifest_version must be exactly 1")

    core = _require_object(manifest["core"], "core")
    _require_exact_keys(core, {"version", "chroot64"}, {"chroot32"}, "core")
    _require_string(core["version"], "core.version", minimum=1, maximum=64)
    _validate_asset(core["chroot64"], "core.chroot64")
    if "chroot32" in core:
        _validate_asset(core["chroot32"], "core.chroot32")

    app = _require_object(manifest["app"], "app")
    _require_exact_keys(
        app,
        {
            "versionCode",
            "versionName",
            "url",
            "sha256",
            "size",
            "mandatory",
            "changelog",
        },
        set(),
        "app",
    )
    _require_int(app["versionCode"], "app.versionCode", 1, 2_147_483_647)
    _require_string(
        app["versionName"], "app.versionName", minimum=1, maximum=64
    )
    _validate_asset(
        {"url": app["url"], "sha256": app["sha256"], "size": app["size"]},
        "app",
    )
    if not isinstance(app["mandatory"], bool):
        raise ManifestError("app.mandatory must be a boolean")
    _require_string(app["changelog"], "app.changelog", maximum=8000)

    news = manifest["news"]
    notifications = manifest["notifications"]
    if not isinstance(news, list) or len(news) > 50:
        raise ManifestError("news must be an array with at most 50 items")
    if not isinstance(notifications, list) or len(notifications) > 50:
        raise ManifestError("notifications must be an array with at most 50 items")
    for index, item in enumerate(news):
        _validate_news(item, index)
    for index, item in enumerate(notifications):
        _validate_notification(item, index)


def load_and_validate_manifest(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if not raw or len(raw) > MAX_MANIFEST_BYTES:
        raise ManifestError("manifest size is outside the accepted range")
    if b"REPLACE_" in raw:
        raise ManifestError("manifest still contains REPLACE_ placeholders")
    try:
        root = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"manifest is not valid UTF-8 JSON: {exc}") from exc
    validate_manifest_object(root)
    return root


def validate_signature(path: Path) -> None:
    raw = path.read_bytes()
    if not raw or len(raw) > MAX_SIGNATURE_BYTES:
        raise ManifestError("signature size is outside the accepted range")
    try:
        decoded = base64.b64decode(raw.strip(), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ManifestError("signature is not valid Base64") from exc
    if len(decoded) != 64:
        raise ManifestError("signature must decode to exactly 64 bytes")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("signature", type=Path)
    args = parser.parse_args()
    try:
        load_and_validate_manifest(args.manifest)
        validate_signature(args.signature)
    except (OSError, ManifestError) as exc:
        print(f"OpenLPS manifest validation failed: {exc}")
        return 1
    print("OpenLPS manifest contract and signature envelope are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
