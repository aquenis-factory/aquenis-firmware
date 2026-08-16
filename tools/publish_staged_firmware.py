#!/usr/bin/env python3
"""Publish one validated staged firmware payload into the repository."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9._-]+$")
REQUIRED_FIELDS = (
    "channel",
    "lane",
    "project",
    "product",
    "deviceType",
    "otaTarget",
    "hardwareProfile",
    "firmwareVersion",
    "build",
    "otaCapable",
    "sourceRepository",
    "sourceCommit",
    "firmwareSizeBytes",
    "firmwareSha256",
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_release(release: dict) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in release]
    if missing:
        raise ValueError(f"Missing release fields: {', '.join(missing)}")
    if release["channel"] not in {"production", "development"}:
        raise ValueError("channel must be production or development")
    for field in ("channel", "lane", "project", "deviceType", "otaTarget", "hardwareProfile", "firmwareVersion"):
        value = str(release[field])
        if not SAFE_SEGMENT.fullmatch(value) or value in {".", ".."}:
            raise ValueError(f"Unsafe {field}: {value!r}")
    if not re.fullmatch(r"[0-9a-f]{40}", str(release["sourceCommit"])):
        raise ValueError("sourceCommit must be a full lowercase Git SHA")
    if not re.fullmatch(r"[0-9a-f]{64}", str(release["firmwareSha256"])):
        raise ValueError("firmwareSha256 must be a lowercase SHA-256")
    if not isinstance(release["firmwareSizeBytes"], int) or release["firmwareSizeBytes"] <= 0:
        raise ValueError("firmwareSizeBytes must be a positive integer")
    if not isinstance(release["otaCapable"], bool):
        raise ValueError("otaCapable must be boolean")


def assemble_firmware(staging: Path, target: Path) -> tuple[int, str]:
    parts = sorted(staging.glob("firmware.part*.b64"))
    if not parts:
        raise ValueError("No firmware.part*.b64 files found")

    digest = hashlib.sha256()
    size = 0
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("wb") as output:
        for part in parts:
            encoded = "".join(part.read_text(encoding="ascii").split())
            payload = base64.b64decode(encoded, validate=True)
            output.write(payload)
            digest.update(payload)
            size += len(payload)
    return size, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging", required=True, type=Path)
    parser.add_argument("--repository", required=True, type=Path)
    args = parser.parse_args()

    staging = args.staging.resolve()
    repository = args.repository.resolve()
    release = read_json(staging / "release.json")
    validate_release(release)

    version_dir = (
        repository
        / release["channel"]
        / release["lane"]
        / release["project"]
        / f"v{release['firmwareVersion']}"
    )
    firmware_path = version_dir / "firmware.bin"
    metadata_path = version_dir / "metadata.json"
    if firmware_path.exists() or metadata_path.exists():
        raise ValueError(f"Release already exists: {version_dir.relative_to(repository)}")

    size, sha256 = assemble_firmware(staging, firmware_path)
    if size != release["firmwareSizeBytes"]:
        raise ValueError(f"Firmware size mismatch: expected {release['firmwareSizeBytes']}, got {size}")
    if sha256 != release["firmwareSha256"]:
        raise ValueError(f"Firmware SHA-256 mismatch: expected {release['firmwareSha256']}, got {sha256}")

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    relative_metadata = metadata_path.relative_to(repository).as_posix()
    metadata = {
        "schemaVersion": 1,
        "product": release["product"],
        "deviceType": release["deviceType"],
        "otaTarget": release["otaTarget"],
        "hardwareProfile": release["hardwareProfile"],
        "firmwareVersion": release["firmwareVersion"],
        "build": release["build"],
        "channel": release["channel"],
        "otaCapable": release["otaCapable"],
        "artifactsAvailable": True,
        "firmwareSizeBytes": size,
        "files": {"firmware": "firmware.bin"},
        "sha256": {"firmware": sha256},
        "sourceRepository": release["sourceRepository"],
        "sourceCommit": release["sourceCommit"],
        "publishedAt": timestamp,
    }
    write_json(metadata_path, metadata)

    channel_path = repository / "channels" / f"{release['channel']}.json"
    channel = read_json(channel_path)
    entries = [
        item
        for item in channel.get("firmwares", [])
        if not (
            item.get("deviceType") == release["deviceType"]
            and item.get("hardwareProfile") == release["hardwareProfile"]
        )
    ]
    entries.append(
        {
            "deviceType": release["deviceType"],
            "hardwareProfile": release["hardwareProfile"],
            "version": release["firmwareVersion"],
            "path": relative_metadata,
        }
    )
    channel["generatedAt"] = timestamp
    channel["firmwares"] = sorted(entries, key=lambda item: (item["deviceType"], item["hardwareProfile"]))
    write_json(channel_path, channel)

    manifest_path = repository / "manifest.json"
    manifest = read_json(manifest_path)
    manifest["generatedAt"] = timestamp
    manifest["updatedAt"] = timestamp
    write_json(manifest_path, manifest)

    print(f"Published {release['deviceType']} {release['firmwareVersion']}")
    print(f"Path: {version_dir.relative_to(repository)}")
    print(f"Size: {size}")
    print(f"SHA-256: {sha256}")


if __name__ == "__main__":
    main()
