#!/usr/bin/env python3
"""Offline helper for OpenLPS APK and manifest release keys.

This tool never accepts passwords on the command line. Passwords are read from
environment variables so they are not stored in shell history. Permanent keys
must be generated outside the repository on a trusted offline machine.
"""

from __future__ import annotations

import argparse
import base64
import ctypes
import datetime as dt
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PASSWORD_ENV = "OPENLPS_MANIFEST_KEY_PASSWORD"
APK_STORE_PASSWORD_ENV = "OPENLPS_RELEASE_STORE_PASSWORD"
APK_KEY_PASSWORD_ENV = "OPENLPS_RELEASE_KEY_PASSWORD"
DEFAULT_ALIAS = "openlps-release"
DEFAULT_DNAME = (
    "CN=OpenLPS Network Toolkit, OU=Release Signing, O=OpenLPS"
)
ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")
MINIMUM_PASSWORD_LENGTH = 24


class ReleaseKeyError(RuntimeError):
    """Raised for a safe, user-facing release-key error."""


def is_inside(path: Path, parent: Path) -> bool:
    path = path.resolve()
    parent = parent.resolve()
    try:
        return os.path.commonpath((str(path), str(parent))) == str(parent)
    except ValueError:
        return False


def windows_drive_type(path: Path) -> int | None:
    if os.name != "nt":
        return None
    anchor = path.resolve().anchor
    if not anchor:
        return None
    return int(ctypes.windll.kernel32.GetDriveTypeW(anchor))


def validate_new_output(path: Path, allow_fixed_drive: bool) -> Path:
    output = path.expanduser().resolve()
    if is_inside(output, REPOSITORY_ROOT):
        raise ReleaseKeyError(
            "release-key output must be outside the Git repository"
        )
    if output.exists():
        raise ReleaseKeyError(
            f"output already exists; choose a new empty path: {output}"
        )
    if not output.parent.exists():
        raise ReleaseKeyError(
            f"output parent does not exist: {output.parent}"
        )
    # Windows DRIVE_FIXED is 3. Removable media is DRIVE_REMOVABLE (2).
    if windows_drive_type(output) == 3 and not allow_fixed_drive:
        raise ReleaseKeyError(
            "refusing permanent key generation on a fixed Windows drive; "
            "use removable offline media or explicitly pass "
            "--allow-fixed-drive only on a trusted offline machine"
        )
    return output


def require_password(name: str) -> str:
    value = os.environ.get(name, "")
    if len(value) < MINIMUM_PASSWORD_LENGTH:
        raise ReleaseKeyError(
            f"{name} must be set to at least "
            f"{MINIMUM_PASSWORD_LENGTH} characters"
        )
    if "\r" in value or "\n" in value:
        raise ReleaseKeyError(f"{name} must not contain line breaks")
    return value


def find_executable(explicit: str | None, name: str) -> str:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.is_file():
            raise ReleaseKeyError(f"{name} executable was not found: {path}")
        return str(path)

    located = shutil.which(name)
    if located:
        return located

    if os.name == "nt" and name == "openssl":
        candidates = (
            Path(r"C:\Program Files\Git\usr\bin\openssl.exe"),
            Path(r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"),
        )
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)

    raise ReleaseKeyError(
        f"{name} was not found; provide its path with --{name}"
    )


def run_checked(command: Iterable[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(command),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        details = (result.stderr or result.stdout).strip()
        if len(details) > 1200:
            details = details[-1200:]
        raise ReleaseKeyError(
            f"external command failed with exit code {result.returncode}: "
            f"{details or 'no diagnostic output'}"
        )
    return result


def write_text(path: Path, value: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def raw_ed25519_public_key(der: bytes) -> bytes:
    if len(der) != len(ED25519_SPKI_PREFIX) + 32:
        raise ReleaseKeyError(
            "unexpected Ed25519 public-key DER length"
        )
    if not der.startswith(ED25519_SPKI_PREFIX):
        raise ReleaseKeyError(
            "unexpected Ed25519 SubjectPublicKeyInfo prefix"
        )
    return der[len(ED25519_SPKI_PREFIX) :]


def private_file_mode(path: Path) -> None:
    try:
        path.chmod(0o600)
    except OSError as exc:
        raise ReleaseKeyError(
            f"could not restrict private-key permissions: {exc}"
        ) from exc


def atomic_ceremony(
    output: Path,
    builder,
) -> None:
    temporary = Path(
        tempfile.mkdtemp(prefix=".openlps-key-", dir=str(output.parent))
    )
    try:
        builder(temporary)
        os.replace(temporary, output)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def new_temporary_path(prefix: str, directory: Path | None = None) -> Path:
    descriptor, name = tempfile.mkstemp(
        prefix=prefix,
        dir=str(directory) if directory is not None else None,
    )
    os.close(descriptor)
    return Path(name)


def generate_manifest_key(
    output_dir: Path,
    openssl: str,
    allow_fixed_drive: bool,
) -> None:
    require_password(MANIFEST_PASSWORD_ENV)
    output = validate_new_output(output_dir, allow_fixed_drive)

    def build(directory: Path) -> None:
        private_key = directory / "manifest-ed25519-private.pem"
        public_key = directory / "manifest-ed25519-public.pem"
        public_der = directory / "manifest-ed25519-public.der"
        public_base64 = directory / "manifest-ed25519-public-base64.txt"
        record = directory / "manifest-key-record.md"

        run_checked(
            (
                openssl,
                "genpkey",
                "-algorithm",
                "ED25519",
                "-aes-256-cbc",
                "-pass",
                f"env:{MANIFEST_PASSWORD_ENV}",
                "-out",
                str(private_key),
            )
        )
        private_file_mode(private_key)
        run_checked(
            (
                openssl,
                "pkey",
                "-in",
                str(private_key),
                "-passin",
                f"env:{MANIFEST_PASSWORD_ENV}",
                "-pubout",
                "-out",
                str(public_key),
            )
        )
        run_checked(
            (
                openssl,
                "pkey",
                "-pubin",
                "-in",
                str(public_key),
                "-outform",
                "DER",
                "-out",
                str(public_der),
            )
        )

        raw_public = raw_ed25519_public_key(public_der.read_bytes())
        encoded = base64.b64encode(raw_public).decode("ascii")
        fingerprint = hashlib.sha256(raw_public).hexdigest()
        write_text(public_base64, encoded + "\n")
        write_text(
            record,
            "\n".join(
                (
                    "# OpenLPS manifest key record",
                    "",
                    f"- Created UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}",
                    "- Algorithm: Ed25519",
                    f"- Raw public-key SHA-256: `{fingerprint}`",
                    "- Private-key encryption: OpenSSL AES-256-CBC",
                    "- Password storage: separate offline record",
                    "",
                    "The private key and password must never be committed.",
                    "",
                )
            ),
        )

    atomic_ceremony(output, build)
    print(f"Manifest key ceremony completed: {output}")
    print("Only the raw public-key Base64 value may be copied into the app.")


def certificate_der_from_pem(path: Path) -> bytes:
    try:
        return base64.b64decode(
            "".join(
                line.strip()
                for line in path.read_text(encoding="ascii").splitlines()
                if not line.startswith("-----")
            ),
            validate=True,
        )
    except (OSError, ValueError) as exc:
        raise ReleaseKeyError("could not decode exported certificate") from exc


def generate_apk_key(
    output_dir: Path,
    keytool: str,
    alias: str,
    dname: str,
    allow_fixed_drive: bool,
) -> None:
    store_password = require_password(APK_STORE_PASSWORD_ENV)
    key_password = require_password(APK_KEY_PASSWORD_ENV)
    if store_password == key_password:
        raise ReleaseKeyError(
            "APK store and key passwords must be different"
        )
    if not alias or any(char.isspace() for char in alias):
        raise ReleaseKeyError("APK key alias must be non-empty and contain no spaces")

    output = validate_new_output(output_dir, allow_fixed_drive)

    def build(directory: Path) -> None:
        keystore = directory / "openlps-release.jks"
        certificate = directory / "openlps-release-certificate.pem"
        record = directory / "apk-key-record.md"

        run_checked(
            (
                keytool,
                "-genkeypair",
                "-keystore",
                str(keystore),
                "-storetype",
                "JKS",
                "-storepass:env",
                APK_STORE_PASSWORD_ENV,
                "-keypass:env",
                APK_KEY_PASSWORD_ENV,
                "-alias",
                alias,
                "-keyalg",
                "RSA",
                "-keysize",
                "4096",
                "-sigalg",
                "SHA256withRSA",
                "-validity",
                "10000",
                "-dname",
                dname,
                "-noprompt",
            )
        )
        private_file_mode(keystore)
        run_checked(
            (
                keytool,
                "-list",
                "-keystore",
                str(keystore),
                "-storepass:env",
                APK_STORE_PASSWORD_ENV,
                "-alias",
                alias,
            )
        )
        run_checked(
            (
                keytool,
                "-exportcert",
                "-rfc",
                "-keystore",
                str(keystore),
                "-storepass:env",
                APK_STORE_PASSWORD_ENV,
                "-alias",
                alias,
                "-file",
                str(certificate),
            )
        )
        certificate_der = certificate_der_from_pem(certificate)
        fingerprint = hashlib.sha256(certificate_der).hexdigest()
        write_text(
            record,
            "\n".join(
                (
                    "# OpenLPS APK key record",
                    "",
                    f"- Created UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}",
                    f"- Alias: `{alias}`",
                    "- Store type: JKS",
                    "- Key algorithm: RSA 4096",
                    "- Signature algorithm: SHA256withRSA",
                    "- Validity: 10000 days",
                    f"- Certificate SHA-256: `{fingerprint}`",
                    f"- Distinguished name: `{dname}`",
                    "- Password storage: separate offline record",
                    "",
                    "The keystore and passwords must never be committed.",
                    "",
                )
            ),
        )

    atomic_ceremony(output, build)
    print(f"APK key ceremony completed: {output}")
    print("Preserve the certificate fingerprint with the offline release record.")


def decode_signature(path: Path) -> bytes:
    try:
        encoded = path.read_text(encoding="ascii").strip()
        signature = base64.b64decode(encoded, validate=True)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ReleaseKeyError("manifest signature is not valid Base64") from exc
    if len(signature) != 64:
        raise ReleaseKeyError(
            "manifest signature must decode to exactly 64 bytes"
        )
    return signature


def sign_manifest(
    private_key: Path,
    manifest: Path,
    signature_path: Path,
    openssl: str,
    force: bool,
) -> None:
    require_password(MANIFEST_PASSWORD_ENV)
    private_key = private_key.expanduser().resolve()
    manifest = manifest.expanduser().resolve()
    signature_path = signature_path.expanduser().resolve()
    if not private_key.is_file():
        raise ReleaseKeyError(f"private key was not found: {private_key}")
    if not manifest.is_file() or manifest.stat().st_size == 0:
        raise ReleaseKeyError(f"manifest is missing or empty: {manifest}")
    if signature_path.exists() and not force:
        raise ReleaseKeyError(
            f"signature already exists; use --force to replace it: {signature_path}"
        )
    if not signature_path.parent.exists():
        raise ReleaseKeyError(
            f"signature parent does not exist: {signature_path.parent}"
        )

    temporary = new_temporary_path(
        ".openlps-signature-", signature_path.parent
    )
    try:
        run_checked(
            (
                openssl,
                "pkeyutl",
                "-sign",
                "-rawin",
                "-inkey",
                str(private_key),
                "-passin",
                f"env:{MANIFEST_PASSWORD_ENV}",
                "-in",
                str(manifest),
                "-out",
                str(temporary),
            )
        )
        signature = temporary.read_bytes()
        if len(signature) != 64:
            raise ReleaseKeyError(
                "OpenSSL produced an unexpected Ed25519 signature size"
            )
        encoded = base64.b64encode(signature).decode("ascii") + "\n"
        pending = signature_path.with_name(signature_path.name + ".pending")
        write_text(pending, encoded)
        os.replace(pending, signature_path)
    finally:
        temporary.unlink(missing_ok=True)

    print(f"Manifest signed without rewriting its bytes: {signature_path}")


def verify_manifest(
    public_key: Path,
    manifest: Path,
    signature_path: Path,
    openssl: str,
) -> None:
    public_key = public_key.expanduser().resolve()
    manifest = manifest.expanduser().resolve()
    signature_path = signature_path.expanduser().resolve()
    if not public_key.is_file():
        raise ReleaseKeyError(f"public key was not found: {public_key}")
    if not manifest.is_file() or manifest.stat().st_size == 0:
        raise ReleaseKeyError(f"manifest is missing or empty: {manifest}")
    signature = decode_signature(signature_path)

    temporary = new_temporary_path(".openlps-verify-")
    try:
        temporary.write_bytes(signature)
        run_checked(
            (
                openssl,
                "pkeyutl",
                "-verify",
                "-pubin",
                "-rawin",
                "-inkey",
                str(public_key),
                "-in",
                str(manifest),
                "-sigfile",
                str(temporary),
            )
        )
    finally:
        temporary.unlink(missing_ok=True)

    print("Manifest signature verified successfully.")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Generate and use OpenLPS release keys offline."
    )
    result.add_argument("--openssl", help="path to the OpenSSL executable")
    result.add_argument("--keytool", help="path to the Java keytool executable")
    subparsers = result.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser(
        "generate-manifest", help="create an encrypted Ed25519 manifest key"
    )
    manifest.add_argument("--output-dir", type=Path, required=True)
    manifest.add_argument("--allow-fixed-drive", action="store_true")

    apk = subparsers.add_parser(
        "generate-apk", help="create the permanent Android APK keystore"
    )
    apk.add_argument("--output-dir", type=Path, required=True)
    apk.add_argument("--alias", default=DEFAULT_ALIAS)
    apk.add_argument("--dname", default=DEFAULT_DNAME)
    apk.add_argument("--allow-fixed-drive", action="store_true")

    sign = subparsers.add_parser(
        "sign-manifest", help="sign exact manifest bytes with Ed25519"
    )
    sign.add_argument("--private-key", type=Path, required=True)
    sign.add_argument("--manifest", type=Path, required=True)
    sign.add_argument("--signature", type=Path, required=True)
    sign.add_argument("--force", action="store_true")

    verify = subparsers.add_parser(
        "verify-manifest", help="verify a Base64 Ed25519 signature"
    )
    verify.add_argument("--public-key", type=Path, required=True)
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--signature", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "generate-manifest":
            generate_manifest_key(
                arguments.output_dir,
                find_executable(arguments.openssl, "openssl"),
                arguments.allow_fixed_drive,
            )
        elif arguments.command == "generate-apk":
            generate_apk_key(
                arguments.output_dir,
                find_executable(arguments.keytool, "keytool"),
                arguments.alias,
                arguments.dname,
                arguments.allow_fixed_drive,
            )
        elif arguments.command == "sign-manifest":
            sign_manifest(
                arguments.private_key,
                arguments.manifest,
                arguments.signature,
                find_executable(arguments.openssl, "openssl"),
                arguments.force,
            )
        elif arguments.command == "verify-manifest":
            verify_manifest(
                arguments.public_key,
                arguments.manifest,
                arguments.signature,
                find_executable(arguments.openssl, "openssl"),
            )
        else:
            raise ReleaseKeyError("unsupported command")
    except ReleaseKeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
