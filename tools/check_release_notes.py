#!/usr/bin/env python3
"""Validate changelog release-note headings for the current manifest version."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_HEADINGS = (
    "### Added",
    "### Changed",
    "### Fixed",
)


def extract_section(changelog: str, version: str) -> str:
    lines = changelog.splitlines()
    capture = False
    collected: list[str] = []
    for line in lines:
        if line.startswith(f"## [{version}] - "):
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            collected.append(line)
    return "\n".join(collected).strip()


def main() -> int:
    manifest_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("custom_components/zurichsee_ha/manifest.json")
    )
    changelog_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("CHANGELOG.md")

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        return 1
    if not changelog_path.exists():
        print(f"Changelog not found: {changelog_path}")
        return 1

    version = str(json.loads(manifest_path.read_text(encoding="utf-8"))["version"]).strip()
    section = extract_section(changelog_path.read_text(encoding="utf-8"), version)
    if not section:
        print(f"Missing changelog section for version {version}")
        return 1

    # We only check if at least one of the standard headings is present or some content
    if not any(heading in section for heading in REQUIRED_HEADINGS) and len(section) < 10:
        print(
            f"Version {version} is missing standard release-note headings: {', '.join(REQUIRED_HEADINGS)}"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
