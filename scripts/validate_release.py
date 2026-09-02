#!/usr/bin/env python3
"""Confirm that row-level dataset files remain withheld from Git."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WITHHELD_PATHS = {
    "data/train.csv",
    "data/test.csv",
    "data/manifest.json",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    tracked = set(result.stdout.decode("utf-8").split("\0"))
    present = sorted(WITHHELD_PATHS.intersection(tracked))
    if present:
        fail(f"withheld dataset files are tracked: {', '.join(present)}")

    print("PASS withheld state: no row-level dataset files or release manifest are tracked")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
