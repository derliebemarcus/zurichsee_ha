#!/usr/bin/env python3
"""Build a deterministic ZIP archive for the Zürichsee integration."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

SOURCE_ROOT = Path("custom_components/zurichsee_ha")
DEFAULT_OUTPUT = Path("reports/pytest/zurichsee_ha.zip")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def build_release_asset(output: Path = DEFAULT_OUTPUT) -> None:
    """Create the release archive with stable ordering and timestamps."""
    if not (SOURCE_ROOT / "manifest.json").is_file():
        raise FileNotFoundError(f"Missing integration manifest under {SOURCE_ROOT}")

    files = sorted(
        path
        for path in SOURCE_ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = ZipInfo(path.as_posix(), FIXED_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)

    print(f"Created {output} with {len(files)} files")


def main() -> int:
    """Build the archive at the optional command-line path."""
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    build_release_asset(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
