"""Tests for Changesets release metadata and deterministic packaging."""

from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

from tools.build_release_asset import build_release_asset


def test_release_versions_are_synchronized() -> None:
    """Package, manifest and text versions must always match."""
    package = json.loads(Path("package.json").read_text(encoding="utf-8"))
    manifest = json.loads(
        Path("custom_components/zurichsee_ha/manifest.json").read_text(encoding="utf-8")
    )
    version_text = Path("version.txt").read_text(encoding="utf-8").strip()

    assert package["name"] == "homeassistant_zurichsee"
    assert package["version"] == manifest["version"] == version_text


def test_changesets_configuration() -> None:
    """Changesets must version private packages without publishing to npm."""
    config = json.loads(Path(".changeset/config.json").read_text(encoding="utf-8"))

    assert config["baseBranch"] == "main"
    assert config["privatePackages"] == {"version": True, "tag": False}


def test_release_asset_is_deterministic(tmp_path: Path) -> None:
    """Repeated builds must produce the same ordered integration archive."""
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"

    build_release_asset(first)
    build_release_asset(second)

    assert first.read_bytes() == second.read_bytes()
    with ZipFile(first) as archive:
        names = archive.namelist()

    assert names == sorted(names)
    assert "custom_components/zurichsee_ha/manifest.json" in names
    assert all("__pycache__" not in name for name in names)
