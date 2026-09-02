#!/usr/bin/env python3
"""Validate that the release contains Post IDs only, without labels or content."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = {
    "data/train_ids.csv": 16_558,
    "data/test_ids.csv": 2_000,
}
PROHIBITED_PATHS = {
    "data/train.csv",
    "data/test.csv",
    "data/manifest.json",
}
ID_PATTERN = re.compile(r"^[0-9]{1,19}$")


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
    present = sorted(PROHIBITED_PATHS.intersection(tracked))
    if present:
        fail(f"prohibited internal release paths are tracked: {', '.join(present)}")

    tracked_data_csvs = {
        path for path in tracked if path.startswith("data/") and path.endswith(".csv")
    }
    if tracked_data_csvs != set(EXPECTED_FILES):
        fail(
            "tracked data CSVs must be exactly: "
            + ", ".join(sorted(EXPECTED_FILES))
        )

    all_ids: set[str] = set()
    for relative_path, expected_rows in EXPECTED_FILES.items():
        path = ROOT / relative_path
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if header != ["tweet_id"]:
                fail(f"{relative_path}: expected the single header tweet_id, found {header}")

            split_ids: set[str] = set()
            rows = 0
            for line_number, row in enumerate(reader, start=2):
                if len(row) != 1:
                    fail(f"{relative_path}:{line_number}: expected exactly one field")
                post_id = row[0]
                if not ID_PATTERN.fullmatch(post_id):
                    fail(f"{relative_path}:{line_number}: invalid Post ID")
                if post_id in split_ids:
                    fail(f"{relative_path}:{line_number}: duplicate Post ID")
                split_ids.add(post_id)
                rows += 1

        if rows != expected_rows:
            fail(f"{relative_path}: expected {expected_rows:,} IDs, found {rows:,}")
        overlap = all_ids.intersection(split_ids)
        if overlap:
            fail(f"{relative_path}: {len(overlap):,} IDs overlap another split")
        all_ids.update(split_ids)
        print(f"PASS {relative_path}: {rows:,} unique Post IDs; one column")

    print(f"PASS ID-only release: {len(all_ids):,} unique Post IDs; no label fields")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
